# Google Drive Upload & Artifact Organization Guide

This guide explains how to upload and organize your **3 Supporting Documents** (plus the PRD) in Google Drive to create a professional, real-world project artifact repository.

---

### Artifacts Created in Your Workspace

| File Name | Document Type | Purpose / Description |
| :--- | :--- | :--- |
| **[`API_Design_Notes_Offline_Sync.md`](./API_Design_Notes_Offline_Sync.md)** | **API Design Notes** | Detailed engineering contracts for `POST /api/v1/orders/sync` and `GET /api/v1/catalog/delta`, including headers, idempotency keys, payloads, and Redis locking. |
| **[`Bug_Investigation_Summary_OM102.md`](./Bug_Investigation_Summary_OM102.md)** | **Bug Investigation / RCA** | Real-world P0 Root Cause Analysis for duplicate orders on network reconnect (`OM-102` / `INC-49201`), covering the 5 Whys, code diffs, and remediation. |
| **[`Customer_Escalation_Report_ApexWholesale.md`](./Customer_Escalation_Report_ApexWholesale.md)** | **Customer Escalation Report** | Executive incident report from a Tier-1 enterprise account ($420k ARR) facing field failures in cellular dead zones, motivating the Offline Mode feature. |
| **[`PRD_Offline_Mode_Mobile_Order_Processing.md`](./PRD_Offline_Mode_Mobile_Order_Processing.md)** | **Product Requirement Document** | The comprehensive master PRD detailing problem statement, user workflows, metrics, and technical architecture. |

---

### Step-by-Step Google Drive Upload Instructions

#### Step 1: Create a Dedicated Folder in Google Drive
1. Open **[Google Drive](https://drive.google.com)**.
2. Click the **"+ New"** button in the top-left corner &rarr; select **"New folder"**.
3. Name the folder: `DevRev - Offline Mode Project Artifacts`.
4. Double-click to open the newly created folder.

#### Step 2: Upload the Files
1. Drag and drop the following files directly from your computer into the Google Drive window:
   - `c:\Users\sajna\Downloads\devrev\API_Design_Notes_Offline_Sync.md`
   - `c:\Users\sajna\Downloads\devrev\Bug_Investigation_Summary_OM102.md`
   - `c:\Users\sajna\Downloads\devrev\Customer_Escalation_Report_ApexWholesale.md`
   - `c:\Users\sajna\Downloads\devrev\PRD_Offline_Mode_Mobile_Order_Processing.md`
2. *(Alternative: Click **"+ New"** &rarr; **"File upload"** &rarr; select all files).*

#### Step 3: Convert to Google Docs (Optional, for Rich Editing & Comments)
1. Right-click any uploaded `.md` file in Google Drive.
2. Select **"Open with"** &rarr; **"Google Docs"**.
3. Google Docs will automatically convert the markdown headers, bullet points, and tables into native Google Docs formatting.

#### Step 4: Configure Sharing Permissions
1. Click the folder name at the top (`DevRev - Offline Mode Project Artifacts`) &rarr; click **"Share"** &rarr; **"Share"**.
2. Under **General access**, change from *Restricted* to **"Anyone with the link"** (Role: **Viewer** or **Commenter**).
3. Click **"Copy link"** — you can now paste this link in your evaluation or submission!
