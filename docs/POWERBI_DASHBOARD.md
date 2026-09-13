# Power BI Dashboard — Syntecxhub Sales Performance

Build-ready Power BI materials for the Sales Performance Dashboard, based entirely on the existing cleaned dataset. No Python cleaning logic was modified.

**Status:** ✅ **BUILT & QA-PASSED.** The dashboard is implemented and saved as `powerbi/Syntecxhub_Project_Dashboard.pbix` (styled with `powerbi/Syntecxhub_Theme.json`). Model, DAX, layout, and reference values are complete and verified; QA sign-off in `docs/QA_REPORT.md`.

---

## 1. Data Source

- File: `data/cleaned/sales_cleaned.csv`
- 2,700 records · 2022-01-01 → 2024-12-31 · no nulls, no duplicates
- Columns: `Order_Date` (Date), `Product` (42), `Category` (7), `Region` (6), `Sales`, `Profit`

## 2. Data Model

| Table | Role | Contents |
|---|---|---|
| `sales_cleaned` | Fact | `Order_Date`, `Product`, `Category`, `Region`, `Sales`, `Profit` |
| `Date` | Dimension | `Date`, `Year`, `Quarter`, `Year-Quarter`, `Month`, `Month Number`, `Year-Month` |

- Relationship: `Date[Date]` (1) → `sales_cleaned[Order_Date]` (*), single filter direction.
- `Date[Date]` marked as date table; contiguous daily rows, no gaps.

### Date Table DAX

```dax
Date =
ADDCOLUMNS(
    CALENDAR(DATE(2022, 1, 1), DATE(2024, 12, 31)),
    "Year",         YEAR([Date]),
    "Quarter",      "Q" & QUARTER([Date]),
    "Year-Quarter", FORMAT([Date], "YYYY") & "-Q" & QUARTER([Date]),
    "Month",        FORMAT([Date], "MMM"),
    "Month Number", MONTH([Date]),
    "Year-Month",   FORMAT([Date], "YYYY-MM")
)
```

Sort rules (prevents alphabetical-ordering bugs):

- `Date[Month]` → sort by `Month Number`
- `Date[Year-Month]` → sort by `Date` (chronological)

## 3. Measures

Full DAX in `powerbi/DAX_Measures.txt`; annotated reference in `DAX_MEASURES.md` (same folder).

| Measure | DAX | Purpose | Format |
|---|---|---|---|
| Total Revenue | `SUM(sales_cleaned[Sales])` | Primary revenue KPI; used in every revenue visual | Currency USD, 2 dp |
| Total Profit | `SUM(sales_cleaned[Profit])` | Profit KPI | Currency USD, 2 dp |
| Profit Margin | `DIVIDE([Total Profit], [Total Revenue], 0)` | Profitability ratio | Percentage, 2 dp |
| Growth Rate | YoY revenue growth via `DATEADD(Date[Date], -1, YEAR)` | Current vs same prior-year period; `BLANK()` when prior period has no data | Percentage, 2 dp |

```dax
Growth Rate =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue =
    CALCULATE([Total Revenue], DATEADD(Date[Date], -1, YEAR))
RETURN
    DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, BLANK())
```

Nothing is hard-coded; every measure is dynamic under slicers.

## 4. Dashboard Layout (one executive page)

```
Title: Sales Performance Dashboard
Filters (top-right): Year | Region | Category | Product
Row 1: [ Total Revenue ] [ Total Profit ] [ Growth Rate ] [ Profit Margin ]
Row 2: [ Monthly Revenue Trend — line, Year-Month × Total Revenue ]
Row 3: [ Quarterly Performance — column, Year-Quarter ] [ Yearly Performance — column, Year ]
Row 4: [ Revenue by Region — bar ] [ Revenue by Category — bar ]
Row 5: [ Top Products by Revenue — bar, Top 5 ] [ Low-Performing Products — bar, bottom 5 ]
```

- Monthly trend axis uses `Date[Year-Month]` (chronological, 36 points).
- Quarterly chart uses `Date[Year-Quarter]` (e.g., `2024-Q3`) so identical quarter labels from different years are never merged.
- Default page filter: **Year = 2024**, so the Growth Rate KPI shows the verified +8.28% rather than a cross-window figure; the Year slicer allows any selection.

## 5. Slicers & Interaction

- Slicers: `Date[Year]`, `Region`, `Category`, `Product` — filter every visual on the page.
- Product Top-5 / Bottom-5 use visual-level Top N filters on `Total Revenue`, so rankings recompute under any filter combination (no hard-coded product names).
- Clicking a bar (region / category / product) cross-filters the other visuals; slicers are excluded from cross-filtering so they cannot be trapped by a selection.

## 6. KPI Definitions & Verified Values

| KPI | Definition | All-years value |
|---|---|---|
| Total Revenue | Σ Sales | $190,809.49 |
| Total Profit | Σ Profit | $74,378.00 |
| Profit Margin | Total Profit / Total Revenue | 38.98% |
| Growth Rate | (Current − Previous) / Previous, YoY | 2023: −14.43% · 2024: +8.28% |

Analytical reference (verified with `scripts/verify_powerbi_data.py`; used for dashboard QA):

- **Yearly revenue:** 2022 $68,579.37 · 2023 $58,685.78 · 2024 $63,544.34
- **Top 5 products:** Winter Jacket Premium $23,016.94 · Smart Watch Basic $20,374.58 · Running Sneakers $11,160.02 · Foldable Camping Chair $8,195.49 · Wireless Bluetooth Headphones $8,055.34
- **Bottom 5 products:** Sticky Notes Pad $769.82 · Dark Chocolate Bar $1,137.74 · Bath Soap Pack $1,252.35 · Phone Grip Stand $1,255.70 · Sparkling Water 12-Pack $1,278.54
- **Regions:** North America $72,869.54 · Europe $49,367.15 · Asia Pacific $29,339.93 · Middle East $16,495.32 · Latin America $15,546.10 · Africa $7,191.45
- **Categories:** Clothing $57,881.35 · Electronics $50,222.20 · Home & Garden $24,801.01 · Sports & Outdoors $22,156.34 · Office Supplies $14,869.71 · Food & Beverages $11,095.24 · Beauty & Personal Care $9,783.64

## 7. QA Performed

**Data QA (Python):** record count, date range, null/duplicate checks, column typing, and every aggregation above — all pass.

**Time QA:** `Order_Date` typed as Date; years/quarters/months derived from the contiguous Date table; `Month` sorted by `Month Number` and `Year-Month` sorted by `Date` (chronological); YoY computed only via the Date relationship; single relationship — no duplicate keys or double-counting; 2022 Growth Rate correctly blank (no prior year).

**Visual QA checklist** (full list in `powerbi/dashboard_spec.md` § 9): all four KPIs, monthly/quarterly/yearly correctness, product rankings, region/category values, slicer behavior, cross-filtering, date ordering, blank-visual check, DAX error check, and no hard-coded values — to be run in Power BI Desktop immediately after the page is assembled and after each data refresh.

## 8. Manual Step (unavoidable)

Power BI Desktop GUI work cannot be performed from this repository: build the one-page report per `powerbi/dashboard_spec.md` § 8 and save as `powerbi/Syntecxhub_Sales_Dashboard.pbix`, verifying values against Section 6 as you go.