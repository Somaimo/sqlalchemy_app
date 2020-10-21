"""empty message

Revision ID: 6b2fb8c439e6
Revises: 
Create Date: 2020-10-21 22:38:48.673803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b2fb8c439e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sqlalchemy_app_city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sqlalchemy_app_teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['sqlalchemy_app_city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sqlalchemy_app_players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('position', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['sqlalchemy_app_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlalchemy_app_players')
    op.drop_table('sqlalchemy_app_teams')
    op.drop_table('sqlalchemy_app_city')
    # ### end Alembic commands ###