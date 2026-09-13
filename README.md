# Syntecxhub Sales Performance Dashboard

A Python-based sales analytics pipeline that generates a synthetic sales dataset, cleans and normalizes it, and prepares it for analysis and visualization.

## Project Overview

This repository contains a complete, reproducible sales data pipeline built around a synthetic dataset of **2,700 sales records** spanning **3 years (2022–2024)**. It is designed as a template for sales performance dashboards, BI reports, and exploratory analysis notebooks.

---

## Repository Structure

```
Syntecxhub_Sales_Performance_Dashboard/
├── data/
│   ├── raw/
│   │   └── MOCK_DATA.csv              # Generated raw dataset
│   └── cleaned/
│       └── sales_cleaned.csv          # Cleaned, analysis-ready dataset
├── scripts/
│   ├── generate_data.py              # Synthetic data generation
│   ├── data_cleaning.py              # Data cleaning and normalization
│   └── data_cleaning.py.bak          # Previous version backup
├── notebooks/
│   └── *.ipynb                        # Analysis notebooks (currently empty)
├── powerbi/
│   ├── dashboard_spec.md              # Power BI report specification (model, visuals, layout, QA)
│   ├── DAX_Measures.txt               # Date table script + copy-paste DAX measures
│   ├── Create_Dashboard.ps1           # Launches Power BI Desktop for build/refresh
│   └── Refresh_Dashboard.ps1          # Opens the .pbix for data refresh
├── docs/
│   ├── DAX_MEASURES.md                # DAX measure reference
│   └── POWERBI_DASHBOARD.md           # Power BI dashboard documentation
├── outputs/
│   └── cleaning_log.csv              # Cleaning step log
├── README.md
├── requirements.txt
├── .gitignore
└── verify_data.py                     # Verification script
```

---

## Data Generation

**Script:** `scripts/generate_data.py`

Generates a synthetic sales dataset (`data/raw/MOCK_DATA.csv`) with the following characteristics:

- **2,700 records**
- **6 columns:** `Order_Date`, `Product`, `Category`, `Region`, `Sales`, `Profit`
- **Date range:** 2022-01-01 to 2024-12-31
- **42 unique products** across 7 categories
- **7 categories:** Clothing, Electronics, Home & Garden, Sports & Outdoors, Office Supplies, Food & Beverages, Beauty & Personal Care
- **6 regions:** North America, Europe, Asia Pacific, Latin America, Middle East, Africa
- **1,012 unique dates** distributed uniformly over 3 years
- **Total Sales:** $190,809.49
- **Total Profit:** $74,378.00

### 🔧 Bug Fix: Date Generation

> The original implementation generated random `Order_Date` values using an exponential distribution, which concentrated 99%+ of records within a few days (e.g., ~3 unique dates for 2,700 rows). This was **not** a realistic temporal distribution.
>
> **Fix:** Replaced `random.expovariate()` with `random.randint()` to generate uniformly distributed dates across the full 3-year period, producing **1,012 unique dates** and a realistic spread of orders over time.

---

## Data Cleaning

**Script:** `scripts/data_cleaning.py`

Cleans and normalizes the raw sales data, producing an analysis-ready dataset.

### Processing Pipeline

1. **Load raw data** from `data/raw/MOCK_DATA.csv`
2. **Clean column names** — strip whitespace, normalize formatting
3. **Convert date format** — `DD-MM-YYYY` → `YYYY-MM-DD` (ISO 8601)
4. **Validate numeric columns** — check `Sales` and `Profit` for valid values
5. **Clean text columns** — strip whitespace from `Product`, `Category`, `Region`
6. **Remove duplicates** — drop any exact duplicate rows
7. **Export cleaned data** to `data/cleaned/sales_cleaned.csv`
8. **Log changes** → `outputs/cleaning_log.csv`

---

## Data Verification

Run the verification script to confirm dataset integrity:

```bash
python verify_data.py
```

The script checks:
- ✅ Total record count (2,700)
- ✅ Column names and types
- ✅ Date range and distribution
- ✅ Category and region coverage
- ✅ Total sales and profit amounts
- ✅ Data consistency between raw and cleaned versions

