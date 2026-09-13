#!/usr/bin/env python3
"""
Syntecxhub Sales Performance Dashboard
Power BI Export Helper - Phase 5
=====================================
Exports a Power BI-friendly CSV from the cleaned dataset:
- ISO-8601 date column (YYYY-MM-DD)
- Consistent numeric dtypes
- Derived columns: Year, Quarter, Month, MonthName, MonthYear,
  DayOfWeek, DayOfWeekNum, IsWeekend, Profit_Margin_Pct
Output is placed in data/pbi_ready/ for direct import into Power BI Desktop.
"""

import os
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(BASE, 'data', 'cleaned', 'sales_cleaned.csv')
OUT_DIR = os.path.join(BASE, 'data', 'pbi_ready')
OUT_FILE = os.path.join(OUT_DIR, 'sales_for_powerbi.csv')

os.makedirs(OUT_DIR, exist_ok=True)

print('=' * 70)
print('Syntecxhub Sales Dashboard')
print('Power BI Export Helper - Phase 5')
print('=' * 70)
print(f'Source : {SRC}')

df = pd.read_csv(SRC)
print(f'Loaded: {df.shape[0]} rows x {df.shape[1]} cols')

# Normalise date to ISO-8601
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
print(f'Date range : {df["Order_Date"].min().date()} -> {df["Order_Date"].max().date()}')

# Sort by date
df = df.sort_values('Order_Date').reset_index(drop=True)

# --- Derived columns for slicers and time-intelligence ---
df['Year']         = df['Order_Date'].dt.year
df['Quarter']      = df['Order_Date'].dt.to_period('Q').astype(str)
df['Month']        = df['Order_Date'].dt.month
df['MonthName']    = df['Order_Date'].dt.strftime('%b')
df['MonthYear']    = df['Order_Date'].dt.strftime('%Y-%m')
df['DayOfWeek']    = df['Order_Date'].dt.day_name()
df['DayOfWeekNum']  = df['Order_Date'].dt.dayofweek
df['IsWeekend']    = df['DayOfWeekNum'].isin([5, 6])
df['Profit_Margin_Pct'] = (df['Profit'] / df['Sales'] * 100).round(2)

# Final column order
COL_ORDER = [
    'Order_Date', 'Year', 'Quarter', 'Month', 'MonthName', 'MonthYear',
    'DayOfWeek', 'DayOfWeekNum', 'IsWeekend',
    'Product', 'Category', 'Region',
    'Sales', 'Profit', 'Profit_Margin_Pct'
]
df = df[COL_ORDER]

# Enforce dtypes
df['Sales']             = df['Sales'].astype('float64')
df['Profit']            = df['Profit'].astype('float64')
df['Profit_Margin_Pct'] = df['Profit_Margin_Pct'].astype('float64')
df['Year']              = df['Year'].astype('Int64')
df['Month']             = df['Month'].astype('Int64')
df['DayOfWeekNum']      = df['DayOfWeekNum'].astype('Int64')
df['IsWeekend']         = df['IsWeekend'].astype('bool')

print()
print('Summary')
print('-' * 40)
print(f'  Total Sales        : ${df["Sales"].sum():>12,.2f}')
print(f'  Total Profit       : ${df["Profit"].sum():>12,.2f}')
print(f'  Profit Margin      : {df["Profit"].sum()/df["Sales"].sum()*100:>11.1f}%')
print(f'  Unique Products    : {df["Product"].nunique():>12}')
print(f'  Unique Categories  : {df["Category"].nunique():>12}')
print(f'  Unique Regions     : {df["Region"].nunique():>12}')
print(f'  Years Covered      : {sorted(df["Year"].unique())}')
print(f'  Output rows        : {len(df):,}')
print(f'  Output cols        : {len(df.columns)}')

df.to_csv(OUT_FILE, index=False)
print()
print(f'Saved -> {OUT_FILE}')
print('Power BI Export complete!')
