from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.payment import (
    CreateOrderResponse,
    PaymentVerificationRequest,
    PaymentVerificationResponse
)

from app.services.payment_service import (
    create_payment_order,
    verify_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/create-order/{invoice_id}",
    response_model=CreateOrderResponse
)
async def create_order(
    invoice_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await create_payment_order(
        invoice_id,
        db
    )


@router.post(
    "/verify",
    response_model=PaymentVerificationResponse
)
async def verify_payment_endpoint(
    payload: PaymentVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    return await verify_payment(
        payload,
        db
    )