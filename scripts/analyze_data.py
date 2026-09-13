import pandas as pd
import json

df = pd.read_csv('data/cleaned/sales_cleaned.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

results = {}

# Monthly revenue
monthly = df.groupby(df['Order_Date'].dt.to_period('M'))['Sales'].sum()
results['monthly_first6'] = {str(k): round(v, 2) for k, v in monthly.head(6).items()}
results['monthly_last6'] = {str(k): round(v, 2) for k, v in monthly.tail(6).items()}

# Yearly
yearly = df.groupby(df['Order_Date'].dt.year)['Sales'].sum()
results['yearly'] = {str(k): round(v, 2) for k, v in yearly.items()}

# YoY
yoy = []
for i in range(1, len(yearly)):
    curr = yearly.iloc[i]
    prev = yearly.iloc[i-1]
    growth = (curr - prev) / prev * 100
    yoy.append({'period': str(yearly.index[i]), 'prev': str(yearly.index[i-1]), 'growth_pct': round(growth, 2)})
results['yoy_growth'] = yoy

# Quarterly
qtrly = df.groupby(df['Order_Date'].dt.to_period('Q'))['Sales'].sum()
results['quarterly'] = {str(k): round(v, 2) for k, v in qtrly.items()}

# Top 10
top = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
results['top10_products'] = {k: round(v, 2) for k, v in top.items()}

# Bottom 10
bot = df.groupby('Product')['Sales'].sum().sort_values(ascending=True).head(10)
results['bottom10_products'] = {k: round(v, 2) for k, v in bot.items()}

# By region
reg = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
results['by_region'] = {k: round(v, 2) for k, v in reg.items()}

# By category
cat = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
results['by_category'] = {k: round(v, 2) for k, v in cat.items()}

# 2024 monthly (for MoM check)
df_2024 = df[df['Order_Date'].dt.year == 2024]
monthly_2024 = df_2024.groupby(df_2024['Order_Date'].dt.month)['Sales'].sum()
results['monthly_2024'] = {str(k): round(v, 2) for k, v in monthly_2024.items()}

# Total
results['total_sales'] = round(df['Sales'].sum(), 2)
results['total_profit'] = round(df['Profit'].sum(), 2)
results['profit_margin_pct'] = round(df['Profit'].sum() / df['Sales'].sum() * 100, 2)

print(json.dumps(results, indent=2))
