from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.usage_event import (
    UsageEventCreate,
    UsageEventResponse,
    IngestEventResponse
)

from app.services.usage_event_service import (
    ingest_event
)

router = APIRouter(
    prefix="/events",
    tags=["Usage Events"]
)


@router.post(
    "/ingest",
    ##response_model=IngestEventResponse
)
async def create_event(
    payload: UsageEventCreate,
    x_api_key: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    return await ingest_event(
        payload,
        x_api_key,
        db
    )