"""Initial Schema

Revision ID: d90b435ceea
Revises: None
Create Date: 2014-06-01 17:22:13.873664

"""

# revision identifiers, used by Alembic.
revision = 'd90b435ceea'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tg_permission',
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.Column('permission_name', sa.Unicode(length=63), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.PrimaryKeyConstraint('permission_id'),
    sa.UniqueConstraint('permission_name')
    )
    op.create_table('cigarette',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('submit_date', sa.DateTime(), nullable=False),
    sa.Column('user', sa.Unicode(length=255), nullable=False),
    sa.Column('justification', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tg_user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.Unicode(length=16), nullable=False),
    sa.Column('email_address', sa.Unicode(length=255), nullable=False),
    sa.Column('display_name', sa.Unicode(length=255), nullable=True),
    sa.Column('password', sa.Unicode(length=128), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('tg_group',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.Unicode(length=16), nullable=False),
    sa.Column('display_name', sa.Unicode(length=255), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('group_id'),
    sa.UniqueConstraint('group_name')
    )
    op.create_table('unsmoke',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tg_user_group',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['tg_group.group_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['tg_user.user_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_table('fbauth_info',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('registered', sa.Boolean(), nullable=False),
    sa.Column('just_connected', sa.Boolean(), nullable=False),
    sa.Column('profile_picture', sa.String(length=512), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('facebook_id', sa.Unicode(length=255), nullable=False),
    sa.Column('access_token', sa.Unicode(length=255), nullable=False),
    sa.Column('access_token_expiry', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['tg_user.user_id'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('tg_group_permission',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['tg_group.group_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['permission_id'], ['tg_permission.permission_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'permission_id')
    )
    op.drop_table(u'migrate_version')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'migrate_version',
    sa.Column(u'version_num', sa.VARCHAR(length=32), nullable=False),
    sa.PrimaryKeyConstraint()
    )
    op.drop_table('tg_group_permission')
    op.drop_table('fbauth_info')
    op.drop_table('tg_user_group')
    op.drop_table('unsmoke')
    op.drop_table('tg_group')
    op.drop_table('tg_user')
    op.drop_table('cigarette')
    op.drop_table('tg_permission')
    ### end Alembic commands ###
