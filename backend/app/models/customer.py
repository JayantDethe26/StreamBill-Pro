from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.base import UUIDMixin


class Customer(Base, UUIDMixin):

    __tablename__ = "customers"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    external_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )