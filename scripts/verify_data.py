#!/usr/bin/env python3
"""Verify cleaned dataset for README numbers."""
import pandas as pd

df = pd.read_csv("data/cleaned/sales_cleaned.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print("=== CLEANED DATA VERIFICATION ===")
print(f"Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")
print(f"Unique dates: {df['Order_Date'].nunique()}")
print(f"Years: {sorted(df['Order_Date'].dt.year.unique())}")
print(f"Categories ({df['Category'].nunique()}): {sorted(df['Category'].unique())}")
print(f"Regions ({df['Region'].nunique()}): {sorted(df['Region'].unique())}")
print(f"Products ({df['Product'].nunique()}):")
for p in sorted(df["Product"].unique()):
    print(f"  - {p}")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Profit Margin: {(df['Profit'].sum()/df['Sales'].sum()*100):.2f}%")
print(f"Sales range: ${df['Sales'].min():,.2f} - ${df['Sales'].max():,.2f}")
print(f"Profit range: ${df['Profit'].min():,.2f} - ${df['Profit'].max():,.2f}")

# Category breakdown
print("\n=== SALES BY CATEGORY ===")
cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
for cat, sales in cat_sales.items():
    pct = sales / df["Sales"].sum() * 100
    print(f"  {cat}: ${sales:,.2f} ({pct:.1f}%)")

print("\n=== SALES BY REGION ===")
reg_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
for reg, sales in reg_sales.items():
    pct = sales / df["Sales"].sum() * 100
    print(f"  {reg}: ${sales:,.2f} ({pct:.1f}%)")