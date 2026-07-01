from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.models.product import Product
from app.models.organization_member import (
    OrganizationMember
)

from app.models.user import User

from app.schemas.product import (
    ProductCreate
)


async def create_product(
    payload: ProductCreate,
    current_user: User,
    db: AsyncSession
):
    owner_check = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == payload.organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "owner"
        )
    )

    if not owner_check.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only owners can create products"
        )

    existing = await db.execute(
        select(Product).where(
            Product.code == payload.code
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Product code already exists"
        )

    product = Product(
        organization_id=payload.organization_id,
        name=payload.name,
        code=payload.code
    )

    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


async def get_products(
    db: AsyncSession
):
    result = await db.execute(
        select(Product)
    )

    return result.scalars().all()