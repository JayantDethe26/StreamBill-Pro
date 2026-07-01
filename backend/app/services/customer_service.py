from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.models.customer import Customer
from app.models.organization_member import OrganizationMember
from app.models.user import User

from app.schemas.customer import CustomerCreate


async def create_customer(
    organization_id: str,
    payload: CustomerCreate,
    current_user: User,
    db: AsyncSession
):

    owner_check = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "owner"
        )
    )

    if not owner_check.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only owners can create customers"
        )

    existing_customer = await db.execute(
        select(Customer).where(
            Customer.organization_id == organization_id,
            Customer.external_id == payload.external_id
        )
    )

    if existing_customer.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    customer = Customer(
        organization_id=organization_id,
        name=payload.name,
        email=payload.email,
        external_id=payload.external_id
    )

    db.add(customer)

    await db.commit()

    await db.refresh(customer)

    return customer


async def get_customers(
    organization_id: str,
    db: AsyncSession
):

    result = await db.execute(
        select(Customer).where(
            Customer.organization_id == organization_id
        )
    )

    return result.scalars().all()


async def get_customer(
    customer_id: str,
    db: AsyncSession
):

    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id
        )
    )

    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer