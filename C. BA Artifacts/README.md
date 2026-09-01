# Section C: Business Analysis & Enterprise Architecture Artifacts
[![Standard](https://img.shields.io/badge/Standard-BABOK%20%7C%20BPMN%202.0%20%7C%20Gherkin-blue.svg)]()
[![Role](https://img.shields.io/badge/Role-Credit%20Risk%20Business%20Analyst-green.svg)]()

> **Part of Project**: [CreditRisk-LoanDefault-PredictionEngine](https://github.com/Faewon/CreditRisk-LoanDefault-PredictionEngine)  
> **Author**: [Faewon](https://github.com/Faewon)

---

## 1. Overview

This module provides the complete suite of **Business Analysis (BA) Artifacts** and **Enterprise Architecture Blueprints** required to transition commercial credit operations from a slow manual underwriting model into an automated, ML-governed decisioning ecosystem.

All artifacts are designed following international banking standards (BABOK, BPMN 2.0, Gherkin syntax, and Basel/IFRS9 compliance).

---

## 2. Directory Structure

```
C. BA Artifacts/
│
├── README.md                        # Documentation overview & navigation
├── BRD_Credit_Appraisal.md          # Business Requirements Document (BRD)
├── DFD_Loan_Application.md          # Data Flow Diagrams (Context Level 0 & Process Level 1)
├── BPMN_AsIs_ToBe.md                # As-Is vs. To-Be Workflow Process Models
├── User_Stories_RACI.md             # Epics, User Stories (Gherkin format) & RACI Matrix
│
└── diagrams/                        # Architecture & Workflow Diagrams (Draw.io / PNG)
    ├── bpmn_asis.png                # Traditional 3-5 days manual underwriting BPMN
    ├── bpmn_tobe.png                # Medallion & ML automated straight-through BPMN
    ├── dfd_level0.png               # Context boundary diagram
    └── dfd_level1.png               # Detailed process decomposition diagram
```

---

## 3. Artifact Index & Descriptions

| Document Name | Focus Area | Key Highlights & Business Value |
|---|---|---|
| **`BRD_Credit_Appraisal.md`** | **Business Requirements** | • 6 Strategic Business Objectives (TAT < 4 hrs, -73% cost)<br>• 12 Functional & 5 Non-Functional Requirements<br>• Automated 3-Tier Policy Decisioning Gateway (STP 70%) |
| **`DFD_Loan_Application.md`** | **Data Architecture** | • Level 0 Context Boundary with Credit Bureaus & FRED<br>• Level 1 Process Flow across Medallion Pipeline, Scoring & Audit DB<br>• Complete Data Dictionary of all payload elements |
| **`BPMN_AsIs_ToBe.md`** | **Process Transformation** | • As-Is Analysis: 3-5 days manual multi-stage review queue<br>• To-Be Model: Instant straight-through approval for 70% volume<br>• Comparative efficiency matrix (-96% turnaround time) |
| **`User_Stories_RACI.md`** | **Agile & Governance** | • 5 Core User Stories formatted in Gherkin (`Given-When-Then`)<br>• Enterprise RACI Matrix across 5 cross-functional roles |

---

## 4. Key Process Transformation Metrics

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
