from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.base import UUIDMixin


class PricingTier(
    UUIDMixin,
    Base
):
    __tablename__ = "pricing_tiers"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    min_units: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    max_units: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    price_per_unit: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )