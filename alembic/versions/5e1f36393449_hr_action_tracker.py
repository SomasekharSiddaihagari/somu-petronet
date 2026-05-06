"""HR_action_tracker

Revision ID: 5e1f36393449
Revises: d19d7033885a
Create Date: 2026-03-24 11:39:11.726798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e1f36393449'
down_revision: Union[str, Sequence[str], None] = 'd19d7033885a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade():

    # ---------------- HR ACTION ----------------
    op.create_table(
        'hr_action',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('action_type', sa.String(100), nullable=False),
        sa.Column('action_date', sa.DateTime, nullable=False),
        sa.Column('justification', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    op.create_table(
        'hr_action_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.Integer),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('action_type', sa.String(100), nullable=False),
        sa.Column('action_date', sa.DateTime, nullable=False),
        sa.Column('justification', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    # ---------------- HR ACTION DOCUMENT ----------------
    op.create_table(
        'hr_action_documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('hr_action_id', sa.Integer, sa.ForeignKey('hr_action.id'), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime),
    )

    op.create_table(
        'hr_action_documents_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.Integer),
        sa.Column('hr_action_id', sa.Integer, sa.ForeignKey('hr_action.id'), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime),
    )

    # ---------------- PROMOTIONS ----------------
    op.create_table(
        'promotions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('current_grade', sa.String(50), nullable=False),
        sa.Column('new_grade', sa.String(50), nullable=False),
        sa.Column('current_designation', sa.String(100), nullable=False),
        sa.Column('new_designation', sa.String(100), nullable=False),
        sa.Column('effective_date', sa.DateTime, nullable=False),
        sa.Column('remarks', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    op.create_table(
        'promotions_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.Integer),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('current_grade', sa.String(50), nullable=False),
        sa.Column('new_grade', sa.String(50), nullable=False),
        sa.Column('current_designation', sa.String(100), nullable=False),
        sa.Column('new_designation', sa.String(100), nullable=False),
        sa.Column('effective_date', sa.DateTime, nullable=False),
        sa.Column('remarks', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    # ---------------- EMPLOYEE TRANSFER ----------------
    op.create_table(
        'employee_transfers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('current_station', sa.Integer, nullable=False),
        sa.Column('new_station', sa.Integer, nullable=False),
        sa.Column('effective_date', sa.DateTime, nullable=False),
        sa.Column('remarks', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    op.create_table(
        'employee_transfers_history',
        sa.Column('historyid', sa.Integer, primary_key=True),
        sa.Column('id', sa.Integer),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('current_station', sa.Integer, nullable=False),
        sa.Column('new_station', sa.Integer, nullable=False),
        sa.Column('effective_date', sa.DateTime, nullable=False),
        sa.Column('remarks', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    # ---------------- TRANSFER DOCUMENT ----------------
    op.create_table(
        'transfer_documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('transfer_id', sa.Integer, sa.ForeignKey('employee_transfers.id'), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime),
    )

    op.create_table(
        'transfer_documents_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.Integer),
        sa.Column('transfer_id', sa.Integer, sa.ForeignKey('employee_transfers.id'), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime),
    )

    # ---------------- PERFORMANCE ----------------
    op.create_table(
        'employee_performance',
        sa.Column('performance_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('appraisal_start_date', sa.DateTime, nullable=False),
        sa.Column('appraisal_end_date', sa.DateTime, nullable=False),
        sa.Column('annual_appraisal_rating', sa.String(50)),
        sa.Column('annual_rating_score', sa.String(20)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    op.create_table(
        'employee_performance_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('performance_id', sa.Integer),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('appraisal_start_date', sa.DateTime, nullable=False),
        sa.Column('appraisal_end_date', sa.DateTime, nullable=False),
        sa.Column('annual_appraisal_rating', sa.String(50)),
        sa.Column('annual_rating_score', sa.String(20)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    # ---------------- DISCIPLINARY ----------------
    op.create_table(
        'disciplinary_incidents',
        sa.Column('disciplinary_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('incident_date', sa.DateTime, nullable=False),
        sa.Column('severity', sa.String(50), nullable=False),
        sa.Column('incident_details', sa.Text, nullable=False),
        sa.Column('investigation_finding', sa.Text),
        sa.Column('measures_taken', sa.Text),
        sa.Column('enable_suspension', sa.Boolean),
        sa.Column('enable_termination', sa.Boolean),
        sa.Column('suspension_effective_from', sa.DateTime),
        sa.Column('suspension_effective_to', sa.DateTime),
        sa.Column('termination_effective_from', sa.DateTime),
        sa.Column('outcome', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )

    op.create_table(
        'disciplinary_incidents_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('disciplinary_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('incident_date', sa.DateTime, nullable=False),
        sa.Column('severity', sa.String(50), nullable=False),
        sa.Column('incident_details', sa.Text, nullable=False),
        sa.Column('investigation_finding', sa.Text),
        sa.Column('measures_taken', sa.Text),
        sa.Column('enable_suspension', sa.Boolean),
        sa.Column('enable_termination', sa.Boolean),
        sa.Column('suspension_effective_from', sa.DateTime),
        sa.Column('suspension_effective_to', sa.DateTime),
        sa.Column('termination_effective_from', sa.DateTime),
        sa.Column('outcome', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
    )


def downgrade():
    op.drop_table('disciplinary_incidents_history')
    op.drop_table('disciplinary_incidents')
    op.drop_table('employee_performance_history')
    op.drop_table('employee_performance')
    op.drop_table('transfer_documents_history')
    op.drop_table('transfer_documents')
    op.drop_table('employee_transfers_history')
    op.drop_table('employee_transfers')
    op.drop_table('promotions_history')
    op.drop_table('promotions')
    op.drop_table('hr_action_documents_history')
    op.drop_table('hr_action_documents')
    op.drop_table('hr_action_history')
    op.drop_table('hr_action')