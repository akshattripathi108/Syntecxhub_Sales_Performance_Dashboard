# ADR 0001: Automated Sales Data Pipeline Architecture

## Status
Accepted

## Context
The sales dashboard currently relies on manual script execution (`data_cleaning.py` and `export_for_powerbi.py`) against static raw files. To support scheduled updates and periodic batch ingestions without corrupting downstream Power BI dashboards, we need an automated, robust data pipeline.

## Decision
1. **Single Entrypoint Orchestrator**: Built `scripts/pipeline.py` with CLI flags (`--incremental`, `--validate-only`, `--input`) standardizing local developer runs and cloud CI/CD execution.
2. **Incremental Upsert via Compound Natural Key**: Deduplicate incoming transaction batches against existing historical records using `Order_Date + Product + Region + Sales`.
3. **Strict Quarantine Gate**: Any corrupted rows (unparseable dates, negative sales/profit, null required fields) are isolated into `data/quarantine/corrupted_orders.csv` with detailed failure reasons, aborting the Power BI export if anomaly threshold (>5%) is breached.
4. **Dynamic Dimension Ingestion**: Ingests emerging product categories and regions smoothly while maintaining strict typing on financial metrics.
5. **Structured Run Manifest**: Telemetry is persisted append-only in `outputs/pipeline_runs.json` recording timestamps, durations, and row counts.
6. **CI/CD Automation**: A GitHub Actions workflow (`.github/workflows/pipeline.yml`) runs daily at 00:00 UTC and on manual dispatch to keep data artifacts fresh.

## Consequences
- Prevents silent data corruption in production executive dashboards.
- Full auditability via run manifests and quarantine logs.
- Easy transition between local developer runs and headless CI/CD automation.
