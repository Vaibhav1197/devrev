import os
import re
from flask import Flask, jsonify, request, render_template, session

try:
    from flask_cors import CORS
    has_cors = True
except ImportError:
    has_cors = False

from database import (
    init_db, get_all_records, get_record_by_id, 
    create_record, update_record, get_stats
)

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.secret_key = os.environ.get("SECRET_KEY", "devrev-solutions-prototype-secret-2026")

# Enable CORS for cross-origin testing & frontend tooling if available
if has_cors:
    CORS(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# Initialize database schema and initial data
init_db()

@app.after_request
def add_cors_and_cache_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Idempotency-Key"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- Core Web Views ---

@app.route("/", methods=["GET"])
def index():
    """Serves the primary Single Page Application interface."""
    return render_template("index.html")

@app.route("/presentation", methods=["GET"])
def presentation():
    """Serves the 6-slide Walkthrough Presentation Deck."""
    return render_template("presentation.html")

# --- Authentication & Role Switcher (Bonus Feature) ---

ACTIVE_ROLES = {
    "solutions_engineer": {
        "id": "solutions_engineer",
        "name": "Alex Rivera",
        "role": "Staff Solutions Engineer",
        "badge": "SE Lead",
        "can_edit": True,
        "can_triage": True,
        "can_delete": False
    },
    "support_agent": {
        "id": "support_agent",
        "name": "Jordan Taylor",
        "role": "Customer Support Specialist",
        "badge": "Support Tier 2",
        "can_edit": True,
        "can_triage": False,
        "can_delete": False
    },
    "vp_engineering": {
        "id": "vp_engineering",
        "name": "Marcus Vance",
        "role": "VP of Engineering",
        "badge": "Executive Admin",
        "can_edit": True,
        "can_triage": True,
        "can_delete": True
    }
}

CURRENT_ROLE_ID = "solutions_engineer"

@app.route("/api/auth/current", methods=["GET"])
def get_current_user():
    global CURRENT_ROLE_ID
    return jsonify({
        "success": True,
        "user": ACTIVE_ROLES.get(CURRENT_ROLE_ID, ACTIVE_ROLES["solutions_engineer"]),
        "available_roles": list(ACTIVE_ROLES.values())
    }), 200

@app.route("/api/auth/switch", methods=["POST"])
def switch_user_role():
    global CURRENT_ROLE_ID
    data = request.get_json(force=True, silent=True) or {}
    role_id = data.get("role_id", "solutions_engineer")
    if role_id in ACTIVE_ROLES:
        CURRENT_ROLE_ID = role_id
        return jsonify({
            "success": True,
            "message": f"Switched role to {ACTIVE_ROLES[role_id]['role']}",
            "user": ACTIVE_ROLES[role_id]
        }), 200
    return jsonify({"success": False, "error": "Invalid role ID"}), 400

def get_current_actor():
    global CURRENT_ROLE_ID
    user = ACTIVE_ROLES.get(CURRENT_ROLE_ID, ACTIVE_ROLES["solutions_engineer"])
    return f"{user['name']} ({user['role']})"

# --- REST API Endpoints (Supports both /records and /api/records) ---

def handle_list_records():
    search_query = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "All").strip()
    priority_filter = request.args.get("priority", "All").strip()

    records = get_all_records(
        search_query=search_query if search_query else None,
        status_filter=status_filter if status_filter else None,
        priority_filter=priority_filter if priority_filter else None
    )
    return jsonify({
        "success": True,
        "count": len(records),
        "records": records
    }), 200

@app.route("/records", methods=["GET"])
@app.route("/api/records", methods=["GET"])
def list_records():
    """
    GET /records or GET /api/records
    List records with optional search, status, and priority query parameters.
    """
    return handle_list_records()

def handle_get_record(record_id):
    record = get_record_by_id(record_id)
    if not record:
        return jsonify({
            "success": False,
            "error": f"Record with ID {record_id} not found"
        }), 404
    
    return jsonify({
        "success": True,
        "record": record
    }), 200

