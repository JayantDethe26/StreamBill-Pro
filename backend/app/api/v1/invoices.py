from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.invoice import InvoiceResponse

from app.services.invoice_service import generate_invoice

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post(
    "/generate/{product_id}",
    response_model=list[InvoiceResponse]
)
async def create_invoice(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await generate_invoice(
        product_id,
        db
    )