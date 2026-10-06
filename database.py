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
            "Android app ANR freeze on catalog sync containing >15,000 SKUs",
            "During background SQLite catalog ingestion, main UI thread blocks for 4.8 seconds causing Android ANR dialogs. Reps forced to force-quit app and re-authenticate.",
            "Pacific Beverage Logistics",
            "Mid-Market",
            "Bug",
            "P1-High",
            "Open",
            "Marcus Chen (Mobile Tech Lead)",
            28000.0,
            "Negative",
            "Heavy SQLite batch transaction on main thread starves UI rendering; requires Room/Coroutine async worker.",
            "Migrate catalog cache to SQLite WAL mode with split read/write connection pool (PR #492).",
            now,
            now
        ),
        (
            "TICK-104",
            "Request for multi-currency pricing support in offline catalog cache",
            "Canadian cross-border distributors need CAD and USD pricing matrices cached locally with currency exchange rates locked at sync time.",
            "Great Lakes Provisions",
            "Growth",
            "Feature Request",
            "P2-Medium",
            "Open",
            "Sarah Jenkins (Product Specialist)",
            14500.0,
            "Neutral",
            "Product enhancement request for multi-currency offline support; low immediate risk to core operations.",
            "Add to Q3 Product Discovery backlog; gather currency fluctuation volatility requirements.",
            now,
            now
        ),
        (
            "TICK-105",
            "Warehouse sync gateway returning intermittent 401 Unauthorized during token refresh",
            "OAuth JWT access token expired during 6-hour offline shift; client attempted bulk outbox sync with stale token resulting in gateway reject and empty retry backoff.",
            "SunState Food Service",
            "Mid-Market",
            "Bug",
            "P1-High",
            "Resolved",
            "Elena Rostova (Backend Systems Lead)",
            31000.0,
            "Positive",
            "Gateway auth race condition resolved: refresh token exchange now executes proactively prior to bulk outbox push.",
            "Hotfix deployed in Mobile v3.3.2; customer confirmed successful sync across all 24 regional tablets.",
            now,
            now
        ),
        (
            "TICK-106",
            "Customer feedback: Sales team requesting customizable order templates for high-frequency reorders",
            "Weekly recurring grocery deliveries frequently order the exact same 40 SKUs. Reps want one-click order cloning to save 12 minutes per retail store stop.",
            "Southwest Fresh Grocery Alliance",
            "Growth",
            "Feature Request",
            "P2-Medium",
            "Open",
            "Alex Rivera (Staff Solutions Engineer)",
            18500.0,
            "Neutral",
            "High-value workflow enhancement requested by field sales reps to accelerate in-store order turnaround.",
            "Share user journey with Mobile PM; evaluate template caching in local SQLite database.",
            now,
            now
        )
    ]

    for record in sample_records:
        cursor.execute("""
        INSERT INTO records (
            ticket_key, title, description, customer_name, customer_tier,
            category, priority, status, assigned_engineer, impact_revenue,
            ai_sentiment, ai_summary, ai_recommended_action, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, record)
        
        record_id = cursor.lastrowid
        
        # Log initial creation audit
        cursor.execute("""
        INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
        VALUES (?, 'CREATED', 'Record ingested into support queue with initial classification', 'System Seeder', ?)
        """, (record_id, now))

def get_all_records(search_query=None, status_filter=None, priority_filter=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM records WHERE 1=1"
    params = []
    
    if search_query:
        query += " AND (title LIKE ? OR description LIKE ? OR customer_name LIKE ? OR ticket_key LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])
        
    if status_filter and status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
        
    if priority_filter and priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)
        
    query += " ORDER BY CASE priority WHEN 'P0-Blocker' THEN 1 WHEN 'P1-High' THEN 2 WHEN 'P2-Medium' THEN 3 ELSE 4 END, id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_record_by_id(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record_row = cursor.fetchone()
    
    if not record_row:
        conn.close()
        return None
        
    record = dict(record_row)
    
    # Fetch associated activity logs
    cursor.execute(
        "SELECT * FROM activity_logs WHERE record_id = ? ORDER BY id DESC", 
        (record_id,)
    )
    logs = [dict(row) for row in cursor.fetchall()]
    record["activity_logs"] = logs
    
    conn.close()
    return record

def create_record(data, actor="Solutions Engineer"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate sequential ticket key
    cursor.execute("SELECT MAX(id) as max_id FROM records")
    row = cursor.fetchone()
    next_id = (row["max_id"] or 100) + 1
    ticket_key = f"TICK-{next_id}"
    
    now = datetime.now(timezone.utc).isoformat()
    
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    customer_name = data.get("customer_name", "").strip()
    customer_tier = data.get("customer_tier", "Growth")
    category = data.get("category", "Inquiry")
    priority = data.get("priority", "P2-Medium")
    status = data.get("status", "Open")
    assigned_engineer = data.get("assigned_engineer", "Unassigned")
    impact_revenue = float(data.get("impact_revenue", 0.0) or 0.0)
    
    # Default AI heuristics upon creation
    ai_sentiment = "Negative" if priority in ["P0-Blocker", "P1-High"] else "Neutral"
    ai_summary = f"New {category} reported by {customer_name}. Initial triage pending."
    ai_recommended_action = "Review customer ARR and route to assigned on-call team."
    
    cursor.execute("""
    INSERT INTO records (
        ticket_key, title, description, customer_name, customer_tier,
        category, priority, status, assigned_engineer, impact_revenue,
        ai_sentiment, ai_summary, ai_recommended_action, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_key, title, description, customer_name, customer_tier,
        category, priority, status, assigned_engineer, impact_revenue,
        ai_sentiment, ai_summary, ai_recommended_action, now, now
    ))
    
    record_id = cursor.lastrowid
    
    # Insert audit log
    cursor.execute("""
    INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
    VALUES (?, 'CREATED', ?, ?, ?)
    """, (
        record_id, 
        f"Record created via API by {actor}. Priority: {priority}, Status: {status}", 
        actor, 
        now
    ))
    
    conn.commit()
    conn.close()
    
    return get_record_by_id(record_id)

def update_record(record_id, data, actor="Solutions Engineer"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check existing
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return None
        
    existing_dict = dict(existing)
    now = datetime.now(timezone.utc).isoformat()
    
    # Allowed mutable fields
    updatable_fields = [
        "title", "description", "customer_name", "customer_tier",
        "category", "priority", "status", "assigned_engineer",
        "impact_revenue", "ai_sentiment", "ai_summary", "ai_recommended_action"
    ]
    
    updates = []
    params = []
    changes = []
    
    for field in updatable_fields:
        if field in data and data[field] is not None:
            new_val = data[field]
            old_val = existing_dict.get(field)
            if str(new_val) != str(old_val):
                updates.append(f"{field} = ?")
                params.append(new_val)
                changes.append(f"{field}: '{old_val}' -> '{new_val}'")
                
    if not updates:
        conn.close()
        return get_record_by_id(record_id)
        
    updates.append("updated_at = ?")
    params.append(now)
    params.append(record_id)
    
    query = f"UPDATE records SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    
    # Insert audit entry
    change_summary = "; ".join(changes)
    cursor.execute("""
    INSERT INTO activity_logs (record_id, action, details, actor, timestamp)
    VALUES (?, 'UPDATED', ?, ?, ?)
    """, (record_id, change_summary, actor, now))
    
    conn.commit()
    conn.close()
    
    return get_record_by_id(record_id)

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM records")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as count FROM records WHERE status = 'Open'")
    open_count = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM records WHERE status = 'In Progress'")
    in_progress_count = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM records WHERE status = 'Resolved'")
    resolved_count = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM records WHERE priority = 'P0-Blocker'")
    p0_count = cursor.fetchone()["count"]
    
    cursor.execute("SELECT SUM(impact_revenue) as rev FROM records WHERE status != 'Resolved' AND status != 'Closed'")
    rev_row = cursor.fetchone()["rev"]
    revenue_at_risk = float(rev_row or 0.0)
    
    conn.close()
    
    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress_count,
        "resolved": resolved_count,
        "p0_blockers": p0_count,
        "revenue_at_risk": revenue_at_risk
    }
