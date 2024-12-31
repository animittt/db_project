"""initial migration

Revision ID: 9a4ced6e7d21
Revises: 
Create Date: 2024-12-31 16:05:04.800567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4ced6e7d21'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('student', sa.Column('gender', sa.String(20), nullable=True))

def downgrade() -> None:
    op.drop_column('student', 'gender')
