"""create locations table"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "locations",

        sa.Column(
            "location_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "name",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "latitude",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "longitude",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "location",
            Geography(
                geometry_type="POINT",
                srid=4326,
                spatial_index=True,
            ),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )


def downgrade():

    op.drop_table("locations")