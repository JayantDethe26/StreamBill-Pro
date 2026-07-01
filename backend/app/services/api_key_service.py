import secrets
import hashlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import ApiKey
from app.models.organization_member import (
    OrganizationMember
)

from app.models.user import User
from app.schemas.api_key import ApiKeyCreate

from fastapi import HTTPException


def hash_api_key(
    api_key: str
) -> str:
    return hashlib.sha256(
        api_key.encode()
    ).hexdigest()


async def create_api_key(
    organization_id: str,
    payload: ApiKeyCreate,
    current_user: User,
    db: AsyncSession
):
    owner_check = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "owner"
        )
    )

    if not owner_check.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only owners can create API keys"
        )

    raw_key = (
        "sk_live_" +
        secrets.token_hex(24)
    )

    api_key = ApiKey(
        organization_id=organization_id,
        key_hash=hash_api_key(raw_key),
        name=payload.name
    )

    db.add(api_key)

    await db.commit()
    await db.refresh(api_key)

    return {
        "id": api_key.id,
        "name": api_key.name,
        "api_key": raw_key
    }



async def validate_api_key(
    api_key: str,
    db: AsyncSession
):
    key_hash = hashlib.sha256(
        api_key.encode()
    ).hexdigest()

    result = await db.execute(
        select(ApiKey).where(
            ApiKey.key_hash == key_hash
        )
    )

    api_key_record = result.scalar_one_or_none()

    if not api_key_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return api_key_record