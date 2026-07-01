from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.base import UUIDMixin


class SubscriptionPlan(
    UUIDMixin,
    Base
):
    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    max_members: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )