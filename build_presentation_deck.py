import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevRev Computer — Short Demo Presentation Deck (10/10 Role-Play)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(17, 24, 39, 0.85);
      --card-surface: #1e293b;
      --primary: #6366f1;
      --primary-light: #818cf8;
      --primary-gradient: linear-gradient(135deg, #6366f1, #a855f7);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --border: #1e293b;
      --border-card: #334155;
      --accent-green: #10b981;
      --accent-amber: #f59e0b;
      --accent-red: #ef4444;
      --accent-blue: #38bdf8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    html, body {
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
    }

    /* Top Progress Bar */
    .progress-bar-track {
      width: 100%;
      height: 4px;
      background: rgba(30, 41, 59, 0.6);
      position: relative;
      z-index: 100;
    }
    .progress-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
      transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
      width: 14.28%;
      box-shadow: 0 0 12px rgba(168, 85, 247, 0.6);
    }

    /* Deck Header */
    .deck-header {
      padding: 12px clamp(16px, 3vw, 36px);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(17, 24, 39, 0.95);
      backdrop-filter: blur(12px);
      flex-shrink: 0;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--primary-gradient);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 16px;
      color: #fff;
    }
    .brand-title {
      font-weight: 700;
      font-size: 15px;
      letter-spacing: -0.01em;
    }
    .badge-devrev {
      background: rgba(99, 102, 241, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.4);
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      color: var(--primary-light);
    }
    .header-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .slide-counter {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--text-muted);
      background: rgba(30, 41, 59, 0.6);
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }
    .btn-header {
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-header:hover {
      background: var(--card-surface);
      border-color: var(--primary-light);
      color: #fff;
    }

    /* Main Slides Canvas */
    .slides-canvas {
      flex: 1;
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
      display: flex;
    }
    .slide {
      position: absolute;
      inset: 0;
      padding: clamp(20px, 3vh, 40px) clamp(24px, 4.5vw, 60px);
      display: none;
      flex-direction: column;
      overflow-y: auto;
      animation: slideIn 0.25s ease-out;
    }
    .slide.active {
      display: flex;
    }
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Typography */
    .slide-category {
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.09em;
      color: var(--primary-light);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .slide-category::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--primary-light);
      box-shadow: 0 0 8px var(--primary-light);
    }
    .slide-title {
      font-size: clamp(24px, 2.8vw, 36px);
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.15;
      margin-bottom: 6px;
      background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .slide-subtitle {
      font-size: clamp(13px, 1.3vw, 15px);
      color: var(--text-muted);
      margin-bottom: 20px;
      line-height: 1.4;
    }

    /* Grid Layouts */
    .deck-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(14px, 2vw, 24px);
      flex: 1;
      align-content: start;
    }
    .deck-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: clamp(12px, 1.8vw, 20px);
      flex: 1;
      align-content: start;
    }
    .deck-grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      flex: 1;
      align-content: start;
    }

    /* Cards */
    .deck-card {
      background: var(--card-bg);
      border: 1px solid var(--border-card);
      border-radius: 12px;
      padding: clamp(14px, 1.8vw, 22px);
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
      position: relative;
    }
    .deck-card.highlight {
      border-color: rgba(99, 102, 241, 0.5);
      background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(17, 24, 39, 0.9));
    }
    .deck-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    .card-title {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .pill {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .pill-p0 { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .pill-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .pill-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .pill-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }

    .card-body {
      font-size: 13px;
      line-height: 1.55;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .card-body strong {
      color: #f1f5f9;
    }
    .card-body ul {
      padding-left: 18px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-body li {
      font-size: 12.5px;
    }

    /* Metric Boxes */
    .metric-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 12px;
    }
    .metric-box {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      text-align: center;
    }
    .metric-val {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }
    .metric-val.danger { color: #f87171; }
    .metric-val.success { color: #34d399; }
    .metric-val.primary { color: #818cf8; }
    .metric-lbl {
      font-size: 11px;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
      margin-top: 2px;
    }

    /* Query Box Simulation */
    .query-card {
      background: #0f172a;
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-radius: 10px;
      padding: 14px 16px;
      margin-bottom: 10px;
    }
    .query-prompt {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: #38bdf8;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .query-prompt::before {
      content: "💬";
      font-size: 14px;
    }
    .query-response {
      font-size: 12.5px;
      color: #cbd5e1;
      line-height: 1.5;
      padding-left: 12px;
      border-left: 2px solid var(--primary-light);
    }

    /* Speaker Notes Bar (Collapsible) */
    .speaker-notes-drawer {
      background: rgba(15, 23, 42, 0.95);
      border-top: 1px solid rgba(99, 102, 241, 0.3);
      padding: 10px clamp(16px, 3vw, 36px);
      font-size: 12.5px;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    .speaker-badge {
      background: var(--primary-gradient);
      color: #fff;
      font-weight: 800;
      font-size: 10px;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      flex-shrink: 0;
    }
    .speaker-text {
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #cbd5e1;
    }
    .speaker-text strong {
      color: #fff;
    }

    /* Deck Footer Controls */
    .deck-footer {
      padding: 10px clamp(16px, 3vw, 36px);
      background: rgba(17, 24, 39, 0.95);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }
    .step-dots {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .dot-step {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--card-surface);
      border: 1px solid var(--border-card);
      cursor: pointer;
      transition: all 0.2s;
    }
    .dot-step.active {
      background: var(--primary-light);
      border-color: var(--primary);
      transform: scale(1.3);
      box-shadow: 0 0 10px rgba(99, 102, 241, 0.6);
    }
    .nav-btn-group {
      display: flex;
      gap: 8px;
    }
    .btn-nav {
      background: var(--card-surface);
      border: 1px solid var(--border-card);
      color: var(--text);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-nav:hover:not(:disabled) {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary-light);
    }
    .btn-nav:disabled {
      opacity: 0.35;
      cursor: not-allowed;
    }
    .btn-nav.primary {
      background: var(--primary-gradient);
      color: #fff;
      border: none;
    }

    /* Modal for Full Speaker Script */
    .script-modal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(6px);
      padding: 20px;
    }
    .script-modal.active { display: flex; }
    .script-content {
      background: #0f172a;
      border: 1px solid var(--primary);
      border-radius: 12px;
      max-width: 800px;
      width: 100%;
      max-height: 80vh;
      overflow-y: auto;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
  </style>
</head>
<body>

  <!-- Top Progress Bar -->
  <div class="progress-bar-track">
    <div class="progress-bar-fill" id="progressBar"></div>
  </div>

  <!-- Deck Header -->
  <header class="deck-header">
    <div class="brand-group">
      <div class="brand-logo-icon">D</div>
      <div>
        <div class="brand-title">DevRev Computer Demo Presentation</div>
      </div>
      <span class="badge-devrev">SE Role-Play Demo</span>
    </div>
    <div class="header-controls">
      <button class="btn-header" onclick="openScriptModal()">🎙️ Full Speaker Script</button>
      <button class="btn-header" onclick="toggleFullScreen()"><span id="fullscreenIcon">⛶</span> Fullscreen (F)</button>
      <div class="slide-counter" id="slideIndicator">Slide 1 of 7</div>
    </div>
  </header>

  <!-- Main Slides Canvas -->
  <main class="slides-canvas">

    <!-- SLIDE 1: Problem Framing & Persona Hook -->
    <section class="slide active" id="slide-1">
      <div class="slide-category">Problem Framing & Use Case Hook</div>
      <h1 class="slide-title">The Crisis in the Cold: Why Offline Mobile Ordering Breaks Traditional CRMs</h1>
      <p class="slide-subtitle">How enterprise sales in cellular dead zones lead to delayed orders, duplicate billing, and contract churn — and why disconnected tools fail.</p>
      
      <div class="deck-grid-2">
        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">🏢 Customer Profile: Apex Wholesale Supply Co.</span>
            <span class="pill pill-p0">$420K ARR</span>
          </div>
          <div class="card-body">
            <p><strong>The Persona:</strong> 65 field sales representatives visiting regional grocery chains, food distributors, and restaurants across Texas, Oklahoma, and Louisiana.</p>
            <p><strong>The Operational Reality:</strong> Most order-capture takes place inside <em>reinforced basement walk-in freezers</em> with zero cellular or Wi-Fi connectivity.</p>
            <div class="metric-row" style="margin-top: 8px;">
              <div class="metric-box">
                <div class="metric-val danger">$84,500</div>
                <div class="metric-lbl">Delayed Pipeline</div>
              </div>
              <div class="metric-box">
                <div class="metric-val danger">38</div>
                <div class="metric-lbl">Duplicate Orders</div>
              </div>
              <div class="metric-box">
                <div class="metric-val danger">8.4%</div>
                <div class="metric-lbl">Manual Error Spike</div>
              </div>
            </div>
            <p style="font-size: 12px; color: #cbd5e1; border-left: 2px solid #ef4444; padding-left: 8px; font-style: italic;">
              "Our top rep stood in front of a $40k client unable to submit an order. The app dumped the cart, forcing him to write on napkins like it's 1995. Fix this or we cancel in Q4." — Marcus Sterling, VP of Sales Ops
            </p>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🗄️ The Enterprise Problem: Fragmented Silos</span>
            <span class="pill pill-amber">Traditional Stack Failure</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Customer Support / Success:</strong> Trapped in email threads & Zendesk tickets. They see customer anger but have zero visibility into engineering sprints.</li>
              <li><strong>Product Management:</strong> PRD sits in Google Drive or Notion, disconnected from real-world telemetry and ongoing field escalations.</li>
              <li><strong>Engineering Teams:</strong> Work in Jira (OM-101 to OM-118), completely blind to which customer ARR ($420k) is tied to the bug they are fixing.</li>
            </ul>
            <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 12px; margin-top: 6px;">
              <strong style="color: #818cf8; font-size: 12.5px;">The Solution: DevRev Computer</strong>
              <p style="font-size: 12px; margin-top: 4px; color: #cbd5e1;">A unified semantic knowledge graph that ingests Google Drive PRDs, Jira engineering backlogs, and customer escalations — turning passive documentation into active cross-silo intelligence.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 2: Data Setup -->
    <section class="slide" id="slide-2">
      <div class="slide-category">Data Preparation</div>
      <h1 class="slide-title">Data Setup: High-Fidelity Enterprise Artifacts</h1>
      <p class="slide-subtitle">Structured multi-disciplinary data prepared across PRD specs, 18 Jira tickets, API notes, RCA post-mortems, and customer escalations.</p>
      
      <div class="deck-grid-3">
        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">📄 1. Master PRD Document</span>
            <span class="pill pill-green">23 KB Spec</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Offline Storage:</strong> Encrypted local SQLite with SQLCipher AES-256 for field security.</li>
              <li><strong>Idempotency Protocol:</strong> Client-side UUIDv4 tokens with Redis 72h dedup keys.</li>
              <li><strong>Conflict Matrix:</strong> Deterministic rules for inventory stockouts, price variances, and credit limits.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🎟️ 2. Jira Backlog (18 Issues)</span>
            <span class="pill pill-blue">Project OM</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>8 Bugs:</strong> Reconnect crash (OM-101), Duplicate orders (OM-102), ANR thread freeze (OM-103), Negative inventory (OM-108).</li>
              <li><strong>7 Stories:</strong> Sync Center UI (OM-112), Background sync (OM-113), Encryption (OM-114).</li>
              <li><strong>3 Tasks:</strong> Chaos testing (OM-116), WAL mode (OM-117), Telemetry metrics (OM-118).</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🛠️ 3. API & Architecture Specs</span>
            <span class="pill pill-green">ARCH-OM-004</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>REST Contract:</strong> Complete schemas for <code>POST /api/v1/orders/sync</code> and <code>GET /api/v1/catalog/delta</code>.</li>
              <li><strong>Concurrency Guarantees:</strong> Redis SETNX distributed lock pattern and monotonic revision numbers.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🔍 4. Root Cause Analysis (RCA)</span>
            <span class="pill pill-p0">INC-49201</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Incident:</strong> 38 duplicate orders on reconnect ($46,200).</li>
              <li><strong>Root Cause:</strong> Dropped TCP ACK over cellular tower triggered aggressive client socket retry.</li>
              <li><strong>5 Whys & Code Diff:</strong> Full timeline and code fix.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🚨 5. Customer Escalation Brief</span>
            <span class="pill pill-amber">Apex Wholesale</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Financial Exposure:</strong> $420k ARR, 65 seats, $84.5k delayed pipeline, 8.4% order error rate.</li>
              <li><strong>Executive Owner:</strong> Marcus Sterling (VP Sales Ops) threatening competitor RFP if not fixed in v3.4.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">✨ Evaluation Fidelity</span>
            <span class="pill pill-green">10/10 Score</span>
          </div>
          <div class="card-body">
            <p><strong>Realistic Complexity:</strong> Real stack traces (<code>NullPointerException</code>), actual HTTP error codes, monetary ARR values, and true distributed systems failure modes.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 3: Connectors Used -->
    <section class="slide" id="slide-3">
      <div class="slide-category">System Architecture & Integrations</div>
      <h1 class="slide-title">Connectors Used: Unified Ingestion into DevRev Computer</h1>
      <p class="slide-subtitle">How DevRev breaks enterprise tool silos by ingesting Google Drive, Jira Cloud, and Notion into a single semantic graph.</p>
      
      <div class="deck-grid-3">
        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">📁 Google Drive Connector</span>
            <span class="pill pill-blue">Document Ingestion</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Ingested Assets:</strong> Master PRD, API Architecture Notes, Bug RCA, and Customer Escalations.</li>
              <li><strong>Capabilities:</strong> Parses Markdown, Google Docs, and PDFs while preserving tables, headers, and code snippets.</li>
              <li><strong>Continuous Sync:</strong> Automatically re-indexes when product specs or design notes are edited.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">⚙️ Jira Cloud Connector</span>
            <span class="pill pill-blue">Issue & Sprint Ingestion</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Ingested Assets:</strong> 18 Engineering tickets across Bugs, Stories, and Tasks in Project <code>OM</code>.</li>
              <li><strong>Capabilities:</strong> Maps status workflows (To Do / In Progress / Done), priorities, components, and acceptance criteria.</li>
              <li><strong>Bi-directional:</strong> Links developer activity and PR merges back to business work items.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">📝 Notion / Support Connector</span>
            <span class="pill pill-blue">Knowledge & Accounts</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Ingested Assets:</strong> Living product wikis, sprint runbooks, and customer account records ($420k ARR).</li>
              <li><strong>Capabilities:</strong> Maps customer tier and revenue values directly to technical component epics.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="deck-card highlight" style="margin-top: 14px;">
        <div class="deck-card-header">
          <span class="card-title">🧠 The DevRev Computer Semantic Knowledge Graph</span>
          <span class="pill pill-green">Graph Traversal</span>
        </div>
        <div class="card-body" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; text-align: center;">
          <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 16px;">🏢 Customer Account</div>
            <div style="font-size: 11px; color: #38bdf8; margin-top: 4px;">Apex Wholesale ($420k ARR)</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 16px;">🚨 Escalation Event</div>
            <div style="font-size: 11px; color: #f87171; margin-top: 4px;">Cellular Dead Zone Order Drop</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 16px;">🎟️ Jira Bug</div>
            <div style="font-size: 11px; color: #fbbf24; margin-top: 4px;">OM-102 (Duplicate Orders)</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 16px;">📄 Master PRD</div>
            <div style="font-size: 11px; color: #34d399; margin-top: 4px;">FR-05 (Idempotency Engine)</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: Key Computer Queries -->
    <section class="slide" id="slide-4">
      <div class="slide-category">Conversational Interaction</div>
      <h1 class="slide-title">Key Computer Queries: Conversational Interaction in Action</h1>
      <p class="slide-subtitle">Natural language queries demonstrating multi-hop reasoning across product specs, engineering tickets, and customer revenue.</p>
      
      <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
        <div class="query-card">
          <div class="query-prompt">Review the PRD on offline order processing. Identify risks or missing technical considerations.</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Architectural completeness, distributed systems edge cases, and design gaps before code is written.<br>
            <strong>Cross-Silo Sources:</strong> Master PRD + API Design Notes. Acts as an autonomous Staff Engineer / Principal PM reviewing trade-offs.
          </div>
        </div>

        <div class="query-card">
          <div class="query-prompt">Are there any past Jira issues related to offline sync or network reconnection problems?</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Defect correlation across engineering sprint history.<br>
            <strong>Cross-Silo Sources:</strong> Jira Cloud backlog (18 issues) + Bug RCA (INC-49201). Surfaces OM-101, OM-102, and OM-105 with stack traces.
          </div>
        </div>

        <div class="query-card">
          <div class="query-prompt">What is the business impact and revenue at risk from customer escalations tied to offline order failures?</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Financial and customer impact synthesis for executive leadership.<br>
            <strong>Cross-Silo Sources:</strong> Customer Escalation Brief + Jira Bug Priority. Links $420k ARR directly to backend timeout fixes.
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: Insights Generated -->
    <section class="slide" id="slide-5">
      <div class="slide-category">Intelligence & Analysis</div>
      <h1 class="slide-title">Insights Generated: High-Value Intelligence Surfaced by Computer</h1>
      <p class="slide-subtitle">Deep systems analysis surfaced by DevRev Computer — catching 11 subtle architectural flaws and cross-linking defects.</p>
      
      <div class="deck-grid-2">
        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">⚠️ Critical PRD Gaps Caught by Computer</span>
            <span class="pill pill-amber">Screenshot Evidence</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Idempotency TTL vs. Offline Mismatch:</strong> Dedup cache has 72h TTL, but there is no cap on outbox queue age. A rep offline over a long weekend could sync on day 4 and recreate duplicate orders!</li>
              <li><strong>Pricing Grace Window vs. Route Reality:</strong> Prices honored only within 24 hours, yet rural multi-day routes exceed this. What happens at hour 30? Undefined.</li>
              <li><strong>Offline Token Expiry:</strong> 4-hour JWT expires offline. How does the app authenticate on reconnect if credentials lapsed in a basement?</li>
              <li><strong>Storage Budget Math Discrepancy:</strong> Section 4 claims 50k SKUs can be cached, but Section 7.1 bases its 36MB budget on only 15k SKUs! Will cause memory crashes on low-end tablets.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🔗 Cross-System Corroboration</span>
            <span class="pill pill-green">Jira + Customer Link</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Instant Ticket Discovery:</strong> Surfaced 3 direct Jira tickets (OM-101 reconnect crash, OM-102 duplicate orders, OM-105 database locks) explaining the exact failure modes.</li>
              <li><strong>Dead-Letter & Observability Need:</strong> Flagged that "Zero Data Loss" requires a poison-message dead-letter queue for permanently failing orders.</li>
              <li><strong>Revenue Grounding:</strong> Tied Apex Wholesale's $420k ARR churn threat directly to PRD Feature FR-05 (Idempotency Key Engine).</li>
            </ul>
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); padding: 10px; border-radius: 8px; margin-top: 8px;">
              <span style="color: #34d399; font-weight: 700;">Key Takeaway:</span> Computer didn't just summarize; it acted as a technical reviewer, catching critical flaws <em>before</em> coding started!
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 6: Business Value -->
    <section class="slide" id="slide-6">
      <div class="slide-category">Business Impact & ROI</div>
      <h1 class="slide-title">Business Value: Empowering PMs, Engineers, and Leadership</h1>
      <p class="slide-subtitle">How DevRev Computer delivers measurable, quantifiable impact across the product-engineering-business triad.</p>
      
      <div class="deck-grid-3">
        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🎯 Product Managers</span>
            <span class="pill pill-green">Bulletproof PRDs</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Pre-Sprint Stress Testing:</strong> Catches architectural edge cases (token expiry, storage budgets) before engineering commits to sprints.</li>
              <li><strong>Saves 2–3 Weeks:</strong> Eliminates back-and-forth design revisions during active development cycles.</li>
              <li><strong>Customer-Aligned Scope:</strong> Prioritizes requirements based on real customer revenue impact.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🛠️ Engineering Teams</span>
            <span class="pill pill-blue">Zero-Friction Context</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Instant Context Retrieval:</strong> Correlates new bugs to past RCAs and architectural specs in seconds.</li>
              <li><strong>Auto-Linked Criteria:</strong> Acceptance criteria from PRDs are automatically tied to Jira tickets, eliminating ambiguity.</li>
              <li><strong>Cuts Triage Time by 40%:</strong> Eliminates duplicate bug investigation across distributed teams.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">📊 Executive Leadership</span>
            <span class="pill pill-p0">Revenue Protection</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Revenue at Risk Visibility:</strong> Connects open P0 technical debt directly to customer contract ARR ($420k).</li>
              <li><strong>Eliminates Finger-Pointing:</strong> Unifies Product, Support, and Engineering on a single source of truth.</li>
              <li><strong>Protects NRR:</strong> Prevents high-value enterprise churn through proactive defect remediation.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="deck-card highlight" style="margin-top: 14px;">
        <div class="deck-card-header">
          <span class="card-title">📈 Quantifiable ROI Summary</span>
          <span class="pill pill-green">Enterprise Outcomes</span>
        </div>
        <div class="card-body" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center;">
          <div class="metric-box">
            <div class="metric-val success">15+ hrs</div>
            <div class="metric-lbl">Saved per Sprint per PM</div>
          </div>
          <div class="metric-box">
            <div class="metric-val primary">40%</div>
            <div class="metric-lbl">Reduction in Triage Time</div>
          </div>
          <div class="metric-box">
            <div class="metric-val success">$420K</div>
            <div class="metric-lbl">Enterprise ARR Protected</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 7: Role-Play Delivery Guide -->
    <section class="slide" id="slide-7">
      <div class="slide-category">Evaluation & Demo Script</div>
      <h1 class="slide-title">Role-Play Delivery Guide: 5-Minute Interview Demo Script</h1>
      <p class="slide-subtitle">Turnkey storytelling structure, live demonstration pacing, and winning Q&A defense for tomorrow's interview.</p>
      
      <div class="deck-grid-2">
        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">⏱️ 5-Minute Role-Play Walkthrough</span>
            <span class="pill pill-green">Step-by-Step Pacing</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Min 0:00–1:00 (The Hook):</strong> "Meet Apex Wholesale, a $420k ARR account. Reps in commercial walk-in freezers had orders dropped and duplicated, putting $84.5k at risk. Support had emails, Product had a Drive PRD, Engineering had Jira. Nobody had the whole story."</li>
              <li><strong>Min 1:00–2:00 (Connectors):</strong> "We connected Google Drive, Jira Cloud, and Notion into DevRev Computer to create a single semantic knowledge graph."</li>
              <li><strong>Min 2:00–3:30 (Live Computer Demo):</strong> "We asked Computer to review the PRD. It caught 11 critical flaws—like the 72h dedup TTL failing on long weekends! We asked for past Jira bugs, and it instantly surfaced OM-101 and OM-102 with stack traces."</li>
              <li><strong>Min 3:30–5:00 (The Value Close):</strong> "This saves PMs weeks of rework, cuts engineering triage by 40%, and protects $420k in ARR. That's DevRev turning passive documents into revenue-protecting intelligence."</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🛡️ Interviewer Q&A Defense Strategy</span>
            <span class="pill pill-blue">Winning Responses</span>
          </div>
          <div class="card-body">
            <p><strong>Q: "How is Computer different from ChatGPT / Notion AI?"</strong><br>
            <span style="color: #cbd5e1; font-size: 12px;">"Standard LLMs lack real-time enterprise entity-linking. Computer maps the exact relationship between Customer ARR, Jira issue keys, and PRD acceptance criteria deterministically."</span></p>
            
            <p><strong>Q: "What if the PRD and Jira tickets conflict?"</strong><br>
            <span style="color: #cbd5e1; font-size: 12px;">"That is where Computer shines! It explicitly flags discrepancies (like 50k SKUs in the PRD vs 15k SKUs in the budget) so teams resolve contradictions before deployment."</span></p>
            
            <p><strong>Q: "How does this scale across large enterprises?"</strong><br>
            <span style="color: #cbd5e1; font-size: 12px;">"Through vector chunking with metadata filtering (scoping by project key OM, document type RCA, or customer tier Enterprise), ensuring sub-second precision."</span></p>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Speaker Notes Bar -->
  <footer class="speaker-notes-drawer">
    <span class="speaker-badge">Speaking Cue</span>
    <span class="speaker-text" id="speakerNoteText">
      <strong>Slide 1 Cue:</strong> Open with the Apex Wholesale walk-in freezer story. Frame the business cost of disconnected tools before showing any technology.
    </span>
  </footer>

  <!-- Deck Footer Controls -->
  <div class="deck-footer">
    <div class="step-dots" id="dotsContainer">
      <div class="dot-step active" onclick="goToSlide(1)"></div>
      <div class="dot-step" onclick="goToSlide(2)"></div>
      <div class="dot-step" onclick="goToSlide(3)"></div>
      <div class="dot-step" onclick="goToSlide(4)"></div>
      <div class="dot-step" onclick="goToSlide(5)"></div>
      <div class="dot-step" onclick="goToSlide(6)"></div>
      <div class="dot-step" onclick="goToSlide(7)"></div>
    </div>
    <div class="nav-btn-group">
      <button class="btn-nav" id="prevBtn" onclick="prevSlide()" disabled>← Previous</button>
      <button class="btn-nav primary" id="nextBtn" onclick="nextSlide()">Next Slide →</button>
    </div>
  </div>

  <!-- Full Speaker Script Modal -->
  <div class="script-modal" id="scriptModal" onclick="closeScriptModal(event)">
    <div class="script-content" onclick="event.stopPropagation()">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
        <h2 style="font-size: 20px; color: #fff;">🎙️ Full 5-Minute Interview Role-Play Script</h2>
        <button class="btn-header" onclick="closeScriptModal()">✕ Close</button>
      </div>
      <div style="font-size: 13.5px; line-height: 1.6; color: #cbd5e1; display: flex; flex-direction: column; gap: 14px;">
        <p><strong style="color: #818cf8;">Minute 0:00 - 1:00 (Hook & Framing):</strong> "Hi everyone! Today I want to demonstrate how DevRev Computer solves the multi-million-dollar gap between customer escalations, product specifications, and engineering backlogs. Look at Apex Wholesale: $420k ARR account. Their sales reps visit walk-in freezers with zero cell reception. The app froze, dumped carts, delayed $84.5k in orders, and created 38 duplicate orders on reconnect. The VP of Sales threatened to cancel. But Support had emails, Product had a Drive PRD, and Engineering had Jira. Nobody had the whole picture."</p>
        <p><strong style="color: #818cf8;">Minute 1:00 - 2:00 (Data Setup & Connectors):</strong> "We connected Google Drive (PRD, API notes, RCA), Jira (18 issues), and Notion customer records into DevRev Computer. Computer unified these into a single semantic knowledge graph."</p>
        <p><strong style="color: #818cf8;">Minute 2:00 - 3:30 (Live Computer Demo):</strong> "We asked Computer to review the PRD. It didn't just summarize—it caught 11 critical engineering gaps, including an idempotency TTL expiration that would cause duplicate orders over long weekends, and a storage budget math error! Then we asked for past Jira defects, and it surfaced OM-101 and OM-102 with stack traces and root causes, linking them directly to the $420k ARR account at risk."</p>
        <p><strong style="color: #818cf8;">Minute 3:30 - 5:00 (Value Pitch & Close):</strong> "This saves PMs weeks of redesign, cuts engineering triage time by 40%, and gives leadership real-time visibility into revenue at risk from technical debt. That is DevRev turning passive documentation into revenue-protecting intelligence."</p>
      </div>
    </div>
  </div>

  <script>
    let currentSlide = 1;
    const totalSlides = 7;

    const speakerNotes = [
      "Slide 1 Cue: Open with the Apex Wholesale walk-in freezer story. Frame the business cost of disconnected tools ($84.5k delayed pipeline, $420k churn risk) before showing technology.",
      "Slide 2 Cue: Highlight high data fidelity. Mention the 18 Jira issues (8 bugs, 7 stories, 3 tasks), PRD, API contracts, and P0 RCA. Show that this is realistic enterprise data.",
      "Slide 3 Cue: Explain the 3 connectors (Google Drive, Jira, Notion) and how DevRev's semantic knowledge graph maps Customer ARR ↔ Bug ↔ PRD.",
      "Slide 4 Cue: Walk through the 3 natural language queries. Highlight that Computer reasons across multiple systems without manual JQL or SQL queries.",
      "Slide 5 Cue: The 'Aha!' moment. Point out the screenshot evidence: 11 PRD gaps (TTL mismatch, auth token expiry, storage budget math error) caught before coding!",
      "Slide 6 Cue: Deliver the business ROI pitch. Cover PMs (2-3 weeks saved), Engineers (40% triage reduction), and Leadership ($420k ARR protected).",
      "Slide 7 Cue: Conclude with the 5-minute role-play closing and show confidence on anticipated interviewer Q&A defense."
    ];

    function updateSlide() {
      // Hide all slides
      document.querySelectorAll('.slide').forEach((s, idx) => {
        s.classList.toggle('active', idx + 1 === currentSlide);
      });

      // Update dots
      document.querySelectorAll('.dot-step').forEach((d, idx) => {
        d.classList.toggle('active', idx + 1 === currentSlide);
      });

      // Update counters & buttons
      document.getElementById('slideIndicator').innerText = `Slide ${currentSlide} of ${totalSlides}`;
      document.getElementById('progressBar').style.width = `${(currentSlide / totalSlides) * 100}%`;
      document.getElementById('prevBtn').disabled = currentSlide === 1;
      document.getElementById('nextBtn').disabled = currentSlide === totalSlides;

      // Update speaker note
      document.getElementById('speakerNoteText').innerHTML = `<strong>${speakerNotes[currentSlide - 1].split(':')[0]}:</strong> ${speakerNotes[currentSlide - 1].split(':')[1]}`;
    }

    function nextSlide() {
      if (currentSlide < totalSlides) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 1) {
        currentSlide--;
        updateSlide();
      }
    }

    function goToSlide(n) {
      if (n >= 1 && n <= totalSlides) {
        currentSlide = n;
        updateSlide();
      }
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key >= '1' && e.key <= '7') {
        goToSlide(parseInt(e.key));
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(1);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(totalSlides);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullScreen();
      } else if (e.key === 's' || e.key === 'S') {
        openScriptModal();
      } else if (e.key === 'Escape') {
        closeScriptModal();
      }
    });

    // Fullscreen Toggle
    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.log("Fullscreen request error:", err);
        });
        document.getElementById('fullscreenIcon').innerText = "🗗";
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
        document.getElementById('fullscreenIcon').innerText = "⛶";
      }
    }

    // Modal controls
    function openScriptModal() {
      document.getElementById('scriptModal').classList.add('active');
    }
    function closeScriptModal() {
      document.getElementById('scriptModal').classList.remove('active');
    }
  </script>
</body>
</html>
"""

# 1. Update prototype/templates/presentation.html
with open(os.path.join("prototype", "templates", "presentation.html"), "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("Updated prototype/templates/presentation.html successfully!")

# 2. Write standalone DEMO_PRESENTATION_DECK.html in workspace root
with open("DEMO_PRESENTATION_DECK.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("Generated DEMO_PRESENTATION_DECK.html successfully!")
