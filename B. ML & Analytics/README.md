# Section B: Machine Learning & Portfolio Analytics
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![ML Framework](https://img.shields.io/badge/ML-XGBoost%20%7C%20Scikit--Learn-orange.svg)]()
[![BI Tool](https://img.shields.io/badge/Power%20BI-5%20Pages%20Suite-yellow.svg)]()

> **Part of Project**: [CreditRisk-LoanDefault-PredictionEngine](https://github.com/Faewon/CreditRisk-LoanDefault-PredictionEngine)  
> **Author**: [Faewon](https://github.com/Faewon)

---

## 1. Overview

This module delivers the end-to-end analytical and machine learning intelligence layer for the credit risk engine:
- **Predictive Underwriting**: Probability of Default (PD) classification trained on **2.78 Million public loan applications**.
- **Macroeconomic Stress Testing**: Capital adequacy and Expected Loss (EL) simulation across 4 macroeconomic shock scenarios.
- **Business Intelligence**: A 5-page institutional Power BI Dashboard suite covering portfolio overview, risk segmentation, macro trends, stress tests, and model governance.

---

## 2. Directory Structure

```
B. ML & Analytics/
│
├── README.md
├── 01_eda.ipynb                     # Exploratory Data Analysis & visual profiling
├── 02_modeling.ipynb                # Train/test split, scaling, XGBoost & LR training
├── 03_stress_testing.ipynb          # Macro scenario shock simulations & loss calculations
│
├── dashboard/                       # Power BI Dashboard & Visual Assets
│   ├── CreditRisk_Dashboard.pbix    # Complete 5-page interactive Power BI report
│   ├── 01_NPL_Overview.png          # Page 1: Portfolio exposure & denial KPIs
│   ├── 02_Risk_Segmentation.png     # Page 2: Risk by product, purpose & income tiers
│   ├── 03_Macro_Trends.png          # Page 3: Federal Reserve rates & delinquency cycles
│   ├── 04_Stress_Testing.png        # Page 4: Scenario PD migration & Expected Loss
│   └── 05_Model_Performance.png    # Page 5: ROC/PR curves & governance matrix
│
├── models/                          # Serialized Model Artifacts (joblib)
│   ├── xgboost_model.pkl            # Champion model (Production scoring engine)
│   ├── logistic_model.pkl           # Challenger model (Stress testing & baseline)
│   └── scaler.pkl                   # StandardScaler fitted on training features
│
└── models results/                  # Evaluation Visualizations & Diagnostic Curves
    ├── model_comparison.png         # High-res ROC Curve & Precision-Recall curves
    └── stress_test_results.png      # Scenario-based Mean PD bar chart
```

---

## 3. Machine Learning Architecture & Benchmark

We deploy a **Dual-Engine Model Strategy**:
1. **Production Scoring Engine (Champion - XGBoost)**: Optimized for ultra-fast, high-precision automated approvals (Straight-Through Processing) with sub-second latency (**< 500 ms**).
2. **Stress Testing & Capital Engine (Baseline - Logistic Regression)**: Maintained for transparent linear interpretability, regulatory compliance (Basel/IFRS9), and macro shock simulations.

### Model Performance Benchmark

```
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
| Model Architecture  | AUC-ROC     | Avg. Precision  | Precision     | Recall     | F1-Score     | Enterprise Role          |
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
| Logistic Regression | 0.7550      | 0.5145          | 0.6520        | 0.7230     | 0.6857       | Baseline / Stress Engine |
| XGBoost Classifier  | 0.9973      | 0.9911          | 0.9940        | 0.9890     | 0.9915       | Production Scoring (STP) |
+---------------------+-------------+-----------------+---------------+------------+--------------+--------------------------+
```

- **Data Leakage Safeguards**: Rigorous pre-training audits removed post-origination variables (`interest_rate`, `rate_spread`, `property_value`, `total_loan_costs`) ensuring zero target contamination.

---

## 4. Macroeconomic Stress Testing Matrix

Simulated four macroeconomic downturn scenarios assuming **Loss Given Default (LGD) = 45%**:

| Macro Scenario | Shocks Applied | Mean PD (%) | Median PD (%) | High-Risk Share (PD > 50%) | Expected Loss (EL) |
|---|---|---|---|---|---|
| **Baseline (Current)** | Current Economy | 45.28% | 41.16% | 41.24% | **20.38%** |
| **Mild Recession** | Income -10%, DTI +15% | 70.16% | 71.02% | 85.85% | **31.57%** |
| **Severe Recession** | Income -25%, DTI +35%, Loan +10% | 91.07% | 92.88% | 99.92% | **40.98%** |
| **2008-like Housing Crisis** | Income -40%, DTI +60%, Loan +20%, Price -30% | 98.61% | 99.09% | 99.98% | **44.38%** |

*Insight: In a 2008-style crisis, credit losses increase by **2.18x**, requiring an additional **$24B–$48B** counter-cyclical capital buffer.*

---

## 5. Power BI Dashboard Suite (`dashboard/`)

| Page | Title | Key Metrics & Visualizations |
|---|---|---|
| **Page 1** | **Overview** | Total Exposure ($1.11T), Denial Rate (25.44%), Exposure at Risk ($196.75B), Decision distribution donut, Denial rate by state bar chart, and Ticket size distribution. |
| **Page 2** | **Segmentation** | Rejection rates across Loan Products (Conventional vs VA/FHA), Loan Purpose (Purchase vs Refinancing), Applicant Income Brackets, and Portfolio Exposure Treemap. |
| **Page 3** | **Macro Trends** | Dual-axis monetary policy tracking (Fed Funds vs 30Y Mortgage vs Unemployment Rate), CPI inflation YoY, and banking sector delinquency trends (`DRALACBS`). |
| **Page 4** | **Stress Testing** | Comparative scenario PD migration bar chart, Expected Loss bar chart, and complete capital impact matrix. |
| **Page 5** | **Model Performance** | Model comparison table, ROC & Precision-Recall curves image overlay, and Model Governance & MLOps deployment guidelines. |

---

## 6. Notebook Execution Guide

1. **`01_eda.ipynb`**: Run exploratory data analysis, inspect correlation heatmaps, plot applicant income distributions, and assess class balance.
2. **`02_modeling.ipynb`**: Execute stratified train/test split, train Logistic Regression and XGBoost with hyperparameter tuning, evaluate confusion matrices, and serialize model files to `models/`.
3. **`03_stress_testing.ipynb`**: Apply macroeconomic percentage shocks to loan-level features, compute scenario PD shifts, generate Expected Loss estimates, and export `stress_test_results.csv`.
