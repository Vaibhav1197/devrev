# Jira Engineering Backlog
## Feature: Offline Mode for Mobile Order Processing (Project Key: `OM`)

This document catalogs **18 engineering issues** (Bugs, Stories, Tasks, and Technical Debt) created for the Offline Order Processing feature. 

The backlog spans the **Mobile Client (iOS & Android)**, **Sync Engine**, **Data Storage**, and **Backend Cloud APIs**, with realistic status distributions (**Open**, **In Progress**, and **Closed**).

---

### Backlog Summary Table

| Issue Key | Type | Summary | Component | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OM-101** | `Bug` | App crashes with NullPointerException when network reconnects mid-sync | Mobile-Core | `Highest` | **In Progress** |
| **OM-102** | `Bug` | Duplicate order creation on backend when client retries without waiting for ACK | Backend-API | `Highest` | **In Progress** |
| **OM-103** | `Bug` | Main UI thread freezes (ANR) during background catalog delta sync | Mobile-Android | `High` | **Open** |
| **OM-104** | `Bug` | Sync conflict silently overwrites server price adjustments when offline order commits | Sync-Engine | `High` | **Open** |
| **OM-105** | `Bug` | SQLite database locked error (`sqlite3_busy`) when user creates order during pull | Data-Storage | `High` | **In Progress** |
| **OM-106** | `Bug` | Expired JWT auth token causes unhandled 401 and silences outbox queue indefinitely | Mobile-Core | `Medium` | **Open** |
| **OM-107** | `Bug` | Cart calculations display floating-point rounding discrepancies on offline tax calculation | Mobile-Core | `Medium` | **Closed** |
| **OM-108** | `Bug` | Inventory count drops to negative when multiple offline devices sync orders for identical SKU | Backend-API | `High` | **Open** |
| **OM-109** | `Story`| Implement exponential backoff and jitter retry logic in Mobile API sync client | Sync-Engine | `High` | **In Progress** |
| **OM-110** | `Story`| Add persistent visual connection status banner (Online, Offline, Syncing) | Mobile-Core | `Medium` | **In Progress** |
| **OM-111** | `Story`| Implement client-side UUIDv4 idempotency key generation and caching in Redis | Backend-API | `Highest` | **Closed** |
| **OM-112** | `Story`| Build "Sync Center" dashboard to view queued, synced, and conflicted orders | Mobile-Core | `Medium` | **Open** |
| **OM-113** | `Story`| Integrate Android WorkManager and iOS BGAppRefresh for background sync | Mobile-Core | `High` | **In Progress** |
| **OM-114** | `Story`| Implement SQLCipher AES-256 local database encryption with Keystore/Keychain | Data-Storage | `Highest` | **Closed** |
| **OM-115** | `Story`| Create server-side automated backorder split logic for partial inventory depletion | Backend-API | `Medium` | **Open** |
| **OM-116** | `Task` | Set up Charles Proxy and Network Link Conditioner chaos test harness in CI | DevOps | `Medium` | **Closed** |
| **OM-117** | `Tech Debt` | Migrate catalog cache schema to SQLite Write-Ahead Logging (WAL) mode | Data-Storage | `High` | **Closed** |
| **OM-118** | `Task` | Add client telemetry metrics for offline queue depth, sync latency, and battery drain | Mobile-Core | `Low` | **Open** |

---

## Detailed Issue Specifications

### OM-101: [BUG] App crashes with NullPointerException when network reconnects mid-sync
- **Issue Type:** Bug
- **Status:** `In Progress`
- **Priority:** Blocker / Highest
- **Component:** Mobile-Core / Android
- **Assignee:** Senior Android Engineer
- **Labels:** `offline`, `crash`, `network`, `android`

#### Description
When the device regains Wi-Fi or cellular connectivity while an outbox queue dispatch is initializing, the network state callback fires before the SQLite connection pool finishes initialization, causing an uncaught `NullPointerException` and immediate app termination.

#### Steps to Reproduce
1. Enable Airplane mode on mobile test device.
2. Create 3 offline orders to populate the outbox queue.
3. Disable Airplane mode while navigating to the order list screen.
4. **Result:** App crashes instantly with crash dialog.

#### Stack Trace
```text
FATAL EXCEPTION: main
Process: com.devrev.mobileapp, PID: 18429
java.lang.NullPointerException: Attempt to invoke virtual method 'void com.devrev.sync.SyncQueue.dispatch()' on a null object reference
    at com.devrev.network.NetworkReceiver.onAvailable(NetworkReceiver.kt:42)
    at android.net.ConnectivityManager$NetworkCallback.onAvailable(ConnectivityManager.java:3942)
    at android.os.Handler.handleCallback(Handler.java:938)
```

