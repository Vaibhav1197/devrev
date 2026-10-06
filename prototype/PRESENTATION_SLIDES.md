# DevRev Solutions Engineer Demo Presentation
## Topic: DevRev Computer in Action — Offline Mode for Mobile Order Processing
**Role:** Solutions Engineer (Candidate)  
**Evaluation:** Solutions Engineer Interview — Demo & Role-Play Evaluation  
**Live Interactive Deck:** `http://127.0.0.1:5000/presentation` or [`templates/presentation.html`](./templates/presentation.html)  

---

### Executive Slide Outline (7 Slides for Hiring Manager)

* **Slide 1: Problem Framing & Use Case Hook** — The Offline Mobile Ordering Dilemma & Fragmented Systems
* **Slide 2: Data Setup** — Multi-Source Data Preparation (Google Drive PRD, Jira Issues, Supporting Specs)
* **Slide 3: Connectors Used** — Ingestion into DevRev Computer (Google Drive, Jira Cloud, Notion)
* **Slide 4: Key Computer Queries** — Conversational Prompts Used in DevRev Computer
* **Slide 5: Insights Generated** — High-Value Findings Surfaced by Computer (WAL Dependency, Telemetry Gap, PRD Risks)
* **Slide 6: Business Value** — Measurable Impact for Product Managers, Engineering Teams, and Leadership
* **Slide 7: Demo Storytelling & Role-Play Walkthrough** — Turnkey 5-Minute Script & Q&A Strategy

---

## Slide 1: Problem Framing & Use Case Hook

### Slide Title: The Offline Mobile Dilemma: Why Disconnected Systems Fail Field Operations
#### Subtitle: Bridging Customer Escalations, Product Specs, and Engineering Backlogs with DevRev Computer

### 1. The Real-World Customer Use Case
* **Persona:** Field sales representatives and mobile delivery drivers (e.g. wholesale distribution, beverage delivery, field service).
* **The Environment:** Reps visit retail basements, rural distribution centers, and commercial walk-in freezers with **zero cellular or Wi-Fi reception**.
* **The Operational Crisis:**
  * When mobile apps lack true offline architecture, checkout freezes with `HTTP 504 Gateway Timeout` errors.
  * Orders are dropped or delayed, forcing reps to write on paper notebooks, resulting in transcription errors and lost sales.
  * When devices reconnect, unhandled network state transitions trigger **app crashes** or **duplicate order submissions**.

### 2. The Core Enterprise Friction: Disconnected Silos
In traditional enterprise stacks, knowledge lives in separate departmental silos:
* **Product Management:** PRD stored in **Google Drive** or **Notion**, defining theoretical requirements.
* **Engineering Teams:** Technical tasks, bugs, and concurrency fixes tracked in **Jira**, disconnected from product documentation.
* **Customer Support & Success:** Customer escalations and field bug reports isolated in support tools and email.

> **The Takeaway for Evaluators:**  
> When these tools don't talk to each other, engineers build against incomplete specs, critical concurrency fixes go untested, and product managers are blind to technical debt. **DevRev Computer creates a unified semantic knowledge layer that connects product, engineering, and customer reality.**

---

## Slide 2: Data Setup: Structured Multi-Source Preparation

### Slide Title: Data Setup: Multi-Source Data Preparation
#### Subtitle: Structured Enterprise Artifacts Prepared Across Google Drive, Jira Cloud, and Technical Specs

To test DevRev Computer's true analytical intelligence, we prepared a multi-disciplinary data environment:

| Data Source | System / Location | Key Scope & Structural Details |
| :--- | :--- | :--- |
| **1. Master Product Requirement Document (PRD)** | Google Drive (Google Docs) / [`PRD_Offline_Mode_Mobile_Order_Processing.md`](../PRD_Offline_Mode_Mobile_Order_Processing.md) | • Comprehensive PRD defining local encrypted storage (SQLCipher AES-256), client-side UUIDv4 idempotency keys, outbox sync worker, and conflict resolution matrix (inventory depletion, price variances, credit limits). |
| **2. Jira Engineering Issues** | Jira Cloud (Project: `Devrev` / `OM`) / [`jira_issues_import.csv`](../jira_issues_import.csv) | • **`OM-116` (KAN-19):** CI chaos test harness using Charles Proxy & Network Link Conditioner across 5 flaky profiles (*Done*).<br>• **`OM-117` (KAN-20):** Migrate catalog cache to SQLite WAL mode to fix reader/writer starvation (*Done*).<br>• **`OM-118` (KAN-21):** Client telemetry metrics for queue depth, sync latency, and battery drain (*In Progress*).<br>• Plus related defect catalog for reconnection crashes and idempotency locks. |
| **3. Technical Architecture & API Design Notes** | Google Drive / [`API_Design_Notes_Offline_Sync.md`](../API_Design_Notes_Offline_Sync.md) | • Standalone REST contracts for `POST /api/v1/orders/sync` and `GET /api/v1/catalog/delta`.<br>• Redis distributed lock patterns, monotonic revision delta sync, and retry parameters. |
| **4. P0 Root Cause Analysis (Bug Investigation)** | Google Drive / [`Bug_Investigation_Summary_OM102.md`](../Bug_Investigation_Summary_OM102.md) | • Deep post-mortem on duplicate order creation caused by dropped cellular TCP ACKs (`INC-49201`). |
| **5. Customer Escalation Report** | Google Drive / [`Customer_Escalation_Report_ApexWholesale.md`](../Customer_Escalation_Report_ApexWholesale.md) | • Executive report from Apex Wholesale ($420k ARR, 65 seats) detailing $84.5k in delayed orders. |

