"""Add metadata field to student table

Revision ID: f42c08c5d882
Revises: f3d499909b33
Create Date: 2025-01-03 16:24:55.983539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'f42c08c5d882'
down_revision: Union[str, None] = 'f3d499909b33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('student', sa.Column('metadata', JSONB, nullable=True))
    op.create_index('ix_student_metadata_gin', 'student', ['metadata'], postgresql_using='gin')

def downgrade():
    op.drop_index('ix_student_metadata_gin', table_name='student')
    op.drop_column('student', 'metadata')
