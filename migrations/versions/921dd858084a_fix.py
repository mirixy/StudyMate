"""fix

Revision ID: 921dd858084a
Revises: fd1bf523a7f5
Create Date: 2024-12-29 21:52:29.423287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '921dd858084a'
down_revision = 'fd1bf523a7f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('theme',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('theme',
               existing_type=sa.String(length=10),
               type_=sa.BOOLEAN(),
               existing_nullable=True)

    # ### end Alembic commands ###
