# main.py

from fastapi import FastAPI, HTTPException
from app.models import OptimizeRequest
from app.optimizer import optimize
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cleaned_errors = []

    for err in exc.errors():
        cleaned_errors.append({
            "loc": err.get("loc", []),
            "msg": str(err.get("msg")),   # ✅ force string
            "type": err.get("type")
        })

    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid request",
            "details": cleaned_errors
        },
    )

@app.post("/api/v1/load-optimizer/optimize")
def optimize_load(req: OptimizeRequest):
    result = optimize(req.truck, req.orders)

    if not result:
        return {
            "truck_id": req.truck.id,
            "selected_order_ids": [],
            "total_payout_cents": 0
        }

    total_weight = sum(o.weight_lbs for o in result)
    total_volume = sum(o.volume_cuft for o in result)
    total_payout = sum(o.payout_cents for o in result)

    return {
        "truck_id": req.truck.id,
        "selected_order_ids": [o.id for o in result],
        "total_payout_cents": total_payout,
        "total_weight_lbs": total_weight,
        "total_volume_cuft": total_volume,
        "utilization_weight_percent": (total_weight / req.truck.max_weight_lbs) * 100,
        "utilization_volume_percent": (total_volume / req.truck.max_volume_cuft) * 100,
    }