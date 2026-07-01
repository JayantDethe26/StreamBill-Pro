from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.product import Product
from app.models.usage_event import UsageEvent

from app.services.billing_service import calculate_bill


async def generate_invoice(
    product_id: str,
    db: AsyncSession
):

    # Check whether product exists
    product_result = await db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = product_result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Current billing period
    current_date = datetime.utcnow()

    billing_month = current_date.month
    billing_year = current_date.year

    # Get usage grouped by customer
    usage_result = await db.execute(

        select(

            UsageEvent.customer_id,

            func.coalesce(
                func.sum(
                    UsageEvent.quantity
                ),
                0
            )

        )

        .where(
            UsageEvent.product_id == product_id
        )

        .group_by(
            UsageEvent.customer_id
        )

    )

    customer_usages = usage_result.all()

    generated_invoices = []

    for customer_id, total_usage in customer_usages:

        # Skip old usage events that don't have a customer
        if customer_id is None:
            continue

        # Prevent duplicate invoice
        existing_invoice_result = await db.execute(

            select(Invoice).where(

                Invoice.product_id == product_id,

                Invoice.customer_id == customer_id,

                Invoice.billing_month == billing_month,

                Invoice.billing_year == billing_year

            )

        )

        existing_invoice = existing_invoice_result.scalar_one_or_none()

        if existing_invoice:
            continue

        amount = await calculate_bill(
            product_id,
            total_usage,
            db
        )

        invoice = Invoice(

            organization_id=product.organization_id,

            customer_id=customer_id,

            product_id=product.id,

            billing_month=billing_month,

            billing_year=billing_year,

            total_usage=total_usage,

            amount=amount,

            status="pending"

        )

        db.add(invoice)

        generated_invoices.append(
            invoice
        )

    await db.commit()

    for invoice in generated_invoices:
        await db.refresh(invoice)

    return generated_invoices