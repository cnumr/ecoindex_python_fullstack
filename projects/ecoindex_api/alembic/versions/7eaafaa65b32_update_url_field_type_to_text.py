"""Update URL field type to text

Revision ID: 7eaafaa65b32
Revises: e83263a5def4
Create Date: 2023-03-28 11:24:39.089063

"""
import sqlalchemy as sa
from alembic import op

revision = "7eaafaa65b32"
down_revision = "e83263a5def4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("apiecoindex", schema=None) as batch_op:
        batch_op.alter_column(
            "url",
            existing_type=sa.String(length=2048),
            type_=sa.Text(),
        )


def downgrade() -> None:
    with op.batch_alter_table("apiecoindex", schema=None) as batch_op:
        batch_op.alter_column(
            "url",
            existing_type=sa.Text(),
            type_=sa.String(length=2048),
        )
