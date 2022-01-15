"""empty message

Revision ID: a318748b84f7
Revises: 9710e7090274
Create Date: 2022-01-03 21:13:26.849324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a318748b84f7'
down_revision = '9710e7090274'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('design_clothing', sa.Column(
        'category', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('design_clothing', 'category')
    # ### end Alembic commands ###