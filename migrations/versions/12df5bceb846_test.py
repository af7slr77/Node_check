"""test

Revision ID: 12df5bceb846
Revises: 
Create Date: 2023-09-14 19:05:33.343674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12df5bceb846'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocks',
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('update_time', sa.Integer(), nullable=False),
    sa.Column('current_ds_epoch', sa.Integer(), nullable=True),
    sa.Column('current_mini_epoch', sa.Integer(), nullable=True),
    sa.Column('response_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('block_id'),
    sa.UniqueConstraint('block_id')
    )
    op.create_table('nodes',
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.Column('node_url', sa.String(), nullable=False),
    sa.Column('node_name', sa.String(), nullable=False),
    sa.Column('trust_coefficient', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('node_id'),
    sa.UniqueConstraint('node_id'),
    sa.UniqueConstraint('node_url')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_telegram_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=32), nullable=False),
    sa.Column('reg_date', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('user_telegram_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('nodes_users',
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['node_id'], ['nodes.node_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('node_id', 'user_id')
    )
    op.create_table('records',
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('update_time', sa.Integer(), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('current_ds_epoch', sa.Integer(), nullable=True),
    sa.Column('current_mini_epoch', sa.Integer(), nullable=True),
    sa.Column('response_time', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('stake_amount', sa.String(), nullable=True),
    sa.Column('commission', sa.String(), nullable=True),
    sa.Column('number_of_delegates', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['nodes.node_id'], ),
    sa.PrimaryKeyConstraint('record_id'),
    sa.UniqueConstraint('record_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    op.drop_table('nodes_users')
    op.drop_table('users')
    op.drop_table('nodes')
    op.drop_table('blocks')
    # ### end Alembic commands ###
