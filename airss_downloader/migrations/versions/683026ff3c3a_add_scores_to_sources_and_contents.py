"""Add scores to sources and contents

Revision ID: 683026ff3c3a
Revises: 1cad85b87fc3
Create Date: 2020-04-16 10:24:33.859412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '683026ff3c3a'
down_revision = '1cad85b87fc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contents', sa.Column('predicted_certainty', sa.Float(), nullable=True))
    op.add_column('contents', sa.Column('predicted_score', sa.Float(), nullable=True))
    op.add_column('contents', sa.Column('score', sa.Integer(), nullable=True))
    op.add_column('sources', sa.Column('aggregated_certainty', sa.Float(), nullable=True))
    op.add_column('sources', sa.Column('aggregated_score', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sources', 'aggregated_score')
    op.drop_column('sources', 'aggregated_certainty')
    op.drop_column('contents', 'score')
    op.drop_column('contents', 'predicted_score')
    op.drop_column('contents', 'predicted_certainty')
    # ### end Alembic commands ###