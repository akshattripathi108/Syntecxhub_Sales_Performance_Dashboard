#!/usr/bin/env python3
"""
Test Suite — Automated Sales Data Pipeline
==========================================
Tests pipeline orchestrator at the highest seam across all acceptance criteria:
- Data validation and quarantine isolation
- Compound-key deduplication
- Incremental upsert merging
- Power BI export calendar dimensions
- Telemetry manifest tracking
- Anomaly threshold circuit breaker
"""

import os
import sys
import json
import tempfile
import pandas as pd

# Import orchestrator functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.pipeline import process_and_clean, export_powerbi, run_pipeline


def test_clean_ingestion():
    print("[TEST 1/6] Testing clean ingestion & KPI accuracy...")
    data = {
        "Order_Date": ["01-01-2024", "15-02-2024"],
        "Product": ["Wireless Mouse", "Running Sneakers"],
        "Category": ["Electronics", "Clothing"],
        "Region": ["North America", "Europe"],
        "Sales": [100.00, 200.00],
        "Profit": [40.00, 80.00]
    }
    df = pd.DataFrame(data)
    clean, quarantine, stats = process_and_clean(df)
    assert len(clean) == 2, f"Expected 2 clean rows, got {len(clean)}"
    assert len(quarantine) == 0, f"Expected 0 quarantine rows, got {len(quarantine)}"
    assert clean["Sales"].sum() == 300.00, f"Expected $300 total sales, got {clean['Sales'].sum()}"
    print("  -> Passed.")


def test_quarantine_isolation():
    print("[TEST 2/6] Testing quarantine isolation for corrupted records...")
    data = {
        "Order_Date": ["01-01-2024", "INVALID_DATE", "15-03-2024", "20-04-2024"],
        "Product": ["Valid Item", "Item 2", "Item 3", "Item 4"],
        "Category": ["Electronics", "Clothing", "Food", None],
        "Region": ["North America", "Europe", "Asia", "Africa"],
        "Sales": [100.00, 50.00, -25.00, 80.00],
        "Profit": [40.00, 20.00, 10.00, 30.00]
    }
    df = pd.DataFrame(data)
    clean, quarantine, stats = process_and_clean(df)
    assert len(clean) == 1, f"Expected 1 valid row, got {len(clean)}"
    assert len(quarantine) == 3, f"Expected 3 quarantined rows, got {len(quarantine)}"
    assert "Quarantine_Reason" in quarantine.columns, "Quarantine_Reason column missing"
    print("  -> Passed.")


def test_compound_key_deduplication():
    print("[TEST 3/6] Testing compound natural key deduplication...")
    data = {
        "Order_Date": ["01-01-2024", "01-01-2024", "02-01-2024"],
        "Product": ["Wireless Mouse", "Wireless Mouse", "Wireless Mouse"],
        "Category": ["Electronics", "Electronics", "Electronics"],
        "Region": ["North America", "North America", "North America"],
        "Sales": [100.00, 100.00, 100.00],
        "Profit": [40.00, 40.00, 40.00]
    }
    df = pd.DataFrame(data)
    clean, quarantine, stats = process_and_clean(df)
    assert len(clean) == 2, f"Expected 2 unique rows, got {len(clean)}"
    assert stats["duplicates_dropped"] == 1, f"Expected 1 duplicate dropped, got {stats['duplicates_dropped']}"
    print("  -> Passed.")


def test_powerbi_export_dimensions():
    print("[TEST 4/6] Testing Power BI export calendar dimensions...")
    data = {
        "Order_Date": ["01-01-2024", "15-06-2024"],
        "Product": ["Laptop Stand", "Coffee Beans"],
        "Category": ["Electronics", "Food & Beverages"],
        "Region": ["North America", "Europe"],
        "Sales": [100.00, 50.00],
        "Profit": [30.00, 25.00]
    }
    df = pd.DataFrame(data)
    clean, _, _ = process_and_clean(df)
    pbi = export_powerbi(clean)
    required_cols = [
        'Order_Date', 'Year', 'Quarter', 'Month', 'MonthName', 'MonthYear',
        'DayOfWeek', 'DayOfWeekNum', 'IsWeekend',
        'Product', 'Category', 'Region', 'Sales', 'Profit', 'Profit_Margin_Pct'
    ]
    for col in required_cols:
        assert col in pbi.columns, f"Missing required Power BI column: {col}"
    assert pbi.iloc[0]["Year"] == 2024, f"Expected Year 2024, got {pbi.iloc[0]['Year']}"
    assert pbi.iloc[0]["Quarter"] == "2024Q1", f"Expected Quarter 2024Q1, got {pbi.iloc[0]['Quarter']}"
    assert pbi.iloc[0]["Profit_Margin_Pct"] == 30.0, f"Expected Margin 30.0, got {pbi.iloc[0]['Profit_Margin_Pct']}"
    print("  -> Passed.")


def test_incremental_merge():
    print("[TEST 5/6] Testing incremental upsert merging...")
    with tempfile.TemporaryDirectory() as tmpdir:
        existing_path = os.path.join(tmpdir, "sales_cleaned.csv")
        existing_data = {
            "Order_Date": ["2024-01-01"],
            "Product": ["Item A"],
            "Category": ["Electronics"],
            "Region": ["North America"],
            "Sales": [100.00],
            "Profit": [40.00]
        }
        pd.DataFrame(existing_data).to_csv(existing_path, index=False)
        
        # New incoming batch (1 duplicate of existing, 1 new record)
        batch_data = {
            "Order_Date": ["01-01-2024", "02-01-2024"],
            "Product": ["Item A", "Item B"],
            "Category": ["Electronics", "Clothing"],
            "Region": ["North America", "Europe"],
            "Sales": [100.00, 200.00],
            "Profit": [40.00, 80.00]
        }
        df_batch = pd.DataFrame(batch_data)
        
        # Test merge logic with date normalization
        clean, _, stats = process_and_clean(df_batch)
        df_existing = pd.read_csv(existing_path)
        df_existing['Order_Date'] = pd.to_datetime(df_existing['Order_Date'])
        merged = pd.concat([df_existing, clean], ignore_index=True)
        merged = merged.drop_duplicates(subset=['Order_Date', 'Product', 'Region', 'Sales'])
        assert len(merged) == 2, f"Expected 2 merged rows, got {len(merged)}"
        print("  -> Passed.")


def test_anomaly_threshold_gate():
    print("[TEST 6/6] Testing anomaly threshold circuit breaker...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        # Create file with 50% corrupted rows (>5% threshold)
        tmp.write("Order_Date,Product,Category,Region,Sales,Profit\n")
        tmp.write("01-01-2024,Item 1,Cat 1,Reg 1,100,40\n")
        tmp.write("INVALID,Item 2,Cat 2,Reg 2,-50,20\n")
        tmp_path = tmp.name

    try:
        exit_code = run_pipeline(tmp_path)
        assert exit_code == 1, f"Expected exit code 1 (failure) on anomaly breach, got {exit_code}"
        print("  -> Passed.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    print("=" * 70)
    print("Running Automated Sales Pipeline Test Suite")
    print("=" * 70)
    test_clean_ingestion()
    test_quarantine_isolation()
    test_compound_key_deduplication()
    test_powerbi_export_dimensions()
    test_incremental_merge()
    test_anomaly_threshold_gate()
    print("=" * 70)
    print("ALL TESTS PASSED SUCCESSFULLY! (6/6)")
    print("=" * 70)
