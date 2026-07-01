"""add payment details to invoices

Revision ID: 968dba20bb94
Revises: 1dac4ff82c4b
Create Date: 2026-07-01 13:15:58.782318
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "968dba20bb94"
down_revision: Union[str, Sequence[str], None] = "1dac4ff82c4b"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "invoices",
        sa.Column(
            "payment_id",
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        "invoices",
        sa.Column(
            "paid_at",
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade() -> None:

    op.drop_column(
        "invoices",
        "paid_at"
    )

    op.drop_column(
        "invoices",
        "payment_id"
    )