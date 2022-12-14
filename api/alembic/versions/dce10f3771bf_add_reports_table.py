"""add reports table

Revision ID: dce10f3771bf
Revises: 7ab7d8ac36a9
Create Date: 2022-11-21 23:03:09.762344

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dce10f3771bf"
down_revision = "7ab7d8ac36a9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("reporter_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column(
            "content_type", sa.String(), server_default="campaign", nullable=False
        ),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("reporter_id", "content_type", "content_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("reports")
    # ### end Alembic commands ###