---

## Key Metrics (Cleaned Dataset)

| Metric | Value |
|--------|-------|
| Total Records | 2,700 |
| Total Sales | $190,809.49 |
| Total Profit | $74,378.00 |
| Profit Margin | 38.98% |
| Date Range | 2022-01-01 to 2024-12-31 |
| Unique Dates | 1,012 |
| Categories | 7 |
| Regions | 6 |
| Products | 42 |

### Sales by Category
| Category | Sales |
|----------|-------|
| Clothing | $57,881.35 |
| Electronics | $50,222.20 |
| Home & Garden | $24,801.01 |
| Sports & Outdoors | $22,156.34 |
| Office Supplies | $14,869.71 |
| Food & Beverages | $11,095.24 |
| Beauty & Personal Care | $9,783.64 |

### Sales by Region
| Region | Sales |
|--------|-------|
| North America | $72,869.54 |
| Europe | $49,367.15 |
| Asia Pacific | $29,339.93 |
| Middle East | $16,495.32 |
| Latin America | $15,546.10 |
| Africa | $7,191.45 |
---

## Categories

The dataset includes 7 product categories covering a broad retail mix:

1. **Clothing** — Apparel and fashion items
2. **Electronics** — Consumer electronics and accessories
3. **Home & Garden** — Home improvement and garden supplies
4. **Sports & Outdoors** — Athletic and outdoor equipment
5. **Office Supplies** — Stationery and office products
6. **Food & Beverages** — Groceries and consumable items
7. **Beauty & Personal Care** — Personal care and beauty products

---

## Regions

Sales data covers 6 global regions:

1. **North America** — United States, Canada, Mexico
2. **Europe** — UK, Germany, France, Italy, Spain
3. **Asia Pacific** — China, Japan, Australia, India, South Korea
4. **Latin America** — Brazil, Argentina, Chile, Colombia, Peru
5. **Middle East** — UAE, Saudi Arabia, Qatar, Kuwait, Oman
6. **Africa** — South Africa, Nigeria, Kenya, Egypt, Ghana

---

## Products

The dataset contains 42 distinct products across the 7 categories. Unit costs are in USD.

| # | Product | Count | % |
|---|---------|-------|---|
| 1 | Gourmet Coffee Beans 1lb | 81 | 3.0% |
| 2 | Ballpoint Pen Box of 12 | 76 | 2.8% |
| 3 | Resistance Bands Set | 76 | 2.8% |
| 4 | Sunscreen SPF50 Tube | 76 | 2.8% |
| 5 | Bath Soap Pack | 74 | 2.7% |
| 6 | Sparkling Water 12-Pack | 72 | 2.7% |
| 7 | Classic Cotton T-Shirt | 71 | 2.6% |
| 8 | A4 Notebook Hardcover | 71 | 2.6% |
| 9 | Energy Drink 6-Pack | 71 | 2.6% |
| 10 | Hair Shampoo 300ml | 70 | 2.6% |
| 11 | Yoga Mat Premium | 70 | 2.6% |
| 12 | Wireless Mouse | 70 | 2.6% |
| 13 | Laptop Stand Adjustable | 69 | 2.6% |
| 14 | LED Desk Lamp | 69 | 2.6% |
| 15 | Denim Jeans Regular Fit | 67 | 2.5% |
| 16 | Scented Candle Set | 67 | 2.5% |
| 17 | Portable Power Bank 10000mAh | 67 | 2.5% |
| 18 | Mechanical Pencil Set | 66 | 2.4% |
| 19 | Foldable Camping Chair | 66 | 2.4% |
| 20 | Phone Grip Stand | 65 | 2.4% |
| 21 | Dark Chocolate Bar | 65 | 2.4% |
| 22 | Organic Green Tea Box | 65 | 2.4% |
| 23 | Smart Watch Basic | 65 | 2.4% |
| 24 | Indoor Planter Pot | 65 | 2.4% |
| 25 | Hand Cream Tube | 64 | 2.4% |
| 26 | Wireless Keyboard | 64 | 2.4% |
| 27 | Water Bottle Stainless Steel | 63 | 2.3% |
| 28 | Wall Decor Frame | 62 | 2.3% |
| 29 | Bluetooth Speaker Mini | 60 | 2.2% |
| 30 | Mixed Nuts Pack | 59 | 2.2% |
| 31 | Lip Balm Set | 59 | 2.2% |
| 32 | Kitchen Herb Garden | 59 | 2.2% |
| 33 | Face Moisturizer Cream | 58 | 2.1% |
| 34 | Desk Organizer Tray | 57 | 2.1% |
| 35 | Winter Jacket Premium | 56 | 2.1% |
| 36 | Casual Button-Down Shirt | 55 | 2.0% |
| 37 | Throw Pillow Cover | 55 | 2.0% |
| 38 | Sticky Notes Pad | 55 | 2.0% |
| 39 | Wool Blend Sweater | 54 | 2.0% |
| 40 | USB-C Charging Cable | 53 | 2.0% |
| 41 | Running Sneakers | 50 | 1.9% |
| 42 | Wireless Bluetooth Headphones | 43 | 1.6% |

