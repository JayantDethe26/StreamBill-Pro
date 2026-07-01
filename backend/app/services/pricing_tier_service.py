from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pricing_tier import PricingTier
from app.models.product import Product
from app.models.organization_member import (
    OrganizationMember
)

from app.models.user import User

from app.schemas.pricing_tier import (
    PricingTierCreate
)

from fastapi import HTTPException


async def create_pricing_tier(
    payload: PricingTierCreate,
    current_user: User,
    db: AsyncSession
):

    product_result = await db.execute(
        select(Product).where(
            Product.id == payload.product_id
        )
    )

    product = product_result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    owner_check = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == product.organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "owner"
        )
    )

    if not owner_check.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only owners can create pricing tiers"
        )

    tier = PricingTier(
        product_id=payload.product_id,
        min_units=payload.min_units,
        max_units=payload.max_units,
        price_per_unit=payload.price_per_unit
    )

    db.add(tier)

    await db.commit()
    await db.refresh(tier)

    return tier


async def get_pricing_tiers(
    product_id: str,
    db: AsyncSession
):

    result = await db.execute(
        select(PricingTier).where(
            PricingTier.product_id == product_id
        )
    )

    return result.scalars().all()