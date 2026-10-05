# DevRev Solutions Engineer — Rapid Prototype Challenge
## Project: DevRev SupportIQ (Customer Support & Defect Triage Portal)

> A lightweight, modern full-stack web application simulating an enterprise customer support and product defect orchestration portal, designed for the Solutions Engineer Rapid Prototype Challenge.

---

## 1. Quickstart: Running the Application

### Prerequisites
- Python 3.8+ (Compatible with Python 3.10, 3.11, 3.12, 3.14+)
- Pip (Standard package installer)

### Step 1: Install Dependencies
```bash
python -m pip install flask
```

### Step 2: Launch the Prototype Server
Navigate to the `prototype` directory and run:
```bash
cd prototype
python app.py
```
*(Or from the project root: `python prototype/app.py`)*

### Step 3: Access the Application
- 🖥️ **Main Application UI:** Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
- 📊 **Walkthrough Presentation (6 Slides):** Open [http://127.0.0.1:5000/presentation](http://127.0.0.1:5000/presentation)
- 🔌 **REST API Endpoint:** [http://127.0.0.1:5000/api/records](http://127.0.0.1:5000/api/records)

---

## 2. Architecture & Tech Stack

```
┌─────────────────────────────────┐
│         FRONTEND LAYER          │
│  Single-Page Application (SPA)  │
│  • Modern HTML5 & CSS3 Variables│
│  • Dark-Mode Glassmorphic Theme │
│  • Pure ES6 JavaScript          │
│  • Zero Node / Webpack Overhead │
└────────────────┬────────────────┘
                 │ HTTP REST (JSON)
                 ▼
┌─────────────────────────────────┐
│          BACKEND API            │
│  • Python Flask REST Service    │
│  • Input Validation & Error Map │
│  • AI Triage & Analysis Engine  │
└────────────────┬────────────────┘
                 │ SQL / ACID
                 ▼
┌─────────────────────────────────┐
│         DATABASE LAYER          │
│  • SQLite3 (Embedded Engine)    │
│  • Auto-seeded with 5 Records   │
│  • Activity Audit Logs Table    │
└─────────────────────────────────┘
```

### Key Technical Decisions
1. **Zero-Build Frontend:** By utilizing modern vanilla ES6 JavaScript and CSS custom properties, the frontend loads in under 50ms with zero npm build configurations or dependency vulnerabilities.
2. **ACID SQLite Storage:** Built-in Python `sqlite3` requires zero external database installation (like PostgreSQL or MySQL) while providing full transactional integrity and schema constraints.
3. **Cohesive Scenario Design:** The prototype directly simulates the business context of our **"Offline Mode for Mobile Order Processing"** feature, featuring realistic tickets like the *Apex Wholesale Dead Zone Escalation* and *Duplicate Order Creation Bug*.

---

## 3. Data Model & Schema Design

### Table: `records`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique record database ID |
| `ticket_key` | TEXT | UNIQUE NOT NULL | Human-readable identifier (e.g. `TICK-101`) |
| `title` | TEXT | NOT NULL | Short issue summary |
| `description` | TEXT | NOT NULL | Detailed context, environment, repro steps |
| `customer_name` | TEXT | NOT NULL | Customer account name |
| `customer_tier` | TEXT | NOT NULL | `Enterprise`, `Mid-Market`, `Growth` |
| `category` | TEXT | NOT NULL | `Bug`, `Escalation`, `Feature Request`, `Inquiry` |
| `priority` | TEXT | NOT NULL | `P0-Blocker`, `P1-High`, `P2-Medium`, `P3-Low` |
| `status` | TEXT | NOT NULL | `Open`, `In Progress`, `Resolved`, `Closed` |
| `assigned_engineer` | TEXT | NULL | Assigned technical lead |
| `impact_revenue` | REAL | DEFAULT 0.0 | Dollar value of annual contract revenue at risk |
| `ai_sentiment` | TEXT | DEFAULT 'Neutral' | `Frustrated`, `Negative`, `Neutral`, `Positive` |
| `ai_summary` | TEXT | NULL | AI-generated executive digest |
| `ai_recommended_action`| TEXT | NULL | AI-suggested Jira link / resolution step |
| `created_at` | TEXT | NOT NULL | ISO-8601 UTC timestamp |
| `updated_at` | TEXT | NOT NULL | ISO-8601 UTC timestamp |

### Table: `activity_logs`
Tracks immutable audit entries whenever a record is created or updated:
- `id` (INTEGER PRIMARY KEY)
- `record_id` (FOREIGN KEY &rarr; records.id)
- `action` (`CREATED`, `UPDATED`, `STATUS_CHANGE`)
- `details` (Field mutation diff)
- `actor` (User or AI agent)
- `timestamp` (ISO-8601 UTC)

---

## 4. REST API Specification

### 1. List Records
```http
GET /api/records?search={query}&status={status}&priority={priority}
```
**Example Response:**
```json
{
  "success": true,
  "count": 5,
  "records": [
    {
      "id": 1,
      "ticket_key": "TICK-101",
      "title": "Critical: 14 field sales reps blocked from placing orders...",
      "customer_name": "Apex Wholesale Supply Co.",
      "customer_tier": "Enterprise",
      "priority": "P0-Blocker",
      "status": "In Progress",
      "impact_revenue": 84500.0,
      "ai_sentiment": "Frustrated"
    }
  ]
}
```

### 2. Get Single Record
```http
GET /api/records/1
```
Returns complete record fields plus the array of `activity_logs`.

### 3. Create Record
```http
POST /api/records
Content-Type: application/json

{
  "title": "Checkout button disabled on Android 14",
  "description": "Button remains grayed out after customer signature is captured.",
  "customer_name": "Valley Food Service",
  "customer_tier": "Mid-Market",
  "category": "Bug",
  "priority": "P1-High",
  "impact_revenue": 15000
}
```

### 4. Update Record Status
```http
PUT /api/records/1
Content-Type: application/json

{
  "status": "Resolved",
  "actor": "Solutions Engineer"
}
```

### 5. AI Triage & Summarization (Bonus Feature)
```http
POST /api/records/1/ai-triage
```
Dynamically parses ticket context, determines customer sentiment, generates an executive summary, and links matching DevRev Jira work items.

---

## 5. Walkthrough Presentation (Slide Summary)

The interactive presentation can be viewed in the browser at `/presentation`:
- **Slide 1: Problem Scenario** — Connecting customer field escalations with product engineering backlogs.
- **Slide 2: System Architecture** — Full-stack diagram covering the SPA, REST API, SQLite, and AI layer.
- **Slide 3: Data Model** — Relational schema design, enums, and audit logging.
- **Slide 4: Working Demo** — Step-by-step demonstration of Viewing, Creating, Updating, and AI Triage.
- **Slide 5: System Thinking & DevRev Integration** — How DevRev uses clustering, ticket-to-issue linking, and automated release close-the-loop.
- **Slide 6: Extensibility & Future Roadmap** — SSO, webhooks, and semantic vector search.

---

## 6. How AI Tools Were Leveraged in This Build
- **Rapid Prototyping:** Utilized AI code assistance to generate clean SQLite schemas, seed realistic test cases matching our PRD, and implement custom CSS variables for dark-mode UI.
- **Contract-First Design:** AI assisted in designing consistent JSON payloads matching enterprise REST standards.
- **Simulated Intelligence:** Implemented heuristic AI triage logic demonstrating how a production DevRev AI worker operates.
