"""Update blood type constraints

Revision ID: ff61fe467c7b
Revises: 6444720b1d0c
Create Date: 2023-10-04 23:03:18.659515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff61fe467c7b'
down_revision = '6444720b1d0c'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the updated constraint
    op.create_table(
        'donors_temp',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('donor_name', sa.String(), nullable=False),
        sa.Column('blood_type', sa.String(), CheckConstraint("blood_type IN ('A+','A-', 'B+','B-', 'AB+', 'AB-','O+','O-')", name="blood_types"), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False),
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO donors_temp SELECT * FROM donors')

    # Drop the old table
    op.drop_table('donors')

    # Rename the new table to the original table name
    op.rename_table('donors_temp', 'donors')

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
