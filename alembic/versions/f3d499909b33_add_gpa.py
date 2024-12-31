"""add gpa

Revision ID: f3d499909b33
Revises: 9a4ced6e7d21
Create Date: 2024-12-31 16:10:40.257308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3d499909b33'
down_revision: Union[str, None] = '9a4ced6e7d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('student' , sa.Column('gpa', sa.Numeric(precision=4, scale=2), nullable=True))

def downgrade() -> None:
    op.drop_column('student', 'gpa')
