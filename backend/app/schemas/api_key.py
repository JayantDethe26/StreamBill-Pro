from pydantic import BaseModel
import uuid


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class ApiKeyCreateResponse(BaseModel):
    id: uuid.UUID
    name: str
    api_key: str