"""empty message

Revision ID: 6dc7cf1294e7
Revises: be88579480a6
Create Date: 2021-11-16 08:52:53.302283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dc7cf1294e7'
down_revision = 'be88579480a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raw_items', sa.Column('size', sa.String(), nullable=True))
    op.add_column('raw_items', sa.Column('quantity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('raw_items', 'quantity')
    op.drop_column('raw_items', 'size')
    # ### end Alembic commands ###