---

## Slide 3: Connectors Used: Unified Ingestion into DevRev Computer

### Slide Title: Connectors Used: Ingesting Google Drive, Jira, and Notion
#### Subtitle: Building a Living Knowledge Graph Across Product, Engineering, and Support

DevRev Computer natively integrates with the primary systems of record where product and engineering work happens:

```
┌──────────────────────────────────────────┐        ┌──────────────────────────────────────────┐
│          Google Drive Connector          │        │            Jira Cloud Connector          │
│  • Master PRD Google Doc                 │        │  • Connected Project: "Devrev"           │
│  • API Architecture Specifications       │        │  • Issue OM-116: Chaos Harness (KAN-19)  │
│  • Bug Root Cause Analyses (RCA)         │        │  • Issue OM-117: WAL Mode Fix (KAN-20)   │
│  • Customer Escalation Briefs            │        │  • Issue OM-118: Telemetry (KAN-21)      │
└────────────────────┬─────────────────────┘        └────────────────────┬─────────────────────┘
                     │                                                   │
                     ▼                                                   ▼
       ┌───────────────────────────────────────────────────────────────────────────┐
       │                     DevRev Computer Semantic Knowledge Graph              │
       │  • Vector Embedding Search (Deep semantic understanding of text & tables) │
       │  • Cross-System Entity Linking (Customer ARR ↔ Jira Key ↔ PRD Section)    │
       │  • Autonomous Reasoning Engine (Cross-references specs against tasks)     │
       └─────────────────────────────────────┬─────────────────────────────────────┘
                                             ▲
                                             │
                              ┌──────────────┴──────────────┐
                              │  Notion / Knowledge Base    │
                              │  • Meeting Notes & Runbooks │
                              │  • Team Roadmaps & SLAs     │
                              └─────────────────────────────┘
```

### Key Connector Highlights:
1. **Google Drive Connector:** Ingests live Google Docs and Markdown files, preserving headings, tables, and code snippets with real-time change detection.
2. **Jira Cloud Connector:** Connects directly to Atlassian Jira, reading issue summaries, statuses (`Done`, `In Progress`), descriptions, and commit hashes (e.g. commit `e8b2f90`).
3. **Notion / Wiki Connector:** Pulls contextual team notes and runbooks into the unified embedding space.

---

## Slide 4: Key Computer Queries: Conversational Interaction

### Slide Title: Key Computer Queries: Conversational Interaction in Action
#### Subtitle: The Exact Prompts Used in DevRev Computer to Uncover Risks, Bugs, and Documentation Gaps

Instead of manually reading through 25-page specifications or running complex JQL filters, we interacted with DevRev Computer conversationally using the exact prompts below:

### Query 1: Active Engineering Limitations & Concurrency Audit
> **User Prompt (UP):**  
> *"Based on the PRD, what existing bugs or technical limitations might impact this feature?"*
* **Intent:** Interrogates the Jira connector to uncover active engineering limitations, technical debt, and concurrency dependencies that threaten the PRD's promises.
* **Computer Finding:** Discovered that the PRD's concurrency promise relies entirely on `OM-117` (SQLite WAL mode fix in commit `e8b2f90`), flagged that `OM-118` (telemetry metrics) is still In Progress, and revealed that the CI chaos harness (`OM-116`) misses long-offline multi-day scenarios.

### Query 2: Documentation & Specification Gap Audit
> **User Prompt (UP):**  
> *"Are there documents related to retry logic, API reliability, or sync conflicts?"*
* **Intent:** Audits the organization's knowledge library to determine whether critical implementation details exist as build-ready design specs or only as summary tables in the PRD.
* **Computer Finding:** Confirmed that the PRD is the *only* document covering these topics in the organization, and only at requirement depth. Proved that zero standalone design docs, SLA runbooks, or conflict engine specs exist.