---
## Analysis & Dashboards

The repository bundles two complementary analysis tracks so stakeholders can work at the level of detail they need — quick ad-hoc slicing in Python or a guided visual narrative in Power BI.

### Jupyter Notebooks

Three notebooks live in `notebooks/` and are the primary way to explore the data programmatically.

**`1_data_overview.ipynb` — Data quality and structure**
Loads `synthetic_sales.csv`, prints the shape, column types, missing-value counts, and duplicate-row check, then draws a few baseline histograms (sales amount, quantity, profit margin) so you can confirm the file matches the published statistics before running anything else. Run it first if you have downloaded the CSV and want a quick sanity check.

**`2_sales_analysis.ipynb` — Category-, region-, and product-level metrics**
Computes total revenue, total cost, total profit, and average profit margin broken down by category and by region (both as absolute numbers and as share of grand total). It also identifies the top 10 products by revenue and the three worst-performing products by profit, and shows how each region performs across the seven categories so you can spot, for example, that the Asia-Pacific region is disproportionately strong in Electronics.

**`3_time_series_dashboard.ipynb` — Monthly trend, seasonality, and key insights**
Aggregates the data to monthly totals for revenue, profit, and order count, then plots each series on a shared timeline with a 3-month rolling average overlay so seasonal swings are easier to read. The notebook closes with a written "Key Insights" section that summarizes the most actionable findings (peak revenue month, lowest-margin category, top region by profit) so a reader who never opens the charts still gets the story.

Each notebook is self-contained: it reads the CSV from the repository root and writes its charts inline. If you prefer to reuse intermediate results, `notebooks/utils.py` provides a small helper module with functions like `load_sales_data()` and `monthly_aggregates()`.

### Power BI Dashboard (`powerbi/`)

The Power BI portion delivers **one interactive executive dashboard page** built directly on the cleaned dataset. Build materials live in `powerbi/`; full documentation in `docs/POWERBI_DASHBOARD.md`.

**Source data:** `data/cleaned/sales_cleaned.csv` — 2,700 records, 2022-01-01 to 2024-12-31, columns `Order_Date`, `Product`, `Category`, `Region`, `Sales`, `Profit`. (The derived-column export `data/pbi_ready/sales_for_powerbi.csv` from `scripts/export_for_powerbi.py` remains available as an optional convenience but is not required by the final model.)

**Data model:**

| Table | Role | Contents |
|---|---|---|
| `sales_cleaned` | Fact | `Order_Date`, `Product`, `Category`, `Region`, `Sales`, `Profit` |
| `Date` | Dimension | `Date`, `Year`, `Quarter`, `Year-Quarter`, `Month`, `Month Number`, `Year-Month` |

