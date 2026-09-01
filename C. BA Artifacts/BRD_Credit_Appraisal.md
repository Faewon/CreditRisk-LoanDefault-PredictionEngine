# Business Requirements Document (BRD)
## Automated Credit Underwriting & Risk Scoring Engine

**Project Title:** Enterprise Credit Risk Prediction & Automated Decisioning Engine  
**Project Sponsor:** Chief Risk Officer (CRO) & Head of Retail Lending  
**Lead Business Analyst:** Risk Analytics & Digital Transformation Team  
**Version:** 2.0 (Final Enterprise Standard)  
**Date:** September 2026  
**Status:** Approved for Implementation  

---

## 1. Executive Summary & Problem Statement

### 1.1 Business Context
Traditional mortgage loan appraisal at retail commercial banks suffers from high operational friction, reliance on manual ratio spreadsheets, and lengthy turnaround times (**3 to 5 business days**). This operational latency increases underwriting costs (~$450/loan), exposes the bank to human evaluation inconsistency, and causes high customer abandonment to modern digital lenders.

### 1.2 Proposed Solution
The bank is deploying an **Automated Credit Risk & Decisioning Engine** integrated with an institutional Medallion Data Pipeline (Bronze -> Silver -> Gold). The platform utilizes a champion **XGBoost Classifier (AUC: 0.9973)** for real-time straight-through loan scoring and a challenger **Logistic Regression model** for regulatory capital sensitivity and stress testing.

---

## 2. Business Objectives & Project KPIs

```
+--------+------------------------------------+-----------------------+-----------------------+--------------------------+
| ID     | Strategic Business Objective       | Metric / KPI          | Baseline (As-Is)      | Target (To-Be)           |
+--------+------------------------------------+-----------------------+-----------------------+--------------------------+
| BO-01  | Accelerate Decision Velocity       | Turnaround Time (TAT) | 72 - 120 Hours        | < 4 Hours (STP < 1 min)  |
| BO-02  | Automate Standard Approvals        | STP Auto-Approval Rate| 0% (All manual)       | >= 65% (Achieved: 70%)   |
| BO-03  | Lower Unit Underwriting Cost       | Operational Cost/File | $450 per application  | $120 per application     |
| BO-04  | Maximize Underwriting Precision    | Model AUC-ROC         | 0.65 (Legacy rules)   | >= 0.85 (Achieved: 0.997)|
| BO-05  | Reduce Non-Performing Loans (NPL)  | Portfolio NPL Ratio   | 3.20%                 | < 2.00%                  |
| BO-06  | Real-Time Macro Factor Ingestion   | Data Ingestion SLA    | Monthly Manual Pull   | Daily Automated API Feed |
+--------+------------------------------------+-----------------------+-----------------------+--------------------------+
```

---

## 3. Project Scope

```
+----------------------------------------------------+----------------------------------------------------+
| IN-SCOPE                                           | OUT-OF-SCOPE                                       |
+----------------------------------------------------+----------------------------------------------------+
| • 1-4 Single-Family Residential Mortgages          | • Commercial real estate (CRE) & syndicated loans  |
| • Purchase, Refinance & Home Improvement loans     | • Unsecured micro-consumer credit (< $5,000)       |
| • Loan sizes from $25,000 to $2,000,000            | • Core banking general ledger (CBS) replacement    |
| • Automated Straight-Through Processing (STP)      | • Manual property appraisal / physical site survey |
| • Federal Reserve FRED daily macro feed integration| • Cross-border multi-currency offshore lending     |
| • Power BI 5-page risk governance dashboard suite  |                                                    |
+----------------------------------------------------+----------------------------------------------------+
```

---

## 4. Functional Requirements (FR)

