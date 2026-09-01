# Data Flow Diagrams (DFD)
## Enterprise Credit Risk Prediction & Decisioning Architecture

---

## 1. DFD Level 0 — System Context Diagram

The Context Diagram defines the enterprise boundary of the Automated Credit Risk Engine, identifying all external entities, inbound inputs, and outbound decision streams.

```
                                  ┌────────────────────────┐
                                  │      CREDIT BUREAU     │
                                  │   (Experian / Equifax) │
                                  └───────────┬────────────┘
                                              │ Credit History &
                                              │ Score Payload
                                              ▼
┌─────────────────┐  Loan Application Payload ┌────────────────────────┐ Digital Loan Offer ┌─────────────────┐
│                 │ ────────────────────────> │                        │ ──────────────────> │                 │
│  LOAN APPLICANT │                           │  AUTOMATED CREDIT RISK │                     │  LOAN APPLICANT │
│   / BORROWER    │ <──────────────────────── │   & DECISION ENGINE    │ ──────────────────> │   / BORROWER    │
│                 │    Validation / Doc Alert │                        │ Adverse Action Ltr  │                 │
└─────────────────┘                           └───────────┬────────────┘                     └─────────────────┘
                                                   ▲      │
                                Macro Telemetry    │      │ Booking Order /
                                (FEDFUNDS, MORT30) │      │ Disbursement Order
                                                   │      ▼
                                       ┌───────────┴────────────┐
                                       │  FEDERAL RESERVE FRED  │
                                       │   & CORE BANKING (CBS) │
                                       └────────────────────────┘
```

---

## 2. DFD Level 1 — Detailed Process Decomposition

Decomposes the core system into 6 discrete, sequential microservices, incorporating the Medallion Data Pipeline and the Dual-Engine ML Architecture.

```
┌──────────────┐
│  APPLICANT   │
└──────┬───────┘
       │ 1. Loan Application JSON
       ▼
 ┌───────────┐         Invalid Schema         ┌────────────────────┐
 │    1.0    │ ─────────────────────────────> │ Applicant Notified │
 │ Ingestion │                                └────────────────────┘
 │& Validate │
 └─────┬─────┘
       │ Validated Application Stream
       ▼
 ┌───────────┐         Daily Macro Series     ┌────────────────────┐
 │    2.0    │ <───────────────────────────── │ D1: FRED Macro DB  │
 │ Medallion │                                └────────────────────┘
 │  Pipeline │ ─── Raw Data ────────────────> ┌────────────────────┐
 │(Brz/Slv/Gld│                                │ D2: Medallion Store│
 └─────┬─────┘ ─── Feature Vector Store ────> └────────────────────┘
       │ Engineered Gold Vector (OHE, DTI, LTI)
       ▼
 ┌───────────┐         Model Artifacts        ┌────────────────────┐
 │    3.0    │ <───────────────────────────── │ D3: ML Model Store │
 │ ML Scoring│                                └────────────────────┘
 │  Engine   │
 └─────┬─────┘
       │ Calibrated PD Score (0.00 - 1.00)
       ▼
 ┌───────────┐
 │    4.0    │ ─── PD < 15% (70% Vol) ──────> [ Instant Auto-Approval Offer ]
 │ 3-Tier    │ ─── 15% <= PD <= 30% (10%) ──> ┌────────────────────┐
 │ Gateway   │                                │ 5.0 Underwriter    │ ──> Senior Underwriter
 └─────┬─────┘ ─── PD > 30% (20% Vol) ──────> │   Review Queue     │
       │                                      └────────────────────┘
       │ Immutable Execution Log                         │ Manual Approve / Deny
       ▼                                                 ▼
 ┌───────────┐                                ┌────────────────────┐
 │    6.0    │ ─────────────────────────────> │ D4: Audit Log DB   │
 │Reporting &│                                └────────────────────┘
 │ Analytics │ ─────────────────────────────> ┌────────────────────┐
 └───────────┘                                │ Power BI Dashboard │
                                              └────────────────────┘
```

---

## 3. Data Dictionary for Pipeline Entities

```
+---------------------------+-----------------------+-----------------------+-------------------------------------------------------+
| Data Flow Item            | Source Entity         | Destination Entity    | Data Attributes / Schema Details                      |
+---------------------------+-----------------------+-----------------------+-------------------------------------------------------+
| `Application Payload`     | Borrower / Web Portal | 1.0 Ingestion Service | `loan_amount`, `income`, `loan_purpose`, `state_code`,|
|                           |                       |                       | `property_value`, `loan_term`, `applicant_age`        |
| `Macro Telemetry`         | Federal Reserve FRED  | 2.0 Medallion Pipeline| `fedfunds`, `mortgage30us`, `dgs10`, `unrate`, `cpi`  |
| `Gold Feature Vector`     | 2.0 Medallion Pipeline| 3.0 ML Scoring Engine | `dti_bucket`, `loan_to_income`, `rate_vs_market`,     |
|                           |                       |                       | `state_denial_rate`, OHE product vectors              |
| `Model Decision Response` | 3.0 ML Scoring Engine | 4.0 Decision Gateway  | `predicted_pd` (Float), `risk_tier` (1/2/3),          |
|                           |                       |                       | `inference_latency_ms`, `confidence_interval`         |
| `Adverse Action Record`   | 4.0 Decision Gateway  | Customer Notice / D4  | `application_id`, `rejection_code_1`, `rejection_2`,  |
|                           |                       |                       | `max_dti_exceeded_flag`, `timestamp`                  |
| `Audit Trail Entry`       | 4.0 Decision Gateway  | D4: Audit Log Store   | `application_id`, `input_hash`, `model_version`,      |
|                           |                       |                       | `final_decision`, `officer_override_flag`, `timestamp`|
+---------------------------+-----------------------+-----------------------+-------------------------------------------------------+
```
