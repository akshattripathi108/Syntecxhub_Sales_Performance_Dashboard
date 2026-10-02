# Project Glossary — Syntecxhub Sales Performance

Domain terms and concepts used across data processing, modeling, and reporting.

---

### Raw Transaction
An unverified sales record directly ingested from source files containing `Order_Date`, `Product`, `Category`, `Region`, `Sales`, and `Profit`.

### Quarantine
A holding area (`data/quarantine/`) for records that fail validation constraints (such as negative sales, unparseable dates, or missing required fields) before they can pollute clean datasets.

### Compound Natural Key
A combination of business fields (`Order_Date` + `Product` + `Region` + `Sales`) used to detect and prevent duplicate transaction entries across multiple batch ingestions.

### Clean Dataset
The sanitized, deduplicated, and verified fact table (`data/cleaned/sales_cleaned.csv`) representing the single source of truth for analytical aggregations.

### Power BI Export Layer
A denormalized, time-intelligence-ready export (`data/pbi_ready/sales_for_powerbi.csv`) containing derived calendar attributes (Quarter, MonthName, DayOfWeek, IsWeekend, Profit_Margin_Pct) optimized for fast dashboard consumption.

### Pipeline Run Manifest
Structured metadata recorded in `outputs/pipeline_runs.json` tracking timestamp, execution status, input row counts, clean row counts, and quarantine volumes for auditability.

### Dynamic Dimension Ingestion
The process of automatically accepting new business categories or regions introduced in raw transaction batches while validating mandatory numeric and date formats.

