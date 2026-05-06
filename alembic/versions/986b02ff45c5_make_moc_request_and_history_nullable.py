"""make moc request and history nullable

Revision ID: 986b02ff45c5
Revises: 2ca4e46fd453
Create Date: 2026-01-29 16:36:06.177389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '986b02ff45c5'
down_revision: Union[str, Sequence[str], None] = '2ca4e46fd453'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ---- moc_requests ----
    table = "moc_requests"
    cols = [
        "moc_request_no","station_name","title","date","priority","modification_type",
        "time_limit","shutdown_required","present_system","proposed_change","justification",
        "objectives","other_units_impacted","statutory_approval_required",
        "statutory_approval_details","impact_of_modification",
        "consequences_non_implementation","hse","efficiency","quality","reliability",
        "other_aspects","objectives_achieved","attachments","comments","reviewer_comments",
        "approver_comments","submission_date","hira_approved_date","sic_approved_date",
        "approved_date","sic_comments","closure_date","closure_comments","status",
        "is_active","created_by","updated_by","created_at","updated_at"
    ]

    for c in cols:
        op.alter_column(table, c, nullable=True)

    # ---- moc_request_history ----
    table = "moc_request_history"
    cols = [
        # ❌ DO NOT TOUCH PK / CONSTRAINED COLUMN
        # "moc_request_id",

        # ❌ COLUMN DOES NOT EXIST IN DB
        # "moc_closure_id",

        "moc_request_no","station_name","title","date",
        "priority","modification_type","time_limit","shutdown_required","present_system",
        "proposed_change","justification","objectives","other_units_impacted",
        "statutory_approval_required","statutory_approval_details",
        "impact_of_modification","consequences_non_implementation","hse","efficiency",
        "quality","reliability","other_aspects","objectives_achieved","attachments",
        "comments","status","is_active","created_by","updated_by",
        "created_at","updated_at","reviewer_comments","approver_comments",
        "sic_comments","sic_approved_date","submission_date",
        "hira_approved_date","approved_date","closure_date","closure_comments"
    ]

    for c in cols:
        op.alter_column(table, c, nullable=True)
def downgrade():
    pass