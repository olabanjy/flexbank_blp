"""empty message

Revision ID: e38c4f958f3c
Revises: ccde9ac0d3cf
Create Date: 2023-03-27 06:16:14.068417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e38c4f958f3c'
down_revision = 'ccde9ac0d3cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('trans_type',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.Enum('debit', 'credit', name='transtype'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('trans_type',
               existing_type=sa.Enum('debit', 'credit', name='transtype'),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###