### Query 3: Multi-System Architectural Risk Synthesis
> **User Prompt (UP):**  
> *"Summarize the main engineering risks for implementing offline order processing."*
* **Intent:** Synthesizes multi-system risks across Data Integrity, Reliability, Local Storage, and Security into a prioritized pre-GA action register.
* **Computer Finding:** Flagged 72h Redis dedup TTL vs unbounded outbox queue age, lack of dead-letter queue (DLQ) for poison orders, 4-hour offline JWT auth expiry, and storage budget calculation discrepancy (50k vs 15k SKUs).

### Query 4: Historical Jira Defect Search & Greenfield Verification
> **User Prompt (UP):**  
> *"Are there any past Jira issues related to offline sync or network reconnection problems?"*
* **Intent:** Searches historical defect records in Jira Cloud (Project `Devrev` / `OM`).
* **Computer Finding:** Surfaced `OM-118` (P2, In Progress), `OM-117` (P0, Done), `OM-116` (P1, Done) in Jira, and confirmed that zero actual field failure bugs are logged—proving this is a greenfield feature with unvalidated conflict rules.

---

## Slide 5: Insights Generated: What Computer Surfaced

### Slide Title: Insights Generated: High-Value Intelligence Surfaced by Computer
#### Subtitle: Real Findings Surfaced from Your Connected PRD and Jira Issues

DevRev Computer went beyond simple summarization — it performed **deep cross-silo systems thinking**, surfacing four major categories of actionable intelligence:

### 1. Existing Engineering Limitations Uncovered in Jira
* ⚙️ **WAL Concurrency is Load-Bearing (`OM-117` / KAN-20):**  
  *Computer Insight:* Computer identified that reader/writer starvation was previously a real defect, resolved by migrating SQLite to Write-Ahead Logging (WAL) in commit `e8b2f90`. **Crucial finding:** The PRD's core concurrency promise (syncing while writing orders) depends entirely on this fix holding — Computer recommended a regression test to prevent silent backslides under load!
* 📡 **Observability Blind Spot at Launch (`OM-118` / KAN-21):**  
  *Computer Insight:* Client telemetry (queue depth, reconnect latency, error codes) is still *In Progress*. Computer warned that shipping before `OM-118` lands means shipping blind: headline KPIs (>99.5% sync rate, <3s latency) cannot be verified in the field!
* 🧪 **Chaos Testing Misses Long-Offline Scenarios (`OM-116` / KAN-19):**  
  *Computer Insight:* The CI chaos harness validates connection flapping and short blips, but does **not** exercise multi-day offline scenarios where 72h dedup TTL and 24h price windows bite.

### 2. Documentation Gaps Identified
* 📑 **No Dedicated Technical Design Docs:**  
  *Computer Insight:* Computer audited the library and found that retry logic, API reliability, and conflict resolution exist **only as summary tables in the PRD** — there were no standalone specs or runbooks behind them. *(Validating why we created `API_Design_Notes_Offline_Sync.md`!)*

### 3. Critical PRD Risks Caught Before Code Was Written
* ⚠️ **Idempotency Window Mismatch:** 72h Redis dedup TTL vs unbounded outbox queue (duplicate order risk on long weekends).
* ⚠️ **Auth Token Expiration:** 4-hour JWT tokens lapse offline; sync has no re-authentication flow upon reconnect.
* ⚠️ **Storage Budget Discrepancy:** PRD claimed 50,000 SKUs fits in 36MB, but the math was modeled on only 15,000 SKUs.

---

## Slide 6: Business Value: Empowering PMs, Engineers, and Leadership

### Slide Title: Business Value: Empowering PMs, Engineers, and Leadership
#### Subtitle: Delivering Quantifiable ROI Across the Product-Engineering-Business Triad

```
┌─────────────────────────────────────────┐   ┌─────────────────────────────────────────┐   ┌─────────────────────────────────────────┐
│          For Product Managers           │   │          For Engineering Teams          │   │         For Executive Leadership        │
│        "Bulletproof PRDs Faster"        │   │        "Zero-Friction Context"          │   │        "Revenue-Driven Roadmaps"        │
├─────────────────────────────────────────┤   ├─────────────────────────────────────────┤   ├─────────────────────────────────────────┤
│ • Catches missing failure states and    │   │ • Uncovers load-bearing dependencies    │   │ • Proactively surfaces technical debt   │
│   edge cases (auth lapse, queue TTL)    │     (OM-117 WAL fix) before regressions     │     threatening feature delivery and KPIs.  │
│   before engineering sprint kickoff.    │     happen in production.                   │ • Connects engineering issues to customer   │
│ • Validates technical feasibility and   │   • Flags test harness gaps (chaos testing  │     trust and revenue outcomes.             │
│   saves 2–3 weeks of redesign cycles.   │     missing multi-day offline profiles).    │ • Eliminates departmental finger-pointing   │
│ • Audits doc coverage to ensure design  │   • Cuts bug triage and cross-referencing   │     between Product, Support, and           │
│   depth matches requirement scope.      │     time by 40%.                            │     Engineering.                            │
└─────────────────────────────────────────┘   └─────────────────────────────────────────┘   └─────────────────────────────────────────┘
```

