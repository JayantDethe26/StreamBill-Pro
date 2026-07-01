from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.core.config import settings

from app.models.invoice import Invoice

from datetime import datetime

from app.schemas.payment import (
    CreateOrderResponse,
    PaymentVerificationRequest,
    PaymentVerificationResponse
)

from app.services.razorpay_service import (
    create_razorpay_order,
    verify_payment_signature
)


async def create_payment_order(
    invoice_id: str,
    db: AsyncSession
):

    # Find invoice
    invoice_result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id
        )
    )

    invoice = invoice_result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    # Prevent paying an already paid invoice
    if invoice.status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    # Create Razorpay Order
    order = await create_razorpay_order(
        amount=invoice.amount,
        invoice_id=str(invoice.id)
    )

    return CreateOrderResponse(
        order_id=order["id"],
        amount=order["amount"],
        currency=order["currency"],
        key_id=settings.RAZORPAY_KEY_ID,
        invoice_id=str(invoice.id)
    )



async def verify_payment(
    payload: PaymentVerificationRequest,
    db: AsyncSession
):

    # Find Invoice
    invoice_result = await db.execute(
        select(Invoice).where(
            Invoice.id == payload.invoice_id
        )
    )

    invoice = invoice_result.scalar_one_or_none()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    # Already paid?
    if invoice.status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    # Verify Razorpay Signature
    await verify_payment_signature(
        razorpay_order_id=payload.razorpay_order_id,
        razorpay_payment_id=payload.razorpay_payment_id,
        razorpay_signature=payload.razorpay_signature
    )

    # Update Invoice
    invoice.status = "paid"

    invoice.payment_id = (
        payload.razorpay_payment_id
    )

    invoice.paid_at = datetime.utcnow()

    await db.commit()

    await db.refresh(invoice)

    return PaymentVerificationResponse(
        success=True,
        message="Payment verified successfully."
    )