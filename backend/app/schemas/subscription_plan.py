from pydantic import BaseModel
import uuid


class SubscriptionPlanCreate(BaseModel):
    name: str
    price: int
    max_members: int


class SubscriptionPlanResponse(BaseModel):
    id: uuid.UUID
    name: str
    price: int
    max_members: int
    is_active: bool

    class Config:
        from_attributes = True