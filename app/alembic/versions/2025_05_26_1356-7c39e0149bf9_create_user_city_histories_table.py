"""create user_city_histories table

Revision ID: 7c39e0149bf9
Revises: 3c0ac686983d
Create Date: 2025-05-26 13:56:13.189540

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7c39e0149bf9"
down_revision: Union[str, None] = "3c0ac686983d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_city_histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
            name=op.f("fk_user_city_histories_city_id_cities"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["anonymous_users.id"],
            name=op.f("fk_user_city_histories_user_id_anonymous_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_city_histories")),
    )


def downgrade() -> None:
    op.drop_table("user_city_histories")
