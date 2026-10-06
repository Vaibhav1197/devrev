import os
import re
from flask import Flask, jsonify, request, render_template, send_from_directory
from database import (
    init_db, get_all_records, get_record_by_id, 
    create_record, update_record, get_stats
)

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# Initialize database on startup
init_db()

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Idempotency-Key"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS":
        return "", 204
    return render_template("index.html")

@app.route("/presentation", methods=["GET", "OPTIONS"])
def presentation():
    if request.method == "OPTIONS":
        return "", 204
    return render_template("presentation.html")

# --- REST API Endpoints ---

@app.route("/api/records", methods=["GET"])
def list_records():
    """
    GET /api/records
    Optional query parameters:
      - search: string to search across title, description, customer, key
      - status: 'All', 'Open', 'In Progress', 'Resolved', 'Closed'
      - priority: 'All', 'P0-Blocker', 'P1-High', 'P2-Medium', 'P3-Low'
    """
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

@app.route("/api/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    """
    GET /api/records/:id
    Retrieves full record details including audit activity logs.
    """
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

@app.route("/api/records", methods=["POST"])
def add_record():
    """
    POST /api/records
    Creates a new support ticket / issue record.
    Required fields: title, description, customer_name
    """
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

    new_record = create_record(data)
    return jsonify({
        "success": True,
        "message": "Record successfully created",
        "record": new_record
    }), 201

@app.route("/api/records/<int:record_id>", methods=["PUT"])
def modify_record(record_id):
    """
    PUT /api/records/:id
    Updates record status, priority, engineer assignment, or resolution notes.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid or missing JSON payload"}), 400

    updated = update_record(record_id, data)
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

# --- BONUS FEATURE: AI TRIAGE & SUMMARIZATION ENGINE ---
@app.route("/api/records/<int:record_id>/ai-triage", methods=["POST"])
def ai_triage(record_id):
    """
    POST /api/records/:id/ai-triage
    Simulates DevRev's AI agent engine:
    1. Sentiment & urgency detection
    2. Automated executive summary generation
    3. Intelligent recommended action & matching Jira/PRD work item linkage
    """
    record = get_record_by_id(record_id)
    if not record:
        return jsonify({"success": False, "error": "Record not found"}), 404

    text = f"{record['title']} {record['description']}".lower()

    # Heuristic AI Classification & Sentiment Analysis
    urgent_keywords = ["crash", "freeze", "duplicate", "504", "lost", "blocked", "dead zone", "emergency", "fail"]
    positive_keywords = ["resolved", "verified", "thank", "fixed", "great", "working"]
    
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
    else:
        ai_summary = f"Support inquiry logged by {record['customer_name']}. Issue classified under {record['category']} category with {sentiment} sentiment."
        ai_action = "Acknowledge receipt within SLA; review telemetry diagnostic logs; assign to on-call Solutions Engineer."

    triage_payload = {
        "ai_sentiment": sentiment,
        "priority": recommended_priority,
        "ai_summary": ai_summary,
        "ai_recommended_action": ai_action,
        "actor": "DevRev AI Triage Engine"
    }

    updated_record = update_record(record_id, triage_payload)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f"  DevRev SupportIQ Rapid Prototype Server Running")
    print(f"  Access UI at: http://127.0.0.1:{port}")
    print(f"  API Docs at:  http://127.0.0.1:{port}/api/records")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
