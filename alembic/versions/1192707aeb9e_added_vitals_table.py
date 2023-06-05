"""added Vitals table

Revision ID: 1192707aeb9e
Revises: f892f0de192e
Create Date: 2023-06-05 17:28:16.833107

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1192707aeb9e'
down_revision = 'f892f0de192e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vital_signs',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('patient_id', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('o2_level', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('vitals')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vitals',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('vitals', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='vitals_pkey')
    )
    op.drop_table('vital_signs')
    # ### end Alembic commands ###
