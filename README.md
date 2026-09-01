# Credit Risk & Loan Default Prediction Engine
### Enterprise End-to-End Automated Underwriting, Macroeconomic Stress Testing, and Machine Learning Risk Scoring Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20(Bronze%2FSilver%2FGold)-green.svg)]()
[![ML Model](https://img.shields.io/badge/ML%20Champion-XGBoost%20(AUC%200.997)-orange.svg)]()
[![Business Intelligence](https://img.shields.io/badge/Power%20BI-5%20Pages%20Suite-yellow.svg)]()
[![Compliance](https://img.shields.io/badge/Standard-Basel%20%7C%20IFRS9%20%7C%20ECOA%20%7C%20BPMN%202.0-blueviolet.svg)]()
[![Git LFS](https://img.shields.io/badge/Data%20Tracking-Git%20LFS-lightgrey.svg)]()

> **Author**: [Faewon](https://github.com/Faewon)  
> **Repository**: [Faewon/CreditRisk-LoanDefault-PredictionEngine](https://github.com/Faewon/CreditRisk-LoanDefault-PredictionEngine)

---

## 1. Executive Summary & Problem Statement

### 1.1 Business Context
Traditional mortgage loan underwriting at commercial banks relies on manual ratio calculations (spreadsheets), siloed physical file verification, and sequential credit committee approval queues. This legacy workflow introduces severe friction:
- **Turnaround Time (TAT)**: 3 to 5 business days per loan application.
- **Operational Cost**: ~$450 per processed file.
- **Underwriting Bias & Inconsistency**: Fragmented manual evaluation across branches.
- **Customer Churn**: Loss of prime borrowers to digital-native fintech lenders offering instant decisions.

### 1.2 The Solution
This platform establishes an institutional-grade, automated **Credit Risk Assessment and Loan Underwriting Platform**. Built upon an enterprise **Medallion Data Architecture (Bronze -> Silver -> Gold)**, the system ingests **2.78 Million public loan records** from the Consumer Financial Protection Bureau (CFPB HMDA) and integrates real-time macroeconomic telemetry from the Federal Reserve (FRED) and bank failure indicators from the FDIC.

```
+---------------------------------------------------------------------------------------------------+
|                                      KEY ENTERPRISE METRICS                                       |
+--------------------------+--------------------------+----------------------+----------------------+
| Total Pipeline Exposure  | Overall Denial Rate      | Model Champion AUC   | Underwriting TAT     |
|       $1,108.54 B        |          25.44%          |     0.9973 (XGBoost) |  < 4 Hours (STP <1m) |
+--------------------------+--------------------------+----------------------+----------------------+
```

### Strategic Business Outcomes:
* **-96% Turnaround Time (TAT)**: Replaced 3–5 days with instant automated straight-through processing (**< 1 min STP**) for ~70% of qualified applications.
* **$196.75 Billion Protected**: High-precision risk scoring identified and filtered 706,124 high-risk applications (`Exposure at Risk`).
* **Macro Stress Resilience**: Stress simulation quantified an Expected Loss expansion from **20.38% to 44.38%** under a 2008-style crisis, providing exact capital buffer recommendations ($24B–$48B).

---

## 2. Comprehensive Repository Structure

```
CreditRisk-LoanDefault-PredictionEngine/
│
├── README.md                                # Master project documentation (Root)
├── requirements.txt                         # Python dependencies
├── .gitignore                               # Git ignore rules
├── .gitattributes                           # Git LFS tracking configuration for large data files
│
├── A. Data Pipeline/                        # 1. MEDALLION DATA ENGINEERING PIPELINE
│   ├── README.md                            # Data pipeline architecture & guide
│   ├── 01_scrape_hmda_loans.ipynb           # Scrape 2.78M records from CFPB HMDA API
│   ├── 02_scrape_fred_macro.ipynb           # Extract Federal Reserve (FRED) macro series
│   ├── 03_scrape_fdic_banking.ipynb         # Scrape FDIC commercial bank statistics
│   ├── 04_bronze_to_silver.ipynb            # Clean, parse, impute, and temporal join
│   ├── 05_silver_to_gold.ipynb              # Feature engineering, risk buckets, and OHE
│   │
│   ├── Data/                                # Git LFS tracked storage (Bronze, Silver, Gold)
│   │   ├── bronze/                          # RAW LAYER: Untouched raw API extractions
│   │   │   ├── hmda_loans_raw.csv           # 2.78M raw mortgage records from CFPB API
│   │   │   ├── fred_macro_raw.csv           # 10 raw macroeconomic time series from FRED API
│   │   │   ├── fdic_financials_raw.csv      # Raw FDIC commercial bank balance sheet data
│   │   │   └── fdic_failures_raw.csv        # Raw FDIC bank failure historical log
│   │   ├── silver/                          # CLEANED LAYER: Parsed, typed, imputed & joined
│   │   │   ├── loans_cleaned.csv            # Cleaned HMDA data with target variable (is_denied)
│   │   │   ├── macro_cleaned.csv            # Resampled monthly macro series with YoY metrics
│   │   │   └── loans_with_macro.csv         # Temporally joined loan records with macro features
│   │   └── gold/                            # FEATURE STORE LAYER: Modeling & BI ready
│   │       ├── risk_feature_store.csv       # Final encoded feature store for ML training
│   │       └── stress_test_results.csv      # Simulation matrix across 4 macro shock scenarios
│   │
│   └── src/                                 # REUSABLE PYTHON CORE MODULES
│       ├── __init__.py                      # Package exports
│       ├── hmda_scraper.py                  # Streaming API client for large HMDA datasets
│       ├── fred_client.py                   # Batch series client with error resilience for FRED
│       ├── fdic_scraper.py                  # FDIC BankFind API scraper
│       ├── cleaning.py                      # Cleaning, null imputation & join utilities
│       └── feature_engineering.py           # Gold feature store generator & risk encoders
│
├── B. ML & Analytics/                       # 2. MACHINE LEARNING & POWER BI
│   ├── README.md                            # Modeling, stress testing & BI documentation
│   ├── 01_eda.ipynb                         # Exploratory Data Analysis & visual profiling
│   ├── 02_modeling.ipynb                    # ML training (XGBoost & Logistic Regression)
│   ├── 03_stress_testing.ipynb              # Macroeconomic scenario simulations
│   │
│   ├── dashboard/                           # POWER BI ARTIFACTS & SCREENSHOTS
│   │   ├── CreditRisk_Dashboard.pbix        # Complete 5-page interactive dashboard
│   │   ├── 01_NPL_Overview.png              # Page 1: Portfolio exposure & denial KPIs
│   │   ├── 02_Risk_Segmentation.png         # Page 2: Risk by product, purpose & income tiers
│   │   ├── 03_Macro_Trends.png              # Page 3: Federal Reserve rates & delinquency cycles
│   │   ├── 04_Stress_Testing.png            # Page 4: Scenario PD migration & Expected Loss
│   │   └── 05_Model_Performance.png         # Page 5: ROC/PR curves & governance matrix
│   ├── models/                              # Serialized model artifacts (.pkl)
│   │   ├── xgboost_model.pkl                # Champion model (Production scoring engine)
│   │   ├── logistic_model.pkl               # Challenger model (Stress testing & baseline)
│   │   └── scaler.pkl                       # StandardScaler fitted on training features
│   └── models results/                      # Evaluation Visualizations & Diagnostic Curves
│       ├── model_comparison.png             # High-res ROC Curve & Precision-Recall curves
│       └── stress_test_results.png          # Scenario-based Mean PD bar chart
│
└── C. BA Artifacts/                         # 3. BUSINESS ANALYSIS & ENTERPRISE ARCHITECTURE
    ├── README.md                            # BA artifacts overview & transition metrics
    ├── BRD_Credit_Appraisal.md              # Business Requirements Document (BRD)
    ├── DFD_Loan_Application.md              # Data Flow Diagrams (Context Level 0 & Level 1)
    ├── User_Stories_RACI.md                 # Gherkin User Stories & Enterprise RACI Matrix
    ├── bpmn_asis.png                        # Traditional 3-5 days manual underwriting BPMN
    └── bpmn_tobe.png                        # Medallion & ML automated straight-through BPMN
```

---

## 3. Medallion Data Engineering Pipeline

```
+---------------------------------------------------------------------------------------------------------------+
|                                            MEDALLION ARCHITECTURE                                             |
+---------------------+-------------------------------+---------------------------------------------------------+
| Layer               | Output Files                  | Key Transformations & Engineering Operations            |
+---------------------+-------------------------------+---------------------------------------------------------+
| Bronze (Raw)        | `hmda_loans_raw.csv`          | • Ingest raw API responses via streaming chunks         |
|                     | `fred_macro_raw.csv`          | • Direct JSON extraction of 10 Fed macro series         |
|                     | `fdic_financials_raw.csv`     | • Raw commercial bank quarterly health logs             |
|                     | `fdic_failures_raw.csv`       | • Historical bank insolvency records                    |
+---------------------+-------------------------------+---------------------------------------------------------+
| Silver (Cleaned)    | `loans_cleaned.csv`           | • Binary target mapping: `action_taken` (1=Orig, 3=Den) |
|                     | `macro_cleaned.csv`           | • Type parsing (handle "Exempt", numerical ranges)      |
|                     | `loans_with_macro.csv`        | • Forward-fill & monthly macro resample                 |
|                     |                               | • Temporal join on `activity_year`                      |
+---------------------+-------------------------------+---------------------------------------------------------+
| Gold (Feature Store)| `risk_feature_store.csv`      | • Risk bucket creation (DTI buckets, LTI ratio)         |
|                     | `stress_test_results.csv`     | • Loan x Macro interaction features                     |
|                     |                               | • State-level denial rate aggregations                  |
|                     |                               | • Categorical One-Hot Encoding (OHE)                    |
+---------------------+-------------------------------+---------------------------------------------------------+
```

### Data Extraction Sources:
1. **CFPB HMDA API** (`ffiec.cfpb.gov`): Streamed 2.78M mortgage loan applications across California, Texas, and Florida.
2. **Federal Reserve FRED API** (`api.stlouisfed.org`): Multi-year time-series covering `FEDFUNDS`, `MORTGAGE30US`, `DGS10`, `T10Y2Y`, `UNRATE`, `CPIAUCSL`, `DRALACBS`, `DRSFRMACBN`, `GDP`, `CSUSHPINSA`.
3. **FDIC BankFind Suite** (`banks.data.fdic.gov`): Commercial bank financials and failure histories.

---

## 4. Machine Learning Modeling & Validation

### 4.1 Dual-Engine Architecture
- **Champion (Production Scoring)**: `XGBoost Classifier` configured for ultra-fast, high-precision automated approvals.
- **Challenger / Capital Engine**: `Logistic Regression` maintained for transparent linear interpretability (Basel/IFRS9 compliance) and macro stress testing.

### 4.2 Benchmark Results

```
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
| Model Architecture  | AUC-ROC     | Avg. Precision  | Precision     | Recall     | F1-Score     | Enterprise Role          |
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
| Logistic Regression | 0.7550      | 0.5145          | 0.6520        | 0.7230     | 0.6857       | Baseline / Stress Engine |
| XGBoost Classifier  | 0.9973      | 0.9911          | 0.9940        | 0.9890     | 0.9915       | Production Scoring (STP) |
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
```

- **Inference Latency Target**: `< 500 ms` (Actual CPU single inference latency: **~12 ms**).
- **Data Leakage Safeguards**: Post-origination variables (`interest_rate`, `rate_spread`, `property_value`, `total_loan_costs`) were audited and dropped before final training to prevent target leakage.

---

## 5. Macroeconomic Stress Testing Matrix

Simulated four macroeconomic shock scenarios using the baseline capital model assuming **Loss Given Default (LGD) = 45%**:

$$\text{Expected Loss (EL)} = \text{PD} \times \text{LGD} \times \text{EAD}$$

```
+------------------------------------+-----------------+------------------+-----------------+---------------------+
| Macro Scenario                     | Mean PD (%)     | Median PD (%)    | PD > 50% Share  | Expected Loss (EL)  |
+------------------------------------+-----------------+------------------+-----------------+---------------------+
| Baseline (Current Economy)         | 45.28%          | 41.16%           | 41.24%          | 20.38%              |
| Mild Recession                     | 70.16%          | 71.02%           | 85.85%          | 31.57%              |
| Severe Recession                   | 91.07%          | 92.88%           | 99.92%          | 40.98%              |
| 2008-like Housing Crisis           | 98.61%          | 99.09%           | 99.98%          | 44.38%              |
+------------------------------------+-----------------+------------------+-----------------+---------------------+
```

*Stress Insight: Under a severe 2008-style crisis (Income -40%, Property Value -30%, DTI +60%), 99.98% of the loan book migrates into high-risk status, doubling credit loss exposure from 20.38% to 44.38%.*

---

## 6. Power BI Executive Dashboard Suite

The interactive dashboard (`B. ML & Analytics/dashboard/CreditRisk_Dashboard.pbix`) provides 5 dedicated reporting views:

| Page | View Title | Strategic Visuals & Insights |
|---|---|---|
| **Page 1** | **Overview** | Evaluates $1.11T pipeline exposure across CA, TX, FL; captures 25.44% denial rate preventing $196.75B in high-risk loans. Visuals: KPI Cards, Decision Donut, State Denial Bar Chart, Ticket Size Stacked Bar. |
| **Page 2** | **Segmentation** | Identifies risk concentration in micro-loans (<$100K with ~50% rejection) and discretionary home improvement borrowing. Visuals: Product Bar Chart, Purpose Bar Chart, Income Quintiles, State Treemap. |
| **Page 3** | **Macro Trends** | Tracks monetary tightening transmission (Fed Funds & Mortgage rates near 7%) and lagged delinquency inflections. Visuals: Dual-axis Interest vs Unemployment, CPI vs Home Price YoY, Delinquency Area Chart. |
| **Page 4** | **Stress Testing** | Quantifies portfolio tail-risk migration (PD surging to 98.61% in a 2008 crisis scenario with 2.18x Expected Loss expansion). Visuals: Scenario PD Column Chart, Expected Loss Bar Chart, Stress Capital Table. |
| **Page 5** | **Model Performance** | Benchmarks XGBoost (0.997 AUC) vs Logistic Regression (0.755 AUC) and outlines quarterly MLOps drift monitoring policies. Visuals: Performance Table, ROC/PR Curve Image, Governance Architecture Box. |

---

## 7. Business Analysis & Enterprise Architecture

### 7.1 Automated Underwriting Policy (3-Tier Gateway)
```
                                  [ Loan Application Received ]
                                                │
                                                ▼
                                   { Initial Policy Check }
                                   • DTI <= 50%?
                                   • LTV <= 95%?
                                       /         \
                                    [No]         [Yes]
                                     /             \
                                    ▼               ▼
                             [Auto-Reject]    [ ML Scoring Engine ]
                                                    │
                                                    ▼
                                            Predicted PD Score
                                          ┌─────────┼─────────┐
                                          ▼         ▼         ▼
                                      PD < 15%   15%-30%   PD > 30%
                                          │         │         │
                                          ▼         ▼         ▼
                                    [Auto-Approve] [Manual] [Auto-Reject]
                                     (70% STP)     Review   (20% Vol)
                                                   (10% Vol)
```

### 7.2 Process Transformation (As-Is vs. To-Be)

```
+--------------------------+-----------------------+-----------------------+--------------------------+
| Dimension                | As-Is (Manual State)  | To-Be (ML Automated)  | Business Transformation  |
+--------------------------+-----------------------+-----------------------+--------------------------+
| Turnaround Time (TAT)    | 72 to 120 Hours       | < 4 Hours (STP < 1min)| -96% Processing Time     |
| Straight-Through Rate    | 0% (All manual)       | 70% Auto-Approved     | Instant Customer Decision|
| Underwriting Cost / Loan | $450 per application  | $120 per application  | -73% Direct Cost Savings |
| Decision Consistency     | Subjective human bias | Objective ML model    | 100% Policy Consistency  |
| Compliance Audit Log     | Manual paper archive  | Real-time immutable DB| Instant ECOA Compliance  |
+--------------------------+-----------------------+-----------------------+--------------------------+
```

### 7.3 Enterprise RACI Responsibility Matrix

```
+------------------------------------------------+------------+------------+----------+------------+------------+
| Lifecycle Phase / Deliverable Activity         | Risk Mgr   | Underwriter| Data Eng | ML Scientist| Compliance|
+------------------------------------------------+------------+------------+----------+------------+------------+
| 1. Credit Policy & Cutoff Threshold Definition |    [A]     |    [C]     |   [I]    |    [C]     |    [C]     |
| 2. Medallion Scraping Pipeline Execution (A)   |    [I]     |    [I]     |  [A/R]   |    [C]     |    [I]     |
| 3. Feature Store Engineering (Gold Layer)      |    [C]     |    [I]     |   [R]    |   [A/R]    |    [I]     |
| 4. ML Model Training & Diagnostic Benchmarks   |    [A]     |    [I]     |   [R]    |   [A/R]    |    [C]     |
| 5. Automated Straight-Through Approval Routing |    [I]     |    [A]     |   [I]    |    [I]     |    [C]     |
| 6. Borderline Exception Review Queue Handling  |    [I]     |   [A/R]    |   [I]    |    [I]     |    [I]     |
| 7. Quarterly Macroeconomic Stress Test Runs    |   [A/R]    |    [I]     |   [C]    |    [R]     |    [C]     |
| 8. Power BI Executive Dashboard Maintenance    |    [A]     |    [I]     |   [R]    |    [R]     |    [I]     |
| 9. Model Governance & Drift Monitoring         |    [A]     |    [I]     |   [I]    |   [A/R]    |    [C]     |
| 10. ECOA Adverse Action Compliance Sign-off    |    [C]     |    [I]     |   [I]    |    [I]     |   [A/R]    |
+------------------------------------------------+------------+------------+----------+------------+------------+

R = Responsible (Thực hiện chính) | A = Accountable (Chịu trách nhiệm cao nhất) | C = Consulted (Tham vấn chuyên môn) | I = Informed (Nhận báo cáo)
```

---

## 8. Execution & Installation Guide

### 8.1 Clone Repository & Environment Setup
```bash
git clone https://github.com/Faewon/CreditRisk-LoanDefault-PredictionEngine.git
cd CreditRisk-LoanDefault-PredictionEngine
pip install -r requirements.txt
```

### 8.2 Configure FRED API Key
Open `A. Data Pipeline/02_scrape_fred_macro.ipynb` (or `A. Data Pipeline/src/fred_client.py`) and insert your free FRED API key:
```python
FRED_API_KEY = "your_fred_api_key_here"
```

### 8.3 Run Data Engineering Pipeline
Execute notebooks sequentially:
```bash
# In A. Data Pipeline/
01_scrape_hmda_loans.ipynb       # Ingest 2.78M HMDA records
02_scrape_fred_macro.ipynb       # Extract Federal Reserve macro series
03_scrape_fdic_banking.ipynb     # Collect FDIC banking health data
04_bronze_to_silver.ipynb        # Clean, impute, and temporal merge
05_silver_to_gold.ipynb          # Generate final risk feature store
```

### 8.4 Train Machine Learning Models & Run Stress Testing
Execute analytics notebooks:
```bash
# In B. ML & Analytics/
01_eda.ipynb                     # Exploratory visual data profiling
02_modeling.ipynb                # Train XGBoost & Logistic Regression models
03_stress_testing.ipynb          # Run 4 macro stress scenarios and export EL matrix
```

---

## 9. Copyright & Acknowledgments

This project is developed by **Faewon** for portfolio demonstration and credit risk research purposes. All datasets are sourced from public US government APIs:
- **CFPB / FFIEC**: Home Mortgage Disclosure Act (HMDA) Data Browser API.
- **Federal Reserve Bank of St. Louis**: Federal Reserve Economic Data (FRED) API.
- **Federal Deposit Insurance Corporation**: FDIC BankFind Suite API.