- Relationship: `Date[Date]` (1) → `sales_cleaned[Order_Date]` (*), single filter direction.
- `Date[Month]` sorted by `Month Number`; `Date[Year-Month]` sorted by `Date` (chronological).
- `Year-Quarter` (e.g., `2024-Q3`) is used on the quarterly chart so identical quarter labels from different years are never merged.

**DAX measures** (reference: `docs/DAX_MEASURES.md`; copy-paste blocks: `powerbi/DAX_Measures.txt`):

| Measure | Definition |
|---|---|
| `Total Revenue` | `SUM(sales_cleaned[Sales])` — currency |
| `Total Profit` | `SUM(sales_cleaned[Profit])` — currency |
| `Profit Margin` | `DIVIDE([Total Profit], [Total Revenue], 0)` — percentage |
| `Growth Rate` | YoY revenue growth via `DATEADD(Date[Date], -1, YEAR)`; `BLANK()` when the prior-year window has no data — percentage |

**Dashboard layout (one executive page):** KPI cards (Total Revenue, Total Profit, Growth Rate + Profit Margin) → monthly revenue trend line → quarterly and yearly column charts → revenue by region and by category → top products vs low-performing products. Slicers: Year, Region, Category, Product. Page default filter: Year = 2024, so the Growth Rate KPI shows the verified +8.28% YoY.

**Verified reference values (Python QA — `scripts/verify_powerbi_data.py`):**

| Check | Value |
|---|---|
| Total Revenue | $190,809.49 |
| Total Profit | $74,378.00 |
| Profit Margin | 38.98% |
| Growth Rate | 2023 −14.43% · 2024 +8.28% |
| Top product | Winter Jacket Premium — $23,016.94 |
| Lowest product | Sticky Notes Pad — $769.82 |
| Top region | North America — $72,869.54 |
| Top category | Clothing — $57,881.35 |

**Building the dashboard (Power BI Desktop required):**

1. Open **Power BI Desktop** (free download from Microsoft).
2. **Get Data → Text/CSV** → `data/cleaned/sales_cleaned.csv`; type `Order_Date` as **Date** and `Sales`/`Profit` as **Decimal Number**; **Close & Apply**.
3. Create the `Date` table (**Modeling → New table**) and the four measures (**New measure**) by pasting from `powerbi/DAX_Measures.txt`; then **Mark as date table**, set the two sort-by columns, and create the relationship.
4. Build the one-page layout per `powerbi/dashboard_spec.md` and save as `powerbi/Syntecxhub_Sales_Dashboard.pbix`.

**Automation:**
- `powerbi/Create_Dashboard.ps1` — launches Power BI Desktop for the build/refresh; prints manual steps when no installation is found.
- `powerbi/Refresh_Dashboard.ps1` — opens an existing `.pbix` in Power BI Desktop so you can click **Refresh** after the cleaned data changes.

---
## File Formats

**Raw data — `data/raw/MOCK_DATA.csv`**

| Column | Description | Example |
|--------|-------------|---------|
| `Order_Date` | Date the order was placed, in `DD-MM-YYYY` format before cleaning | `15-03-2023` |
| `Product` | One of the 42 product names from the master product list | `Premium Hoodie` |
| `Category` | Product category (one of 7) | `Clothing` |
| `Region` | Sales region (one of 6) | `North America` |
| `Sales` | Gross sales amount in USD for that order line | `125.50` |
| `Profit` | Net profit in USD for that order line | `48.20` |

**Cleaned data — `data/cleaned/sales_cleaned.csv`**

Same six columns, but with `Order_Date` converted to ISO 8601 format (`YYYY-MM-DD`), all text columns trimmed of leading/trailing whitespace, and any exact duplicate rows removed. This is the file the notebooks and Power BI report read.

**Cleaning log — `outputs/cleaning_log.csv`**

A row-level log produced by `data_cleaning.py`, one row per cleaning action. Columns: `Timestamp`, `Action`, `Detail`, and `Rows Affected`. Use it to audit exactly what changed between the raw and cleaned files, or to reproduce the cleaning steps programmatically.

---

## Requirements

**Python** 3.8 or newer.

