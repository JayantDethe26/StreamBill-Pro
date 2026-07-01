from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.pricing_tier import (
    PricingTierCreate,
    PricingTierResponse
)

from app.services.pricing_tier_service import (
    create_pricing_tier,
    get_pricing_tiers
)

router = APIRouter(
    prefix="/pricing-tiers",
    tags=["Pricing Tiers"]
)


@router.post(
    "",
    response_model=PricingTierResponse,
    status_code=201
)
async def create_tier(
    payload: PricingTierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_pricing_tier(
        payload,
        current_user,
        db
    )


@router.get(
    "/{product_id}",
    response_model=list[PricingTierResponse]
)
async def list_tiers(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_pricing_tiers(
        product_id,
        db
    )