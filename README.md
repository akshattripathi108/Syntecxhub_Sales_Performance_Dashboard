# Sales Performance Dashboard

> An end-to-end sales analytics and business intelligence project built with Python, Pandas, NumPy, and Microsoft Power BI as part of the Syntecxhub Data Analysis Internship.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Objective](#project-objective)
- [Internship Context](#internship-context)
- [Business Questions](#business-questions)
- [Project Scope](#project-scope)
- [Dataset](#dataset)
- [Dataset Schema](#dataset-schema)
- [Data Preparation](#data-preparation)
- [Data Quality and Validation](#data-quality-and-validation)
- [Power BI Data Model](#power-bi-data-model)
- [DAX Measures](#dax-measures)
- [Dashboard Overview](#dashboard-overview)
- [Dashboard Components](#dashboard-components)
- [Interactive Analysis](#interactive-analysis)
- [Analytical Methodology](#analytical-methodology)
- [Verified Results](#verified-results)
- [Key Business Insights](#key-business-insights)
- [Project Workflow](#project-workflow)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Python Environment Setup](#python-environment-setup)
- [Running the Data Pipeline](#running-the-data-pipeline)
- [Opening the Power BI Dashboard](#opening-the-power-bi-dashboard)
- [Refreshing the Dashboard](#refreshing-the-dashboard)
- [Documentation](#documentation)
- [Quality Assurance](#quality-assurance)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Assignment Requirements](#assignment-requirements)
- [Project Status](#project-status)
- [Author](#author)
- [Disclaimer](#disclaimer)

---

# Project Overview

The **Sales Performance Dashboard** is a complete data analysis and business intelligence project that transforms raw sales transaction data into a clean, validated, and interactive analytical dashboard.

The project combines Python-based data preparation with Microsoft Power BI to provide a structured view of sales performance across:

- Time
- Products
- Categories
- Regions
- Revenue
- Profit
- Growth

The project follows a reproducible analytical workflow:

```text
Raw Sales Data
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Clean Analytical Dataset
      ↓
Power BI Data Model
      ↓
DAX Measures
      ↓
Interactive Dashboard
      ↓
Business Insights
````

The final Power BI dashboard provides an executive-level view of sales performance through KPIs, time-series analysis, product rankings, regional comparisons, category comparisons, and interactive filtering.

---

# Project Objective

The primary objective of this project is to analyze sales transaction data and convert it into meaningful business intelligence.

The project focuses on identifying:

* Overall revenue performance
* Overall profit performance
* Profitability
* Revenue growth
* Monthly sales trends
* Quarterly sales trends
* Yearly sales trends
* Top-performing products
* Low-performing products
* Regional performance
* Category performance

The resulting dashboard is designed to allow users to quickly understand the major patterns in the sales dataset and interactively investigate performance across different dimensions.

---

# Internship Context

This project was developed as part of the **Syntecxhub Data Analysis Internship**.

The assigned Sales Performance Dashboard project requires the following analytical tasks:

1. Import and clean a raw sales dataset.
2. Remove null values and duplicate records.
3. Analyze monthly, quarterly, and yearly sales trends.
4. Identify top-selling products and low-performing products.
5. Compare sales performance by region.
6. Compare sales performance by category.
7. Create KPIs for total revenue, total profit, and growth rate.
8. Build an interactive dashboard using Power BI or Tableau.

This repository implements those requirements using:

* Python
* Pandas
* NumPy
* Power BI
* DAX

---

# Business Questions

The dashboard is designed around practical sales-analysis questions.

## Overall Performance

* What is the total revenue generated?
* What is the total profit generated?
* What is the overall profit margin?
* How has revenue changed compared with the previous year?

## Time-Based Performance

* How does revenue change from month to month?
* Which quarters generate the highest revenue?
* How does annual revenue change across the available years?
* Are there periods of increasing or decreasing sales performance?

## Product Performance

* Which products generate the highest revenue?
* Which products generate the lowest revenue?
* How does product performance change when filters are applied?

## Regional Performance

* Which regions contribute the most revenue?
* Which regions contribute the least revenue?
* How does regional performance change under different filters?

## Category Performance

* Which categories generate the highest revenue?
* Which categories generate the lowest revenue?
* How do category contributions compare?

---

# Project Scope

The project deliberately focuses on the assigned Sales Performance Dashboard requirements.

## Included

* Sales dataset processing
* Data cleaning
* Data validation
* Date-based analysis
* Monthly sales analysis
* Quarterly sales analysis
* Yearly sales analysis
* Product performance analysis
* Regional analysis
* Category analysis
* Revenue KPI
* Profit KPI
* Growth KPI
* Profit margin KPI
* Power BI data modeling
* DAX measures
* Interactive filtering
* Dashboard development
* Analytical documentation

## Outside the Current Scope

The following technologies and analytical areas are intentionally not included because they are outside the requirements of this project:

* Machine learning
* Predictive modeling
* Customer churn
* Customer segmentation
* Forecasting
* SQL databases
* Web applications
* Flask
* FastAPI
* Streamlit
* Cloud deployment
* Docker
* API development
* Automated social-media workflows

The objective is to deliver a focused, reliable, and well-documented sales analytics solution rather than unnecessarily expanding the project into unrelated areas.

---

# Dataset

The project uses a synthetic sales transaction dataset created specifically for analytical and educational purposes.

The final cleaned dataset contains:

* **2,700 records**
* **3 years of transaction data**
* **42 unique products**
* **7 categories**
* **6 regions**
* **6 analytical columns**

### Date Range

```text
2022-01-01 → 2024-12-31
```

The dataset is structured to provide enough variation and repetition for meaningful:

* Monthly analysis
* Quarterly analysis
* Yearly analysis
* Product ranking
* Regional comparison
* Category comparison
* Year-over-year growth analysis

The dataset is synthetic and does not represent actual transactions from a real organization.

---

# Dataset Schema

The analytical dataset contains the following columns.

| Column       | Data Type | Description                                       |
| ------------ | --------- | ------------------------------------------------- |
| `Order_Date` | Date      | Date of the sales transaction                     |
| `Product`    | Text      | Product associated with the transaction           |
| `Category`   | Text      | Category to which the product belongs             |
| `Region`     | Text      | Geographic region associated with the transaction |
| `Sales`      | Numeric   | Revenue generated by the transaction              |
| `Profit`     | Numeric   | Profit generated by the transaction               |

## Order_Date

The transaction date used for:

* Monthly analysis
* Quarterly analysis
* Yearly analysis
* Time-based filtering
* Year-over-year calculations

## Product

The individual product associated with a sales transaction.

This field is used to rank products according to revenue.

## Category

The broader product classification used for category-level analysis.

## Region

The geographic sales grouping used for regional performance analysis.

## Sales

The revenue generated by an individual transaction.

## Profit

The profit generated by an individual transaction.

---

# Data Preparation

The raw dataset is processed using a Python data-cleaning pipeline before being used for Power BI analysis.

The objective of the preparation stage is to ensure that the dataset is consistent, valid, and suitable for analytical use.

## Data Preparation Workflow

```text
Raw CSV
   ↓
Load Dataset
   ↓
Normalize Columns
   ↓
Parse Dates
   ↓
Validate Numeric Fields
   ↓
Clean Text Values
   ↓
Detect Duplicates
   ↓
Remove Duplicates
   ↓
Validate Final Dataset
   ↓
Export Clean Dataset
```

## Data Loading

The raw CSV dataset is loaded using Pandas.

## Column Standardization

Column names are standardized to ensure consistent references throughout the project.

## Date Processing

`Order_Date` is converted into a valid date representation so that Power BI can correctly perform chronological and time-based analysis.

## Numeric Validation

`Sales` and `Profit` are validated and converted to appropriate numeric data types.

## Duplicate Detection

Duplicate transaction records are detected and removed from the analytical dataset.

## Missing-Value Handling

The dataset is checked for missing values and handled during the cleaning process.

## Final Dataset

The resulting cleaned dataset is stored at:

```text
data/cleaned/sales_cleaned.csv
```

---

# Data Quality and Validation

Data validation is performed before the dataset is used for dashboard analysis.

The validation process checks:

* Required columns
* Column data types
* Missing values
* Duplicate records
* Date validity
* Date range
* Product coverage
* Category coverage
* Region coverage
* Sales values
* Profit values
* Aggregate revenue
* Aggregate profit

The Power BI reference metrics are independently calculated from the cleaned dataset so that the dashboard can be checked against known analytical results.

---

# Key Dataset Statistics

The final cleaned dataset contains:

| Metric        |                       Result |
| ------------- | ---------------------------: |
| Total Records |                    **2,700** |
| Date Range    | **2022-01-01 to 2024-12-31** |
| Products      |                       **42** |
| Categories    |                        **7** |
| Regions       |                        **6** |
| Total Revenue |              **$190,809.49** |
| Total Profit  |               **$74,378.00** |
| Profit Margin |                   **38.98%** |

All monetary values in the dashboard are represented in USD.

---

# Power BI Data Model

The Power BI report uses a simple analytical model consisting of:

1. A sales transaction table
2. A dedicated Date dimension

This structure supports reliable time-based analysis and avoids unnecessary model complexity.

---

## Sales Table

The primary fact table is:

```text
sales_cleaned
```

It contains:

```text
Order_Date
Product
Category
Region
Sales
Profit
```

---

## Date Table

A dedicated Date table is used to support chronological analysis and time intelligence.

The Date table contains:

```text
Date
Year
Quarter
Year-Quarter
Month
Month Number
Year-Month
```

The Date table supports:

* Monthly aggregation
* Quarterly aggregation
* Yearly aggregation
* Chronological sorting
* Year-over-year analysis
* Date filtering

---

## Relationship

The Power BI model uses the following relationship:

```text
Date[Date]  1 ───────── * sales_cleaned[Order_Date]
```

The relationship is:

* One-to-many
* Single-direction filtering

The Date table is the one side of the relationship and the sales table is the many side.

---

# Date Sorting

Correct chronological ordering is essential for time-series analysis.

The project uses:

```text
Month → Month Number
```

to ensure months are displayed chronologically.

The project also uses:

```text
Year-Month → Date
```

to ensure monthly trends are displayed in chronological order.

Quarterly analysis uses:

```text
Year-Quarter
```

rather than only `Quarter`.

This prevents values such as:

```text
Q1 2022
Q1 2023
Q1 2024
```

from being incorrectly grouped together.

---

# DAX Measures

The Power BI dashboard uses dynamic DAX measures rather than manually entered KPI values.

## Total Revenue

```DAX
Total Revenue =
SUM(sales_cleaned[Sales])
```

Calculates total revenue according to the current filter context.

---

## Total Profit

```DAX
Total Profit =
SUM(sales_cleaned[Profit])
```

Calculates total profit according to the current filter context.

---

## Profit Margin

```DAX
Profit Margin =
DIVIDE(
    [Total Profit],
    [Total Revenue],
    0
)
```

Calculates profit as a percentage of revenue.

---

## Growth Rate

The Growth Rate measure calculates year-over-year revenue growth using the Power BI Date table and time-intelligence logic.

Conceptually:

```text
Growth Rate =
(Current Revenue - Previous Year Revenue)
/
Previous Year Revenue
```

The calculation safely handles situations where a comparable previous-period value is unavailable.

---

## What-If Scenario Modeling Measures

For sensitivity forecasting, the model incorporates disconnected parameter tables and dynamic scenario measures:

* **Price Change % & Volume Change %**: Dual sliders (`GENERATESERIES(-0.20, 0.30, 0.01)`) for real-time scenario simulation.
* **Simulated Revenue**: `[Total Revenue] * (1 + [Price Change % Value]) * (1 + [Volume Change % Value])`
* **Simulated Profit**: `[Simulated Revenue] - ([Baseline Cost] * (1 + [Volume Change % Value]))`
* **Revenue & Profit Variance**: Dynamic deltas comparing simulated outcomes against actual baseline performance.

---

# Dashboard Overview

The dashboard consists of two executive pages:

1. **Executive Sales Overview (Page 1)**: Core KPIs, chronological trends, regional and categorical breakdowns, and product rankings.
2. **Scenario & What-If Planning (Page 2)**: Interactive pricing and volume sensitivity modeling with side-by-side KPI comparisons and waterfall revenue impact decomposition.

The layout prioritizes:

1. Key performance indicators
2. Revenue trends
3. Quarterly and yearly performance
4. Regional performance
5. Category performance
6. Product performance
7. Interactive filtering

The dashboard intentionally avoids unnecessary visual complexity.

---

# Dashboard Components

## 1. Total Revenue

A KPI card displays total revenue.

This measure dynamically responds to the selected filter context.

---

## 2. Total Profit

A KPI card displays total profit.

The value dynamically updates when dashboard filters are applied.

---

## 3. Growth Rate

A KPI card displays year-over-year revenue growth.

The dashboard uses the appropriate selected time period to calculate the comparison.

---

## 4. Profit Margin

A KPI card displays the relationship between profit and revenue.

The metric is calculated as:

```text
Profit Margin =
Total Profit / Total Revenue
```

---

## 5. Monthly Revenue Trend

A line chart displays revenue by:

```text
Year-Month
```

The visualization provides a detailed view of monthly sales performance across the available years.

The axis is sorted chronologically.

---

## 6. Quarterly Performance

A column chart displays revenue by:

```text
Year-Quarter
```

This allows quarterly performance to be compared across different years without incorrectly combining identical quarters.

---

## 7. Yearly Performance

A column chart compares total revenue by year.

The visualization provides a high-level view of annual sales performance.

---

## 8. Revenue by Region

A bar chart compares revenue across the available regions.

This makes it possible to quickly identify stronger and weaker regional contributors.

---

## 9. Revenue by Category

A bar or column chart compares revenue across product categories.

This allows users to identify the categories contributing the most revenue.

---

## 10. Top Products by Revenue

A product ranking visual identifies the top five products based on revenue.

The ranking is calculated dynamically from the underlying sales data.

Product names are not manually hard-coded into the dashboard.

---

## 11. Low-Performing Products

A product ranking visual identifies the bottom five products based on revenue.

In this project, "low-performing" refers specifically to lower revenue ranking.

It does not imply that the product has poor profitability, quality, customer satisfaction, or market potential.

---

# Interactive Analysis

The dashboard contains interactive slicers for:

* Year
* Region
* Category
* Product

These slicers allow users to dynamically change the analytical context.

For example, a user can select:

```text
Year = 2024
Region = Europe
Category = Electronics
```

and immediately examine the corresponding revenue, profit, growth, product, and trend performance.

Visual interactions are configured so that relevant selections update other dashboard components.

---

# Analytical Methodology

## Revenue

Revenue is calculated using:

```text
Total Revenue = SUM(Sales)
```

Revenue is analyzed across:

* Time
* Products
* Categories
* Regions

---

## Profit

Profit is calculated using:

```text
Total Profit = SUM(Profit)
```

---

## Profit Margin

Profit margin is calculated using:

```text
Profit Margin =
Total Profit / Total Revenue
```

---

## Growth

Year-over-year growth is calculated by comparing current-period revenue against the corresponding previous-year revenue.

```text
Growth Rate =
(Current Revenue - Previous Year Revenue)
/
Previous Year Revenue
```

This provides a relative measure of performance change rather than simply reporting absolute revenue.

---

## Product Ranking

Products are ranked according to total revenue.

Two rankings are used:

* Top five products
* Bottom five products

The rankings remain dynamic under dashboard filters.

---

## Regional Analysis

Regional performance is evaluated using total revenue by region.

---

## Category Analysis

Category performance is evaluated using total revenue by category.

---

# Verified Results

The core dashboard metrics were independently calculated from the cleaned dataset.

## Overall Metrics

| Metric        |  Verified Value |
| ------------- | --------------: |
| Total Revenue | **$190,809.49** |
| Total Profit  |  **$74,378.00** |
| Profit Margin |      **38.98%** |

---

## Year-over-Year Revenue Growth

| Year |        Growth |
| ---- | ------------: |
| 2022 | Not available |
| 2023 |   **-14.43%** |
| 2024 |    **+8.28%** |

The 2024 view is used for the primary Growth Rate KPI because it provides a meaningful comparison against 2023.

---

# Category Performance

The verified category-level revenue results are:

| Category               |        Revenue |
| ---------------------- | -------------: |
| Clothing               | **$57,881.35** |
| Electronics            | **$50,222.20** |
| Home & Garden          | **$24,801.01** |
| Sports & Outdoors      | **$22,156.34** |
| Office Supplies        | **$14,869.71** |
| Food & Beverages       | **$11,095.24** |
| Beauty & Personal Care |  **$9,783.64** |

Clothing is the highest-revenue category in the cleaned dataset.

---

# Regional Performance

The verified regional revenue results are:

| Region        |        Revenue |
| ------------- | -------------: |
| North America | **$72,869.54** |
| Europe        | **$49,367.15** |
| Asia Pacific  | **$29,339.93** |
| Middle East   | **$16,495.32** |
| Latin America | **$15,546.10** |
| Africa        |  **$7,191.45** |

North America is the highest-revenue region in the dataset.

---

# Product Performance

The verified highest-revenue product is:

```text
Winter Jacket Premium
$23,016.94
```

The verified lowest-revenue product is:

```text
Sticky Notes Pad
$769.82
```

These rankings are based specifically on revenue.

They should not be interpreted as profitability rankings.

---

# Key Business Insights

The following insights are derived from the cleaned dataset.

## Overall Performance

The dataset generates:

```text
Revenue: $190,809.49
Profit:  $74,378.00
Margin:  38.98%
```

---

## Revenue Growth

Revenue declined by:

```text
14.43%
```

in 2023 compared with 2022.

Revenue subsequently increased by:

```text
8.28%
```

in 2024 compared with 2023.

This indicates that the dataset experienced a decline followed by a recovery in the following year.

---

## Category Performance

Clothing is the largest revenue contributor at:

```text
$57,881.35
```

Electronics is the second-largest contributor at:

```text
$50,222.20
```

---

## Regional Performance

North America contributes the highest regional revenue:

```text
$72,869.54
```

Africa contributes the lowest:

```text
$7,191.45
```

---

## Product Performance

Winter Jacket Premium is the highest-revenue product.

Sticky Notes Pad is the lowest-revenue product.

These results are based on total revenue and do not represent product profitability.

---

# Project Workflow

The complete project workflow is:

```text
┌───────────────────────────┐
│     Raw Sales Dataset     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    Python Data Cleaning   │
│       Pandas / NumPy      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Data Validation       │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   Cleaned Sales Dataset   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      Power BI Import      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Date Dimension      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       DAX Measures        │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   Interactive Dashboard   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Business Insights     │
└───────────────────────────┘
```

---

# Repository Structure

```text
Syntecxhub_Sales_Performance_Dashboard/
│
├── data/
│   ├── raw/
│   │   └── MOCK_DATA.csv
│   ├── cleaned/
│   │   └── sales_cleaned.csv
│   ├── pbi_ready/
│   │   └── sales_for_powerbi.csv
│   └── quarantine/
│       └── corrupted_orders.csv
│
├── docs/
│   ├── adr/
│   │   └── 0001-automated-data-pipeline-architecture.md
│   ├── DAX_MEASURES.md
│   └── POWERBI_DASHBOARD.md
│
├── powerbi/
│   ├── DAX_Measures.txt
│   ├── dashboard_spec.md
│   ├── Create_Dashboard.ps1
│   ├── Refresh_Dashboard.ps1
│   └── Syntecxhub_Project_Dashboard.pbix
│
├── scripts/
│   ├── pipeline.py
│   ├── data_cleaning.py
│   ├── export_for_powerbi.py
│   ├── generate_data.py
│   └── verify_powerbi_data.py
│
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── .gitignore
├── GLOSSARY.md
├── README.md
└── requirements.txt
```

The repository separates:

* Raw and cleaned data
* Python processing scripts
* Power BI assets
* Technical documentation
* Project-level configuration

This keeps the project organized while avoiding unnecessary enterprise-level complexity.

---

# Technology Stack

| Technology   | Purpose                                        |
| ------------ | ---------------------------------------------- |
| **Python**   | Data preparation and validation                |
| **Pandas**   | Data cleaning and transformation               |
| **NumPy**    | Numerical data processing                      |
| **Power BI** | Dashboard development and visualization        |
| **DAX**      | KPI and time-intelligence calculations         |
| **Git**      | Version control                                |
| **GitHub**   | Source-code hosting and portfolio presentation |

---

# Getting Started

## Prerequisites

To reproduce the Python processing pipeline, install:

* Python
* pip

To open and interact with the final dashboard, install:

* Microsoft Power BI Desktop

---

# Python Environment Setup

Clone the repository:

```bash
git clone https://github.com/akshattripathi108/Syntecxhub_Sales_Performance_Dashboard.git
```

Navigate to the project directory:

```bash
cd Syntecxhub_Sales_Performance_Dashboard
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

---

# Running the Data Pipeline

## Automated End-to-End Pipeline

Run the unified orchestrator:

```powershell
python scripts/pipeline.py
```

The orchestrator executes the complete pipeline:
1. Ingests and sanitizes raw data from `data/raw/MOCK_DATA.csv`.
2. Isolates corrupted records to `data/quarantine/corrupted_orders.csv`.
3. Deduplicates transactions using a compound natural key (`Order_Date + Product + Region + Sales`).
4. Updates clean analytical fact tables in `data/cleaned/sales_cleaned.csv`.
5. Prepares denormalized Power BI exports in `data/pbi_ready/sales_for_powerbi.csv`.
6. Logs structured telemetry to `outputs/pipeline_runs.json`.

### Pipeline Options

```powershell
# Ingest new batch incrementally
python scripts/pipeline.py --input path/to/batch.csv --incremental

# Validate data without writing files
python scripts/pipeline.py --validate-only
```

---

## Data Validation

Run:

```powershell
python scripts/verify_powerbi_data.py
```

The validation script independently checks the cleaned dataset and verifies the key reference metrics used during Power BI development.


---

# Opening the Power BI Dashboard

The completed Power BI report is stored in:

```text
powerbi/Syntecxhub_Sales_Dashboard.pbix
```

Open the file using Microsoft Power BI Desktop.

The report uses:

```text
data/cleaned/sales_cleaned.csv
```

as its analytical data source.

---

# Refreshing the Dashboard

If the underlying cleaned dataset is updated:

1. Open the `.pbix` file in Power BI Desktop.
2. Refresh the data.
3. Review the KPI values.
4. Verify the dashboard visuals.
5. Save the updated report.

The dashboard is designed around the cleaned dataset, so changes to the underlying data should be validated before being treated as final analytical results.

---

# Documentation

Additional technical documentation is available in the repository.

## DAX Measures

```text
docs/DAX_MEASURES.md
```

Contains:

* DAX formulas
* Measure descriptions
* KPI definitions
* Calculation purposes

---

## Power BI Dashboard Documentation

```text
docs/POWERBI_DASHBOARD.md
```

Contains information about:

* Data source
* Data model
* Date dimension
* DAX measures
* Dashboard components
* Slicers
* Interactions
* KPI definitions
* Dashboard behavior

---

## Dashboard Specification

```text
powerbi/dashboard_spec.md
```

Contains the detailed dashboard implementation specification, including:

* Data model configuration
* Visual requirements
* Dashboard layout
* Slicers
* Formatting
* Reference values
* QA checklist

---

# Quality Assurance

The project follows a validation-first approach.

## Dataset QA

* [x] Required columns verified
* [x] Data types verified
* [x] Date values verified
* [x] Missing values checked
* [x] Duplicate records checked
* [x] Product coverage verified
* [x] Category coverage verified
* [x] Region coverage verified
* [x] Revenue independently calculated
* [x] Profit independently calculated
* [x] Date range verified

## Power BI Model QA

* [x] Sales table imported
* [x] Date table created
* [x] Date relationship configured
* [x] One-to-many relationship verified
* [x] Single-direction filtering configured
* [x] Date table used for time analysis
* [x] Month sorting configured
* [x] Year-Month chronological sorting configured
* [x] Year-Quarter used for quarterly analysis

## DAX QA

* [x] Total Revenue measure verified
* [x] Total Profit measure verified
* [x] Profit Margin measure verified
* [x] Growth Rate measure verified
* [x] Measures are dynamic
* [x] KPI values are not hard-coded

## Dashboard QA

* [x] Monthly revenue trend
* [x] Quarterly performance
* [x] Yearly performance
* [x] Revenue by region
* [x] Revenue by category
* [x] Top products
* [x] Low-performing products
* [x] KPI cards
* [x] Year slicer
* [x] Region slicer
* [x] Category slicer
* [x] Product slicer
* [x] Interactive filtering
* [x] Chronological date sorting

---

# Limitations

The dataset used in this project is synthetic.

Therefore:

* The transactions do not represent real company transactions.
* The products are synthetic examples.
* Regional results do not represent actual geographic markets.
* Revenue and profit values are not real commercial figures.
* Business insights demonstrate analytical methodology rather than real-world business recommendations.

The purpose of the project is to demonstrate the ability to:

* Prepare data
* Validate data
* Model data
* Create analytical measures
* Build dashboards
* Interpret business performance

---

# Future Improvements

If the project were expanded beyond the current internship requirements, potential enhancements could include:

* Automated Power BI data refresh
* Power BI Service deployment
* Target-versus-actual analysis
* Budget comparison
* Product profitability analysis
* Drill-through reports
* More detailed geographic analysis
* Advanced dashboard navigation
* Additional business KPIs

These improvements are intentionally outside the current project scope.

---

# Assignment Requirements

The project satisfies the assigned Sales Performance Dashboard requirements.

| Syntecxhub Requirement           | Implementation         | Status |
| -------------------------------- | ---------------------- | ------ |
| Import raw sales dataset         | Python / Power BI      | ✅      |
| Clean raw sales dataset          | Python / Pandas        | ✅      |
| Handle null values               | Data cleaning pipeline | ✅      |
| Remove duplicate records         | Data cleaning pipeline | ✅      |
| Analyze monthly sales trends     | Power BI               | ✅      |
| Analyze quarterly sales trends   | Power BI               | ✅      |
| Analyze yearly sales trends      | Power BI               | ✅      |
| Identify top-selling products    | Power BI               | ✅      |
| Identify low-performing products | Power BI               | ✅      |
| Region-wise sales comparison     | Power BI               | ✅      |
| Category-wise sales comparison   | Power BI               | ✅      |
| Total Revenue KPI                | DAX                    | ✅      |
| Total Profit KPI                 | DAX                    | ✅      |
| Growth Rate KPI                  | DAX                    | ✅      |
| Interactive dashboard            | Power BI               | ✅      |

---

# Project Status

## Completed

The project has been completed as an internship-level sales analytics and business intelligence solution.

### Data Layer

* Cleaned sales dataset
* Validated data
* Reproducible Python processing

### Analytical Layer

* Monthly analysis
* Quarterly analysis
* Yearly analysis
* Product analysis
* Regional analysis
* Category analysis
* Revenue analysis
* Profit analysis
* Growth analysis

### BI Layer

* Power BI data model
* Date dimension
* DAX measures
* KPI cards
* Interactive slicers
* Executive dashboard
* Dashboard QA

### Documentation Layer

* Project README
* DAX documentation
* Power BI documentation
* Dashboard specification
* Data validation script

---

# Author

## Akshat Tripathi

Computer Science & Engineering
Data Analytics | Business Intelligence

GitHub:

**[https://github.com/akshattripathi108](https://github.com/akshattripathi108)**

---

# Disclaimer

This project was developed for educational, internship, and portfolio purposes as part of the Syntecxhub Data Analysis Internship.

The dataset is synthetic and does not contain confidential, proprietary, or real customer transaction information.

The analytical results and business insights presented in this repository are based entirely on the synthetic dataset used for this project.

