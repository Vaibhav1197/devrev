// State management
let currentRecords = [];
let activeRecordId = null;
let searchDebounceTimer = null;

// Initialize app on load
document.addEventListener("DOMContentLoaded", () => {
  fetchStats();
  fetchRecords();

  // Close modals on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDetailModal();
      closeCreateModal();
    }
  });

  // Close modal when clicking on backdrop
  const detailModal = document.getElementById("detailModal");
  if (detailModal) {
    detailModal.addEventListener("click", (e) => {
      if (e.target === detailModal) closeDetailModal();
    });
  }

  const createModal = document.getElementById("createModal");
  if (createModal) {
    createModal.addEventListener("click", (e) => {
      if (e.target === createModal) closeCreateModal();
    });
  }
});

// Fetch KPI statistics
async function fetchStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();
    if (data.success) {
      const s = data.stats;
      document.getElementById("kpi-total").innerText = s.total;
      document.getElementById("kpi-open").innerText = s.open;
      document.getElementById("kpi-progress").innerText = s.in_progress;
      document.getElementById("kpi-p0").innerText = s.p0_blockers;
      document.getElementById("kpi-revenue").innerText = `$${s.revenue_at_risk.toLocaleString()}`;
    }
  } catch (err) {
    console.error("Error fetching stats:", err);
  }
}

// Fetch Records with filters
async function fetchRecords() {
  const search = document.getElementById("searchInput").value.trim();
  const status = document.getElementById("statusFilter").value;
  const priority = document.getElementById("priorityFilter").value;

  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (status !== "All") params.append("status", status);
  if (priority !== "All") params.append("priority", priority);

  try {
    const res = await fetch(`/api/records?${params.toString()}`);
    const data = await res.json();
    if (data.success) {
      currentRecords = data.records;
      renderTable(currentRecords);
      document.getElementById("recordCount").innerText = `Showing ${currentRecords.length} record(s)`;
    }
  } catch (err) {
    console.error("Error fetching records:", err);
    showToast("Failed to load records from backend", "error");
  }
}

// Debounced Search Handler
function debounceSearch() {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    fetchRecords();
  }, 250);
}

// Reset all search & filter dropdowns
function resetFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("statusFilter").value = "All";
  document.getElementById("priorityFilter").value = "All";
  fetchRecords();
}

