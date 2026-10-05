# Walkthrough Presentation (5–6 Slides)
## Solutions Engineer — Rapid Prototype Challenge
**Candidate / Solutions Engineer:** DevRev Candidate  
**Project:** DevRev SupportIQ (Customer Support & Defect Triage Portal)  
**Interactive Slide Deck:** `http://127.0.0.1:5000/presentation` or [`templates/presentation.html`](./templates/presentation.html)

---

### Slide 1: Problem Scenario & Objective

#### Title: DevRev SupportIQ — Bridging Customer Escalations & Product Engineering
- **Context & Business Need:**
  - Field sales representatives and enterprise customers (e.g., Apex Wholesale) operating in cellular dead zones suffer from dropped orders, checkout timeouts, and duplicate transactions.
  - Traditional CRM tools operate as "black boxes" where customer support tickets sit disconnected from engineering backlogs (Jira, GitHub, DevRev Work), causing delayed root-cause resolution and churn risks.
- **Prototype Objective:**
  - Build a lightweight, responsive, full-stack prototype simulating an enterprise support operations portal that tracks customer tickets, business revenue impact, and live status transitions.
  - Implement an **AI Triage Engine** that summarizes customer context, assesses sentiment, and links support tickets directly to product roadmap epics and bug fixes.

---

### Slide 2: System Architecture

#### Title: Full-Stack Modern Architecture (Zero-Friction Stack)
- **High-Level Diagram:**
  ```text
  [ Frontend Client ]  <==== REST API / JSON ====>  [ Flask Backend ]  <==== SQLite / WAL ====>  [ SQLite Database ]
  Vanilla JS + HTML5         (HTTP GET, POST, PUT)      Python 3.14 + REST                          devrev_support.db
  Glassmorphic Dark UI                                        |
                                                              v
                                                    [ AI Triage Engine ]
                                                    Sentiment & Recommendations
  ```
- **Layer Breakdown:**
  1. **Frontend Layer:** Semantic HTML5, pure CSS variables with dark-mode glassmorphic styling, and vanilla ES6 JavaScript. Zero node_modules dependencies, zero build steps, instant load time.
  2. **Backend API Layer:** Python Flask REST API with structured REST endpoints (`GET /api/records`, `GET /api/records/:id`, `POST /api/records`, `PUT /api/records/:id`, `POST /api/records/:id/ai-triage`).
  3. **Data Persistence Layer:** SQLite database with Write-Ahead Logging (WAL) and audit trail table (`activity_logs`).

---

### Slide 3: Data Model & Schema

#### Title: Entity Relationships & Attribute Design
- **Primary Entity: `records` (Support Ticket / Defect Record)**
  - `id`: Auto-increment integer primary key.
  - `ticket_key`: Unique customer-facing reference (e.g., `TICK-101`).
  - `title` & `description`: Technical summary and steps to reproduce.
  - `customer_name` & `customer_tier`: Enterprise, Mid-Market, Growth.
  - `category`: Bug, Escalation, Feature Request, Inquiry.
  - `priority`: `P0-Blocker`, `P1-High`, `P2-Medium`, `P3-Low`.
  - `status`: `Open`, `In Progress`, `Resolved`, `Closed`.
  - `impact_revenue`: Financial ARR tied to the customer account ($84,500).
  - `ai_sentiment`: Frustrated, Negative, Neutral, Positive.
  - `ai_summary` & `ai_recommended_action`: AI-generated triage insights.
  - `created_at` & `updated_at`: ISO-8601 UTC timestamps.
- **Audit Entity: `activity_logs`**
  - `record_id`: Foreign key referencing `records(id)`.
  - `action`: `CREATED`, `UPDATED`, `STATUS_CHANGE`.
  - `details`: Audit diff of modified fields.
  - `actor`: User, Solutions Engineer, or AI Engine.
  - `timestamp`: Event creation time.

---

### Slide 4: Demo Walkthrough

#### Title: Demonstrating Core Workflows & Prototype Capabilities
1. **View & Real-Time Filtering (`GET /api/records`):**
   - Live search across ticket keys, titles, and customer names with 250ms debouncing.
   - Filter dropdowns for Status and Priority.
   - Live KPI dashboard cards dynamically compute Open count, P0 Blockers, and Revenue at Risk.
2. **Record Creation (`POST /api/records`):**
   - Modal form capturing title, customer tier, initial priority, and business impact with automatic key generation (e.g., `TICK-106`).
3. **Record Detail & Status Updates (`PUT /api/records/:id`):**
   - Detail drawer showing customer context, ticket description, and timestamped audit logs.
   - 1-click status pills to transition from `Open` &rarr; `In Progress` &rarr; `Resolved`.
4. **AI Triage & Summarization (`POST /api/records/:id/ai-triage`):**
   - Interactive button evaluates ticket severity, generates executive summary, and links customer tickets to engineering Jira issues (e.g., `OM-102`)!

---

### Slide 5: How AI & CRM Systems (DevRev) Leverage This Data

#### Title: System Thinking: Connecting Customer Support to Product Development
1. **Clustering & Automated Defect Deduplication:**
   - DevRev's AI agent clusters incoming tickets reporting similar symptoms (e.g., "504 checkout timeouts" + "dead zones") into a single parent Work item (Jira `OM-101` / PRD v3.4).
2. **Customer Health & Churn Risk Modeling:**
   - Aggregating `impact_revenue` across open P0 blockers alerts Account Executives when an enterprise client ($420k ARR Apex Wholesale) reaches critical churn threshold.
3. **Automated Close-the-Loop Release Notifications:**
   - When an engineer merges PR #251 in GitHub and resolves Jira issue `OM-102`, DevRev automatically notifies all affected customer contacts that their duplicate order bug is fixed.
4. **AI Copilot for Support Engineers:**
   - AI scans past incident RCAs, API design specs, and PRD documents to suggest instant resolution steps directly to tier-1 agents.

---

### Slide 6: Summary, Evaluation Rubric & Extensibility

#### Title: Challenge Deliverables & Production Roadmap
- **Challenge Deliverables Met:**
  - ✅ **Source Code:** Clean, modular repository in `/prototype` (Flask + SQLite + Vanilla JS/CSS).
  - ✅ **Running Demo:** Runs locally in seconds via `python app.py` (Port 5000).
  - ✅ **5–6 Slide Presentation:** Interactive HTML deck (`presentation.html`) + Markdown slides.
  - ✅ **Bonus Features Included:** AI Triage Engine, Audit Logging, and Revenue Impact Analytics.
- **Production Roadmap:**
  - **DevRev Airdrop & Webhooks:** Bi-directional sync with DevRev GraphQL/REST APIs.
  - **Enterprise SSO / RBAC:** Role-based access control (Admin, Support Lead, Customer).
  - **Vector Semantic Search:** Semantic embeddings over ticket history using pgvector.
