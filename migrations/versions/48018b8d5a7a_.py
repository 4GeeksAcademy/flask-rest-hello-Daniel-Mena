"""empty message

Revision ID: 48018b8d5a7a
Revises: 261aca6ead43
Create Date: 2024-02-12 14:20:15.508747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48018b8d5a7a'
down_revision = '261aca6ead43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favourite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favourite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('url')

    # ### end Alembic commands ###