```
+--------+--------------------------+-------------------------------------------------------------------------------+----------+
| ID     | Requirement Area         | Detailed Functional Requirement Specification                                 | Priority |
+--------+--------------------------+-------------------------------------------------------------------------------+----------+
| FR-01  | Digital Ingestion        | Ingest digital loan application payloads via JSON REST API from web portal.   | Must     |
| FR-02  | Pre-flight Validation    | Validate schema integrity, data types, mandatory fields, and KYC constraints. | Must     |
| FR-03  | Medallion Ingestion      | Automatically route raw payloads into Bronze layer and trigger Silver parsing.| Must     |
| FR-04  | Macro Data Enrichment    | Query FRED API for daily macro rates (FEDFUNDS, MORTGAGE30US, CPI, UNRATE).   | Must     |
| FR-05  | Feature Generation       | Construct Gold Feature vectors (DTI, LTI buckets, rate spreads, and OHE).     | Must     |
| FR-06  | Real-Time ML Scoring     | Execute production XGBoost model to predict Probability of Default (PD).      | Must     |
| FR-07  | 3-Tier Decision Gateway  | Route applications into Auto-Approve, Exception Review, or Auto-Reject tiers. | Must     |
| FR-08  | Adverse Action Notice    | Generate CFPB/ECOA compliant rejection letters with top 3 denial reason codes.| Must     |
| FR-09  | Underwriter Workqueue    | Route borderline files (15% <= PD <= 30%) to Senior Underwriter with < 2h SLA.| Must     |
| FR-10  | Macro Stress Engine      | Allow Risk Analysts to run 4 predefined macro shock simulations on demand.    | Should   |
| FR-11  | Executive Dashboard      | Publish interactive Power BI dashboard tracking NPL, exposure, and models.    | Should   |
| FR-12  | Immutable Audit Trail    | Store full input vector, timestamp, score, and decision payload for 7 years.  | Must     |
+--------+--------------------------+-------------------------------------------------------------------------------+----------+
```

---

## 5. Non-Functional Requirements (NFR)

* **NFR-01 (Performance & Latency)**: End-to-end scoring API latency must not exceed **500 ms** per transaction (Target CPU model inference `< 15 ms`).
* **NFR-02 (High Availability)**: The underwriting decision service must maintain **99.9% uptime** during operational hours (24/7 digital intake).
* **NFR-03 (Scalability)**: Capability to process **10,000 applications/hour** during peak promotional campaign surges.
* **NFR-04 (Data Security & Compliance)**: Encryption in-transit (TLS 1.3) and at-rest (AES-256). Masking of borrower PII according to GLBA & GDPR guidelines.
* **NFR-05 (Auditability & Retention)**: Complete decision reproducibility for regulatory audit inspection for a minimum of **7 years**.

---

## 6. Underwriting Policy & Decision Gateway Rules

```
+---------------------------+-----------------------------------+---------------------------------------------------------+
| Risk Tier                 | Probability of Default (PD) Range | System Action & Business Routing                        |
+---------------------------+-----------------------------------+---------------------------------------------------------+
| Tier 1: Low Risk (STP)    | PD < 15.0% (~70% Volume)          | Instant Auto-Approval -> Generate digital offer letter  |
| Tier 2: Borderline Risk   | 15.0% <= PD <= 30.0% (~10% Volume)| Route to Senior Underwriter Exception Queue (SLA < 2h)  |
| Tier 3: High Risk         | PD > 30.0% (~20% Volume)          | Instant Auto-Rejection -> Dispatch Adverse Action Notice|
+---------------------------+-----------------------------------+---------------------------------------------------------+
```

---

## 7. Stakeholder Sign-Off & Approvals

| Stakeholder Role | Department | Sign-Off Date | Status |
|---|---|---|---|
| **Chief Risk Officer (CRO)** | Enterprise Risk Management | Sep 2026 | **APPROVED** |
| **Head of Retail Credit Underwriting** | Credit Operations | Sep 2026 | **APPROVED** |
| **Lead Machine Learning Architect** | AI & Analytics Engineering | Sep 2026 | **APPROVED** |
| **Chief Information Security Officer (CISO)** | IT Security & Compliance | Sep 2026 | **APPROVED** |
