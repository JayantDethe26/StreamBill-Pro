from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.models.product import Product
from app.models.usage_event import UsageEvent

from app.schemas.usage_event import (
    UsageEventCreate
)

from app.services.api_key_service import (
    validate_api_key
)
from app.core.redis import redis_client
from app.models.customer import Customer

async def ingest_event(
    payload: UsageEventCreate,
    api_key: str,
    db: AsyncSession
):
    # Validate API Key
    api_key_record = await validate_api_key(
        api_key,
        db
    )

    organization_id = (
        api_key_record.organization_id
    )

    customer_result = await db.execute(
        select(Customer).where(
            Customer.organization_id == organization_id,
            Customer.external_id == payload.customer_id
        )
    )

    customer = customer_result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Check if event already exists (Idempotency)
    existing_event_result = await db.execute(
        select(UsageEvent).where(
            UsageEvent.event_id == payload.event_id
        )
    )

    existing_event = (
        existing_event_result.scalar_one_or_none()
    )

    if existing_event:
        return {
            "duplicate": True,
            "message": "Event already processed",
            "event": existing_event
        }

    # Find product
    product_result = await db.execute(
        select(Product).where(
            Product.organization_id == organization_id,
            Product.code == payload.product_code
        )
    )

    product = product_result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    stream_id = await redis_client.xadd(
        "usage_events_stream",
        {
            "event_id": payload.event_id,
            "organization_id": str(organization_id),
            "customer_id": str(customer.id),   # <-- ADD THIS
            "product_id": str(product.id),
            "quantity": str(payload.quantity),
            "event_type": payload.event_type
        }
    )

    return {
        "duplicate": False,
        "message": "Event pushed to Redis Stream",
        "stream_id": stream_id
    }