@app.route("/records/<int:record_id>", methods=["GET"])
@app.route("/api/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    """
    GET /records/:id or GET /api/records/:id
    Retrieves full record detail and immutable activity audit logs.
    """
    return handle_get_record(record_id)

def handle_create_record():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid or missing JSON payload"}), 400

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    customer_name = data.get("customer_name", "").strip()

    if not title:
        return jsonify({"success": False, "error": "Field 'title' is required"}), 400
    if not description:
        return jsonify({"success": False, "error": "Field 'description' is required"}), 400
    if not customer_name:
        return jsonify({"success": False, "error": "Field 'customer_name' is required"}), 400

    actor = get_current_actor()
    new_record = create_record(data, actor=actor)
    return jsonify({
        "success": True,
        "message": "Record successfully created",
        "record": new_record
    }), 201

@app.route("/records", methods=["POST"])
@app.route("/api/records", methods=["POST"])
def add_record():
    """
    POST /records or POST /api/records
    Creates a new support record with validation and audit logging.
    """
    return handle_create_record()

def handle_update_record(record_id):
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid or missing JSON payload"}), 400

    actor = get_current_actor()
    updated = update_record(record_id, data, actor=actor)
    if not updated:
        return jsonify({
            "success": False,
            "error": f"Record with ID {record_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "message": f"Record {record_id} successfully updated",
        "record": updated
    }), 200

@app.route("/records/<int:record_id>", methods=["PUT"])
@app.route("/api/records/<int:record_id>", methods=["PUT"])
def modify_record(record_id):
    """
    PUT /records/:id or PUT /api/records/:id
    Updates record status, priority, or details with audit tracking.
    """
    return handle_update_record(record_id)

@app.route("/api/stats", methods=["GET"])
def stats():
    """
    GET /api/stats
    Returns live operational metrics: Open, In Progress, Resolved, P0 Blockers, Revenue at Risk.
    """
    metrics = get_stats()
    return jsonify({
        "success": True,
        "stats": metrics
    }), 200

# --- BONUS FEATURE 1: AI TRIAGE & EXECUTIVE SUMMARIZATION ENGINE ---

@app.route("/api/records/<int:record_id>/ai-triage", methods=["POST"])
def ai_triage(record_id):
    """
    POST /api/records/:id/ai-triage
    Simulates DevRev's AI agent triage:
    1. Sentiment & urgency detection
    2. Automated executive summary generation
    3. Intelligent recommended action & matching Jira/PRD work item linkage
    """
    record = get_record_by_id(record_id)
    if not record:
        return jsonify({"success": False, "error": "Record not found"}), 404

    text = f"{record['title']} {record['description']}".lower()

    urgent_keywords = ["crash", "freeze", "duplicate", "504", "lost", "blocked", "dead zone", "emergency", "fail", "timeout"]
    positive_keywords = ["resolved", "verified", "thank", "fixed", "great", "working", "hotfix"]
    
    urgency_hits = sum(1 for w in urgent_keywords if w in text)
    positive_hits = sum(1 for w in positive_keywords if w in text)

    if urgency_hits >= 2 or "blocked" in text or "crash" in text:
        sentiment = "Frustrated"
        recommended_priority = "P0-Blocker"
    elif urgency_hits == 1:
        sentiment = "Negative"
        recommended_priority = "P1-High"
    elif positive_hits > 0:
        sentiment = "Positive"
        recommended_priority = "P3-Low"
    else:
        sentiment = "Neutral"
        recommended_priority = record["priority"]

    # AI Summary Generation
    if "dead zone" in text or "offline" in text or "reps" in text:
        ai_summary = f"Field sales operational breakdown for {record['customer_name']}. Mobile app failure in non-coverage environments blocks revenue generation. Direct link to Offline Sync roadmap."
        ai_action = "Link ticket to Epic OM-MOP (PRD v3.4); assign Mobile Sync Squad; schedule customer de-escalation briefing."
    elif "duplicate" in text or "idempotency" in text:
        ai_summary = f"Data-integrity defect: dropped cellular acknowledgments causing repeat order generation for {record['customer_name']}."
        ai_action = "Link to Jira issue OM-102; verify Redis Lua idempotency lock; coordinate with warehouse to void duplicate invoice."
    elif "freeze" in text or "anr" in text:
        ai_summary = f"Client performance bottleneck: main UI thread blocked by heavy background payload on Android devices."
        ai_action = "Link to Jira issue OM-103; dispatch coroutine offloader; profile SQLite batch commit size."
    elif "token" in text or "401" in text or "auth" in text:
        ai_summary = f"Authentication session race condition: token refreshed failed after extended disconnected state for {record['customer_name']}."
        ai_action = "Link to Jira issue OM-118; verify proactive JWT refresh interceptor prior to bulk outbox sync."
    else:
        ai_summary = f"Support inquiry logged by {record['customer_name']}. Issue classified under {record['category']} category with {sentiment} sentiment."
        ai_action = "Acknowledge receipt within SLA; review telemetry diagnostic logs; assign to on-call Solutions Engineer."

    triage_payload = {
        "ai_sentiment": sentiment,
        "priority": recommended_priority,
        "ai_summary": ai_summary,
        "ai_recommended_action": ai_action
    }

    actor = "DevRev AI Triage Engine"
    updated_record = update_record(record_id, triage_payload, actor=actor)

    return jsonify({
        "success": True,
        "message": "AI Triage analysis complete",
        "analysis": {
            "detected_sentiment": sentiment,
            "recommended_priority": recommended_priority,
            "executive_summary": ai_summary,
            "recommended_action": ai_action
        },
        "record": updated_record
    }), 200

# --- BONUS FEATURE 2: INTERACTIVE AI COPILOT CHAT ASSISTANT ---

@app.route("/api/ai/chat", methods=["POST"])
def ai_copilot_chat():
    """
    POST /api/ai/chat
    Simulates DevRev's AI Conversational Copilot for Support & Product Teams.
    Answers natural language queries grounded in the live records database:
    - "Which customer has the highest ARR at risk?"
    - "Summarize all P0 blocker issues"
    - "What tickets relate to mobile offline sync?"
    - "Give me an executive briefing of open issues"
    """
    data = request.get_json(force=True, silent=True) or {}
    user_prompt = data.get("prompt", "").strip().lower()

    if not user_prompt:
        return jsonify({"success": False, "error": "Prompt query cannot be empty"}), 400

    records = get_all_records()
    stats_data = get_stats()

    # Context analysis
    p0_records = [r for r in records if r["priority"] == "P0-Blocker"]
    open_records = [r for r in records if r["status"] in ["Open", "In Progress"]]
    enterprise_records = [r for r in records if r["customer_tier"] == "Enterprise"]
    highest_rev_record = max(records, key=lambda x: x["impact_revenue"]) if records else None

    # Conversational intent matching
    if any(k in user_prompt for k in ["highest arr", "highest revenue", "most revenue", "money"]):
        if highest_rev_record:
            answer = (
                f"**Customer with Highest Revenue at Risk:**\n\n"
                f"🏢 **{highest_rev_record['customer_name']}** ({highest_rev_record['customer_tier']} Tier)\n"
                f"• **Revenue Impact:** ${highest_rev_record['impact_revenue']:,.2f}\n"
                f"• **Ticket:** `{highest_rev_record['ticket_key']}` — {highest_rev_record['title']}\n"
                f"• **Status / Priority:** {highest_rev_record['status']} | {highest_rev_record['priority']}\n"
                f"• **Recommended Action:** {highest_rev_record['ai_recommended_action'] or 'Immediate executive briefing'}"
            )
        else:
            answer = "No active records with revenue impact found."

    elif any(k in user_prompt for k in ["p0", "blocker", "critical", "urgent"]):
        if p0_records:
            lines = [f"Found **{len(p0_records)} active P0-Blocker(s)**:"]
            for r in p0_records:
                lines.append(
                    f"\n🚨 **`{r['ticket_key']}` — {r['title']}**\n"
                    f"  • **Customer:** {r['customer_name']} (${r['impact_revenue']:,.2f} ARR)\n"
                    f"  • **Status:** {r['status']} | **Lead:** {r['assigned_engineer'] or 'Unassigned'}\n"
                    f"  • **Action:** {r['ai_recommended_action'] or 'Requires immediate engineering escalation'}"
                )
            answer = "\n".join(lines)
        else:
            answer = "Great news! There are currently no unresolved P0-Blockers in the queue."

    elif any(k in user_prompt for k in ["offline", "mobile", "sync", "dead zone", "cellular"]):
        sync_records = [r for r in records if any(w in (r["title"] + r["description"]).lower() for w in ["offline", "sync", "dead zone", "cellular", "reconnect", "anr"])]
        if sync_records:
            lines = [f"Identified **{len(sync_records)} record(s)** impacting Mobile Offline Sync:"]
            for r in sync_records:
                lines.append(
                    f"\n📱 **`{r['ticket_key']}` ({r['customer_name']})**\n"
                    f"  • **Issue:** {r['title']}\n"
                    f"  • **Priority:** {r['priority']} | **Status:** {r['status']}\n"
                    f"  • **AI Summary:** {r['ai_summary'] or 'Pending triage'}"
                )
            lines.append("\n💡 *DevRev Insight: These issues correlate directly with Mobile v3.4 Offline Mode PRD requirements (SQLCipher + Redis Lua Idempotency).*")
            answer = "\n".join(lines)
        else:
            answer = "No records found matching offline mobile sync issues."

    elif any(k in user_prompt for k in ["summary", "briefing", "overview", "status", "stats"]):
        answer = (
            f"**📊 Executive Support Portfolio Briefing:**\n\n"
            f"• **Total Active Records:** {stats_data['total']}\n"
            f"• **Open Records:** {stats_data['open']}\n"
            f"• **In Progress:** {stats_data['in_progress']}\n"
            f"• **Resolved:** {stats_data['resolved']}\n"
            f"• **Critical P0 Blockers:** {stats_data['p0_blockers']}\n"
            f"• **Cumulative Revenue at Risk:** ${stats_data['revenue_at_risk']:,.2f}\n\n"
            f"**Key Recommendation:** Accelerate P0-Blocker resolution for {p0_records[0]['customer_name'] if p0_records else 'key enterprise clients'} to protect high-value ARR."
        )

    else:
        answer = (
            f"I analyzed all {len(records)} support records in the database.\n\n"
            f"You can ask me to:\n"
            f"• 'Show all P0 blockers'\n"
            f"• 'Which customer has the highest revenue at risk?'\n"
            f"• 'Summarize issues affecting offline mobile sync'\n"
            f"• 'Give an executive briefing of open tickets'"
        )

    return jsonify({
        "success": True,
        "query": user_prompt,
        "response": answer
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f"  DevRev SupportIQ Rapid Prototype Server Running")
    print(f"  Access UI at:        http://127.0.0.1:{port}")
    print(f"  Walkthrough Slides:  http://127.0.0.1:{port}/presentation")
    print(f"  API Docs / Records:  http://127.0.0.1:{port}/records")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
