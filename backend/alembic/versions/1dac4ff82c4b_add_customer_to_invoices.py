"""add customer to invoices

Revision ID: 1dac4ff82c4b
Revises: ff6ec099337b
Create Date: 2026-06-30 18:42:11.291707

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1dac4ff82c4b"
down_revision: Union[str, Sequence[str], None] = "ff6ec099337b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "invoices",
        sa.Column(
            "customer_id",
            sa.UUID(),
            nullable=True
        )
    )

    op.create_foreign_key(
        None,
        "invoices",
        "customers",
        ["customer_id"],
        ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        None,
        "invoices",
        type_="foreignkey"
    )

    op.drop_column(
        "invoices",
        "customer_id"
    )