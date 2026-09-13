# DAX Measures — Syntecxhub Sales Performance Dashboard

All measures use the `sales_cleaned` table and the `Date` table.

---

## Data Model

| Table | Key Columns | Role |
|-------|-------------|------|
| `sales_cleaned` | `Order_Date`, `Sales`, `Profit`, `Product`, `Category`, `Region` | Fact table |
| `Date` | `Date`, `Year`, `Quarter`, `Month`, `Month Number`, `Year-Month` | Dimension table |

**Relationship:** `Date[Date]` (1) → (*) `sales_cleaned[Order_Date]`  
**Cross-filter direction:** Single (Date → sales_cleaned)

---

## Measures

### Total Revenue

```dax
Total Revenue = SUM(sales_cleaned[Sales])
```

**Purpose:** Sum of all sales amounts. Currency-formatted. Used as the primary revenue KPI and in all trend/comparison visuals.

---

### Total Profit

```dax
Total Profit = SUM(sales_cleaned[Profit])
```

**Purpose:** Sum of all profit amounts. Currency-formatted. Used as the profit KPI.

---

### Profit Margin

```dax
Profit Margin = 
DIVIDE(
    [Total Profit],
    [Total Revenue],
    0
)
```

**Purpose:** Profit as a percentage of revenue. Formatted as percentage. Returns 0 when revenue is zero to avoid division errors.

---

### Growth Rate

```dax
Growth Rate = 
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = 
    CALCULATE(
        [Total Revenue],
        DATEADD(Date[Date], -1, YEAR)
    )
RETURN
    DIVIDE(
        CurrentRevenue - PreviousRevenue,
        PreviousRevenue,
        BLANK()
    )
```

**Purpose:** Year-over-year revenue growth percentage. Uses `DATEADD` on the Date table for time intelligence. Returns `BLANK()` when previous-period revenue is zero or null (no misleading 100%/−100% artifacts).

**Note:** When viewed at the yearly granularity, this compares each year to the prior year. When viewed at a lower granularity (e.g., monthly) with a 1-year window, it compares the same month in the prior year.

---

## Formatting

| Measure | Format |
|---------|--------|
| Total Revenue | Currency (USD), 2 decimal places |
| Total Profit | Currency (USD), 2 decimal places |
| Profit Margin | Percentage, 2 decimal places |
| Growth Rate | Percentage, 2 decimal places |

---

## Sorting Configuration

- `Date[Month]` is sorted by `Date[Month Number]` (not alphabetically).
- `Date[Year-Month]` is sorted by `Date[Date]` (chronologically).
- Quarter labels (`Q1`, `Q2`, `Q3`, `Q4`) appear in correct temporal order when used with Year.

---

## Time Intelligence Notes

- All time-based calculations rely on the contiguous `Date` table (no gaps).
- `DATEADD(Date[Date], -1, YEAR)` is the single source of truth for "previous period."
- If a slicer filters to a single year, Growth Rate will show `BLANK()` for the first year in context (no prior year to compare).
