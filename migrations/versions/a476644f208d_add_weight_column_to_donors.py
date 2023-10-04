"""Add weight column to donors

Revision ID: a476644f208d
Revises: 7885434e4fd1
Create Date: 2023-10-04 22:01:10.945896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a476644f208d'
down_revision = '7885434e4fd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donors', sa.Column('weight', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donors', 'weight')
    # ### end Alembic commands ###
