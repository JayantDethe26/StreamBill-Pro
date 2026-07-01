from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse
)
from app.models.user import User

from app.dependencies import get_current_user

from app.services.customer_service import (
    create_customer,
    get_customer,
    get_customers
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/{organization_id}",
    response_model=CustomerResponse
)
async def create_customer_endpoint(
    organization_id: UUID,
    payload: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_customer(
        str(organization_id),
        payload,
        current_user,
        db
    )


@router.get(
    "/{organization_id}",
    response_model=list[CustomerResponse]
)
async def get_all_customers(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_customers(
        str(organization_id),
        db
    )


@router.get(
    "/details/{customer_id}",
    response_model=CustomerResponse
)
async def get_customer_endpoint(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_customer(
        str(customer_id),
        db
    )