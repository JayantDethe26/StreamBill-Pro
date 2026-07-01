from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.base import UUIDMixin


class ApiKey(
    UUIDMixin,
    Base
):
    __tablename__ = "api_keys"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    key_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )