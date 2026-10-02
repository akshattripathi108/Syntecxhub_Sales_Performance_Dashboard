#!/usr/bin/env python3
"""
Syntecxhub Sales Performance Dashboard — Automated Data Pipeline Orchestrator
=============================================================================
Single entrypoint for end-to-end data ingestion, cleaning, quarantine validation,
and Power BI export generation.
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime, timezone
import pandas as pd

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DEFAULT = os.path.join(REPO_ROOT, 'data', 'raw', 'MOCK_DATA.csv')
CLEANED_PATH = os.path.join(REPO_ROOT, 'data', 'cleaned', 'sales_cleaned.csv')
PBI_EXPORT_PATH = os.path.join(REPO_ROOT, 'data', 'pbi_ready', 'sales_for_powerbi.csv')
QUARANTINE_PATH = os.path.join(REPO_ROOT, 'data', 'quarantine', 'corrupted_orders.csv')
RUNS_LOG_PATH = os.path.join(REPO_ROOT, 'outputs', 'pipeline_runs.json')

COLUMNS_FACT = ['Order_Date', 'Product', 'Category', 'Region', 'Sales', 'Profit']
COLUMNS_PBI = [
    'Order_Date', 'Year', 'Quarter', 'Month', 'MonthName', 'MonthYear',
    'DayOfWeek', 'DayOfWeekNum', 'IsWeekend',
    'Product', 'Category', 'Region',
    'Sales', 'Profit', 'Profit_Margin_Pct'
]


def load_raw_data(file_path: str) -> pd.DataFrame:
    """Load raw transactions CSV."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")
    return pd.read_csv(file_path)


