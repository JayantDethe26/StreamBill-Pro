from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserRegister

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


async def create_user(
    payload: UserRegister,
    db: AsyncSession
) -> User:

    result = await db.execute(
        select(User).where(
            User.email == payload.email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError(
            "Email already registered"
        )

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(
            payload.password
        )
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    email: str,
    password: str,
    db: AsyncSession
):

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return access_token