"""Link Post to User

Revision ID: c0bf8dfee365
Revises: c21fdde913e0
Create Date: ...

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c0bf8dfee365'
down_revision = 'c21fdde913e0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE IF EXISTS users")
    users_table = op.create_table('users',
                                  sa.Column('id', sa.Integer(), nullable=False),
                                  sa.Column('username', sa.String(length=50), nullable=False),
                                  sa.Column('email', sa.String(length=100), nullable=False),
                                  sa.Column('password', sa.String(length=100), nullable=False),
                                  sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
                                  sa.UniqueConstraint('email', name=op.f('uq_users_email')),
                                  sa.UniqueConstraint('username', name=op.f('uq_users_username'))
                                  )


    connection = op.get_bind()

    connection.execute(
        sa.insert(users_table).values(
            username='default_user',
            email='default@example.com',
            password='hashed_password_placeholder'
        )
    )

    default_user_id = 1

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False, server_default=str(default_user_id)))

        batch_op.create_foreign_key(batch_op.f('fk_posts_user_id_users'), 'users', ['user_id'], ['id'])
        batch_op.drop_column('author')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('user_id', server_default=None)


def downgrade():

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=20), nullable=False, server_default="Anonymous"))
        batch_op.drop_constraint(batch_op.f('fk_posts_user_id_users'), type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('users')