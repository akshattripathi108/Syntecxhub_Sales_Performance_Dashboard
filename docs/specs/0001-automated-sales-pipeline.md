# Spec: Automated Sales Data Pipeline

## Problem Statement
Sales operations and dashboard reporting currently rely on manual, multi-step script executions on static files. As new sales batches arrive or are scheduled periodically, manual processing risks human error, silent data corruption (e.g., negative prices, invalid dates polluting executive dashboards), and inconsistent Power BI exports.

## Solution
An automated, fault-tolerant end-to-end data pipeline that ingests raw sales transactions, enforces a strict quarantine gate against corrupted records, performs compound-key deduplication, refreshes clean analytical fact tables and Power BI export layers, logs execution telemetry, and runs automatically via CI/CD and manual triggers.

## User Stories
1. As an analyst, I want to execute a single CLI command to run the complete data pipeline, so that I don't have to manually orchestrate multiple disparate scripts.
2. As a data engineer, I want incoming transactions to be validated against required fields, numeric constraints, and date formats, so that corrupted rows are isolated without halting valid data processing.
3. As a business stakeholder, I want any corrupted rows to be recorded in a quarantine holding area with explicit error reasons, so that data anomalies can be investigated and resolved.
4. As an executive, I want the pipeline to halt Power BI updates if the quarantine anomaly rate exceeds 5%, so that executive dashboards never display corrupted numbers.
5. As an analyst, I want to ingest new monthly transaction batches incrementally with automatic deduplication, so that historical sales records are preserved without manual merging.
6. As a developer, I want to run validation checks in dry-run mode, so that I can inspect data quality metrics before writing any files to disk.
7. As an operations engineer, I want structured execution manifests recorded for every pipeline run, so that pipeline duration, row counts, and status history can be audited.
8. As a team member, I want scheduled daily GitHub Actions runs and on-demand workflow triggers, so that dashboard datasets stay automatically fresh without manual server management.

## Implementation Decisions
- **Single Orchestrator Interface**: Unified CLI entrypoint accepting `--input`, `--incremental`, and `--validate-only` arguments.
- **Compound Natural Key Deduplication**: Deduplicates records matching `Order_Date` + `Product` + `Region` + `Sales`.
- **Strict Quarantine Holding Layer**: Isolates bad rows with reasons (`Unparseable Order_Date`, `Invalid or negative Sales/Profit`, `Missing required fields`) into a persistent CSV.
- **Dual Analytical Artifact Generation**: Produces sanitized fact data (`data/cleaned/sales_cleaned.csv`) and enriched time-intelligence dimensions (`data/pbi_ready/sales_for_powerbi.csv`).
- **Telemetry Manifest**: Appends structured JSON execution records (`outputs/pipeline_runs.json`).
- **CI/CD Integration**: Headless runner configured on GitHub Actions executing at 00:00 UTC daily and on workflow dispatch.

## Testing Decisions
- **Test at the Highest Seam**: Test the orchestrator end-to-end against fixture datasets (valid batches, corrupted batches, duplicate batches, incremental additions).
- **External Behavior Verification**: Verify output exit codes, row counts, quarantine file creation, and KPI aggregations match verified benchmarks.
- **No Implementation Coupling**: Tests assert on output files and manifests rather than internal function calls.

## Out of Scope
- Direct cloud database ingestion (e.g. Snowflake / BigQuery connector).
- Direct Power BI Service API dataset refresh publishing (requires Power BI Service Pro/Premium workspace licensing).
- Real-time event streaming / Kafka brokers.

## Further Notes
- Respects [ADR 0001](file:///c:/Users/AKSHAT%20TRIPATHI/OneDrive/Desktop/Syntecxhub_Sales_Performance_Dashboard/docs/adr/0001-automated-data-pipeline-architecture.md) and [GLOSSARY.md](file:///c:/Users/AKSHAT%20TRIPATHI/OneDrive/Desktop/Syntecxhub_Sales_Performance_Dashboard/GLOSSARY.md).
