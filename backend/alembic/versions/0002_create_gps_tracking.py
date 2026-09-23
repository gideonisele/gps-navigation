"""create GPS tracking tables

Revision ID: 0002
Revises: 0001
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "navigation_sessions",

        sa.Column(
            "session_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "session_uuid",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "session_name",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "travel_mode",
            sa.String(length=30),
            server_default="driving",
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            server_default="active",
            nullable=False,
        ),

        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.Column(
            "ended_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "session_uuid",
            name="uq_navigation_sessions_session_uuid",
        ),
    )

    op.create_table(
        "gps_points",

        sa.Column(
            "gps_point_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "session_id",
            sa.BigInteger(),
            sa.ForeignKey(
                "navigation_sessions.session_id",
                ondelete="CASCADE",
            ),
            nullable=False,
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
            "accuracy",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "altitude",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "altitude_accuracy",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "heading",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "speed",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
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

    op.create_index(
        "ix_gps_points_session_id",
        "gps_points",
        ["session_id"],
        unique=False,
    )

    op.create_index(
        "ix_gps_points_session_recorded_at",
        "gps_points",
        [
            "session_id",
            "recorded_at",
        ],
        unique=False,
    )


def downgrade():

    op.drop_index(
        "ix_gps_points_session_recorded_at",
        table_name="gps_points",
    )

    op.drop_index(
        "ix_gps_points_session_id",
        table_name="gps_points",
    )

    op.drop_table("gps_points")

    op.drop_table("navigation_sessions")