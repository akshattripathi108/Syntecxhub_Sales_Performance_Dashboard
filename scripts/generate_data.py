#!/usr/bin/env python3
"""
Syntecxhub Sales Performance Dashboard
Data Generation Script - Phase 2
=====================================
Generates a realistic sales dataset with:
- 2500-3000 rows
- Date range: Jan 2022 - Dec 2024
- 20-25 unique products across 5-7 categories
- 5 regions with varying performance
- Realistic sales/profit values with seasonal patterns
"""

import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

print("=" * 70)
print("Syntecxhub Sales Performance Dashboard")
print("Data Generation Script - Phase 2")
print("=" * 70)

# Product catalog - realistic product names organized by category
products = {
    "Electronics": [
        "Wireless Bluetooth Headphones",
        "USB-C Charging Cable",
        "Smart Watch Basic",
        "Portable Power Bank 10000mAh",
        "Wireless Mouse",
        "Laptop Stand Adjustable",
        "Bluetooth Speaker Mini",
        "Phone Grip Stand"
    ],
    "Clothing": [
        "Classic Cotton T-Shirt",
        "Denim Jeans Regular Fit",
        "Wool Blend Sweater",
        "Running Sneakers",
        "Casual Button-Down Shirt",
        "Winter Jacket Premium"
    ],
    "Food & Beverages": [
        "Organic Green Tea Box",
        "Gourmet Coffee Beans 1lb",
        "Mixed Nuts Pack",
        "Dark Chocolate Bar",
        "Energy Drink 6-Pack",
        "Sparkling Water 12-Pack"
    ],
    "Home & Garden": [
        "Scented Candle Set",
        "Indoor Planter Pot",
        "Throw Pillow Cover",
        "LED Desk Lamp",
        "Wall Decor Frame",
        "Kitchen Herb Garden"
    ],
    "Sports & Outdoors": [
        "Yoga Mat Premium",
        "Water Bottle Stainless Steel",
        "Resistance Bands Set",
        "Sunscreen SPF50 Tube",
        "Foldable Camping Chair"
    ],
    "Office Supplies": [
        "Sticky Notes Pad",
        "Mechanical Pencil Set",
        "Desk Organizer Tray",
        "A4 Notebook Hardcover",
        "Ballpoint Pen Box of 12",
        "Wireless Keyboard"
    ],
    "Beauty & Personal Care": [
        "Face Moisturizer Cream",
        "Hair Shampoo 300ml",
        "Lip Balm Set",
        "Hand Cream Tube",
        "Bath Soap Pack"
    ]
}

categories = list(products.keys())
all_products = []
for cat, prods in products.items():
    for p in prods:
        all_products.append((p, cat))

# Region performance factors (some regions sell better than others)
region_factor = {
    "North America": 1.4,
    "Europe": 1.2,
    "Asia Pacific": 0.9,
    "Middle East": 0.7,
    "Latin America": 0.6,
    "Africa": 0.4
}

# Product base prices (realistic range)
product_base_price = {
    "Wireless Bluetooth Headphones": 79.99,
    "USB-C Charging Cable": 12.99,
    "Smart Watch Basic": 149.99,
    "Portable Power Bank 10000mAh": 39.99,
    "Wireless Mouse": 29.99,
    "Laptop Stand Adjustable": 34.99,
    "Bluetooth Speaker Mini": 44.99,
    "Phone Grip Stand": 9.99,
    "Classic Cotton T-Shirt": 24.99,
    "Denim Jeans Regular Fit": 59.99,
    "Wool Blend Sweater": 69.99,
    "Running Sneakers": 89.99,
    "Casual Button-Down Shirt": 39.99,
    "Winter Jacket Premium": 199.99,
    "Organic Green Tea Box": 14.99,
    "Gourmet Coffee Beans 1lb": 18.99,
    "Mixed Nuts Pack": 12.99,
    "Dark Chocolate Bar": 6.99,
    "Energy Drink 6-Pack": 11.99,
    "Sparkling Water 12-Pack": 8.99,
    "Scented Candle Set": 24.99,
    "Indoor Planter Pot": 32.99,
    "Throw Pillow Cover": 19.99,
    "LED Desk Lamp": 49.99,
    "Wall Decor Frame": 29.99,
    "Kitchen Herb Garden": 27.99,
    "Yoga Mat Premium": 44.99,
    "Water Bottle Stainless Steel": 22.99,
    "Resistance Bands Set": 18.99,
    "Sunscreen SPF50 Tube": 13.99,
    "Foldable Camping Chair": 54.99,
    "Sticky Notes Pad": 5.99,
    "Mechanical Pencil Set": 11.99,
    "Desk Organizer Tray": 24.99,
    "A4 Notebook Hardcover": 14.99,
    "Ballpoint Pen Box of 12": 8.99,
    "Wireless Keyboard": 59.99,
    "Face Moisturizer Cream": 28.99,
    "Hair Shampoo 300ml": 12.99,
    "Lip Balm Set": 14.99,
    "Hand Cream Tube": 9.99,
    "Bath Soap Pack": 7.99
}

