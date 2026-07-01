from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pricing_tier import PricingTier


async def calculate_bill(
    product_id,
    total_usage: int,
    db: AsyncSession
):
    result = await db.execute(
        select(PricingTier)
        .where(
            PricingTier.product_id == product_id
        )
        .order_by(
            PricingTier.min_units
        )
    )

    tiers = result.scalars().all()

    total_cost = 0
    remaining_usage = total_usage

    for tier in tiers:

        if remaining_usage <= 0:
            break

        if tier.max_units >= 99999999:
            usage_in_this_tier = remaining_usage

        else:
            tier_capacity = (
                tier.max_units -
                tier.min_units
            )

            usage_in_this_tier = min(
                remaining_usage,
                tier_capacity
            )

        total_cost += (
            usage_in_this_tier *
            tier.price_per_unit
        )

        remaining_usage -= usage_in_this_tier

    return total_cost



from sqlalchemy import func

from app.models.product import Product
from app.models.usage_event import UsageEvent


async def get_usage_summary(
    product_id,
    db: AsyncSession
):

    product_result = await db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = product_result.scalar_one_or_none()

    if not product:
        return None

    usage_result = await db.execute(
        select(
            func.coalesce(
                func.sum(
                    UsageEvent.quantity
                ),
                0
            )
        ).where(
            UsageEvent.product_id == product_id
        )
    )

    total_usage = usage_result.scalar()

    estimated_cost = await calculate_bill(
        product_id,
        total_usage,
        db
    )

    return {
        "product_name": product.name,
        "total_usage": total_usage,
        "estimated_cost": estimated_cost
    }