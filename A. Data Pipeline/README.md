# Section A: Medallion Data Engineering Pipeline
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20(Bronze%2FSilver%2FGold)-green.svg)]()
[![Data Source](https://img.shields.io/badge/Source-CFPB%20HMDA%20%7C%20FRED%20%7C%20FDIC-orange.svg)]()

> **Part of Project**: [CreditRisk-LoanDefault-PredictionEngine](https://github.com/Faewon/CreditRisk-LoanDefault-PredictionEngine)  
> **Author**: [Faewon](https://github.com/Faewon)

---

## 1. Overview

This module automates the entire ingestion, cleaning, normalization, enrichment, and risk feature generation pipeline for **2.78 Million public loan records** combined with macroeconomic time-series data using **Medallion Architecture (Bronze -> Silver -> Gold)**.

- **100% Programmatic Ingestion**: All datasets are extracted via REST APIs and web scraping (No manual file downloads, zero synthetic data).
- **Production-grade Engineering**: Structured modular utilities in `src/` enabling clean, reusable, and testable notebook pipelines.

---

## 2. Directory Structure

```
A. Data Pipeline/
│
├── README.md
├── 01_scrape_hmda_loans.ipynb       # Scrape 2.78M loan records from CFPB HMDA API
├── 02_scrape_fred_macro.ipynb       # Extract macro time-series from Federal Reserve (FRED)
├── 03_scrape_fdic_banking.ipynb     # Scrape FDIC banking performance & failure data
├── 04_bronze_to_silver.ipynb        # Clean raw tables, handle missing values & temporal merge
├── 05_silver_to_gold.ipynb          # Feature engineering, risk buckets, interactions & encoding
│
├── Data/                            # Medallion Data Storage (Git LFS tracked)
│   ├── bronze/                      # RAW LAYER: Untouched raw API extractions
│   │   ├── hmda_loans_raw.csv       # 2.78M raw mortgage records from CFPB API
│   │   ├── fred_macro_raw.csv       # 10 raw macroeconomic time series from FRED API
│   │   ├── fdic_financials_raw.csv  # Raw FDIC commercial bank balance sheet data
│   │   └── fdic_failures_raw.csv    # Raw FDIC bank failure historical log
│   │
│   ├── silver/                      # CLEANED LAYER: Parsed, typed, imputed & joined
│   │   ├── loans_cleaned.csv        # Cleaned HMDA data with target variable (is_denied)
│   │   ├── macro_cleaned.csv        # Resampled monthly macro series with YoY metrics
│   │   └── loans_with_macro.csv     # Temporally joined loan records with macro features
│   │
│   └── gold/                        # FEATURE STORE LAYER: Modeling & BI ready
│       ├── risk_feature_store.csv   # Final encoded feature store for ML training
│       └── stress_test_results.csv  # Simulation matrix across 4 macro shock scenarios
│
└── src/                             # REUSABLE CORE MODULES
    ├── __init__.py                  # Package exports
    ├── hmda_scraper.py              # Streaming API client for large HMDA datasets
    ├── fred_client.py               # Batch series client with error resilience for FRED
    ├── fdic_scraper.py              # FDIC BankFind API scraper
    ├── cleaning.py                  # Cleaning, null imputation & join utilities
    └── feature_engineering.py       # Gold feature store generator & risk encoders
```

---

## 3. Data Sources & Extraction Architecture

| Data Source | Provider | Ingestion Protocol | Authentication | Volume / Scope |
|---|---|---|---|---|
| **HMDA Loan Application Register** | CFPB / FFIEC | REST GET (Streamed CSV) | None required | 2.78M mortgage records across CA, TX, FL |
| **Macroeconomic Time-Series** | Federal Reserve (FRED) | REST GET (JSON) | API Key (`.env`) | 10 Series (Fed Funds, 30Y Mortgage, CPI, Unemp) |
| **BankFind Suite** | FDIC | REST GET (JSON) | None required | Institutional balance sheet & failure data |

---

## 4. Medallion Layer Specifications

```
+---------------------------------------------------------------------------------------------------------------+
|                                            MEDALLION ARCHITECTURE                                             |
+---------------------+-------------------------------+---------------------------------------------------------+
| Layer               | Output Files                  | Key Transformations                                     |
+---------------------+-------------------------------+---------------------------------------------------------+
| Bronze (Raw)        | `hmda_loans_raw.csv`          | • Direct API dump (streamed in 8KB chunks)              |
|                     | `fred_macro_raw.csv`          | • Raw JSON-to-tabular macro series                      |
|                     | `fdic_financials_raw.csv`     | • Raw commercial bank performance logs                  |
|                     | `fdic_failures_raw.csv`       | • Historical bank insolvency records                    |
+---------------------+-------------------------------+---------------------------------------------------------+
| Silver (Cleaned)    | `loans_cleaned.csv`           | • Filter action_taken: 1 (Originated) vs 3 (Denied)     |
|                     | `macro_cleaned.csv`           | • Binary target mapping: `is_denied`                    |
|                     | `loans_with_macro.csv`        | • Forward-fill & monthly macro resample                 |
|                     |                               | • Temporal join on `activity_year`                      |
+---------------------+-------------------------------+---------------------------------------------------------+
| Gold (Feature Store)| `risk_feature_store.csv`      | • Risk bucket creation (DTI, LTI)                       |
|                     | `stress_test_results.csv`     | • Loan x Macro interaction features                     |
|                     |                               | • State-level denial rate aggregations                  |
|                     |                               | • Categorical One-Hot Encoding (OHE)                    |
+---------------------+-------------------------------+---------------------------------------------------------+
```

---

## 5. Step-by-Step Execution Guide

### Prerequisites
Ensure dependencies are installed and configure your `.env` file in the root repository directory:
```bash
pip install -r ../requirements.txt
```
```env
FRED_API_KEY=your_fred_api_key_here
```

### Notebook Execution Order:
1. **`01_scrape_hmda_loans.ipynb`**: Fetches loan-level records across California, Texas, and Florida. Saves raw CSV to `Data/bronze/hmda_loans_raw.csv`.
2. **`02_scrape_fred_macro.ipynb`**: Pulls multi-year macro indicators (Interest rates, Inflation, Unemployment, Delinquency rates) into `Data/bronze/fred_macro_raw.csv`.
3. **`03_scrape_fdic_banking.ipynb`**: Collects institutional banking health indicators into `Data/bronze/fdic_financials_raw.csv` and `Data/bronze/fdic_failures_raw.csv`.
4. **`04_bronze_to_silver.ipynb`**: Executes type casting, handles missing values/outliers, filters non-essential fields, and merges loan data with macro factors into `Data/silver/loans_with_macro.csv`.
5. **`05_silver_to_gold.ipynb`**: Produces the final risk feature store with interaction variables (`rate_vs_market`, `rate_x_dti`, `income_x_unrate`) saved to `Data/gold/risk_feature_store.csv`.