# Product profit margins (lower-performing products have lower margins)
product_margin = {
    "Wireless Bluetooth Headphones": 0.35,
    "USB-C Charging Cable": 0.45,
    "Smart Watch Basic": 0.28,
    "Portable Power Bank 10000mAh": 0.32,
    "Wireless Mouse": 0.40,
    "Laptop Stand Adjustable": 0.38,
    "Bluetooth Speaker Mini": 0.33,
    "Phone Grip Stand": 0.50,
    "Classic Cotton T-Shirt": 0.55,
    "Denim Jeans Regular Fit": 0.48,
    "Wool Blend Sweater": 0.45,
    "Running Sneakers": 0.38,
    "Casual Button-Down Shirt": 0.52,
    "Winter Jacket Premium": 0.30,
    "Organic Green Tea Box": 0.42,
    "Gourmet Coffee Beans 1lb": 0.38,
    "Mixed Nuts Pack": 0.50,
    "Dark Chocolate Bar": 0.45,
    "Energy Drink 6-Pack": 0.48,
    "Sparkling Water 12-Pack": 0.52,
    "Scented Candle Set": 0.45,
    "Indoor Planter Pot": 0.40,
    "Throw Pillow Cover": 0.48,
    "LED Desk Lamp": 0.35,
    "Wall Decor Frame": 0.42,
    "Kitchen Herb Garden": 0.40,
    "Yoga Mat Premium": 0.45,
    "Water Bottle Stainless Steel": 0.42,
    "Resistance Bands Set": 0.50,
    "Sunscreen SPF50 Tube": 0.45,
    "Foldable Camping Chair": 0.32,
    "Sticky Notes Pad": 0.55,
    "Mechanical Pencil Set": 0.50,
    "Desk Organizer Tray": 0.40,
    "A4 Notebook Hardcover": 0.45,
    "Ballpoint Pen Box of 12": 0.52,
    "Wireless Keyboard": 0.32,
    "Face Moisturizer Cream": 0.48,
    "Hair Shampoo 300ml": 0.45,
    "Lip Balm Set": 0.50,
    "Hand Cream Tube": 0.52,
    "Bath Soap Pack": 0.55
}

# Seasonal multipliers by month (0=January, 11=December)
seasonal = [
    0.85,  # Jan - post-holiday lull
    0.90,  # Feb
    1.00,  # Mar
    1.05,  # Apr
    1.10,  # May
    1.20,  # Jun - summer start
    1.25,  # Jul
    1.15,  # Aug
    1.05,  # Sep
    0.95,  # Oct
    1.00,  # Nov
    1.35   # Dec - holiday season
]

# Generate orders
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
total_days = (end_date - start_date).days

# Target ~2700 orders over 3 years
num_orders = 2700

print(f"\nGenerating {num_orders} orders...")
print(f"Date range: {start_date.date()} to {end_date.date()}")
print(f"Categories: {len(categories)}")
print(f"Products: {len(all_products)}")
print(f"Regions: {len(region_factor)}")

orders = []

for i in range(num_orders):
    # Random date uniformly distributed across the full 3-year range
    day_offset = np.random.randint(0, total_days + 1)
    order_date = start_date + timedelta(days=day_offset)
    
    # Random region (weighted by performance)
    region = np.random.choice(list(region_factor.keys()), p=[0.25, 0.22, 0.18, 0.12, 0.13, 0.10])
    
    # Random product (weighted towards popular items)
    product, category = random.choice(all_products)
    base_price = product_base_price[product]
    margin = product_margin[product]
    
    # Apply seasonal multiplier
    month = order_date.month - 1
    seasonal_mult = seasonal[month]
    
    # Apply region factor
    region_mult = region_factor[region]
    
    # Quantity (1-5, skewed towards 1-2)
    quantity = int(np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.12, 0.08, 0.05]))
    
    # Calculate sales and profit
    sales = base_price * quantity * seasonal_mult * region_mult * np.random.uniform(0.9, 1.1)
    profit = sales * margin * np.random.uniform(0.85, 1.15)
    
    orders.append({
        "Order_Date": order_date.strftime("%d-%m-%Y"),
        "Product": product,
        "Category": category,
        "Region": region,
        "Sales": round(sales, 2),
        "Profit": round(profit, 2)
    })

# Create DataFrame
df = pd.DataFrame(orders)

print(f"\nDataset generated:")
print(f"  Rows: {len(df)}")
print(f"  Unique Products: {df['Product'].nunique()}")
print(f"  Categories: {df['Category'].nunique()}")
print(f"  Regions: {df['Region'].nunique()}")
print(f"  Total Sales: ${df['Sales'].sum():,.2f}")
print(f"  Total Profit: ${df['Profit'].sum():,.2f}")
print(f"  Profit Margin: {(df['Profit'].sum()/df['Sales'].sum()*100):.2f}%")

# Save to CSV
BASE = __file__ if '__file__' in dir() else '.'
import os
BASE = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE, '..', 'data', 'raw', 'MOCK_DATA.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nSaved to: {output_path}")
print("\nData generation complete!")
