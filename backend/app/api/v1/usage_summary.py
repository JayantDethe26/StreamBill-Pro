from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.usage_summary import (
    UsageSummaryResponse
)

from app.services.billing_service import (
    get_usage_summary
)

router = APIRouter(
    prefix="/usage-summary",
    tags=["Usage Summary"]
)


@router.get(
    "/{product_id}",
    response_model=UsageSummaryResponse
)
async def usage_summary(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):

    return await get_usage_summary(
        product_id,
        db
    )