#### Expected vs Actual Behavior
- **Expected:** The network callback must verify the readiness of the connection pool via a mutex lock and queue background sync execution safely on an IO dispatcher.
- **Actual:** Direct invocation of an uninitialized singleton causes a crash.

---

### OM-102: [BUG] Duplicate order creation on backend when client retries without waiting for ACK
- **Issue Type:** Bug
- **Status:** `In Progress`
- **Priority:** Highest / Blocker
- **Component:** Backend-API / Sync-Engine
- **Assignee:** Backend Infrastructure Lead
- **Labels:** `sync`, `idempotency`, `data-integrity`, `p0`

#### Description
When cellular network latency exceeds 15,000ms, the mobile HTTP client socket times out and initiates a retry on the subsequent sync tick. If the backend received the initial request and committed the order to the database, but the outbound HTTP 201 ACK was dropped due to poor cellular reception, the retried request commits a second order with an identical line item manifest and customer ID.

#### Steps to Reproduce
1. Configure Charles Proxy with 90% packet drop and 10,000ms latency.
2. Submit an order from the mobile app.
3. Observe client-side socket timeout after 15s.
4. Mobile sync engine automatically retries payload.
5. Inspect database: Two distinct order records created with identical item totals and customer IDs.

#### Acceptance Criteria
- [ ] Mobile client must attach header `X-Idempotency-Key: <UUIDv4>` created at order capture time.
- [ ] Backend API Gateway checks Redis key `idemp:{key}` before database transaction.
- [ ] If key exists, return HTTP 200 with original saved payload instead of re-inserting.

---

### OM-103: [BUG] Main UI thread freezes (ANR) during background catalog delta sync
- **Issue Type:** Bug
- **Status:** `Open`
- **Priority:** High
- **Component:** Mobile-Android
- **Labels:** `performance`, `sqlite`, `ui`, `anr`

#### Description
On lower-end Android devices (e.g., Samsung Galaxy A14, MediaTek Dimensity 700), processing a delta catalog synchronization payload of 5,000+ updated SKU records blocks the main UI thread for 3.8 to 4.5 seconds, triggering the Android OS "Application Not Responding" (ANR) modal.

#### Technical Analysis
The JSON parsing (`Gson.fromJson`) and the subsequent SQLite batch insertion loop are executing on `Dispatchers.Default` rather than `Dispatchers.IO`, and the SQLite transaction holds an exclusive database lock without pagination.

#### Proposed Solution
1. Move parsing and inserts to a dedicated background thread pool.
2. Chunk SQL insertions into batches of 200 records using `db.beginTransactionNonExclusive()`.
3. Yield the thread between chunks using `yield()` or 10ms delays to keep the UI frame rate at 60 FPS.

---

### OM-104: [BUG] Sync conflict silently overwrites server price adjustments when offline order commits
- **Issue Type:** Bug
- **Status:** `Open`
- **Priority:** High
- **Component:** Sync-Engine
- **Labels:** `conflict-resolution`, `pricing`, `sync`

#### Description
If an item's base price was adjusted on the server from $45.00 to $50.00 while a field sales representative was working offline, syncing the offline order (calculated at the old price of $45.00) mistakenly overwrites the master catalog price table in the ERP instead of applying an offline pricing concession rule.

#### Steps to Reproduce
1. Sales rep caches catalog at 08:00 AM (SKU-8821 = $45.00).
2. Pricing Manager raises SKU-8821 to $50.00 at 09:30 AM via Web Dashboard.
3. Rep creates an offline order for 10 units of SKU-8821 at 10:15 AM ($45.00).
4. Rep reconnects to Wi-Fi at 12:00 PM; sync completes.
5. In the master database, SKU-8821's global price is corrupted back to $45.00.

#### Resolution Rule
Master catalog prices must be immutable from the mobile order endpoint. The order submission must pass the quoted price at creation time, which the server honors within a 24-hour grace window, logging the $5/unit discrepancy as `OFFLINE_PRICE_VARIANCE`.

---

### OM-105: [BUG] SQLite database locked error (`sqlite3_busy`) when user creates order during background pull
- **Issue Type:** Bug
- **Status:** `In Progress`
- **Priority:** High
- **Component:** Data-Storage
- **Labels:** `sqlite`, `concurrency`, `mobile`

#### Description
While the background worker is writing newly fetched catalog deltas, any simultaneous user action to save an order throws:
`android.database.sqlite.SQLiteDatabaseLockedException: database is locked (code 5)`

#### Root Cause
The local SQLite database was initialized with the default `DELETE` journal mode. In this mode, a write lock blocks all other read and write connections.