// Render records into data table
function renderTable(records) {
  const tbody = document.getElementById("recordsTableBody");
  tbody.innerHTML = "";

  if (records.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
          No records found matching current filters.
        </td>
      </tr>
    `;
    return;
  }

  records.forEach((r) => {
    const tr = document.createElement("tr");

    // Format priority class
    const priorityClass = getPriorityClass(r.priority);
    const statusClass = getStatusClass(r.status);
    const sentimentClass = `sentiment-${r.ai_sentiment || 'Neutral'}`;

    tr.innerHTML = `
      <td>
        <span class="key-badge">${escapeHtml(r.ticket_key)}</span>
      </td>
      <td>
        <div class="record-summary">
          <span class="record-title-text" onclick="openDetailModal(${r.id})">${escapeHtml(r.title)}</span>
          <span class="record-customer">
            🏢 ${escapeHtml(r.customer_name)}
            <span class="tier-pill tier-${r.customer_tier}">${r.customer_tier}</span>
          </span>
        </div>
      </td>
      <td>
        <span class="pill ${priorityClass}">${escapeHtml(r.priority)}</span>
      </td>
      <td>
        <span class="status-badge ${statusClass}">${escapeHtml(r.status)}</span>
      </td>
      <td>
        <span class="font-mono ${r.impact_revenue > 0 ? 'text-green font-semibold' : 'text-muted'}">
          ${r.impact_revenue > 0 ? '$' + Number(r.impact_revenue).toLocaleString() : '$0'}
        </span>
      </td>
      <td>
        <span class="sentiment-pill ${sentimentClass}">${escapeHtml(r.ai_sentiment || 'Neutral')}</span>
      </td>
      <td style="text-align: right;">
        <div class="table-actions-cell">
          <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="openDetailModal(${r.id})">
            View
          </button>
        </div>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

// Helper class formatters
function getPriorityClass(priority) {
  if (priority.startsWith("P0")) return "priority-p0";
  if (priority.startsWith("P1")) return "priority-p1";
  if (priority.startsWith("P2")) return "priority-p2";
  return "priority-p3";
}

function getStatusClass(status) {
  if (status === "Open") return "status-open";
  if (status === "In Progress") return "status-progress";
  if (status === "Resolved") return "status-resolved";
  return "status-closed";
}

// ==================== DETAIL MODAL & AI TRIAGE ====================

async function openDetailModal(recordId) {
  activeRecordId = recordId;
  const modal = document.getElementById("detailModal");
  modal.classList.add("active");

  try {
    const res = await fetch(`/api/records/${recordId}`);
    const data = await res.json();
    if (!data.success) throw new Error(data.error);

    const r = data.record;
    document.getElementById("modalKey").innerText = r.ticket_key;
    document.getElementById("modalTitle").innerText = r.title;
    document.getElementById("modalDescription").innerText = r.description;
    document.getElementById("modalCustomer").innerText = r.customer_name;
    document.getElementById("modalCategory").innerText = r.category;
    document.getElementById("modalAssignee").innerText = r.assigned_engineer || "Unassigned";
    document.getElementById("modalRevenue").innerText = `$${Number(r.impact_revenue || 0).toLocaleString()}`;
    document.getElementById("modalCreatedAt").innerText = new Date(r.created_at).toLocaleString();

    // Tier & Priority Pills
    const tierPill = document.getElementById("modalTier");
    tierPill.innerText = r.customer_tier;
    tierPill.className = `tier-pill tier-${r.customer_tier}`;

    const priorityPill = document.getElementById("modalPriority");
    priorityPill.innerText = r.priority;
    priorityPill.className = `pill ${getPriorityClass(r.priority)}`;

    // AI Fields
    const sentimentPill = document.getElementById("modalAiSentiment");
    sentimentPill.innerText = r.ai_sentiment || "Neutral";
    sentimentPill.className = `sentiment-pill sentiment-${r.ai_sentiment || 'Neutral'}`;

    document.getElementById("modalAiSummary").innerText = r.ai_summary || "No summary generated yet.";
    document.getElementById("modalAiAction").innerText = r.ai_recommended_action || "Awaiting triage.";

    // Render Timeline
    const timeline = document.getElementById("modalTimeline");
    timeline.innerHTML = "";
    if (r.activity_logs && r.activity_logs.length > 0) {
      r.activity_logs.forEach(log => {
        const item = document.createElement("div");
        item.className = "timeline-item";
        item.innerHTML = `
          <div class="timeline-actor">👤 ${escapeHtml(log.actor)} • <span style="font-weight: 400; color: #94a3b8;">${escapeHtml(log.action)}</span></div>
          <div class="timeline-detail">${escapeHtml(log.details)}</div>
          <div class="timeline-time">${new Date(log.timestamp).toLocaleTimeString()} (${new Date(log.timestamp).toLocaleDateString()})</div>
        `;
        timeline.appendChild(item);
      });
    } else {
      timeline.innerHTML = `<span style="font-size: 12px; color: var(--text-muted);">No activity recorded yet.</span>`;
    }

  } catch (err) {
    console.error("Error opening detail:", err);
    showToast("Error loading ticket detail", "error");
  }
}

function closeDetailModal() {
  document.getElementById("detailModal").classList.remove("active");
  activeRecordId = null;
}

// Quick status update from modal buttons
async function quickUpdateStatus(newStatus) {
  if (!activeRecordId) return;

  try {
    const res = await fetch(`/api/records/${activeRecordId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        status: newStatus,
        actor: "Solutions Engineer"
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Status updated to ${newStatus}`, "success");
      openDetailModal(activeRecordId); // refresh modal view
      fetchRecords(); // refresh background table
      fetchStats();   // refresh counters
    } else {
      showToast(data.error || "Failed to update status", "error");
    }
  } catch (err) {
    console.error("Status update error:", err);
    showToast("Server error updating status", "error");
  }
}

// Trigger AI Triage
async function triggerAiTriage() {
  if (!activeRecordId) return;

  const btn = document.getElementById("runAiTriageBtn");
  const originalText = btn.innerText;
  btn.innerText = "Analyzing with AI...";
  btn.disabled = true;

  try {
    const res = await fetch(`/api/records/${activeRecordId}/ai-triage`, {
      method: "POST"
    });
    const data = await res.json();
    if (data.success) {
      showToast("✨ AI Triage Analysis Completed!", "success");
      openDetailModal(activeRecordId);
      fetchRecords();
      fetchStats();
    } else {
      showToast(data.error || "AI analysis failed", "error");
    }
  } catch (err) {
    console.error("AI triage error:", err);
    showToast("Server error during AI triage", "error");
  } finally {
    btn.innerText = originalText;
    btn.disabled = false;
  }
}

// ==================== CREATE RECORD MODAL ====================

function openCreateModal() {
  document.getElementById("createRecordForm").reset();
  document.getElementById("createModal").classList.add("active");
}

function closeCreateModal() {
  document.getElementById("createModal").classList.remove("active");
}

async function handleCreateRecord(e) {
  e.preventDefault();
  const btn = document.getElementById("submitRecordBtn");
  btn.disabled = true;
  btn.innerText = "Creating...";

  const payload = {
    title: document.getElementById("formTitle").value.trim(),
    customer_name: document.getElementById("formCustomer").value.trim(),
    customer_tier: document.getElementById("formTier").value,
    category: document.getElementById("formCategory").value,
    priority: document.getElementById("formPriority").value,
    impact_revenue: parseFloat(document.getElementById("formRevenue").value) || 0,
    assigned_engineer: document.getElementById("formAssignee").value.trim(),
    description: document.getElementById("formDescription").value.trim()
  };

  try {
    const res = await fetch("/api/records", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Record ${data.record.ticket_key} created successfully!`, "success");
      closeCreateModal();
      fetchRecords();
      fetchStats();
    } else {
      showToast(data.error || "Failed to create record", "error");
    }
  } catch (err) {
    console.error("Create record error:", err);
    showToast("Server error creating record", "error");
  } finally {
    btn.disabled = false;
    btn.innerText = "Create Record";
  }
}

// Open Walkthrough slides in new tab or popup
function openPresentationModal() {
  window.open("/presentation", "_blank");
}

// Toast Helper
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = "toast";
  const icon = type === "success" ? "✅" : type === "error" ? "❌" : "ℹ️";
  toast.innerHTML = `<span>${icon}</span> <span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(50px)";
    toast.style.transition = "all 0.3s";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Escape HTML utility
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// ==================== ROLE SWITCHER (BONUS FEATURE) ====================

async function switchUserRole(roleId) {
  try {
    const res = await fetch("/api/auth/switch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role_id: roleId })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Active User: ${data.user.name} (${data.user.role})`, "info");
    }
  } catch (err) {
    console.error("Role switch error:", err);
  }
}

// ==================== AI COPILOT DRAWER (BONUS FEATURE) ====================

function toggleCopilotDrawer() {
  const drawer = document.getElementById("copilotDrawer");
  drawer.classList.toggle("active");
  if (drawer.classList.contains("active")) {
    document.getElementById("copilotInput").focus();
  }
}

function handleCopilotKey(e) {
  if (e.key === "Enter") {
    sendCopilotMessage();
  }
}

function askCopilot(promptText) {
  document.getElementById("copilotInput").value = promptText;
  sendCopilotMessage();
}

async function sendCopilotMessage() {
  const input = document.getElementById("copilotInput");
  const prompt = input.value.trim();
  if (!prompt) return;

  const messagesContainer = document.getElementById("copilotMessages");

  // Append user message
  const userMsg = document.createElement("div");
  userMsg.className = "copilot-msg user-msg";
  userMsg.innerHTML = `<div class="msg-bubble">${escapeHtml(prompt)}</div>`;
  messagesContainer.appendChild(userMsg);
  input.value = "";
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Typing indicator
  const typingMsg = document.createElement("div");
  typingMsg.className = "copilot-msg bot-msg";
  typingMsg.id = "copilotTyping";
  typingMsg.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble" style="color: var(--text-muted); font-style: italic;">
      Analyzing live support tickets &amp; revenue context...
    </div>
  `;
  messagesContainer.appendChild(typingMsg);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const res = await fetch("/api/ai/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: prompt })
    });
    const data = await res.json();
    typingMsg.remove();

    if (data.success) {
      const botMsg = document.createElement("div");
      botMsg.className = "copilot-msg bot-msg";
      // Convert basic markdown formatting (bold, bullet points)
      let formatted = escapeHtml(data.response)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/`(.*?)`/g, "<code>$1</code>")
        .replace(/\n/g, "<br>");

      botMsg.innerHTML = `
        <div class="msg-avatar">🤖</div>
        <div class="msg-bubble">${formatted}</div>
      `;
      messagesContainer.appendChild(botMsg);
    } else {
      const errorMsg = document.createElement("div");
      errorMsg.className = "copilot-msg bot-msg";
      errorMsg.innerHTML = `
        <div class="msg-avatar">⚠️</div>
        <div class="msg-bubble" style="color: #f87171;">${escapeHtml(data.error || "Failed to analyze query")}</div>
      `;
      messagesContainer.appendChild(errorMsg);
    }
  } catch (err) {
    typingMsg.remove();
    console.error("Copilot error:", err);
    const errorMsg = document.createElement("div");
    errorMsg.className = "copilot-msg bot-msg";
    errorMsg.innerHTML = `
      <div class="msg-avatar">⚠️</div>
      <div class="msg-bubble" style="color: #f87171;">Network error contacting DevRev Copilot service.</div>
    `;
    messagesContainer.appendChild(errorMsg);
  } finally {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