### Quantifiable Impact Summary:
1. **Time Saved:** 15+ hours saved per sprint per PM in manual cross-referencing and risk discovery.
2. **Defect Prevention:** Prevents catastrophic regressions by proving that concurrency promises depend on specific past commits (`e8b2f90`).
3. **Delivery Confidence:** Ensures telemetry (`OM-118`) lands *before* GA so headline KPIs (>99.5% sync) can actually be measured.

---

## Slide 7: Demo Storytelling & Role-Play Walkthrough

### Slide Title: Demo Storytelling & Role-Play Walkthrough
#### Subtitle: Turnkey 5-Minute Interview Script & Winning Q&A Strategy

### 5-Minute Role-Play Script (Word-for-Word Guide for Your Interview)

#### Minute 0:00 - 1:00: Problem Framing & The Persona Hook
> *"Hi everyone! Today, I want to show you how DevRev Computer solves one of the hardest challenges in software delivery: the disconnect between product documentation, engineering issue trackers, and technical debt.*
> 
> *Consider our use case: Offline Mode for Mobile Order Processing. Field sales reps operate in commercial basement walk-in freezers with zero cellular reception. When apps freeze, orders are lost or duplicated on reconnect. But when teams try to build a solution, Product has a PRD in Google Drive, and Engineering has issues in Jira. Let's see how DevRev Computer bridges these silos."*

#### Minute 1:00 - 2:00: Data Setup & Connectors
> *"To demonstrate this, we connected two core systems into DevRev Computer: Google Drive containing our master PRD Google Doc, and Jira Cloud containing our engineering issues in the Devrev project.*
> 
> *DevRev Computer ingested these disparate assets and synthesized a living semantic knowledge graph connecting requirements to actual engineering records."*

#### Minute 2:00 - 3:45: Conversational Interaction & Live Insights (The "Aha!" Moment)
> *"Now, watch what happens when we converse with Computer.*
> 
> *First, I asked: 'Based on the PRD, what existing bugs or technical limitations might impact this feature?'*
> 
> *Computer didn't just summarize text. It performed deep systems analysis across our Jira project. It discovered that our concurrency promise relies entirely on Jira issue OM-117 — a previous WAL mode migration in commit e8b2f90 — and warned us that this fix needs a guarding regression test so the UI doesn't freeze under load.*
> 
> *Next, it analyzed OM-118 and caught that our telemetry metrics are still In Progress, meaning we risk shipping without the instrumentation needed to measure our 99.5% sync rate KPI.*
> 
> *Then, when asked about retry logic and API reliability documents, Computer audited our library and surfaced that these critical topics exist only as summary tables in the PRD, with no standalone design specifications behind them.*
> 
> *Finally, Computer synthesized 11 critical engineering risks — including a mismatch where a 72-hour dedup key could expire over a long weekend and cause duplicate orders."*

#### Minute 3:45 - 5:00: Business Value Pitch & Close
> *"This is the transformative power of DevRev Computer: Product Managers write bulletproof specs before development starts; Engineers catch load-bearing dependencies and test coverage gaps; and Leadership gets proactive risk visibility before shipping to customers.*
> 
> *That is how DevRev transforms passive documentation into active, revenue-protecting intelligence. Thank you, and I look forward to your questions!"*

---

### Interviewer Q&A Defense Strategy

| Anticipated Interviewer Question | Recommended Winning Response |
| :--- | :--- |
| **"How does Computer know OM-117 is load-bearing?"** | *"DevRev Computer doesn't just match keywords; it analyzes semantic relationships. It recognized that the PRD's architectural requirement for concurrent local reads and writes directly maps to the SQLite WAL fix recorded in Jira issue OM-117 and commit `e8b2f90`."* |
| **"How does this scale to larger enterprise Jira instances?"** | *"DevRev uses vector embedding search with metadata scoping. It filters by project key (e.g. `Devrev` / `OM`), issue status, and document type to deliver sub-second, highly relevant context even across hundreds of thousands of tickets."* |
| **"What action did you take on the documentation gap Computer found?"** | *"Computer specifically flagged that retry logic and API reliability lacked standalone design docs. Because Computer surfaced this gap early, we drafted a dedicated API Design Note (`ARCH-OM-004`) to give engineering build-ready specifications."* |
