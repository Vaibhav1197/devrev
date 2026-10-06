# Jira Cloud Trial Setup & 1-Click CSV Import Guide

This guide walks you through setting up a **free Jira Cloud trial account**, creating the project, and importing all 18 engineering issues in under 3 minutes using the provided [`jira_issues_import.csv`](./jira_issues_import.csv) file.

---

### Step 1: Sign Up for a Free Jira Cloud Account

1. Go to **[https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free)**.
2. Click **"Get it free"** under Jira (Free for up to 10 users, no credit card required).
3. Sign in with your Google account, Apple ID, or work email.
4. Set your site name (e.g., `yourname-devrev.atlassian.net`) and click **Agree and sign up**.

---

### Step 2: Create Your Trial Project

1. When Jira prompts you to create your first project, select:
   - **Template:** **Scrum** or **Kanban** (Software Development)
   - **Project Type:** **Team-managed** or **Company-managed** (either works great)
2. Enter the project details:
   - **Project Name:** `Offline Mobile Order Processing`
   - **Project Key:** `OM`
3. Click **Create Project**.

---

### Step 3: Import All 18 Issues via CSV (1-Click Method)

We provide two pre-validated CSV files:
1. **[`jira_issues_import.csv`](./jira_issues_import.csv)**: Standard format matching the challenge specifications (`Open`, `In Progress`, `Closed`).
2. **[`jira_issues_import_scrum_kanban.csv`](./jira_issues_import_scrum_kanban.csv)**: Agile board format (`To Do`, `In Progress`, `Done`) which **auto-matches 100% of values with zero manual mapping** on default Scrum/Kanban boards.

#### Import Steps:
1. In your Jira dashboard, click the **Settings (gear icon ⚙️)** in the top right, then select **System**.  
   *(Alternative shortcut: Click **Filters** &rarr; **View all issues** &rarr; Click the `•••` top right &rarr; **Import issues from CSV**)*.
2. Under the **IMPORT AND EXPORT** section on the left sidebar, click **External System Import**.
3. Select **CSV**.
4. Click **Choose File** and select either:
   - `c:\Users\sajna\Downloads\devrev\jira_issues_import.csv` (Standard)
   - `c:\Users\sajna\Downloads\devrev\jira_issues_import_scrum_kanban.csv` (Zero-Config Agile)
5. Leave the default encoding (**UTF-8**) and click **Next**.
6. **Project Mapping:**
   - Select your project: `Offline Mobile Order Processing` (or whatever your project is named).
   - Click **Next**.
7. **Field Mapping (Auto-matched by Jira):**
   - `Issue Key` &rarr;
     - *If your project key is `OM`:* Map to **Issue Key**.
     - *If your project key is different (e.g., `DEV`, `SCRUM`):* Leave **unmapped** (Jira will generate project keys, and each issue's title already starts with `OM-101:`, `OM-102:`, etc.).
   - `Summary` &rarr; **Summary**
   - `Issue Type` &rarr; **Issue Type**
   - `Status` &rarr; **Status**
   - `Priority` &rarr; **Priority**
   - `Component/s` &rarr; **Component/s**
   - `Labels` &rarr; **Labels**
   - `Description` &rarr; **Description**
8. **Value Mapping (Click Next):**
   - For `jira_issues_import.csv`:
     - `Open` &rarr; Select **To Do** (or **Open**)
     - `In Progress` &rarr; Select **In Progress**
     - `Closed` &rarr; Select **Done** (or **Closed**)
   - For `jira_issues_import_scrum_kanban.csv`:
     - Jira automatically recognizes `To Do`, `In Progress`, and `Done` without needing manual selection.
9. Click **Begin Import**. All 18 tickets will be imported in 5–10 seconds!

---

### Step 4: Verify Your Jira Board

Once the import completes (usually takes 5–10 seconds):
1. Navigate back to your **Board** or **Backlog** in Jira.
2. You will see 18 issues cleanly organized across the workflow columns:
   - 🟢 **Closed / Done (5 issues):** Foundation architecture, idempotency keys, SQLCipher encryption, and WAL mode.
   - 🟡 **In Progress (6 issues):** Reconnect crash, duplicate order fix, exponential retry logic, and background sync worker.
   - ⚪ **Open / To Do (7 issues):** ANR prevention on low-end devices, sync dashboard UI, and negative inventory resolution.
3. Every issue has complete descriptions, steps to reproduce, code snippets, stack traces, and acceptance criteria!

---

### Alternative: Manual Creation Reference

If you prefer to enter tickets manually or during an interview walkthrough, consult [`Jira_Engineering_Issues.md`](./Jira_Engineering_Issues.md) which contains copy-pasteable blocks for each individual issue.
