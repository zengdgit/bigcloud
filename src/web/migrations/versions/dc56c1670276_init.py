"""init

Revision ID: dc56c1670276
Revises: 
Create Date: 2016-12-28 15:09:06.901937

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'dc56c1670276'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('littleclouds',
    sa.Column('主键', sa.Integer(), nullable=False),
    sa.Column('小云平台名称', sa.Unicode(length=255), nullable=True),
    sa.Column('小云平台URL', sa.String(length=255), nullable=True),
    sa.Column('是否允许接入', sa.Boolean(), nullable=True),
    sa.Column('是否已经接入', sa.Boolean(), nullable=True),
    sa.Column('联系电话', sa.String(length=20), nullable=True),
    sa.Column('联系邮箱', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
    sa.Column('接入IP', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('接入端口', sa.Integer(), nullable=True),
    sa.Column('接入协议', sa.String(length=20), nullable=True),
    sa.Column('创建时间', sa.DateTime(), nullable=True),
    sa.Column('修改时间', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('\u4e3b\u952e'),
    sa.UniqueConstraint('小云平台URL'),
    sa.UniqueConstraint('小云平台名称')
    )
    op.create_table('users',
    sa.Column('主键', sa.Integer(), nullable=False),
    sa.Column('用户名', sa.String(length=50), nullable=True),
    sa.Column('邮箱', sa.String(length=120), nullable=True),
    sa.Column('哈希加密密码', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('\u4e3b\u952e'),
    sa.UniqueConstraint('用户名')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('littleclouds')
    # ### end Alembic commands ###