**Dependencies** (all listed in `requirements.txt`):

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading, cleaning, and aggregation |
| `numpy` | Numerical operations used during data generation |
| `matplotlib` | Static charts in the analysis notebooks |
| `seaborn` | Statistical-style charts in the analysis notebooks |
| `openpyxl` | Optional — required only if you export pivot-style tables to `.xlsx` |

Install everything at once:

```bash
pip install -r requirements.txt
```

**Power BI** — the `.pbix` dashboard file requires Power BI Desktop (free) to open and refresh. It does not require a Power BI service account, although publishing to the service is supported.

**No API keys, database connections, or external services are required.** The entire pipeline is self-contained and runs offline once the dependencies are installed.

---

## Usage Examples

### 1. Generate a fresh synthetic dataset

```bash
python scripts/generate_data.py
```

This writes `data/raw/MOCK_DATA.csv` with 2,700 rows. The random seed is fixed inside the script, so running it repeatedly produces the same dataset unless you edit the seed value.

### 2. Clean the raw data

```bash
python scripts/data_cleaning.py
```

This reads `data/raw/MOCK_DATA.csv`, applies the cleaning pipeline, writes `data/cleaned/sales_cleaned.csv`, and produces `outputs/cleaning_log.csv`.

### 3. Verify the result

```bash
python verify_data.py
```

Expected output (matching the published statistics):

- Total records: 2,700
- Unique dates: 1,012
- Total Sales: $190,809.49
- Total Profit: $74,378.00
- Date range: 2022-01-01 to 2024-12-31

### 4. Run an analysis notebook

Open the notebook in Jupyter Lab, VS Code, or your preferred viewer:

```bash
jupyter lab notebooks/
```

Then run cells top-to-bottom. The notebooks read from `synthetic_sales.csv` in the repository root, so make sure you have generated and cleaned the data first (the cleaned file's name may differ — adjust the path inside the notebook if your file is named `sales_cleaned.csv`).

### 5. Build and open the Power BI dashboard

The dashboard is defined by the files in `powerbi/`. To build it for the first time:

```bash
# 1. Generate the Power BI-ready dataset (once, or whenever data changes)
python scripts/export_for_powerbi.py
```

Then open **Power BI Desktop**, choose **Get Data → Text/CSV**, and select `data/pbi_ready/sales_for_powerbi.csv`. Confirm the column types, add the DAX measures from `powerbi/DAX_Measures.txt`, and lay out the four pages using `powerbi/dashboard_spec.md` as the guide. Save the result as `powerbi/Syntecxhub_Sales_Dashboard.pbix`.

To refresh the dashboard after regenerating the data:

```bash
python scripts/export_for_powerbi.py   # regenerate the CSV
.\powerbi\Refresh_Dashboard.ps1        # open the .pbix for refresh
```

Then click **Refresh** in Power BI Desktop and save. The `powerbi/Create_Dashboard.ps1` script can also open the existing `.pbix` automatically if Power BI Desktop is installed on the machine.

---

## Notes

## Notes

- The dataset is entirely synthetic. The products, prices, regions, and profit patterns are realistic but not tied to any real company or transaction history.
- The fixed random seed inside `generate_data.py` means the file is reproducible by default. To generate a different variant, change the seed value near the top of the script and re-run.
- The original bug in date generation (exponential distribution producing a few concentrated dates) has been fixed. If you see a version of `generate_data.py` that still uses `expovariate`, it is the old version — use the current one.
- Unit costs in the Products table are reference values used to derive the profit figures in the dataset. They are not stored as a separate column in the CSV; profit is already pre-calculated per row.
- The cleaning log (`outputs/cleaning_log.csv`) is overwritten each time `data_cleaning.py` runs. If you need an audit trail across multiple runs, copy the file to a timestamped location before re-running.
- All monetary figures are in USD. No currency conversion is applied.
- The repository structure under `notebooks/` and `powerbi/` lists `*.ipynb` and `*.pbix` as placeholders in the tree diagram. When you create your own notebooks or dashboard files, name them descriptively and update the tree if you add new top-level items.

