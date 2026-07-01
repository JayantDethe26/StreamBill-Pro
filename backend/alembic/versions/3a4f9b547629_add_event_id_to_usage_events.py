"""add event id to usage events

Revision ID: 3a4f9b547629
Revises: 5a16998388c3
Create Date: 2026-06-26 11:54:14.259350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a4f9b547629"
down_revision: Union[str, Sequence[str], None] = "5a16998388c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("DELETE FROM usage_events")

    op.add_column(
        "usage_events",
        sa.Column(
            "event_id",
            sa.String(length=255),
            nullable=False
        )
    )

    op.create_unique_constraint(
        "uq_usage_events_event_id",
        "usage_events",
        ["event_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_usage_events_event_id",
        "usage_events",
        type_="unique"
    )

    op.drop_column(
        "usage_events",
        "event_id"
    )