def process_and_clean(df_raw: pd.DataFrame, incremental: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Cleans raw transactions, isolates invalid rows to quarantine,
    and performs deduplication.
    """
    stats = {
        "raw_rows": len(df_raw),
        "quarantined_rows": 0,
        "duplicates_dropped": 0,
        "clean_rows": 0,
        "new_rows_appended": 0,
    }

    # 1. Null / Missing Required Field Check
    null_mask = df_raw[['Order_Date', 'Product', 'Category', 'Region', 'Sales', 'Profit']].isnull().any(axis=1)
    
    # 2. Negative Value & Numeric Validity Check
    sales_numeric = pd.to_numeric(df_raw['Sales'], errors='coerce')
    profit_numeric = pd.to_numeric(df_raw['Profit'], errors='coerce')
    invalid_nums = sales_numeric.isna() | profit_numeric.isna() | (sales_numeric < 0) | (profit_numeric < 0)

    # 3. Date Validity Check
    dates_parsed = pd.to_datetime(df_raw['Order_Date'], format='mixed', dayfirst=True, errors='coerce')
    invalid_dates = dates_parsed.isna()

    # Isolate Quarantine Rows
    quarantine_mask = null_mask | invalid_nums | invalid_dates
    df_quarantine = df_raw[quarantine_mask].copy()
    if not df_quarantine.empty:
        reasons = []
        for idx, row in df_quarantine.iterrows():
            r = []
            if null_mask.loc[idx]: r.append("Missing required fields")
            if invalid_nums.loc[idx]: r.append("Invalid or negative Sales/Profit")
            if invalid_dates.loc[idx]: r.append("Unparseable Order_Date")
            reasons.append("; ".join(r))
        df_quarantine['Quarantine_Reason'] = reasons
        df_quarantine['Quarantined_At'] = datetime.now(timezone.utc).isoformat()
    
    stats["quarantined_rows"] = len(df_quarantine)

    # Process Valid Records
    df_valid = df_raw[~quarantine_mask].copy()
    df_valid['Order_Date'] = pd.to_datetime(df_valid['Order_Date'], format='mixed', dayfirst=True)
    df_valid['Sales'] = pd.to_numeric(df_valid['Sales']).round(2)
    df_valid['Profit'] = pd.to_numeric(df_valid['Profit']).round(2)
    df_valid = df_valid[COLUMNS_FACT]

    # Deduplication via Compound Natural Key
    dups_before = len(df_valid)
    df_valid = df_valid.drop_duplicates(subset=['Order_Date', 'Product', 'Region', 'Sales'])
    stats["duplicates_dropped"] = dups_before - len(df_valid)

    # Incremental Merge if requested
    if incremental and os.path.exists(CLEANED_PATH):
        df_existing = pd.read_csv(CLEANED_PATH)
        df_existing['Order_Date'] = pd.to_datetime(df_existing['Order_Date'])
        merged = pd.concat([df_existing, df_valid], ignore_index=True)
        merged = merged.drop_duplicates(subset=['Order_Date', 'Product', 'Region', 'Sales'])
        stats["new_rows_appended"] = len(merged) - len(df_existing)
        df_clean = merged
    else:
        df_clean = df_valid
        stats["new_rows_appended"] = len(df_clean)

    df_clean = df_clean.sort_values('Order_Date').reset_index(drop=True)
    stats["clean_rows"] = len(df_clean)
    return df_clean, df_quarantine, stats


def export_powerbi(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Generates the denormalized Power BI export layer with derived date dimensions."""
    df = df_clean.copy()
    df['Year'] = df['Order_Date'].dt.year
    df['Quarter'] = df['Order_Date'].dt.to_period('Q').astype(str)
    df['Month'] = df['Order_Date'].dt.month
    df['MonthName'] = df['Order_Date'].dt.strftime('%b')
    df['MonthYear'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['DayOfWeek'] = df['Order_Date'].dt.day_name()
    df['DayOfWeekNum'] = df['Order_Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeekNum'].isin([5, 6])
    df['Profit_Margin_Pct'] = (df['Profit'] / df['Sales'] * 100).round(2)
    return df[COLUMNS_PBI]


def record_run_manifest(stats: dict, duration: float, status: str):
    """Appends execution telemetry to outputs/pipeline_runs.json."""
    os.makedirs(os.path.dirname(RUNS_LOG_PATH), exist_ok=True)
    manifest = []
    if os.path.exists(RUNS_LOG_PATH):
        try:
            with open(RUNS_LOG_PATH, 'r') as f:
                manifest = json.load(f)
        except json.JSONDecodeError:
            manifest = []

    run_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "duration_seconds": round(duration, 3),
        **stats
    }
    manifest.append(run_record)

    with open(RUNS_LOG_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)


def run_pipeline(input_file: str, incremental: bool = False, validate_only: bool = False) -> int:
    """Orchestrates pipeline execution."""
    start_time = time.time()
    print("=" * 70)
    print("Syntecxhub Sales Performance — Automated Pipeline")
    print("=" * 70)
    print(f"Input file   : {input_file}")
    print(f"Mode         : {'Incremental' if incremental else 'Full Refresh'}")
    print(f"Action       : {'Validation Only' if validate_only else 'Full Pipeline Run'}\n")

    try:
        df_raw = load_raw_data(input_file)
        df_clean, df_quarantine, stats = process_and_clean(df_raw, incremental=incremental)

        # Anomaly threshold gate (>5% quarantined fails pipeline)
        quarantine_pct = (stats['quarantined_rows'] / stats['raw_rows'] * 100) if stats['raw_rows'] > 0 else 0
        if quarantine_pct > 5.0:
            print(f"[!] QUARANTINE BREACH: {quarantine_pct:.1f}% of rows failed validation. Halting export.", file=sys.stderr)
            record_run_manifest(stats, time.time() - start_time, "QUARANTINE_ALERT")
            return 1

        # Save Quarantine if any
        if not df_quarantine.empty:
            os.makedirs(os.path.dirname(QUARANTINE_PATH), exist_ok=True)
            mode = 'a' if os.path.exists(QUARANTINE_PATH) else 'w'
            header = not os.path.exists(QUARANTINE_PATH)
            df_quarantine.to_csv(QUARANTINE_PATH, mode=mode, header=header, index=False)
            print(f"[+] Quarantined {len(df_quarantine)} invalid rows -> {QUARANTINE_PATH}")

        # Validation summary
        print("Pipeline Metrics:")
        print(f"  Raw Rows Ingested     : {stats['raw_rows']:,}")
        print(f"  Quarantined Records   : {stats['quarantined_rows']:,}")
        print(f"  Duplicates Eliminated : {stats['duplicates_dropped']:,}")
        print(f"  Clean Fact Rows       : {stats['clean_rows']:,}")
        print(f"  Total Revenue         : ${df_clean['Sales'].sum():,.2f}")
        print(f"  Total Profit          : ${df_clean['Profit'].sum():,.2f}")
        print(f"  Profit Margin         : {(df_clean['Profit'].sum() / df_clean['Sales'].sum() * 100):.2f}%")

        if validate_only:
            print("\nValidation complete (no files modified).")
            record_run_manifest(stats, time.time() - start_time, "VALIDATED")
            return 0

        # Save Clean Dataset
        os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
        df_clean.to_csv(CLEANED_PATH, index=False)
        print(f"\n[OK] Clean Fact Table saved  -> {CLEANED_PATH}")

        # Save Power BI Export
        os.makedirs(os.path.dirname(PBI_EXPORT_PATH), exist_ok=True)
        df_pbi = export_powerbi(df_clean)
        df_pbi.to_csv(PBI_EXPORT_PATH, index=False)
        print(f"[OK] Power BI Export saved   -> {PBI_EXPORT_PATH}")

        duration = time.time() - start_time
        record_run_manifest(stats, duration, "SUCCESS")
        print(f"\nPipeline finished in {duration:.2f}s with status: SUCCESS")
        return 0

    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}", file=sys.stderr)
        record_run_manifest({}, time.time() - start_time, f"FAILED: {str(e)}")
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automated Sales Data Pipeline")
    parser.add_argument('--input', default=RAW_DEFAULT, help="Path to input raw CSV")
    parser.add_argument('--incremental', action='store_true', help="Append and deduplicate against existing dataset")
    parser.add_argument('--validate-only', action='store_true', help="Run validation checks without writing files")
    args = parser.parse_args()

    sys.exit(run_pipeline(args.input, incremental=args.incremental, validate_only=args.validate_only))
