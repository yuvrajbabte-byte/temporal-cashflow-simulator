# Results & Master Patent Reference Dossier

This folder contains the complete, self-contained reference documentation, synthetic datasets analysis, experimental trajectory results, and high-resolution visualizations for the **Temporal Cash-Flow Disturbance Simulator (TCDS)** patent invention.

---

## 📄 Primary Deliverable

### **[`TCDS_Complete_Patent_Reference_and_Results_Dossier.pdf`](file:///Users/yuvi/Patents/patent1/Results/TCDS_Complete_Patent_Reference_and_Results_Dossier.pdf)**
* **Scope:** 100% Comprehensive Master Dossier (16 pages, 1.46 MB, publication-grade typography)
* **Purpose:** Authoritative reference guide containing all formulas, pseudocode, prior art comparisons, datasets, data tables, graphs, validation test logs, and legal patent claims A–H.
* **Canvas Format:** A4 format with dynamic running headers and `"Page X of Y"` footers.

---

## 📑 Content Structure of the Master Dossier

| Section | Title | Summary of Contents Included |
|---|---|---|
| **Cover** | Executive Purpose & Table of Contents | Metadata, technology classification, and navigation overview |
| **Section 1** | Invention Identification & Institutional Alignment | Formal title, VIT IPR & TT Cell Format-B alignment, field classification, core problem |
| **Section 2** | Prior Art Landscape & Novelty Scorecard | 8 prior art references (US20240362563A1, US12380389B2, etc.), differentiation matrix, **Figure 1 (Novelty Radar Chart)**, and 5 novelty pillars |
| **Section 3** | Mathematical Model & System Architecture | Graph theory \\( \mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{T}) \\), 13 Node Types Taxonomy, 10 Edge Attributes, **Figure 2 (Temporal Business Graph)**, 14 Graph Edges Table, **Figure 3 (Dependency Heatmap)**, and 11-Stage Pipeline |
| **Section 4** | Temporal Monetary Propagation & Multi-Path Convergence | Dual-transform propagation equations, **Figure 4 (Propagation Timeline)**, DIST-001 worked example (Path A: 81%, Path B: 19%), convergence summary table, **Figure 5 (Convergence Attribution Chart)**, and full 12-step audit trail |
| **Section 5** | Liquidity Impact Window (LIW) Detection | Mathematical 7-tuple definitions, **Figure 6 (LIW Dashboard)**, **Figure 7 (Cash Trajectory Curve)**, and official JSON metrics table |
| **Section 6** | Comprehensive Dataset Inventory & Data Dumps | Full `suppliers.csv` (12 suppliers), **Figure 8 (Supplier Risk Profile)**, `purchase_orders.csv` sample, `inventory_receipts.csv` sample, `customer_orders.csv` sample, and 14-point trajectory milestones |
| **Section 7** | Experimental Validation Suite | 6 system integrity tests (Determinism, Baseline Immutability, Multi-Path Convergence, Threshold Rules, Audit Log, Attribution Conservation) |
| **Section 8** | Complete Patent Claims Specification | Formal legal text for Claims A through H (Independent Method Claims, System Pipeline Claims, Threshold Claims, Immutability Claims, and UI Claims) |
| **Section 9** | Technology Readiness Level (TRL 1–9) | Comprehensive TRL matrix with NASA/Horizon 2020 definitions and empirical evidence justifying TRL 3 status |
| **Section 10** | Technical Glossary & Workspace File Inventory | 13 core domain definitions, cross-reference artifact table, and inventor attestation block |

---

## 🛠️ Regeneration Script

The document can be recompiled at any time using:
```bash
python3 /Users/yuvi/Patents/patent1/Results/build_master_dossier.py
```
