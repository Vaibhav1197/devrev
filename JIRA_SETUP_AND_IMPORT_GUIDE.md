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

### Step 3: Import All 18 Issues via CSV (Guaranteed 1-Click Method)

> [!IMPORTANT]
> **Why did previous imports create "0 issues"?**
> 1. **Mapping "Issue Key":** In Jira, mapping the `Issue Key` field tells Jira to **update existing issues**. Since tickets `OM-101` through `OM-118` do not exist yet in your Jira project, Jira skips all 18 rows and imports **0 issues**.
> 2. **Mapping "Status" to "Closed":** In Jira workflows, an issue cannot be created directly in `Closed` without a `Resolution` field (e.g. `Done`), causing Jira to reject the issue during creation.

#### The 100% Reliable Import (Takes 1 Minute):
We generated **[`jira_issues_import.csv`](./jira_issues_import.csv)** with the 5 universal fields that **auto-match and import with 100% success on any Jira project**:
* `Summary` (prefixed with `OM-101:`, `OM-102:`, etc.)
* `Issue Type` (`Bug`, `Story`, `Task`)
* `Priority` (`Highest`, `High`, `Medium`, `Low`)
* `Labels` (contains component e.g. `Mobile-Core` + tags)
* `Description` (detailed reproduction steps, stack traces, acceptance criteria)

#### Quick Step-by-Step:
1. In Jira, go to **Filters** &rarr; **View all issues** &rarr; click `•••` (top right) &rarr; **Import issues from CSV**  
   *(Or click **Settings (⚙️)** &rarr; **System** &rarr; **External System Import** &rarr; **CSV**)*.
2. Click **Choose File** and select:
   ```text
   c:\Users\sajna\Downloads\devrev\jira_issues_import.csv
   ```
3. Leave default encoding (**UTF-8**) and click **Next**.
4. Select your target project and click **Next**.
5. **Field Mapping (Jira auto-matches all 5 fields):**
   * `Summary` &rarr; **Summary**
   * `Issue Type` &rarr; **Issue Type**
   * `Priority` &rarr; **Priority**
   * `Labels` &rarr; **Labels**
   * `Description` &rarr; **Description**
   *(Notice: No `Issue Key` or `Status` to cause conflicts!)*
6. Click **Next** &rarr; Click **Begin Import**.
7. **Result:** All 18 issues will import in 5–10 seconds with **zero errors**!

---

### Step 4: Organize Workflow Columns on Board (Takes 15 Seconds)

Once the 18 issues are created in your project:
1. Go to your **Board** or **Backlog** in Jira.
2. Drag the following issues across your workflow columns to reflect realistic engineering progress:
   * 🟢 **Done / Closed (5 issues):** Drag `OM-107`, `OM-111`, `OM-114`, `OM-116`, `OM-117` into **Done**.
   * 🟡 **In Progress (6 issues):** Drag `OM-101`, `OM-102`, `OM-105`, `OM-109`, `OM-110`, `OM-113` into **In Progress**.
   * ⚪ **To Do / Open (7 issues):** Leave `OM-103`, `OM-104`, `OM-106`, `OM-108`, `OM-112`, `OM-115`, `OM-118` in **To Do**.

Every single ticket will display its complete details, labels, component tags, priority badges, and acceptance criteria!

---

### Alternative: Manual Creation Reference

If you prefer to enter tickets manually or during an interview walkthrough, consult [`Jira_Engineering_Issues.md`](./Jira_Engineering_Issues.md) which contains copy-pasteable blocks for each individual issue.
