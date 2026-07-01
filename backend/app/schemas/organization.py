from pydantic import BaseModel
import uuid
from pydantic import BaseModel, EmailStr



class OrganizationCreate(BaseModel):
    name: str


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str

class Config:
    from_attributes = True


class InviteMemberRequest(BaseModel):
    email: EmailStr


class InviteMemberRequest(BaseModel):
    email: EmailStr