from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.api_key import (
    ApiKeyCreate,
    ApiKeyCreateResponse
)

from app.services.api_key_service import (
    create_api_key
)

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"]
)


@router.post(
    "/{organization_id}",
    response_model=ApiKeyCreateResponse
)
async def generate_api_key(
    organization_id: str,
    payload: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_api_key(
        organization_id,
        payload,
        current_user,
        db
    )