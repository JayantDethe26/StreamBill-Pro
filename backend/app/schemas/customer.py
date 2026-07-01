from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    external_id: str


class CustomerResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    email: EmailStr
    external_id: str

    model_config = {
        "from_attributes": True
    }