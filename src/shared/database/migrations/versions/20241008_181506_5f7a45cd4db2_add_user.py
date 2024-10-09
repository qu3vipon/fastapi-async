"""Add User

Revision ID: 5f7a45cd4db2
Revises:
Create Date: 2024-10-08 18:15:06.512131

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "5f7a45cd4db2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "service_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=16), nullable=False),
        sa.Column("password_hash", sa.String(length=60), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(precision=6), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("service_user")
    # ### end Alembic commands ###
