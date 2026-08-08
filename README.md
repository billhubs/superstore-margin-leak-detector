# Commercial Operations & Supply Chain Diagnostic Suite

An enterprise-grade diagnostic dashboard engineered to identify commercial profit erosion, fulfillment latencies, and operational bottlenecks in large-scale retail supply chains.

> **A Note on Data Privacy & Context:**  
> The architecture and operational workflows in this repository represent a production-ready framework built for enterprise-scale environments. To protect sensitive business logic and proprietary corporate information, all underlying numbers use a sanitized public retail dataset (*Superstore*).

---

## Why I Built This (Executive Summary)

When retail margins shrink, high-level revenue charts rarely tell the full story. You might see sales going up while net profit quietly bleeds away. 

I built this diagnostic suite to bridge that gap. Instead of just displaying static charts, this platform connects top-line financial metrics directly to their root operational causes—specifically isolating heavy promotional discounting and regional supply chain delays.

To make it truly actionable, the application doesn't stop at data visualization. It embeds an automated **AI Governance module** that actively monitors threshold violations and dispatches cross-divisional remediation tasks directly to department leads.

---

## Core Problems This Suite Solves

* **Margin Erosion from Uncapped Discounts:**  
  Pinpoints exact transactions where discounts cross the critical 20% profitability threshold, proving how aggressive clearance strategies erode gross margins in categories like *Tables* and *Bookcases*.

* **Fulfillment Lead-Time Latency:**  
  Maps order-to-ship times across different delivery tiers and regions to evaluate logistics performance against internal Service Level Agreements (SLAs).

* **Cross-Functional Incident Management:**  
  Turns data insights into real-world accountability. Includes a built-in operations hub to assign task owners, track investigator leads, and manage resolution deadlines across Merchandising, Logistics, and Finance teams.

---

## System Architecture & Data Pipeline

```text
[ POS / ERP Data Sources ]
           │
           ▼
[ SQLite In-Memory Engine ] ──► (Dynamic Querying & Parameterized Filtering)
           │
           ▼
[ Feature Engineering ] ────► (Profit Status & Delivery Lead-Time Calculations)
           │
           ├──► [ Executive KPI & Anomaly Diagnostics ]
           ├──► [ AI Incident Governance Engine ]
           └──► [ Cross-Divisional Operations Hub ]

```

---

## Tech Stack

* **Core Framework:** Streamlit (Custom CSS, Fortune 500 Theme Engine)
* **Data Processing & Analytics:** Pandas, NumPy
* **Database Engine:** Embedded SQLite3 (`:memory:`)
* **Visualization:** Plotly Express & Plotly Graph Objects
* **Language:** Python 3.11+

---

## Key Platform Features

* **Dynamic Executive Themes:** Seamlessly switch visual palettes between enterprise standards, including *Walmart Corporate Navy*, *McKinsey Executive Slate*, and *Amazon Supply Chain*.
* **In-Memory SQL Pipeline:** Fast, responsive data querying with parameterized filtering for rapid slice-and-dice analysis.
* **Automated AI Governance:** Continuous threshold evaluation that automatically flags margin drops or delivery delays to key stakeholders.
* **Data Lineage Auditing:** Embedded source badges (`POS / SAP ERP`, `Financial Ledger`, `WMS Logistics`) on every visual component to maintain data transparency.
* **Interactive Operations Hub:** Complete task management interface for incident assignment, SLA lifecycle tracking (`On Duty`, `Reaching Due Date`, `Past Due`), and auditor tagging.


---

## Terms of Use & Intellectual Property

This repository is maintained as a **Personal Portfolio Case Study** to demonstrate end-to-end data architecture, dashboard design, and operational problem-solving capabilities to prospective employers and clients.

* **All Rights Reserved:** Reproduction, redistribution, or commercial use of this codebase without explicit written consent is strictly prohibited.
* **Live Demo Access:** Prospective recruiters and technical reviewers can test the live application via the hosted dashboard link or request temporary collaborator access to inspect the private codebase.

```
Link : https://commercial-supplychain-dashboard.streamlit.app/
```
