"""create lat changes

Revision ID: ea13198c8610
Revises: 60c00e9f32ac
Create Date: 2026-01-24 19:08:43.361611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea13198c8610'
down_revision: Union[str, Sequence[str], None] = '60c00e9f32ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ---- location_access_token ----
    op.alter_column('location_access_token', 'user_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token', 'station_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token', 'token',
                     existing_type=sa.String(length=128),
                     nullable=True)

    op.alter_column('location_access_token', 'access_type',
                     existing_type=sa.Enum('IP', 'GEO', 'APPROVAL', name='accesstypeenum'),
                     nullable=True)

    op.alter_column('location_access_token', 'ip_address',
                     existing_type=sa.String(length=45),
                     nullable=True)

    op.alter_column('location_access_token', 'latitude',
                     existing_type=sa.Float(),
                     nullable=True)

    op.alter_column('location_access_token', 'longitude',
                     existing_type=sa.Float(),
                     nullable=True)

    op.alter_column('location_access_token', 'approved_by_user_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token', 'expires_at',
                     existing_type=sa.DateTime(timezone=True),
                     nullable=True)

    op.alter_column('location_access_token', 'is_active',
                     existing_type=sa.Boolean(),
                     nullable=True)

    op.alter_column('location_access_token', 'created_at',
                     existing_type=sa.DateTime(timezone=True),
                     nullable=True)
    

    op.alter_column('location_access_token_history', 'user_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'station_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'token',
                     existing_type=sa.String(length=128),
                     nullable=True)

    op.alter_column('location_access_token_history', 'access_type',
                     existing_type=sa.Enum('IP', 'GEO', 'APPROVAL', name='accesstypeenum'),
                     nullable=True)

    op.alter_column('location_access_token_history', 'ip_address',
                     existing_type=sa.String(length=45),
                     nullable=True)

    op.alter_column('location_access_token_history', 'latitude',
                     existing_type=sa.Float(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'longitude',
                     existing_type=sa.Float(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'approved_by_user_id',
                     existing_type=sa.Integer(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'expires_at',
                     existing_type=sa.DateTime(timezone=True),
                     nullable=True)

    op.alter_column('location_access_token_history', 'is_active',
                     existing_type=sa.Boolean(),
                     nullable=True)

    op.alter_column('location_access_token_history', 'created_at',
                     existing_type=sa.DateTime(timezone=True),
                     nullable=True)