#### Fix
1. Enable Write-Ahead Logging: `PRAGMA journal_mode=WAL;`.
2. Configure a 5,000ms busy timeout: `PRAGMA busy_timeout = 5000;`.
3. Allocate two separate connection pools: one read-only pool for UI queries, and one serialized write queue.

---

### OM-106: [BUG] Expired JWT auth token causes unhandled 401 and silences outbox queue indefinitely
- **Issue Type:** Bug
- **Status:** `Open`
- **Priority:** Medium
- **Component:** Mobile-Core / Security
- **Labels:** `auth`, `security`, `outbox`

#### Description
When a field representative remains disconnected longer than the 4-hour JWT token expiration window, the sync worker receives an HTTP 401 response on reconnection. The worker crashes silently without triggering the OAuth refresh token flow, leaving orders stranded in the local outbox.

#### Acceptance Criteria
- [ ] HTTP network interceptor detects HTTP 401 from sync endpoints.
- [ ] Interceptor pauses queue, invokes `/oauth/token/refresh` with secure refresh token from Keystore.
- [ ] Updates in-memory authorization header and retries failed sync payload.
- [ ] If refresh token is expired, displays user-friendly prompt: *"Session expired. Please enter PIN to sync orders."*

---

### OM-107: [BUG] Cart calculations display floating-point rounding discrepancies on offline tax calculation
- **Issue Type:** Bug
- **Status:** `Closed` (Resolved in PR #284)
- **Priority:** Medium
- **Component:** Mobile-Core
- **Labels:** `cart`, `tax`, `calculations`

#### Problem & Resolution
Line item tax calculations performed on the client used standard double IEEE 754 floating-point numbers, resulting in sub-cent anomalies (e.g., `$149.99999999999997` instead of `$150.00`). Backend schema validation rejected these payloads with HTTP 422 Unprocessable Entity.
- **Fix:** Refactored pricing and tax calculation engine to use `BigDecimal` on Android and `NSDecimalNumber` on iOS with half-up rounding.

---

### OM-108: [BUG] Inventory count drops to negative when multiple offline devices sync orders for identical SKU
- **Issue Type:** Bug
- **Status:** `Open`
- **Priority:** High
- **Component:** Backend-API
- **Labels:** `inventory`, `race-condition`, `backend`

#### Description
If two sales reps each sell 5 units of an item while offline (total 10 units), but the central warehouse only had 6 units in stock, both syncs process sequentially without validation, resulting in warehouse inventory displaying `-4 units`.

#### Proposed Fix
Implement optimistic concurrency checks on warehouse stock deduction:
```sql
UPDATE inventory 
SET available_quantity = available_quantity - :requested_qty 
WHERE sku_id = :sku_id AND available_quantity >= :requested_qty;
```
If update row count is 0, trigger automated split fulfillment: allocate remaining stock to the order and assign the balance to a `BACKORDER` status.

---

### OM-109: [STORY] Implement exponential backoff and jitter retry logic in Mobile API sync client
- **Issue Type:** Story
- **Status:** `In Progress`
- **Priority:** High
- **Component:** Sync-Engine
- **Labels:** `network`, `resilience`, `sync`

#### User Story
> **As a** mobile platform engineer,  
> **I want** the sync client to employ exponential backoff with decorrelated full jitter when retrying failed network calls,  
> **So that** hundreds of reconnecting field devices do not trigger a Thundering Herd denial-of-service on our API gateway.

#### Acceptance Criteria
1. Base retry interval set to 2.0s with multiplier of 2.0 (2s, 4s, 8s, 16s, max 60s).
2. Random jitter formula applied: `sleep = rand(0, min(max_backoff, base * 2^attempt))`.
3. Stop retries immediately on non-transient 4xx errors (400, 401, 403, 422).
4. Unit tests verify backoff delay distribution across 100 simulated failures.

---

### OM-110: [STORY] Add persistent visual connection status banner (Online, Offline, Syncing)
- **Issue Type:** Story
- **Status:** `In Progress`
- **Priority:** Medium
- **Component:** Mobile-Core / UI
- **Labels:** `ui`, `ux`, `feedback`

#### User Story
> **As a** field sales representative,  
> **I want** a clear, persistent connectivity indicator at the top of the mobile screen,  
> **So that** I always know whether my orders are being processed locally or synced live with the server.

#### Acceptance Criteria
1. **Green Status Pill:** "Online" when ping roundtrip time is < 500ms.
2. **Amber Status Pill:** "Offline Mode Active" with tooltip: *"Orders saved securely on device. Auto-sync on reconnect."*
3. **Blue Animated Pill:** "Syncing (3 of 5 orders remaining)..." with live counter.
4. Indicator must be non-intrusive and never obscure cart actions or checkout buttons.

---

### OM-111: [STORY] Implement client-side UUIDv4 idempotency key generation and caching in Redis
- **Issue Type:** Story
- **Status:** `Closed` (Resolved in PR #251)
- **Priority:** Highest
- **Component:** Backend-API
- **Labels:** `idempotency`, `redis`, `backend`

#### User Story & Resolution
Implemented mandatory `X-Idempotency-Key` requirement for all `/api/v1/orders/sync` endpoints. Backend validates keys against a Redis cluster with 72-hour retention, ensuring complete deduplication of retry bursts.

---

### OM-112: [STORY] Build 'Sync Center' dashboard to view queued, synced, and conflicted orders
- **Issue Type:** Story
- **Status:** `Open`
- **Priority:** Medium
- **Component:** Mobile-Core / UI
- **Labels:** `ui`, `dashboard`, `sync`

#### Acceptance Criteria
1. Dedicated navigation drawer item: "Sync Center".
2. Three segmented tabs:
   - **Queued (Offline):** List of orders awaiting connectivity with timestamp and item count.
   - **Synced:** History of successfully uploaded orders with cloud receipt numbers.
   - **Attention Needed:** Conflicted orders (e.g., partial stockout) with manual override options.
3. Floating action button: "Sync Now" to force manual sync retry.
4. Export option: Save pending orders as an encrypted `.bak` file for emergency manual upload.

---

### OM-113: [STORY] Integrate Android WorkManager and iOS BGAppRefresh for background sync
- **Issue Type:** Story
- **Status:** `In Progress`
- **Priority:** High
- **Component:** Mobile-Core
- **Labels:** `background`, `battery`, `android`, `ios`

#### Acceptance Criteria
1. Android: Register `PeriodicWorkRequest` with `Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build()`.
2. iOS: Configure `BGAppRefreshTask` with `BGTaskScheduler.shared.register()`.
3. Battery safety constraint: Suppress heavy background sync if battery level is below 15% unless plugged into charger.
4. Execution window capped at 25 seconds to prevent OS termination.

---

### OM-114: [STORY] Implement SQLCipher AES-256 local database encryption with Keystore/Keychain
- **Issue Type:** Story
- **Status:** `Closed` (Resolved in PR #230)
- **Priority:** Highest
- **Component:** Data-Storage
- **Labels:** `security`, `compliance`, `encryption`

#### Resolution
Integrated SQLCipher 4.5. Cryptographic 256-bit database master key generated using hardware-backed SecureRandom and stored in Android Keystore / iOS Keychain. Confirmed zero raw text exposure via SQLite hex dumps.

---

### OM-115: [STORY] Create server-side automated backorder split logic for partial inventory depletion
- **Issue Type:** Story
- **Status:** `Open`
- **Priority:** Medium
- **Component:** Backend-API
- **Labels:** `inventory`, `order-processing`, `backend`

#### Acceptance Criteria
1. When `requested_qty > available_qty`, server creates:
   - Group 1: Available quantity (Status: `ALLOCATED`, ready for packing).
   - Group 2: Unfulfilled quantity (Status: `BACKORDERED`).
2. Parent order status transitions to `PARTIALLY_ALLOCATED`.
3. Automated email/SMS sent to customer detailing the split shipment schedule.

---

### OM-116: [TASK] Set up Charles Proxy and Network Link Conditioner chaos test harness in CI
- **Issue Type:** Task
- **Status:** `Closed` (Merged in `.github/workflows/network-chaos-tests.yml`)
- **Priority:** Medium
- **Component:** DevOps / QA
- **Labels:** `qa`, `testing`, `chaos`, `ci`

---

### OM-117: [TECH-DEBT] Migrate catalog cache schema to SQLite Write-Ahead Logging (WAL) mode
- **Issue Type:** Tech Debt
- **Status:** `Closed` (Merged in commit `e8b2f90`)
- **Priority:** High
- **Component:** Data-Storage
- **Labels:** `sqlite`, `performance`, `database`

---

### OM-118: [TASK] Add client telemetry metrics for offline queue depth, sync latency, and battery drain
- **Issue Type:** Task
- **Status:** `Open`
- **Priority:** Low
- **Component:** Mobile-Core / Analytics
- **Labels:** `telemetry`, `analytics`, `observability`

#### Acceptance Criteria
1. Track `offline_orders_queued_count` gauge in Datadog/OpenTelemetry.
2. Track `sync_duration_seconds` histogram from reconnect to completion.
3. Track `offline_session_duration_minutes` timer.
