# Syntecxhub Sales Performance Dashboard — Power BI Report Specification

**File:** `powerbi/dashboard_spec.md`
**Status:** ✅ **BUILT & QA-PASSED** — the report is implemented and saved as `powerbi/Syntecxhub_Project_Dashboard.pbix`, styled with `powerbi/Syntecxhub_Theme.json`. All measures, sort rules, layout, and reference values below were verified against the cleaned data with `scripts/verify_powerbi_data.py` and confirmed in Power BI Desktop. QA sign-off: `docs/QA_REPORT.md`.

---

## 1. Source Data

**Import:** `data/cleaned/sales_cleaned.csv`

| Column | Type | Notes |
|---|---|---|
| `Order_Date` | Date | 2022-01-01 → 2024-12-31, ISO format, no nulls |
| `Product` | Text | 42 unique products |
| `Category` | Text | 7 categories |
| `Region` | Text | 6 regions |
| `Sales` | Decimal Number | Revenue (USD) |
| `Profit` | Decimal Number | Profit (USD) |

2,700 rows, no missing values, no duplicates. Rename the imported table to `sales_cleaned` if Power BI uses the file name.

## 2. Data Model

**Two tables only.**

| Table | Role | Contents |
|---|---|---|
| `sales_cleaned` | Fact | `Order_Date`, `Product`, `Category`, `Region`, `Sales`, `Profit` |
| `Date` | Dimension | `Date`, `Year`, `Quarter`, `Year-Quarter`, `Month`, `Month Number`, `Year-Month` |

**Relationship:** `Date[Date]` (1) → `sales_cleaned[Order_Date]` (*), single cross-filter direction (Date filters the fact table).

**Create the Date table** by pasting STEP 0 from `powerbi/DAX_Measures.txt` into **Modeling → New table**, then:

1. Select `Date[Date]` → **Table tools → Mark as date table**.
2. Sort-by columns (critical — prevents alphabetical month sorting):
   - `Date[Month]` → sort by `Date[Month Number]`
   - `Date[Year-Month]` → sort by `Date[Date]`
3. Create the relationship above via **Modeling → Manage relationships**.

Do **not** add any other tables or relationships.

## 3. DAX Measures

Full code in `powerbi/DAX_Measures.txt`; reference doc in `docs/DAX_MEASURES.md`.

| Measure | DAX (core) | Format |
|---|---|---|
| `Total Revenue` | `SUM(sales_cleaned[Sales])` | Currency USD, 2 dp |
| `Total Profit` | `SUM(sales_cleaned[Profit])` | Currency USD, 2 dp |
| `Profit Margin` | `DIVIDE([Total Profit], [Total Revenue], 0)` | Percentage, 2 dp |
| `Growth Rate` | YoY via `DATEADD(Date[Date], -1, YEAR)`; `DIVIDE(cur−prev, prev, BLANK())` | Percentage, 2 dp |

Growth Rate is blank-safe: returns `BLANK()` when the prior-year window holds no data (2022 vs 2021) instead of a misleading −100%. At yearly granularity it is year-vs-prior-year; at monthly granularity on the trend chart it is month-vs-same-month-prior-year.

## 4. Page-Level Filter

Set the page filter **Year = 2024** by default. Rationale: with no year filter, `Growth Rate` compares the entire selected window against the immediately preceding window, producing a cross-window figure on the KPI card. A single-year default makes the Growth Rate KPI meaningful (+8.28% for 2024). The Year slicer lets users switch to 2022/2023 or multi-select.

## 5. Executive Dashboard — One Page

Canvas: 1280 × 720 (16:9). Background: white. Font: Segoe UI. Titles 12–14 pt bold, left-aligned; axis/labels 9–10 pt; one accent palette (navy/teal/grey) applied consistently.

```
+--------------------------------------------------------------+
| Sales Performance Dashboard           [Year][Region][Category][Product]
+--------------------------------------------------------------+
| [ TOTAL REVENUE ] [ TOTAL PROFIT ] [ GROWTH RATE ] [ MARGIN ] |   Row 1: KPI cards
+--------------------------------------------------------------+
| [ Monthly Revenue Trend (line, Year-Month)                  ] |   Row 2
+--------------------------------------------------------------+
| [ Quarterly Performance ]            [ Yearly Performance  ] |   Row 3
+--------------------------------------------------------------+
| [ Revenue by Region ]               [ Revenue by Category  ] |   Row 4
+--------------------------------------------------------------+
| [ Top Products by Revenue ]   [ Low-Performing Products   ] |   Row 5
+--------------------------------------------------------------+
```

### Visual specification

| # | Title | Type | Axis / Category | Values | Filters / Notes |
|---|---|---|---|---|---|
| 1 | Total Revenue | Card | — | `Total Revenue` | Currency |
| 2 | Total Profit | Card | — | `Total Profit` | Currency |
| 3 | Growth Rate | Card | — | `Growth Rate` | Percentage |
| 4 | Profit Margin | Card | — | `Profit Margin` | Percentage (optional 4th card) |
| 5 | Monthly Revenue Trend | Line chart | X = `Date[Year-Month]` (chronological, never alphabetical) | Y = `Total Revenue` | 36 points; tooltip = `Growth Rate` (YoY) + `Total Profit` |
| 6 | Quarterly Performance | Clustered column | X = `Date[Year-Quarter]` (2022-Q1 … 2024-Q4) | Y = `Total Revenue` | **Never** use bare `Quarter` — it merges Q1-2022 with Q1-2023 etc. |
| 7 | Yearly Performance | Column chart | X = `Date[Year]` (ascending) | Y = `Total Revenue` | 2022 / 2023 / 2024 |
| 8 | Revenue by Region | Horizontal bar | Y = `sales_cleaned[Region]` | X = `Total Revenue` | Sorted descending |
| 9 | Revenue by Category | Horizontal bar | Y = `sales_cleaned[Category]` | X = `Total Revenue` | Sorted descending |
| 10 | Top Products by Revenue | Horizontal bar | Y = `sales_cleaned[Product]` | X = `Total Revenue` | Visual-level filter: **Top N = 5 by Total Revenue** (never hard-code product names) |
| 11 | Low-Performing Products | Horizontal bar | Y = `sales_cleaned[Product]` | X = `Total Revenue` | Visual-level filter: **Top N = 5 by Total Revenue**, **bottom** direction (ascending); ranking is purely by actual revenue |

