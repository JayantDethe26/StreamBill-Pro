from pydantic import BaseModel
import uuid


class ProductCreate(BaseModel):
    organization_id: str
    name: str
    code: str


class ProductResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    code: str

    class Config:
        from_attributes = True