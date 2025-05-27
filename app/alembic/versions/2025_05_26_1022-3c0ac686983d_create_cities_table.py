"""create cities table

Revision ID: 3c0ac686983d
Revises: 90cc42142187
Create Date: 2025-05-26 10:22:33.157754

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3c0ac686983d"
down_revision: Union[str, None] = "90cc42142187"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cities",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "search_count", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cities")),
        sa.UniqueConstraint("name", name=op.f("uq_cities_name")),
    )


def downgrade() -> None:
    op.drop_table("cities")
