"""Add source_has_category

Revision ID: 9f90c7bac550
Revises: ac89081ef597
Create Date: 2020-04-16 12:08:38.477347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f90c7bac550'
down_revision = 'ac89081ef597'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('source_has_category',
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('source_has_category')
    # ### end Alembic commands ###
