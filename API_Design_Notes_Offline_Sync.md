# Technical Design Notes: Offline Order Sync & Delta API Specification
**Document ID:** `ARCH-2026-OM-004`  
**Author:** Lead Systems Architect & Mobile Infrastructure Lead  
**Feature:** Offline Mode for Mobile Order Processing (`OM`)  
**Status:** `Approved for Implementation`  
**Target Release:** Mobile App v3.4 & Backend Sync Gateway v2.8  

---

## 1. Architectural Overview & Design Principles

The Offline Sync API is designed around three foundational distributed systems principles:
1. **At-Least-Once Delivery with Idempotency:** The mobile client is untrusted in its network reliability. Requests will be retried multiple times over flaky connections. The backend guarantees that processing an order payload $N$ times has the exact same state mutation as processing it once.
2. **Delta-Only Differential Sync:** Full catalog payloads exceed 35MB. The synchronization mechanism must support incremental chunked differential streaming using monotonic revision numbers.
3. **Partition-Tolerant Conflict Handling:** When network partitions occur, the client must never be blocked. Discrepancies (inventory shortages, price updates) are resolved via deterministic multi-status batch responses.

```
┌─────────────────┐                                      ┌─────────────────┐
│  Mobile Client  │                                      │  Cloud Gateway  │
└────────┬────────┘                                      └────────┬────────┘
         │                                                        │
         │ 1. POST /api/v1/orders/sync                            │
         │    [Header: X-Idempotency-Key: UUIDv4]                 │
         ├───────────────────────────────────────────────────────►│
         │                                                        │ 2. Check Redis
         │                                                        │    SETNX(key, PENDING)
         │                                                        │
         │                                                        │ 3. Database Transaction
         │                                                        │    - Insert Order
         │                                                        │    - Deduct Inventory
         │                                                        │    - Set Redis(key, ACK)
         │ 4. HTTP 201 Created (Order Acknowledged)               │
         │◄───────────────────────────────────────────────────────┤
         │                                                        │
```

---

## 2. API Endpoint Specifications

### 2.1 Batch Order Synchronization Endpoint

Submit queued offline orders once cellular or Wi-Fi connectivity is detected.

- **HTTP Method:** `POST`
- **Route:** `/api/v1/orders/sync`
- **Content-Type:** `application/json`
- **Content-Encoding:** `gzip` (supported and recommended)

#### Mandatory Headers

| Header Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `Authorization` | `String` | Bearer JWT access token | `Bearer eyJhbGciOi...` |
| `X-Idempotency-Key`| `UUIDv4` | Unique client-generated token for this batch | `7c9e6679-7425-40de-944b-e07fc1f90ae7` |
| `X-Client-Timestamp`| `ISO-8601`| Client wall-clock time when sync was triggered | `2026-10-06T08:14:02Z` |
| `X-Device-ID` | `String` | Hardware-backed UUID of mobile device | `dev-a82f-410c` |
| `X-App-Version` | `SemVer` | Mobile application release version | `3.4.0-build.812` |

#### Request Payload Schema

```json
{
  "batch_id": "batch_7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "sync_attempt": 1,
  "orders": [
    {
      "client_order_id": "ord_550e8400-e29b-41d4-a716-446655440000",
      "customer_id": "cust_enterprise_88291",
      "created_at_client": "2026-10-06T07:42:15Z",
      "sales_rep_id": "usr_alex_rivera",
      "payment_terms": "NET_30",
      "currency": "USD",
      "line_items": [
        {
          "sku": "SKU-BEV-0012",
          "quantity": 24,
          "unit_price_quoted": 14.50,
          "discount_rate": 0.05,
          "line_total": 330.60
        },
        {
          "sku": "SKU-SNK-4081",
          "quantity": 10,
          "unit_price_quoted": 8.00,
          "discount_rate": 0.00,
          "line_total": 80.00
        }
      ],
      "pricing_summary": {
        "subtotal": 410.60,
        "tax_total": 33.87,
        "grand_total": 444.47
      },
      "signature": {
        "captured": true,
        "signer_name": "Dave Miller",
        "hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      }
    }
  ]
}
```

#### Response Payloads

##### Scenario A: Clean Ingestion (HTTP 201 Created)
```json
{
  "status": "SUCCESS",
  "batch_id": "batch_7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "processed_at": "2026-10-06T08:14:03.112Z",
  "results": [
    {
      "client_order_id": "ord_550e8400-e29b-41d4-a716-446655440000",
      "server_order_id": "ORD-2026-904812",
      "status": "CONFIRMED",
      "fulfillment_status": "READY_FOR_PICKING",
      "adjustments": []
    }
  ]
}
```

