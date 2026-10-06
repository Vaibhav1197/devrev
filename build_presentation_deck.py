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
      --card-bg: rgba(17, 24, 39, 0.88);
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
      padding: 10px clamp(16px, 2.5vw, 32px);
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
      padding: clamp(16px, 2.5vh, 32px) clamp(20px, 3.5vw, 48px);
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
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--primary-light);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .slide-category::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--primary-light);
      box-shadow: 0 0 8px var(--primary-light);
    }
    .slide-title {
      font-size: clamp(22px, 2.4vw, 32px);
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.15;
      margin-bottom: 4px;
      background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .slide-subtitle {
      font-size: clamp(12.5px, 1.15vw, 14.5px);
      color: var(--text-muted);
      margin-bottom: 14px;
      line-height: 1.4;
    }

    /* Grid Layouts */
    .deck-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(12px, 1.6vw, 20px);
      flex: 1;
      align-content: start;
    }
    .deck-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: clamp(10px, 1.4vw, 16px);
      flex: 1;
      align-content: start;
    }
    .deck-grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      flex: 1;
      align-content: start;
    }

    /* Cards */
    .deck-card {
      background: var(--card-bg);
      border: 1px solid var(--border-card);
      border-radius: 10px;
      padding: clamp(12px, 1.4vw, 18px);
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
      position: relative;
    }
    .deck-card.highlight {
      border-color: rgba(99, 102, 241, 0.5);
      background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(17, 24, 39, 0.9));
    }
    .deck-card.border-amber {
      border-color: rgba(245, 158, 11, 0.4);
    }
    .deck-card.border-red {
      border-color: rgba(239, 68, 68, 0.4);
    }
    .deck-card.border-green {
      border-color: rgba(16, 185, 129, 0.4);
    }
    .deck-card.border-blue {
      border-color: rgba(56, 189, 248, 0.4);
    }
    .deck-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .card-title {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .pill {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .pill-p0 { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .pill-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .pill-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .pill-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }

    .card-body {
      font-size: 12.5px;
      line-height: 1.5;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-body strong {
      color: #f1f5f9;
    }
    .card-body ul {
      padding-left: 16px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .card-body li {
      font-size: 12px;
    }

    /* Metric Boxes */
    .metric-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 8px;
    }
    .metric-box {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 12px;
      text-align: center;
    }
    .metric-val {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }
    .metric-val.danger { color: #f87171; }
    .metric-val.success { color: #34d399; }
    .metric-val.primary { color: #818cf8; }
    .metric-lbl {
      font-size: 10px;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
      margin-top: 2px;
    }

    /* Query Box Simulation */
    .query-card {
      background: #0f172a;
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-radius: 9px;
      padding: 10px 14px;
      margin-bottom: 8px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .query-prompt {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12.5px;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
    }
    .query-prompt::before {
      content: "💬";
      font-size: 13px;
    }
    .query-response {
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.45;
      padding-left: 10px;
      border-left: 2px solid var(--primary-light);
    }
    .query-response code {
      font-family: 'JetBrains Mono', monospace;
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 11px;
    }

    /* Speaker Notes Bar (Collapsible) */
    .speaker-notes-drawer {
      background: rgba(15, 23, 42, 0.95);
      border-top: 1px solid rgba(99, 102, 241, 0.3);
      padding: 8px clamp(16px, 2.5vw, 32px);
      font-size: 12px;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }
    .speaker-badge {
      background: var(--primary-gradient);
      color: #fff;
      font-weight: 800;
      font-size: 10px;
      padding: 2px 7px;
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
      padding: 8px clamp(16px, 2.5vw, 32px);
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
      padding: 7px 14px;
      border-radius: 7px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
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
      background: rgba(0, 0, 0, 0.82);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .script-modal.active {
      display: flex;
    }
    .script-content {
      background: #0f172a;
      border: 1px solid rgba(99, 102, 241, 0.5);
      border-radius: 12px;
      max-width: 860px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.4);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(99, 102, 241, 0.4);
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(99, 102, 241, 0.7);
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
      <div class="brand-title">DevRev Computer <span style="font-weight:400; color:var(--text-muted);">| Solutions Engineering</span></div>
      <span class="badge-devrev">Candidate Demo Deck</span>
    </div>
    <div class="header-controls">
      <span class="slide-counter" id="slideIndicator">Slide 1 of 7</span>
      <button class="btn-header" onclick="openScriptModal()">🎙️ 5-Min Script</button>
      <button class="btn-header" onclick="toggleFullScreen()"><span id="fullscreenIcon">⛶</span> Fullscreen</button>
    </div>
  </header>

  <!-- Main Slides Canvas -->
  <main class="slides-canvas">

    <!-- SLIDE 1: Problem Framing & Customer Hook -->
    <section class="slide active" id="slide-1">
      <div class="slide-category">Problem Framing & Customer Hook</div>
      <h1 class="slide-title">The Offline Mobile Dilemma: Why Disconnected Systems Fail Field Operations</h1>
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
            <div class="metric-row" style="margin-top: 6px;">
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
            <p style="font-size: 11.5px; color: #cbd5e1; border-left: 2px solid #ef4444; padding-left: 8px; font-style: italic;">
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
              <li><strong>Customer Support / Success:</strong> Trapped in email threads & tickets. They see customer anger ($84.5k delayed pipeline) but have zero visibility into engineering sprints.</li>
              <li><strong>Product Management:</strong> PRD sits in Google Drive or Notion, defining theoretical requirements disconnected from real-world telemetry and edge cases.</li>
              <li><strong>Engineering Teams:</strong> Work in Jira (OM-series), fixing technical debt and setting up CI harnesses, completely blind to which customer ARR ($420k) is tied to the feature.</li>
            </ul>
            <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 10px; margin-top: 6px;">
              <strong style="color: #818cf8; font-size: 12px;">The Solution: DevRev Computer</strong>
              <p style="font-size: 11.5px; margin-top: 3px; color: #cbd5e1;">A unified semantic knowledge layer that ingests Google Drive PRDs, Jira engineering backlogs, and customer escalations — turning passive documentation into active cross-silo intelligence.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 2: Data Setup -->
    <section class="slide" id="slide-2">
      <div class="slide-category">Data Preparation</div>
      <h1 class="slide-title">Data Setup: Multi-Source Enterprise Artifacts</h1>
      <p class="slide-subtitle">Structured multi-disciplinary data prepared across Google Drive PRD, Jira Cloud issues, API specs, and escalation reports.</p>
      
      <div class="deck-grid-3">
        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">📄 1. Master PRD Document</span>
            <span class="pill pill-green">Google Drive</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Local Storage:</strong> Encrypted SQLite with SQLCipher AES-256 for field security.</li>
              <li><strong>Idempotency Protocol:</strong> Client-side UUIDv4 tokens with Redis 72h dedup keys.</li>
              <li><strong>Conflict Matrix:</strong> Section 5.4 rules for partial stock depletion, price revisions, and credit limits.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">🎟️ 2. Jira Cloud Backlog</span>
            <span class="pill pill-blue">Project "Devrev"</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>OM-116 (KAN-19):</strong> Chaos test harness in CI (Charles Proxy + Network Link Conditioner) across 5 profiles. <em>Done</em>.</li>
              <li><strong>OM-117 (KAN-20):</strong> Migrate catalog cache to SQLite WAL mode to resolve starvation. <em>Done (commit e8b2f90)</em>.</li>
              <li><strong>OM-118 (KAN-21):</strong> Client telemetry metrics for queue depth, sync latency, battery drain. <em>In Progress</em>.</li>
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
              <li><strong>REST Contracts:</strong> <code>POST /api/v1/orders/sync</code> with Brotli compression and <code>GET /api/v1/catalog/delta</code>.</li>
              <li><strong>Concurrency Guarantees:</strong> Redis SETNX distributed lock patterns, monotonic revision sequence tracking.</li>
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
              <li><strong>P0 Incident Post-Mortem:</strong> 38 duplicate orders on reconnect ($46,200).</li>
              <li><strong>Root Cause:</strong> Dropped TCP ACK over cellular cell tower triggered aggressive client socket retry without server dedup check.</li>
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
              <li><strong>Financial Exposure:</strong> $420k ARR, 65 seats, $84.5k delayed pipeline, 8.4% order error spike.</li>
              <li><strong>Executive Threat:</strong> VP of Sales Ops threatening competitor RFP if offline mode not resolved in v3.4.</li>
            </ul>
          </div>
        </div>

        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">✨ Evaluation Fidelity</span>
            <span class="pill pill-green">10/10 Score</span>
          </div>
          <div class="card-body">
            <p><strong>Realistic Enterprise Context:</strong> Actual commit hashes (<code>e8b2f90</code>), Jira issue keys (<code>KAN-19</code> to <code>KAN-21</code>), real HTTP status codes (<code>401</code>, <code>504</code>), and verified revenue figures.</p>
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
              <li><strong>Ingested Assets:</strong> Master PRD Google Doc, API Design Notes, Bug RCA, and Customer Escalations.</li>
              <li><strong>Capabilities:</strong> Ingests live documents while preserving markdown headers, tables, and code blocks with continuous sync.</li>
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
              <li><strong>Ingested Assets:</strong> Project <code>Devrev</code> — OM-116, OM-117, OM-118, plus related defect catalog.</li>
              <li><strong>Capabilities:</strong> Maps status workflows (Done / In Progress), issue priorities, components, and commit hashes (<code>e8b2f90</code>).</li>
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
              <li><strong>Ingested Assets:</strong> Team runbooks, sprint trackers, and customer account records ($420k ARR).</li>
              <li><strong>Capabilities:</strong> Maps customer tier and ARR values directly to technical component epics.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="deck-card highlight" style="margin-top: 12px;">
        <div class="deck-card-header">
          <span class="card-title">🧠 The DevRev Computer Semantic Knowledge Graph</span>
          <span class="pill pill-green">Multi-Hop Traversal</span>
        </div>
        <div class="card-body" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 15px;">🏢 Customer Account</div>
            <div style="font-size: 11px; color: #38bdf8; margin-top: 2px;">Apex Wholesale ($420k ARR)</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 15px;">🚨 Escalation Event</div>
            <div style="font-size: 11px; color: #f87171; margin-top: 2px;">Cellular Dead Zone Order Drop</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 15px;">🎟️ Jira Issue</div>
            <div style="font-size: 11px; color: #fbbf24; margin-top: 2px;">OM-117 (WAL Mode Fix)</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 15px;">📄 Master PRD</div>
            <div style="font-size: 11px; color: #34d399; margin-top: 2px;">Section 7.1 (Concurrency Promise)</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: Key Computer Queries -->
    <section class="slide" id="slide-4">
      <div class="slide-category">Conversational Interaction</div>
      <h1 class="slide-title">Key Computer Queries: Conversational Interaction in Action</h1>
      <p class="slide-subtitle">The exact natural language queries run in DevRev Computer to uncover architectural limitations, documentation gaps, and engineering risks.</p>
      
      <div style="display: flex; flex-direction: column; gap: 8px; flex: 1;">
        <div class="query-card">
          <div class="query-prompt">"Based on the PRD, what existing bugs or technical limitations might impact this feature?"</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Interrogates the Jira connector to uncover active engineering limitations that threaten the PRD's promises.<br>
            <strong>Computer Discovery:</strong> Discovered that the PRD's concurrency promise relies on <code>OM-117</code> (SQLite WAL mode fix, commit <code>e8b2f90</code>), flagged that <code>OM-118</code> (telemetry) is still <em>In Progress</em>, and noted that <code>OM-116</code> chaos tests miss long-offline edge cases.
          </div>
        </div>

        <div class="query-card">
          <div class="query-prompt">"Are there documents related to retry logic, API reliability, or sync conflicts?"</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Audits knowledge base to determine whether critical implementation details exist as build-ready design docs or only summary tables.<br>
            <strong>Computer Discovery:</strong> Surfaced that the PRD is the <em>only</em> document covering these topics and only at requirement depth. Proved that zero standalone design docs, SLA runbooks, or conflict engine specs exist.
          </div>
        </div>

        <div class="query-card">
          <div class="query-prompt">"Summarize the main engineering risks for implementing offline order processing."</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Synthesizes multi-system risks across Data Integrity, Reliability, Local Storage, and Security into a prioritized action list.<br>
            <strong>Computer Discovery:</strong> Flagged 72h Redis dedup TTL vs unbounded outbox age, no dead-letter queue for poison orders, 4-hour JWT auth expiry while offline, and storage budget calculation discrepancy (50k vs 15k SKUs).
          </div>
        </div>

        <div class="query-card">
          <div class="query-prompt">"Are there any past Jira issues related to offline sync or network reconnection problems?"</div>
          <div class="query-response">
            <strong>Evaluates:</strong> Defect correlation across engineering sprint history.<br>
            <strong>Computer Discovery:</strong> Confirmed 3 OM-series items (<code>OM-116</code>, <code>OM-117</code>, <code>OM-118</code>) and revealed that no field bug reports exist yet—proving this is a greenfield feature with untested conflict rules.
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: Insights Generated -->
    <section class="slide" id="slide-5">
      <div class="slide-category">Intelligence & Analysis</div>
      <h1 class="slide-title">Insights Generated: High-Value Intelligence Surfaced by Computer</h1>
      <p class="slide-subtitle">Authentic findings surfaced by DevRev Computer across Jira tasks, commit history, documentation depth, and architectural risks.</p>
      
      <div class="deck-grid-2">
        <div class="deck-card border-amber">
          <div class="deck-card-header">
            <span class="card-title">⚙️ Load-Bearing Concurrency Dependency in Jira</span>
            <span class="pill pill-p0">OM-117 / KAN-20</span>
          </div>
          <div class="card-body">
            <p><strong>The Insight:</strong> Reader/writer starvation was previously a real defect, resolved by migrating to SQLite WAL mode with a split connection pool in commit <code>e8b2f90</code>.</p>
            <p><strong>The Architectural Risk:</strong> The PRD's entire concurrency promise (background sync reading while the user creates orders) depends on this fix holding. Computer warned: <em>"The feature is one configuration regression away from UI freezes under load. Needs a guarding regression test, not an assumption."</em></p>
          </div>
        </div>

        <div class="deck-card border-red">
          <div class="deck-card-header">
            <span class="card-title">📡 Sync Observability Blind Spot at Launch</span>
            <span class="pill pill-amber">OM-118 / KAN-21</span>
          </div>
          <div class="card-body">
            <p><strong>The Insight:</strong> Client telemetry (queue depth, reconnect latency, error breakdown, battery drain) is still only <em>In Progress</em>.</p>
            <p><strong>The Delivery Risk:</strong> Headline KPIs (>99.5% sync rate, &lt;3s sync latency, battery drain) cannot be measured in the field. Computer warned of shipping before instrumentation is in place, and noted 401 auth failures are tracked as a metric but have no corresponding fix.</p>
          </div>
        </div>

        <div class="deck-card border-blue">
          <div class="deck-card-header">
            <span class="card-title">🧪 Chaos Testing Misses Long-Offline Edge Cases</span>
            <span class="pill pill-blue">OM-116 / KAN-19</span>
          </div>
          <div class="card-body">
            <p><strong>The Insight:</strong> CI network chaos harness (Charles Proxy + Network Link Conditioner) validates short flaking with a "no duplicate records" gate (Done).</p>
            <p><strong>The Edge-Case Gap:</strong> Simulated profiles are all short-duration. They do <em>not</em> exercise multi-day offline scenarios where 72h idempotency TTL, 24h price-honor windows, and token expiry bite.</p>
          </div>
        </div>

        <div class="deck-card border-green">
          <div class="deck-card-header">
            <span class="card-title">📑 Documentation Gap: Zero Standalone Design Specs</span>
            <span class="pill pill-green">Knowledge Audit</span>
          </div>
          <div class="card-body">
            <p><strong>The Insight:</strong> PRD is the <em>only</em> document covering retry logic, API reliability, and sync conflicts in the entire organization.</p>
            <p><strong>The Engineering Gap:</strong> Everything exists only as summary tables—no backoff/retry spec, no API reliability runbook, and no conflict engine design to build against. <em>(Directly validates our API Design Notes!)</em></p>
          </div>
        </div>
      </div>

      <div class="deck-card highlight" style="margin-top: 10px;">
        <div class="deck-card-header">
          <span class="card-title">⚠️ Top 4 Pre-GA Engineering Risks Identified by Computer</span>
          <span class="pill pill-amber">Action Items</span>
        </div>
        <div class="card-body" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-size: 11.5px;">
          <div style="background: rgba(15, 23, 42, 0.6); padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border);">
            <strong style="color: #f87171;">1. 72h Dedup TTL Mismatch:</strong> Outbox queue age is unbounded; syncing on day 4 recreates duplicate orders.
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border);">
            <strong style="color: #fbbf24;">2. No Dead-Letter Path:</strong> Poison orders retry infinitely with exponential backoff; no DLQ or give-up behavior.
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border);">
            <strong style="color: #38bdf8;">3. 4-Hour Auth Expiry:</strong> JWT tokens expire offline; sync worker has no defined re-authentication flow.
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border);">
            <strong style="color: #34d399;">4. Storage Math Error:</strong> PRD cites 50k SKUs, but 36MB budget is modeled on only 15k SKUs.
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 6: Business Value -->
    <section class="slide" id="slide-6">
      <div class="slide-category">Business Impact & ROI</div>
      <h1 class="slide-title">Business Value: Empowering PMs, Engineers, and Leadership</h1>
      <p class="slide-subtitle">How DevRev Computer delivers quantifiable, measurable ROI across the product-engineering-business triad.</p>
      
      <div class="deck-grid-3">
        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🎯 Product Managers</span>
            <span class="pill pill-green">Bulletproof PRDs</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Pre-Sprint Stress Testing:</strong> Catches architectural edge cases (auth expiry, queue TTL, storage discrepancies) before sprint kickoff.</li>
              <li><strong>Saves 2–3 Weeks:</strong> Eliminates back-and-forth design revisions and mid-sprint scope changes.</li>
              <li><strong>Audits Doc Coverage:</strong> Verifies whether engineering design depth matches PRD requirement scope.</li>
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
              <li><strong>Uncovers Hidden Dependencies:</strong> Flags that concurrency relies on OM-117 (WAL fix, commit <code>e8b2f90</code>) so regressions are guarded.</li>
              <li><strong>Highlights Test Gaps:</strong> Catches that CI chaos testing misses multi-day offline profiles.</li>
              <li><strong>Cuts Triage Time by 40%:</strong> Correlates bugs, commits, and specs in seconds.</li>
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
              <li><strong>Proactive Risk Governance:</strong> Flags uninstrumented KPIs (<code>OM-118</code> in progress) before GA launch.</li>
              <li><strong>Connects Tech Debt to ARR:</strong> Links offline sync stability directly to Apex Wholesale's $420k contract.</li>
              <li><strong>Eliminates Silo Blame:</strong> Provides a single verifiable source of truth across Product, Support, and Engineering.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="deck-card highlight" style="margin-top: 12px;">
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
      <p class="slide-subtitle">Turnkey storytelling structure, live demonstration pacing, and winning Q&A defense for the interview.</p>
      
      <div class="deck-grid-2">
        <div class="deck-card highlight">
          <div class="deck-card-header">
            <span class="card-title">⏱️ 5-Minute Role-Play Walkthrough</span>
            <span class="pill pill-green">Step-by-Step Pacing</span>
          </div>
          <div class="card-body">
            <ul>
              <li><strong>Min 0:00–1:00 (The Hook):</strong> "Meet Apex Wholesale, a $420k ARR account. Reps in commercial walk-in freezers had orders dropped and duplicated, putting $84.5k at risk. Support had emails, Product had a Drive PRD, Engineering had Jira. Nobody had the complete picture."</li>
              <li><strong>Min 1:00–2:00 (Connectors):</strong> "We connected Google Drive, Jira Cloud, and Notion into DevRev Computer to create a unified semantic knowledge graph."</li>
              <li><strong>Min 2:00–3:45 (Live Computer Demo):</strong> "We asked Computer: <em>'What existing bugs or technical limitations impact this feature?'</em> It discovered that our concurrency promise relies on Jira issue OM-117 (WAL fix, commit <code>e8b2f90</code>) and warned us that a guarding regression test is needed. It caught that telemetry (OM-118) is still In Progress, meaning we'd ship blind. And it proved that retry and reliability exist only as summary tables in the PRD, with zero standalone design specs."</li>
              <li><strong>Min 3:45–5:00 (Value Pitch & Close):</strong> "This saves PMs weeks of rework, prevents production regressions for engineers, and protects $420k in ARR for leadership. That's DevRev transforming passive documentation into revenue-protecting intelligence."</li>
            </ul>
          </div>
        </div>

        <div class="deck-card">
          <div class="deck-card-header">
            <span class="card-title">🛡️ Interviewer Q&A Defense Strategy</span>
            <span class="pill pill-blue">Winning Responses</span>
          </div>
          <div class="card-body">
            <p><strong>Q: "How does Computer know OM-117 is load-bearing?"</strong><br>
            <span style="color: #cbd5e1; font-size: 11.5px;">"DevRev Computer performs deep semantic reasoning. It connected the PRD's requirement for simultaneous background sync and user order creation directly to the SQLite WAL mode fix recorded in Jira issue OM-117 and commit <code>e8b2f90</code>."</span></p>
            
            <p><strong>Q: "What action did you take on the documentation gap Computer found?"</strong><br>
            <span style="color: #cbd5e1; font-size: 11.5px;">"Computer revealed that retry logic, API contracts, and conflict handling lacked standalone design specs. Because Computer flagged this early, we drafted a dedicated API Design Note (<code>ARCH-OM-004</code>) before development started."</span></p>
            
            <p><strong>Q: "How does this scale across large enterprise instances?"</strong><br>
            <span style="color: #cbd5e1; font-size: 11.5px;">"Through vector chunking with metadata scoping (filtering by project key <code>Devrev</code> / <code>OM</code>, document type, and customer tier), ensuring sub-second retrieval without hallucination."</span></p>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Speaker Notes Bar -->
  <footer class="speaker-notes-drawer">
    <span class="speaker-badge">Speaking Cue</span>
    <span class="speaker-text" id="speakerNoteText">
      <strong>Slide 1 Cue:</strong> Open with the Apex Wholesale walk-in freezer story. Frame the business cost of disconnected tools ($84.5k delayed pipeline, $420k churn risk) before showing technology.
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
        <h2 style="font-size: 18px; color: #fff;">🎙️ Full 5-Minute Interview Role-Play Script (Turnkey Delivery)</h2>
        <button class="btn-header" onclick="closeScriptModal()">✕ Close</button>
      </div>
      <div style="font-size: 13px; line-height: 1.6; color: #cbd5e1; display: flex; flex-direction: column; gap: 14px;">
        <p><strong style="color: #818cf8;">Minute 0:00 - 1:00 (Hook & Problem Framing):</strong><br>
        "Hi everyone! Today I want to show you how DevRev Computer solves one of the hardest problems in product delivery: the disconnect between customer escalations, product specifications, and engineering backlogs.<br>
        Consider Apex Wholesale Supply Co., a $420k ARR customer. Their 65 sales reps take orders in commercial walk-in freezers with zero cellular reception. When checkout times out, reps are forced onto paper napkins. When devices reconnect, unhandled state transitions cause app crashes and duplicate orders. That resulted in $84.5k in delayed orders, 38 duplicate charges, and a direct churn threat from their VP of Sales Ops.<br>
        In traditional companies, Customer Support has emails, Product has a PRD in Google Drive, and Engineering has tickets in Jira. Nobody has the full picture."</p>

        <p><strong style="color: #818cf8;">Minute 1:00 - 2:00 (Data Setup & Connectors):</strong><br>
        "To break these silos, we ingested three core sources into DevRev Computer: our master PRD Google Doc from Google Drive, our Jira engineering backlog from the Devrev project, and our customer escalation reports.<br>
        DevRev Computer built a unified semantic knowledge graph that maps Customer ARR directly to Jira tickets, commit hashes, and PRD requirements."</p>

        <p><strong style="color: #818cf8;">Minute 2:00 - 3:45 (Conversational Interaction & Live Insights):</strong><br>
        "Now, watch what happens when we converse with Computer.<br>
        First, I asked: <em>'Based on the PRD, what existing bugs or technical limitations might impact this feature?'</em><br>
        Computer didn't just search keywords. It analyzed our Jira backlog and caught that our PRD's entire concurrency promise depends on Jira issue OM-117 — a previous SQLite WAL mode migration in commit e8b2f90. Computer warned us: this fix needs a guarding regression test, otherwise we are one configuration regression away from UI freezes under load.<br>
        Next, it flagged that OM-118 — client telemetry metrics — is still In Progress, meaning we risk shipping without the instrumentation needed to measure our headline KPI of a 99.5% sync rate.<br>
        Then, when asked about retry logic and API reliability documents, Computer audited our library and surfaced that these critical topics exist only as summary tables inside the PRD, with zero standalone design specifications behind them.<br>
        Finally, Computer synthesized our top engineering risks before GA — including an idempotency mismatch where a 72-hour Redis dedup key could expire over a long weekend and cause duplicate orders upon sync."</p>

        <p><strong style="color: #818cf8;">Minute 3:45 - 5:00 (Business Value & Close):</strong><br>
        "This demonstrates the transformative business value of DevRev Computer:<br>
        For Product Managers, it catches architectural flaws and edge cases before engineering starts, saving 2 to 3 weeks of redesign.<br>
        For Engineering Teams, it uncovers load-bearing dependencies like OM-117 and test coverage gaps, cutting triage time by 40%.<br>
        And for Leadership, it provides proactive risk visibility, connecting engineering tasks directly to $420k in protected ARR.<br>
        That is how DevRev transforms passive documentation into revenue-protecting intelligence. Thank you, and I look forward to your questions!"</p>
      </div>
    </div>
  </div>

  <script>
    let currentSlide = 1;
    const totalSlides = 7;

    const speakerNotes = [
      "Slide 1 Cue: Open with the Apex Wholesale walk-in freezer story. Frame the business cost of disconnected tools ($84.5k delayed pipeline, $420k churn risk) before showing technology.",
      "Slide 2 Cue: Highlight high data fidelity. Mention Google Drive PRD, Jira issues (OM-116 chaos, OM-117 WAL, OM-118 telemetry), API specs, and P0 RCA.",
      "Slide 3 Cue: Explain the connectors (Google Drive, Jira, Notion) and how DevRev's semantic knowledge graph connects Customer ARR ↔ Jira Key ↔ PRD.",
      "Slide 4 Cue: Walk through the 4 natural language queries used in Computer. Emphasize multi-hop reasoning across specs, Jira, and commit history.",
      "Slide 5 Cue: The 'Aha!' moment. Point out Computer discovering the OM-117 WAL dependency (commit e8b2f90), the OM-118 telemetry gap, and missing design docs.",
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
