from pydantic import BaseModel
import uuid


class PricingTierCreate(BaseModel):
    product_id: str
    min_units: int
    max_units: int
    price_per_unit: int


class PricingTierResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    min_units: int
    max_units: int
    price_per_unit: int

    class Config:
        from_attributes = True