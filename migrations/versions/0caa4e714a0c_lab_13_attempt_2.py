"""lab 13 attempt 2

Revision ID: 0caa4e714a0c
Revises: 5c5fc91da414
Create Date: 2021-12-31 14:24:03.071291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0caa4e714a0c'
down_revision = '5c5fc91da414'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Enum('News', 'Publication', 'Other', name='posttype'), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['user.id'], name=op.f('fk_posts_post_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
