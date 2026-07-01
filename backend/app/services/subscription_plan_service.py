from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subscription_plan import SubscriptionPlan

from app.schemas.subscription_plan import (
    SubscriptionPlanCreate
)


async def create_plan(
    payload: SubscriptionPlanCreate,
    db: AsyncSession
):
    existing_plan = await db.execute(
        select(SubscriptionPlan).where(
            SubscriptionPlan.name == payload.name
        )
    )

    if existing_plan.scalar_one_or_none():
        raise ValueError(
            "Plan already exists"
        )

    plan = SubscriptionPlan(
        name=payload.name,
        price=payload.price,
        max_members=payload.max_members
    )

    db.add(plan)

    await db.commit()
    await db.refresh(plan)

    return plan


async def get_plans(
    db: AsyncSession
):
    result = await db.execute(
        select(SubscriptionPlan)
    )

    return result.scalars().all()