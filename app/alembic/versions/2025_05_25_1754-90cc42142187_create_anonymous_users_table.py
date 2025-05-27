"""create anonymous_users table

Revision ID: 90cc42142187
Revises: 
Create Date: 2025-05-25 17:54:03.380180

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "90cc42142187"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "anonymous_users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_anonymous_users")),
    )


def downgrade() -> None:
    op.drop_table("anonymous_users")
