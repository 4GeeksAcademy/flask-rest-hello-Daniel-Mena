"""empty message

Revision ID: e316b62cec07
Revises: 6050a19f3e5e
Create Date: 2024-02-09 10:59:57.349290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e316b62cec07'
down_revision = '6050a19f3e5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('gravity', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('terrain', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('orbital_period', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('rotation_period', sa.String(length=250), nullable=True))
        batch_op.drop_column('population')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('population', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.drop_column('rotation_period')
        batch_op.drop_column('orbital_period')
        batch_op.drop_column('terrain')
        batch_op.drop_column('gravity')
        batch_op.drop_column('description')

    # ### end Alembic commands ###
