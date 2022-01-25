"""empty message

Revision ID: b1ea58ec52b9
Revises: a318748b84f7
Create Date: 2022-01-15 19:49:29.235518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ea58ec52b9'
down_revision = 'a318748b84f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('design_clothing',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('sku_id', sa.String(), nullable=True),
                    sa.Column('color', sa.String(), nullable=True),
                    sa.Column('material', sa.String(), nullable=True),
                    sa.Column('sleeve_type', sa.String(), nullable=True),
                    sa.Column('size', sa.String(), nullable=True),
                    sa.Column('location', sa.String(), nullable=True),
                    sa.Column('image_url', sa.String(), nullable=True),
                    sa.Column('category', sa.String(), nullable=True),
                    sa.Column('total_quantity', sa.Integer(), nullable=True),
                    sa.Column('quantity_debit_count',
                              sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('sku_id')
                    )
    op.create_table('design_imprinted_htp',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('sku_id', sa.String(), nullable=True),
                    sa.Column('location', sa.String(), nullable=True),
                    sa.Column('category', sa.String(), nullable=True),
                    sa.Column('total_quantity', sa.Integer(), nullable=True),
                    sa.Column('quantity_debit_count',
                              sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('sku_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('design_imprinted_htp')
    op.drop_table('design_clothing')
    # ### end Alembic commands ###
