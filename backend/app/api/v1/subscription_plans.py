from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.subscription_plan import (
    SubscriptionPlanCreate,
    SubscriptionPlanResponse
)

from app.services.subscription_plan_service import (
    create_plan,
    get_plans
)

router = APIRouter(
    prefix="/plans",
    tags=["Subscription Plans"]
)


@router.post(
    "",
    response_model=SubscriptionPlanResponse,
    status_code=201
)
async def create_subscription_plan(
    payload: SubscriptionPlanCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_plan(
            payload,
            db
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "",
    response_model=list[SubscriptionPlanResponse]
)
async def list_plans(
    db: AsyncSession = Depends(get_db)
):
    return await get_plans(db)