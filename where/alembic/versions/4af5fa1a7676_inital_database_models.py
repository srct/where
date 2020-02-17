"""inital database models

Revision ID: 4af5fa1a7676
Revises: 
Create Date: 2020-02-16 19:07:30.646828

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4af5fa1a7676'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('category',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('slug', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    sa.UniqueConstraint('slug')
                    )
    op.create_table('field',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('type', sa.Enum('STRING', 'FLOAT', 'INTEGER', 'BOOLEAN', 'RATING', name='fieldtype'), nullable=False),
                    sa.Column('unit', sa.String(), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(('category_id',), ['category.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('point',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('lat', sa.Float(), nullable=False),
                    sa.Column('lon', sa.Float(), nullable=False),
                    sa.Column('attributes', sa.JSON(), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=False),
                    sa.Column('parent_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(('category_id',), ['category.id'], ),
                    sa.ForeignKeyConstraint(('parent_id',), ['point.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('point')
    op.drop_table('field')
    op.drop_table('category')
