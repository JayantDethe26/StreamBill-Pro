from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.base import UUIDMixin
from sqlalchemy import DateTime
from datetime import datetime

class Invoice(
    UUIDMixin,
    Base
):
    __tablename__ = "invoices"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True
    )

    total_usage: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    payment_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    billing_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    billing_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )