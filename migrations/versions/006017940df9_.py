"""empty message

Revision ID: 006017940df9
Revises: 1237e897b93d
Create Date: 2019-02-27 13:13:09.504382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006017940df9'
down_revision = '1237e897b93d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'about')
    # ### end Alembic commands ###