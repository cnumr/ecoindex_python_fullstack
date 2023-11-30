"""Add ecoindex_version field

Revision ID: 826abb0c4222
Revises: fd9a1f5662c8
Create Date: 2022-09-12 17:39:44.209071

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from ecoindex.database.helper import column_exists

# revision identifiers, used by Alembic.
revision = "826abb0c4222"
down_revision = "fd9a1f5662c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if not column_exists(op.get_bind(), "apiecoindex", "ecoindex_version"):
        op.add_column(
            "apiecoindex",
            sa.Column(
                "ecoindex_version", sqlmodel.sql.sqltypes.AutoString(), nullable=True
            ),
        )


def downgrade() -> None:
    if column_exists(op.get_bind(), "apiecoindex", "ecoindex_version"):
        op.drop_column("apiecoindex", "ecoindex_version")
