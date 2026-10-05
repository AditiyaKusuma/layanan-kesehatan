"""add email to pasien

Revision ID: b201019a5917
Revises: d7909386742c
Create Date: 2026-10-05 14:54:33.085675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b201019a5917'
down_revision: Union[str, Sequence[str], None] = 'd7909386742c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'pasien',
        sa.Column('email', sa.String(length=100), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pasien', 'email')
