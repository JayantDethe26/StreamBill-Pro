from pydantic import BaseModel
import uuid
from uuid import UUID


class InvoiceResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    product_id: uuid.UUID
    customer_id: UUID | None
    total_usage: int
    amount: int
    status: str

    class Config:
        from_attributes = True