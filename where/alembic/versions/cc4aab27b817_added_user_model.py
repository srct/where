"""Added user model

Revision ID: cc4aab27b817
Revises: 09ab4264e119
Create Date: 2020-02-26 16:05:12.284942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc4aab27b817'
down_revision = '09ab4264e119'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('net_id', sa.String(), nullable=False),
    sa.Column('access_level', sa.Enum('USER', 'ADMIN', name='accesslevel'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###