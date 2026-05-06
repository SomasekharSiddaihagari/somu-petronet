"""placeholder fix for missing migration b3dda78de46d"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b3dda78de46d'
down_revision = None  # or the previous revision id if you know it
branch_labels = None
depends_on = None

def upgrade():
    # This is just a placeholder. No schema changes.
    pass

def downgrade():
    # This is just a placeholder. No schema changes.
    pass
