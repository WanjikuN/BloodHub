"""Add age column to donors

Revision ID: 7885434e4fd1
Revises: 10a80de3f04f
Create Date: 2023-10-04 21:56:55.736795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7885434e4fd1'
down_revision = '10a80de3f04f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donors', sa.Column('age', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donors', 'age')
    # ### end Alembic commands ###
