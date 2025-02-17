"""empty message

Revision ID: ea27c96ffeb5
Revises: fd4dd23c20c3
Create Date: 2024-01-31 20:38:35.649274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea27c96ffeb5'
down_revision = 'fd4dd23c20c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
