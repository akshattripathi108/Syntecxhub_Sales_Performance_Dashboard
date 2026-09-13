#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_PATH = os.path.join(BASE, 'data', 'raw', 'MOCK_DATA.csv')
CLEANED_PATH = os.path.join(BASE, 'data', 'cleaned', 'sales_cleaned.csv')
LOG_PATH = os.path.join(BASE, 'outputs', 'cleaning_log.csv')

os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def parse_date(date_str):
    if pd.isna(date_str):
        return pd.NaT
    date_str = str(date_str).strip()
    for fmt in ['%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d']:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            pass
    return pd.NaT

def fmt_date_summary(series):
    s = pd.to_datetime(series, errors='coerce')
    valid = s.dropna()
    if valid.empty:
        return 'none'
    return f'{valid.min().date()} to {valid.max().date()} ({len(valid)} rows)'

print('=' * 70)
print('Phase 4: Data Cleaning')
print('=' * 70)
print(f'Loading raw data from: {RAW_PATH}')

raw = pd.read_csv(RAW_PATH)
print(f'Raw shape: {raw.shape[0]} rows x {raw.shape[1]} cols')
print(f'Columns: {list(raw.columns)}')

log_rows = []

print()
print('-' * 70)
print('CHECK 1: Null Values')
print('-' * 70)
null_counts = raw.isnull().sum()
total_nulls = null_counts.sum()
if total_nulls > 0:
    print(f'Found {total_nulls} null values')
    raw = raw.dropna()
    log_rows.append({'check': 'null_values', 'detail': f'dropped {total_nulls} nulls', 'action': 'dropped'})
else:
    print('No null values found')
    log_rows.append({'check': 'null_values', 'detail': '0 nulls', 'action': 'none'})

print()
print('-' * 70)
print('CHECK 2: Duplicate Rows')
print('-' * 70)
dup_count = raw.duplicated().sum()
if dup_count > 0:
    print(f'Found {dup_count} duplicates')
    raw = raw.drop_duplicates()
    log_rows.append({'check': 'duplicates', 'detail': f'dropped {dup_count}', 'action': 'dropped'})
else:
    print('No duplicates found')
    log_rows.append({'check': 'duplicates', 'detail': '0 duplicates', 'action': 'none'})

print()
print('-' * 70)
print('CHECK 3: Negative Values')
print('-' * 70)
neg_sales = (raw['Sales'] < 0).sum()
neg_profit = (raw['Profit'] < 0).sum()
neg_total = neg_sales + neg_profit
if neg_total > 0:
    print(f'Found {neg_total} negative values')
    neg_mask = (raw['Sales'] < 0) | (raw['Profit'] < 0)
    raw = raw[~neg_mask]
    log_rows.append({'check': 'negative_values', 'detail': f'dropped {neg_total}', 'action': 'dropped'})
else:
    print('No negative values found')
    log_rows.append({'check': 'negative_values', 'detail': '0 negative', 'action': 'none'})

print()
print('-' * 70)
print('CHECK 4: Date Parsing')
print('-' * 70)
raw['Order_Date'] = raw['Order_Date'].apply(parse_date)
print(f'Date range: {fmt_date_summary(raw["Order_Date"])}')
log_rows.append({'check': 'date_parsing', 'detail': 'dates parsed', 'action': 'parsed'})

print()
print('-' * 70)
print('CHECK 5: Data Types')
print('-' * 70)
raw['Sales'] = pd.to_numeric(raw['Sales'], errors='coerce')
raw['Profit'] = pd.to_numeric(raw['Profit'], errors='coerce')
print(f'Sales: {raw["Sales"].dtype}, Profit: {raw["Profit"].dtype}')
log_rows.append({'check': 'dtype_coercion', 'detail': 'dtypes coerced', 'action': 'coerced'})

print()
print('=' * 70)
print('CLEANED DATASET SUMMARY')
print('=' * 70)
print(f'Shape: {raw.shape[0]} rows x {raw.shape[1]} cols')
print(f'Categories: {raw["Category"].nunique()}')
print(f'Regions: {raw["Region"].nunique()}')
print(f'Products: {raw["Product"].nunique()}')
total_sales = raw['Sales'].sum()
total_profit = raw['Profit'].sum()
print(f'Total Sales: ${total_sales:,.2f}')
print(f'Total Profit: ${total_profit:,.2f}')
print(f'Profit Margin: {(total_profit/total_sales*100):.2f}%')

log_rows.append({'check': 'final_shape', 'detail': f'{raw.shape[0]} rows', 'action': 'final'})
log_rows.append({'check': 'totals', 'detail': f'Sales: ${total_sales:,.2f}, Profit: ${total_profit:,.2f}', 'action': 'verified'})

raw.to_csv(CLEANED_PATH, index=False)
print(f'\nCleaned CSV saved -> {CLEANED_PATH}')

log_df = pd.DataFrame(log_rows, columns=['check', 'detail', 'action'])
log_df.to_csv(LOG_PATH, index=False)
print(f'Cleaning log saved -> {LOG_PATH}')

print()
print('Phase 4 complete!')
