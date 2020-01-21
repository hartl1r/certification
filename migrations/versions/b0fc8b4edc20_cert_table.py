"""cert table

Revision ID: b0fc8b4edc20
Revises: 
Create Date: 2019-03-20 17:14:01.153008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0fc8b4edc20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trnDate', sa.String(length=30), nullable=True),
    sa.Column('maxSize', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cert_trnDate'), 'cert', ['trnDate'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cert_trnDate'), table_name='cert')
    op.drop_table('cert')
    # ### end Alembic commands ###
