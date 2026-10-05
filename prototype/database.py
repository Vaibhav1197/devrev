import sqlite3
import json
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "devrev_support.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tickets / records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_key TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        customer_tier TEXT NOT NULL, -- Enterprise, Mid-Market, Growth
        category TEXT NOT NULL,      -- Bug, Escalation, Feature Request, Inquiry
        priority TEXT NOT NULL,      -- P0-Blocker, P1-High, P2-Medium, P3-Low
        status TEXT NOT NULL,        -- Open, In Progress, Resolved, Closed
        assigned_engineer TEXT,
        impact_revenue REAL DEFAULT 0.0,
        ai_sentiment TEXT DEFAULT 'Neutral', -- Positive, Neutral, Negative, Frustrated
        ai_summary TEXT,
        ai_recommended_action TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Create activity / audit log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        details TEXT NOT NULL,
        actor TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (record_id) REFERENCES records (id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # Seed with initial records if empty
    cursor.execute("SELECT COUNT(*) as count FROM records")
    count = cursor.fetchone()["count"]
    
    if count == 0:
        seed_initial_data(cursor)
        conn.commit()

    conn.close()

def seed_initial_data(cursor):
    now = datetime.now(timezone.utc).isoformat()
    
    sample_records = [
        (
            "TICK-101",
            "Critical: 14 field sales reps blocked from placing orders in warehouse dead zones",
            "Apex Wholesale sales team is operating in steel-reinforced basements in Texas with zero cellular bars. Orders freeze on checkout with HTTP 504. High risk of losing $84k wholesale deals today.",
            "Apex Wholesale Supply Co.",
            "Enterprise",
            "Escalation",
            "P0-Blocker",
            "In Progress",
            "Alex Rivera (Staff Solutions Engineer)",
            84500.0,
            "Frustrated",
            "Tier-1 Enterprise client experiencing complete field sales blockage in cellular dead zones. Urgent roadmap requirement for Offline-First mobile sync.",
            "Schedule emergency executive briefing with VP Sales Ops; expedite Mobile v3.4 Offline Mode beta deployment.",
            now,
            now
        ),
        (
            "TICK-102",
            "Duplicate order creation when mobile client retries over flaky 3G connection",
            "When TCP ACK is dropped in weak coverage, mobile client socket times out after 15s and retries. Server creates duplicate order records without idempotency check, triggering double inventory allocation.",
            "Metro Foodservice Distribution",
            "Enterprise",
            "Bug",
            "P0-Blocker",
            "In Progress",
            "Elena Rostova (Backend Systems Lead)",
            46200.0,
            "Negative",
            "Lack of distributed idempotency key validation causes repeat order generation on cellular packet loss.",
            "Deploy Redis Lua script enforcing SETNX lock on X-Idempotency-Key with 72-hour TTL.",
            now,
            now
        ),
        (
            "TICK-103",
            "Application freezes (ANR) on budget Android devices during catalog delta sync",
            "On Samsung Galaxy A14 devices, parsing 5,000+ SKU delta records blocks main UI thread for 4.2 seconds, resulting in Android OS Application Not Responding modal.",
            "Pacific Retailers Alliance",
            "Mid-Market",
            "Bug",
            "P1-High",
            "Open",
            "David Chen (Mobile Engineer)",
            12000.0,
            "Negative",
            "JSON deserialization and SQLite batch writes executing on main thread rather than IO dispatcher.",
            "Migrate catalog parsing to background coroutines and chunk insertions in batches of 250.",
            now,
            now
        ),
        (
            "TICK-104",
            "Request for digital QR code on offline customer invoice receipts",
            "Merchants need a printable or on-screen verification QR code generated offline so store receiving managers can verify order integrity before goods are unloaded.",
            "Lone Star Wholesale",
            "Growth",
            "Feature Request",
            "P2-Medium",
            "Open",
            "Unassigned",
            5000.0,
            "Neutral",
            "Feature enhancement to generate localized cryptographic QR hashes representing offline order snapshots.",
            "Evaluate client-side QR generation library for mobile receipt rendering in v3.5.",
            now,
            now
        ),
        (
            "TICK-105",
            "Floating-point rounding discrepancy on local tax calculations resolved",
            "Client-side IEEE 754 floating-point math produced sub-cent rounding errors causing backend schema validation to reject offline carts. Migrated to integer micro-cents.",
            "Summit Food & Beverage",
            "Mid-Market",
            "Bug",
            "P2-Medium",
            "Resolved",
            "Marcus Vance (Principal Architect)",
            0.0,
            "Positive",
            "Client tax calculation precision issue resolved via BigDecimal migration.",
            "Verified in Staging PR #284. Monitored zero validation rejections over past 48 hours.",
            now,
            now
        )
    ]

    for rec in sample_records:
        cursor.execute("""
        INSERT INTO records (
            ticket_key, title, description, customer_name, customer_tier,
            category, priority, status, assigned_engineer, impact_revenue,
            ai_sentiment, ai_summary, ai_recommended_action, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, rec)
        
        rec_id = cursor.lastrowid
        cursor.execute("""
        INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
        VALUES (?, 'CREATED', 'Record created via system ingestion', 'System Seeder', ?);
        """, (rec_id, now))

def get_all_records(search_query=None, status_filter=None, priority_filter=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM records WHERE 1=1"
    params = []

    if status_filter and status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)

    if priority_filter and priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)

    if search_query:
        query += " AND (title LIKE ? OR description LIKE ? OR customer_name LIKE ? OR ticket_key LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term])

    query += " ORDER BY CASE priority WHEN 'P0-Blocker' THEN 1 WHEN 'P1-High' THEN 2 WHEN 'P2-Medium' THEN 3 ELSE 4 END, id DESC"
    
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_record_by_id(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ? OR ticket_key = ?", (record_id, record_id))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    record = dict(row)
    
    # Fetch activity logs
    cursor.execute("SELECT * FROM activity_logs WHERE record_id = ? ORDER BY id DESC", (record["id"],))
    record["activity_logs"] = [dict(log) for log in cursor.fetchall()]
    
    conn.close()
    return record

def create_record(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    # Generate unique ticket key
    cursor.execute("SELECT MAX(id) as max_id FROM records")
    row = cursor.fetchone()
    next_id = (row["max_id"] or 100) + 1
    ticket_key = f"TICK-{next_id}"

    cursor.execute("""
    INSERT INTO records (
        ticket_key, title, description, customer_name, customer_tier,
        category, priority, status, assigned_engineer, impact_revenue,
        ai_sentiment, ai_summary, ai_recommended_action, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        ticket_key,
        data.get("title"),
        data.get("description"),
        data.get("customer_name", "Anonymous Account"),
        data.get("customer_tier", "Mid-Market"),
        data.get("category", "Bug"),
        data.get("priority", "P2-Medium"),
        data.get("status", "Open"),
        data.get("assigned_engineer", "Unassigned"),
        float(data.get("impact_revenue", 0.0)),
        data.get("ai_sentiment", "Neutral"),
        data.get("ai_summary", "Awaiting AI triage analysis..."),
        data.get("ai_recommended_action", "Review ticket details and assign to technical owner."),
        now,
        now
    ))
    new_id = cursor.lastrowid

    # Add audit log
    cursor.execute("""
    INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
    VALUES (?, 'CREATED', 'Record submitted via Support Portal', ?, ?);
    """, (new_id, data.get("created_by", "Support Portal User"), now))

    conn.commit()
    conn.close()
    return get_record_by_id(new_id)

def update_record(record_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    # Verify existence
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    current = cursor.fetchone()
    if not current:
        conn.close()
        return None
    
    fields_to_update = []
    params = []
    
    updatable = [
        "title", "description", "customer_name", "customer_tier", 
        "category", "priority", "status", "assigned_engineer", 
        "impact_revenue", "ai_sentiment", "ai_summary", "ai_recommended_action"
    ]

    changes = []
    for field in updatable:
        if field in data and data[field] is not None:
            fields_to_update.append(f"{field} = ?")
            params.append(data[field])
            if str(current[field]) != str(data[field]):
                changes.append(f"{field}: '{current[field]}' -> '{data[field]}'")

    if not fields_to_update:
        conn.close()
        return get_record_by_id(record_id)

    fields_to_update.append("updated_at = ?")
    params.append(now)
    params.append(record_id)

    query = f"UPDATE records SET {', '.join(fields_to_update)} WHERE id = ?"
    cursor.execute(query, params)

    # Log changes
    if changes:
        log_detail = "; ".join(changes)
        cursor.execute("""
        INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
        VALUES (?, 'UPDATED', ?, ?, ?);
        """, (record_id, log_detail, data.get("actor", "Support Engineer"), now))

    conn.commit()
    conn.close()
    return get_record_by_id(record_id)

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM records")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as open_count FROM records WHERE status = 'Open'")
    open_count = cursor.fetchone()["open_count"]

    cursor.execute("SELECT COUNT(*) as in_progress FROM records WHERE status = 'In Progress'")
    in_progress = cursor.fetchone()["in_progress"]

    cursor.execute("SELECT COUNT(*) as resolved FROM records WHERE status IN ('Resolved', 'Closed')")
    resolved = cursor.fetchone()["resolved"]

    cursor.execute("SELECT COUNT(*) as p0_count FROM records WHERE priority = 'P0-Blocker' AND status != 'Closed'")
    p0_count = cursor.fetchone()["p0_count"]

    cursor.execute("SELECT SUM(impact_revenue) as revenue_at_risk FROM records WHERE status != 'Closed'")
    rev = cursor.fetchone()["revenue_at_risk"] or 0.0

    conn.close()
    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "p0_blockers": p0_count,
        "revenue_at_risk": rev
    }