##### Scenario B: Duplicate Retry Detected (HTTP 200 OK)
Returned when the client re-submits an idempotency key that already completed successfully.
```json
{
  "status": "IDEMPOTENT_REPLAY",
  "batch_id": "batch_7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "original_processed_at": "2026-10-06T08:14:03.112Z",
  "message": "Transaction already committed. Replaying original acknowledgment without state mutation.",
  "results": [
    {
      "client_order_id": "ord_550e8400-e29b-41d4-a716-446655440000",
      "server_order_id": "ORD-2026-904812",
      "status": "CONFIRMED"
    }
  ]
}
```

##### Scenario C: Partial Inventory Depletion / Backorder (HTTP 207 Multi-Status)
```json
{
  "status": "PARTIALLY_FULFILLED",
  "batch_id": "batch_7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "results": [
    {
      "client_order_id": "ord_550e8400-e29b-41d4-a716-446655440000",
      "server_order_id": "ORD-2026-904812",
      "status": "SPLIT_FULFILLMENT",
      "adjustments": [
        {
          "sku": "SKU-BEV-0012",
          "code": "STOCK_SHORTAGE_AUTO_BACKORDER",
          "allocated_quantity": 18,
          "backordered_quantity": 6,
          "estimated_backorder_dispatch": "2026-10-09T00:00:00Z"
        }
      ]
    }
  ]
}
```

---

### 2.2 Catalog Delta Synchronization Endpoint

Pulls only modified or deleted SKUs since the mobile device's last synced revision number.

- **HTTP Method:** `GET`
- **Route:** `/api/v1/catalog/delta`

#### Query Parameters
- `since_revision` *(integer, required)*: Monotonically increasing revision sequence (e.g. `104829`).
- `category_filter` *(string, optional)*: Specific product line.
- `page_size` *(integer, optional, default: 1000, max: 2500)*: Batch limit for client memory preservation.

#### Response Payload (HTTP 200 OK)
```json
{
  "current_server_revision": 105140,
  "has_more": false,
  "changes_count": 2,
  "deltas": [
    {
      "operation": "UPSERT",
      "sku": "SKU-BEV-0012",
      "revision_id": 105002,
      "name": "Sparkling Mineral Water 500ml",
      "base_price": 14.50,
      "tax_category": "STANDARD_FOOD",
      "available_stock": 240,
      "updated_at": "2026-10-06T06:12:00Z"
    },
    {
      "operation": "DELETE",
      "sku": "SKU-OLD-9999",
      "revision_id": 105140,
      "reason": "DISCONTINUED",
      "updated_at": "2026-10-06T07:00:00Z"
    }
  ]
}
```

---

## 3. Distributed Idempotency Mechanism

### Redis Atomicity Implementation
To prevent race conditions during concurrent retry bursts, the backend uses a Redis Lua script for distributed locking:

```lua
-- KEYS[1]: idemp:<UUID>
-- ARGV[1]: expiry_seconds (e.g. 259200 for 72 hours)
-- ARGV[2]: request_hash
local state = redis.call('GET', KEYS[1])
if state == false then
  -- Key does not exist; acquire lock and flag as IN_FLIGHT
  redis.call('SET', KEYS[1], 'IN_FLIGHT:' .. ARGV[2], 'EX', ARGV[1])
  return 'ACQUIRED'
elseif string.sub(state, 1, 9) == 'IN_FLIGHT' then
  -- Previous request still being processed
  return 'LOCKED'
else
  -- Already processed; return cached response body
  return state
end
```

---

## 4. Error Codes & Client Handling Matrix

| HTTP Status | Error Code | Root Cause | Client Action |
| :--- | :--- | :--- | :--- |
| `400 Bad Request` | `INVALID_SCHEMA` | Malformed line item or missing UUID | Reject order; move to `DEAD_LETTER` outbox queue; notify user. |
| `401 Unauthorized` | `TOKEN_EXPIRED` | JWT lifetime expired | Pause outbox queue; trigger silent refresh token flow; resume upon success. |
| `409 Conflict` | `FATAL_RULE_VIOLATION` | Customer account permanently terminated | Flag order in "Sync Center" as `NEEDS_REVIEW`; block automated retry. |
| `429 Too Many Requests` | `RATE_LIMIT_EXCEEDED` | Throttled by API gateway | Read `Retry-After` header; apply decorrelated jitter backoff. |
| `502 / 503 / 504` | `SERVER_UNAVAILABLE` | Cloud infrastructure outage | Keep order in local outbox; retry during next scheduled network tick. |

---

## 5. Security & Transport Requirements
1. **mTLS / TLS 1.3:** All communication must be encrypted via TLS 1.3 with strict Certificate Pinning configured in the mobile application binary.
2. **Payload Verification:** Orders with customer signatures must include an SHA-256 HMAC generated using the client session key to guarantee non-repudiation.
3. **Data at Rest:** Client-side local payload queue must remain fully encrypted via SQLCipher until decrypted in-memory immediately prior to socket transmission.
