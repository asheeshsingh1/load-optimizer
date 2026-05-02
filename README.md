# 🚛 SmartLoad Optimization API

A high-performance backend service that selects the optimal combination of shipment orders for a truck, maximizing revenue while respecting operational constraints.

---

## 🧠 Problem Overview

Given:

* A truck with **weight and volume capacity**
* A list of shipment orders

The system determines the **best subset of orders** such that:

* ✅ Total weight ≤ truck capacity
* ✅ Total volume ≤ truck capacity
* ✅ Orders are route-compatible (same origin & destination)
* ✅ No hazmat conflicts
* ✅ Pickup & delivery constraints are valid
* 💰 **Total payout is maximized**

---

## 🚀 Tech Stack

* Python 3.11
* FastAPI
* Uvicorn
* Pydantic (v2)

---

## 📦 Project Structure

```
app/
 ├── main.py          # FastAPI entry point
 ├── models.py        # Request/response validation
 ├── optimizer.py     # Core optimization logic
 └── __init__.py
```

---

## ▶️ How to Run (Docker)

```bash
git clone https://github.com/asheeshsingh1/load-optimizer.git
cd load-optimizer

docker build -t load-optimizer .
docker run -p 8080:8080 load-optimizer
```

👉 Service will be available at:

```
http://localhost:8080
```

---

## ▶️ How to Run (Local)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

---

## 🔍 Health Check

```bash
curl http://localhost:8080/docs
```

👉 Swagger UI available for testing APIs

---

## 📡 API Endpoint

### POST `/api/v1/load-optimizer/optimize`

---

### 📥 Sample Request

```bash
curl -X POST http://localhost:8080/api/v1/load-optimizer/optimize \
-H "Content-Type: application/json" \
-d '{
  "truck": {
    "id": "truck-123",
    "max_weight_lbs": 44000,
    "max_volume_cuft": 3000
  },
  "orders": [
    {
      "id": "ord-001",
      "payout_cents": 250000,
      "weight_lbs": 18000,
      "volume_cuft": 1200,
      "origin": "Los Angeles, CA",
      "destination": "Dallas, TX",
      "pickup_date": "2025-12-05",
      "delivery_date": "2025-12-09",
      "is_hazmat": false
    },
    {
      "id": "ord-002",
      "payout_cents": 180000,
      "weight_lbs": 12000,
      "volume_cuft": 900,
      "origin": "Los Angeles, CA",
      "destination": "Dallas, TX",
      "pickup_date": "2025-12-04",
      "delivery_date": "2025-12-10",
      "is_hazmat": false
    }
  ]
}'
```

---

### 📤 Sample Response

```json
{
  "truck_id": "truck-123",
  "selected_order_ids": ["ord-001", "ord-002"],
  "total_payout_cents": 430000,
  "total_weight_lbs": 30000,
  "total_volume_cuft": 2100,
  "utilization_weight_percent": 68.18,
  "utilization_volume_percent": 70.0
}
```

---

## ⚠️ Error Handling

* `400 Bad Request` → Invalid input
* `200 OK` → Successful optimization

Example:

```json
{
  "error": "Invalid request",
  "details": [
    "body.truck.max_weight_lbs: must be greater than 0"
  ]
}
```

---

## ⚙️ Algorithm

* Uses **Bitmask Enumeration (2^n subsets)**
* Efficient for n ≤ 22
* Filters:

  * Weight constraint
  * Volume constraint
  * Route compatibility
  * Hazmat constraint

---

## 🧪 Edge Cases Handled

* Empty order list
* No valid combination
* Duplicate order IDs
* Invalid dates
* Invalid numeric inputs

---

## 🚀 Future Improvements

* Dynamic Programming (memoization)
* Backtracking with pruning
* Pareto-optimal solutions (revenue vs utilization)
* Caching frequent requests
* Rate limiting

---

## 🐳 Docker Notes

* Runs on port **8080**
* Stateless (no DB used)
* Lightweight image (Python slim)

---

## 👨‍💻 Author

Asheesh Singh

---
