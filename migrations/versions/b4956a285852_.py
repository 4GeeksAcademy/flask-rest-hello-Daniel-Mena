"""empty message

Revision ID: b4956a285852
Revises: 736356322e3b
Create Date: 2024-02-09 11:11:07.900416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4956a285852'
down_revision = '736356322e3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.alter_column('url_img',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.alter_column('url_img',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)

    # ### end Alembic commands ###
