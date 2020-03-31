"""empty message

Revision ID: 7113619b58ca
Revises: dca5505876c6
Create Date: 2020-03-31 13:35:28.501409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7113619b58ca'
down_revision = 'dca5505876c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('past_shows', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('past_shows', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'upcoming_shows_count')
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Venue', 'past_shows')
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_column('Artist', 'upcoming_shows')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'past_shows')
    # ### end Alembic commands ###