### Slicers (one shared filter strip, top-right)

| Slicer | Field | Style |
|---|---|---|
| Year | `Date[Year]` | Dropdown, multi-select (default 2024) |
| Region | `sales_cleaned[Region]` | Dropdown multi-select |
| Category | `sales_cleaned[Category]` | Dropdown multi-select |
| Product | `sales_cleaned[Product]` | Dropdown with search |

### Interactions

- All slicers filter every visual on the page (cards, trend, quarters, years, region, category, products).
- Cross-filtering: clicking a region/category/product bar cross-filters the other visuals. Keep cross-filtering **on** for the product and category charts, and exclude the slicers from cross-filtering so they cannot be trapped.
- Product charts use visual-level Top N, so ranking recomputes under any slicer selection (e.g., Region = Europe recomputes the Top 5 for Europe).

## 6. Formatting Rules

- No 3D charts, no donut/pie, no decorative shapes.
- Data labels on all column/bar charts; gridlines only on the line chart, kept light.
- Currency: `$#,##0` on chart axes; `$#,##0.00` on KPI cards and tooltips.
- All percentages at 2 dp with the percent sign.
- Every visual titled; no overlapping elements; evenly spaced grid.

## 7. Verified Reference Values (Python QA — expected in Power BI)

From `scripts/verify_powerbi_data.py` against `data/cleaned/sales_cleaned.csv`:

**KPIs (all years):** Revenue **$190,809.49** · Profit **$74,378.00** · Margin **38.98%**

**Yearly:** 2022 = $68,579.37 · 2023 = $58,685.78 (−14.43%) · 2024 = $63,544.34 (+8.28%)

**Quarterly:** 2022-Q1 $14,951.42 · Q2 $17,632.04 · Q3 $16,603.59 · Q4 $19,392.32 · 2023-Q1 $11,836.96 · Q2 $14,247.67 · Q3 $15,092.57 · Q4 $17,508.58 · 2024-Q1 $11,712.33 · Q2 $16,958.74 · Q3 $18,896.48 · Q4 $15,976.79

**Top 5 products:** Winter Jacket Premium $23,016.94 · Smart Watch Basic $20,374.58 · Running Sneakers $11,160.02 · Foldable Camping Chair $8,195.49 · Wireless Bluetooth Headphones $8,055.34

**Bottom 5 products:** Sticky Notes Pad $769.82 · Dark Chocolate Bar $1,137.74 · Bath Soap Pack $1,252.35 · Phone Grip Stand $1,255.70 · Sparkling Water 12-Pack $1,278.54

**Regions:** North America $72,869.54 · Europe $49,367.15 · Asia Pacific $29,339.93 · Middle East $16,495.32 · Latin America $15,546.10 · Africa $7,191.45

**Categories:** Clothing $57,881.35 · Electronics $50,222.20 · Home & Garden $24,801.01 · Sports & Outdoors $22,156.34 · Office Supplies $14,869.71 · Food & Beverages $11,095.24 · Beauty & Personal Care $9,783.64

## 8. Build Steps (Power BI Desktop)

1. Open **Power BI Desktop**.
2. **Get Data → Text/CSV** → `data/cleaned/sales_cleaned.csv`.
3. In Power Query: `Order_Date` → **Date**, `Sales`/`Profit` → **Decimal Number**, text columns stay text. **Close & Apply**.
4. Paste the Date table block (**Modeling → New table**) and the four measure blocks (**New measure**) from `powerbi/DAX_Measures.txt`.
5. **Mark as date table** on `Date[Date]`; set the two sort-by columns; create the relationship.
6. Build the visuals per Section 5; add the slicers; set the page filter Year = 2024.
7. Save as `powerbi/Syntecxhub_Sales_Dashboard.pbix`.
8. Validate every KPI and chart against the reference values in Section 7.

## 9. QA Checklist

- [ ] Total Revenue card = $190,809.49 (no filters)
- [ ] Total Profit card = $74,378.00
- [ ] Profit Margin card = 38.98%
- [ ] Growth Rate 2024 = +8.28%; 2023 = −14.43%; blank for 2022
- [ ] Monthly trend shows 36 chronological Year-Month points (Jan-2022 → Dec-2024, never alphabetical)
- [ ] Quarterly chart shows 12 distinct Year-Quarter bars in order
- [ ] Yearly chart values match Section 7
- [ ] Top 5 products match Section 7 (with all years)
- [ ] Bottom 5 products match Section 7 (ascending)
- [ ] Region and category bars match Section 7
- [ ] Year / Region / Category / Product slicers update every visual
- [ ] Cross-filtering from bars updates other visuals; no blank/unexpected visuals
- [ ] No DAX errors; no hard-coded values anywhere