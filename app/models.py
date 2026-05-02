from pydantic import BaseModel, field_validator
from typing import List
from datetime import date

class Truck(BaseModel):
    id: str
    max_weight_lbs: int
    max_volume_cuft: int

    @field_validator("max_weight_lbs", "max_volume_cuft")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("must be greater than 0")
        return v


class Order(BaseModel):
    id: str
    payout_cents: int
    weight_lbs: int
    volume_cuft: int
    origin: str
    destination: str
    pickup_date: date
    delivery_date: date
    is_hazmat: bool

    @field_validator("payout_cents")
    def payout_non_negative(cls, v):
        if v < 0:
            raise ValueError("payout must be >= 0")
        return v

    @field_validator("weight_lbs", "volume_cuft")
    def positive_values(cls, v):
        if v <= 0:
            raise ValueError("must be > 0")
        return v

    @field_validator("origin", "destination")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("cannot be empty")
        return v

    @field_validator("delivery_date")
    def check_dates(cls, delivery_date, info):
        pickup_date = info.data.get("pickup_date")
        if pickup_date and delivery_date < pickup_date:
            raise ValueError("delivery_date must be >= pickup_date")
        return delivery_date


class OptimizeRequest(BaseModel):
    truck: Truck
    orders: List[Order]

    @field_validator("orders")
    def validate_orders(cls, orders):
        if len(orders) > 22:
            raise ValueError("maximum 22 orders allowed")

        ids = [o.id for o in orders]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate order IDs found")

        return orders