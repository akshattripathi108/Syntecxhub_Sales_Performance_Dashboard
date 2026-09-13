import pandas as pd
import numpy as np

df = pd.read_csv('data/cleaned/sales_cleaned.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Year'] = df['Order_Date'].dt.year
df['Quarter'] = df['Order_Date'].dt.quarter
df['Month'] = df['Order_Date'].dt.month
df['Year-Month'] = df['Order_Date'].dt.strftime('%Y-%m')

print('=== DATA VERIFICATION ===')
print(f'Records: {len(df)}')
print(f'Date range: {df["Order_Date"].min().date()} to {df["Order_Date"].max().date()}')
print(f'Products: {df["Product"].nunique()}')
print(f'Categories: {df["Category"].nunique()} - {list(df["Category"].unique())}')
print(f'Regions: {df["Region"].nunique()} - {list(df["Region"].unique())}')
print()

print('=== KPI VERIFICATION ===')
rev = df['Sales'].sum()
prof = df['Profit'].sum()
margin = (prof/rev)*100
print(f'Total Revenue: ${rev:,.2f}')
print(f'Total Profit: ${prof:,.2f}')
print(f'Profit Margin: {margin:.2f}%')
print()

print('=== YEARLY ===')
yearly = df.groupby('Year').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
yearly['Growth'] = yearly['Sales'].pct_change()*100
for _, r in yearly.iterrows():
    print(f'  {int(r.Year)}: Revenue=${r.Sales:,.2f}, Profit=${r.Profit:,.2f}', end='')
    if pd.notna(r.Growth):
        print(f', Growth={r.Growth:+.2f}%')
    else:
        print()
print()

print('=== QUARTERLY ===')
quarterly = df.groupby(['Year','Quarter']).agg(Sales=('Sales','sum')).reset_index()
quarterly['Period'] = quarterly['Year'].astype(str) + '-Q' + quarterly['Quarter'].astype(str)
for _, r in quarterly.iterrows():
    print(f'  {r.Period}: ${r.Sales:,.2f}')
print()

print('=== TOP 5 PRODUCTS ===')
top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)
for p, s in top_products.items():
    print(f'  {p}: ${s:,.2f}')
print()

print('=== BOTTOM 5 PRODUCTS ===')
bottom_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=True).head(5)
for p, s in bottom_products.items():
    print(f'  {p}: ${s:,.2f}')
print()

print('=== REGION ===')
region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
for r, s in region.items():
    print(f'  {r}: ${s:,.2f}')
print()

print('=== CATEGORY ===')
cat = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
for c, s in cat.items():
    print(f'  {c}: ${s:,.2f}')
print()

print('=== MONTHLY TREND (sample) ===')
monthly = df.groupby('Year-Month')['Sales'].sum().reset_index()
print(monthly.to_string(index=False))