# User Stories & RACI Matrix
## Enterprise Credit Risk & Underwriting Platform

---

## 1. Agile User Stories (Gherkin Acceptance Criteria)

### Epic 1: Real-Time Scoring & Automated Underwriting

#### US-01: Real-Time Probability of Default (PD) Scoring
* **As a** Credit Underwriter  
* **I want** the system to automatically calculate the calibrated Probability of Default (PD) and risk tier within milliseconds of application receipt  
* **So that** I eliminate manual Excel spreadsheet ratio calculations and focus on complex exceptions.
* **Acceptance Criteria**:
  - `Given` a complete loan application payload with valid DTI, LTV, and Income fields,
  - `When` the payload is submitted to the scoring REST endpoint,
  - `Then` the system must return a calibrated PD probability [0.0 - 1.0] and risk tier in `< 500 ms` (Target CPU inference `< 15 ms`).

#### US-02: Straight-Through Processing (STP) Auto-Approval
* **As a** Retail Loan Operations Manager  
* **I want** low-risk applications ($\text{PD} < 15.0\%$) to receive instant automated approval without human touch  
* **So that** qualified customer onboarding time is reduced from 5 days to under 1 minute.
* **Acceptance Criteria**:
  - `Given` an application with calculated $\text{PD} < 15.0\%$ and zero credit policy violations,
  - `When` the decision gateway executes,
  - `Then` the system automatically issues a digital offer letter and creates a pending disbursement record in the Core Banking System.

#### US-03: Automated Adverse Action Letter Generation
* **As a** Compliance & Fair Lending Officer  
* **I want** rejected applications ($\text{PD} > 30.0\%$) to automatically output CFPB-compliant adverse action reason codes  
* **So that** the bank complies with Equal Credit Opportunity Act (ECOA) disclosure mandates without manual drafting.
* **Acceptance Criteria**:
  - `Given` an application rejected by the gateway ($\text{PD} > 30.0\%$),
  - `When` the denial flow is triggered,
  - `Then` the system attaches the top 3 contributing risk factors (e.g., High Debt-to-Income, Insufficient Collateral Coverage) to the digital notice.

---

### Epic 2: Portfolio Analytics & Macro Stress Testing

#### US-04: Macroeconomic Stress Simulation Engine
* **As a** Senior Risk Analyst  
* **I want** to execute multi-factor macroeconomic stress tests (interest rate shocks, income contraction, property depreciation)  
* **So that** I can calculate portfolio Expected Loss (EL) and advise the Risk Committee on capital buffer adequacy.
* **Acceptance Criteria**:
  - `Given` active portfolio loan holdings in the Gold feature store,
  - `When` the analyst applies macro shock parameters (e.g., +300 bps Fed rate, -25% Income),
  - `Then` the engine recalculates portfolio PD distribution and displays Expected Loss assuming $\text{LGD} = 45\%$ in `< 30 seconds`.

#### US-05: Executive Risk Intelligence Dashboard
* **As a** Chief Risk Officer (CRO)  
* **I want** an interactive 5-page Power BI dashboard tracking portfolio exposure, denial rates, and macro transmission  
* **So that** I maintain real-time oversight of risk concentration across states and loan products.
* **Acceptance Criteria**:
  - `Given` daily updated Medallion pipeline files,
  - `When` the Power BI report is refreshed,
  - `Then` all KPI cards, state-level choropleths, and macro transmission graphs must update dynamically with multi-slicer filtering.

---

## 2. Enterprise RACI Responsibility Matrix

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
