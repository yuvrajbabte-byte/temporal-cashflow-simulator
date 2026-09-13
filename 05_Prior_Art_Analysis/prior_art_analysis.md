# Prior Art Analysis Report
## Temporal Cash-Flow Disturbance Simulator (TCDS)
### Novelty & Patentability Assessment — September 2026

---

## 1. Search Methodology

All prior art searches were conducted in September 2026 using:
- Web-based patent search (USPTO, Google Patents references via web)
- Academic publication search (ACM, IEEE, Springer, arXiv, ResearchGate)
- Commercial platform landscape scan (FinTech product search)
- Targeted keyword combinations covering each of the five novel elements

---

## 2. Search Queries and Results Summary

| Query | Sources Searched | Matching Prior Art Found |
|---|---|---|
| `"liquidity impact window" cash flow trajectory business event graph supply chain` | Web, Google Patents | **None** — term appears only in commercial FinYeld AI marketing; no patent claims found |
| `"monetary disturbance" propagation "business events" "cash flow" temporal graph supply chain` | Web, USPTO | **None** — concepts appear as separate academic domains, not unified in a single patent |
| `"multi-path convergence" cash event "accounts receivable" "accounts payable" temporal simulation supply chain` | Web, USPTO | **None** — no prior patent found combining these elements |
| `patent "supply chain disturbance" "cash flow" simulation "event-level" graph propagation "working capital" "liquidity"` | Web, USPTO | **None** — relevant results found only for generic supply chain finance instruments |
| `US20240362563A1 financial risk graph seed node weighted edge exposure score` | Web, Google Patents | **Found**: US20240362563A1 — closest prior art (risk graph, exposure scoring) — confirmed **not** to claim monetary disturbance propagation |
| `patent temporal graph cash flow disturbance propagation liquidity 2022 2024` | Web, arXiv, preprints | **Found**: TAGN research (anomaly detection / risk scoring via temporal graph) — **not** cash-event scheduling |
| `"cash flow bullwhip" patent event graph propagation liquidity window peak deficit recovery date` | Web, Tandfonline, PSU | **Found**: Academic papers on Cash-Flow Bullwhip Effect — analytical/theoretical only, **no computational patent** |

---

## 3. Closest Prior Art — Detailed Analysis

### 3.1 US20240362563A1 (pub. Nov 2024)

**Title:** (Financial/Business Risk Graph System — exact title not publicly indexed)
**Assignee:** Not confirmed
**What it covers:** Builds a graph of business/financial entities. Seeds a risk event at a node. Traverses the graph via weighted edges. Computes risk/exposure scores for downstream entities. Visualizes affected subgraph.

**Critical claim analysis:**

| Claim Element in Prior Art | TCDS Approach | Patentable Difference |
|---|---|---|
| Risk/exposure **score** propagated | Quantified **monetary amount** (USD) with settlement date propagated | Different state variable — dimensionless score vs. typed monetary object |
| Entity-to-entity **company** graph | Business-mechanism graph (PO, Invoice, AR, AP, Cash as nodes) | Fundamentally different graph structure |
| Output: **risk score** or **exposure label** | Output: **Liquidity Impact Window** (start/peak/deficit/duration/recovery) | Different primary output object |
| No time-aware cash scheduling | Every propagation step schedules a future cash event date | Novel temporal dimension |
| No multi-path convergence at cash events | Detects + attributes multiple causal paths at shared cash events | Novel convergence + attribution mechanism |

**Conclusion:** US20240362563A1 is the closest prior art but addresses a categorically different problem (risk labeling vs. cash scheduling). TCDS is **patentably distinct**.

---

### 3.2 US12380389B2 (granted 2025)

**What it covers:** Entity-level financial risk graph; subgraph visualization; exposure metrics across organizational relationships.

**TCDS differentiation:**
- Nodes in prior art = companies/organizations
- TCDS nodes = individual business events (transactions, settlements) — the mechanisms that actually create cash flows
- Prior art: no event scheduling, no monetary state transitions, no LIW

