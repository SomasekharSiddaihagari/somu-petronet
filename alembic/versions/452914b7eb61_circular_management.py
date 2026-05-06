"""circular management

Revision ID: 452914b7eb61
Revises: acde2ebaf45f
Create Date: 2026-02-03 18:25:05.332619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '452914b7eb61'
down_revision: Union[str, Sequence[str], None] = 'acde2ebaf45f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =========================
    # CATEGORY MASTER
    # =========================
    op.create_table(
        "category_master",
        sa.Column("category_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("category_name", sa.String(150), unique=True, nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "category_master_history",
        sa.Column("category_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("category_name", sa.String(150), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
    )

    # =========================
    # SUB CATEGORY MASTER
    # =========================
    op.create_table(
        "subcategory_master",
        sa.Column("subcategory_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("subcategory_name", sa.String(150), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category_master.category_id"],
        ),
    )

    op.create_table(
        "subcategory_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("subcategory_name", sa.String(150), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
    )

    # =========================
    # PUBLISHER MASTER
    # =========================
    op.create_table(
        "publisher_master",
        sa.Column("publisher_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category_master.category_id"],
        ),
    )

    op.create_table(
        "publisher_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("publisher_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
    )

    # =========================
    # CIRCULAR MASTER
    # =========================
    op.create_table(
        "circular_master",
        sa.Column("circular_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(250), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("subcategory_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("change_type", sa.String(50), nullable=True),
        sa.Column("mandatory_status", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("is_archived", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("read_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("acknowledge_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category_master.category_id"],
        ),
        sa.ForeignKeyConstraint(
            ["subcategory_id"],
            ["subcategory_master.subcategory_id"],
        ),
    )

    op.create_table(
        "circular_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("circular_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(250), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("subcategory_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("change_type", sa.String(50), nullable=True),
        sa.Column("mandatory_status", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=True),
        sa.Column("read_count", sa.Integer(), nullable=True),
        sa.Column("acknowledge_count", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
    )


def downgrade():

    op.drop_table("circular_master_history")
    op.drop_table("circular_master")
    op.drop_table("publisher_master_history")
    op.drop_table("publisher_master")
    op.drop_table("subcategory_master_history")
    op.drop_table("subcategory_master")
    op.drop_table("category_master_history")
    op.drop_table("category_master")
