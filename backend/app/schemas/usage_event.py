from pydantic import BaseModel
from uuid import UUID


class UsageEventCreate(BaseModel):
    event_id: str
    customer_id: str      # external customer id (cust_001)
    product_code: str
    quantity: int
    event_type: str


class UsageEventResponse(BaseModel):
    id: UUID
    organization_id: UUID
    product_id: UUID
    quantity: int
    event_type: str
    event_id: str

    model_config = {
        "from_attributes": True
    }


class IngestEventResponse(BaseModel):
    duplicate: bool
    message: str
    event: UsageEventResponse

    model_config = {
        "from_attributes": True
    }