"""empty message

Revision ID: a5b7142f7903
Revises: 35c327be2f5c
Create Date: 2025-02-08 20:17:55.851915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5b7142f7903'
down_revision = '35c327be2f5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.FLOAT(), nullable=False))

    # ### end Alembic commands ###