**Conclusion:** Reinforces prior art gap; no overlap with TCDS core claims.

---

### 3.3 US20260120033A1 (pub. 2026)

**What it covers:** Business dependency graph for systemic risk quantification; graph traversal from seed events; exposure scoring.

**TCDS differentiation:** Same fundamental gap as US20240362563A1 — risk-score centric, no monetary disturbance object, no cash trajectory, no LIW.

---

### 3.4 Temporal Attentive Graph Networks (TAGN) — Research 2024

**What it covers:** Machine learning on temporal graphs; learns to predict financial anomalies/risk scores from historical data.

**TCDS differentiation:**
- TAGN: statistical learning → produces a probability/score output
- TCDS: deterministic rule-based propagation → produces a cash trajectory and LIW
- TAGN: does not schedule future cash events; no convergence detection; no LIW
- TAGN: not a simulation system; cannot accept a user-defined disturbance scenario

---

### 3.5 Cash-Flow Bullwhip Effect Research (Tangsucheeva & Prabhu, 2013; Patil & Prabhu, 2024)

**What it covers:** Academic analysis of working-capital variance amplification upstream in supply chains.

**TCDS differentiation:**
- Academic analytical framework; no computational system
- No temporal graph; no disturbance object; no propagation engine; no LIW
- Does not produce per-path attribution; does not schedule individual cash events

---

## 4. Novelty Scorecard — Five Principal Novel Elements

| Novel Element | Prior Art Status | Novelty Confidence |
|---|---|---|
| **Monetary Disturbance as First-Class Typed State** | Closest: US20240362563A1 (risk scores only) | 🟢 **High** — no prior art uses a structured monetary disturbance object as propagation state |
| **Event-Level Temporal Business Graph** | Closest: US12380389B2 (entity-level graph) | 🟢 **High** — no prior art uses POs, Invoices, AR, AP, Cash as graph nodes |
| **Dual-Transform Edges (Amount + Time)** | Closest: TAGN (weighted edges for ML) | 🟢 **High** — no prior art found with edges that transform both monetary magnitude and scheduled settlement date |
| **Multi-Path Monetary Convergence + Attribution** | None found | 🟢 **Very High** — no prior patent found combining convergence detection + per-path monetary attribution at cash events |
| **Liquidity Impact Window (7-metric output)** | None found | 🟢 **Very High** — no prior patent produces this structured output characterizing liquidity stress onset, peak, duration, and recovery |

---

## 5. Freedom to Operate Assessment (Preliminary, Non-Legal)

Based on the prior art search:
- The **core method claims** (Claims A, B, C, D) appear to have **strong novelty** with no blocking prior art found.
- The **system claims** (Claims E, F, G) are also novel as a unified pipeline.
- The **UI claims** (Claim H) are more commonly found in general dashboard patents but the specific combination of propagation timeline + path attribution + LIW visualization appears novel.

> [!WARNING]
> **Disclaimer:** This is a preliminary non-legal prior art analysis for IDF submission purposes only. It does not constitute a formal patentability opinion or freedom-to-operate legal opinion. A qualified patent attorney should conduct a formal prior art search before filing.

---

## 6. Recommended Patent Strategy

1. **File a provisional patent application** immediately to establish a priority date (September 2026).
2. **Primary claims** should center on the Liquidity Impact Window computation method and the multi-path monetary convergence — these have the clearest differentiation from all identified prior art.
3. **Secondary claims** should cover the event-level temporal graph structure and the dual-transform edge schema.
4. **Avoid centering claims** on: generic graph-based risk propagation, weighted edges alone, exposure scoring, generic cash-flow forecasting, or generic what-if simulation (well-covered by prior art).
5. **IPC classes to target:** G06Q 40/00 (Finance), G06Q 10/06 (Supply Chain), G06F 16/90 (Graph Databases), G06N 5/00 (Expert Systems).

---

*Analysis prepared: September 2026 | Status: Preliminary — for IDF submission*
