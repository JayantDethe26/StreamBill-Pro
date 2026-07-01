from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)

from app.services.product_service import (
    create_product,
    get_products
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201
)
async def create_new_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_product(
        payload,
        current_user,
        db
    )


@router.get(
    "",
    response_model=list[ProductResponse]
)
async def list_products(
    db: AsyncSession = Depends(get_db)
):
    return await get_products(db)