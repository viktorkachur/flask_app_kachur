"""Insert new car data into tables

Revision ID: 933aadcd70ae
Revises: f83170cf1e0d
Create Date: 2025-11-16 15:37:51.709057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933aadcd70ae'
down_revision = 'f83170cf1e0d'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = sa.table('categories',
                                sa.column('id', sa.Integer),
                                sa.column('name', sa.String)
                                )
    products_table = sa.table('products',
                              sa.column('name', sa.String),
                              sa.column('price', sa.Float),
                              sa.column('active', sa.Boolean),
                              sa.column('category_id', sa.Integer)
                              )


    op.bulk_insert(categories_table, [
        {'name': 'Electric Cars'},
        {'name': 'Hypercars'},
        {'name': 'Classic Cars'}
    ])


    conn = op.get_bind()


    e_cars_id = conn.execute(sa.text("SELECT id FROM categories WHERE name = 'Electric Cars'")).scalar()
    h_cars_id = conn.execute(sa.text("SELECT id FROM categories WHERE name = 'Hypercars'")).scalar()
    c_cars_id = conn.execute(sa.text("SELECT id FROM categories WHERE name = 'Classic Cars'")).scalar()


    op.bulk_insert(products_table, [
        {'name': 'Model S', 'price': 75000.0, 'active': True, 'category_id': e_cars_id},
        {'name': 'Chiron', 'price': 3000000.0, 'active': True, 'category_id': h_cars_id},
        {'name': 'Mustang 1969', 'price': 65000.0, 'active': False, 'category_id': c_cars_id},
        {'name': 'Model 3', 'price': 40000.0, 'active': True, 'category_id': e_cars_id}
    ])


def downgrade():
    op.execute("""
               DELETE
               FROM products
               WHERE name IN ('Model S', 'Chiron', 'Mustang 1969', 'Model 3');
               """)

    op.execute("""
               DELETE
               FROM categories
               WHERE name IN ('Electric Cars', 'Hypercars', 'Classic Cars');
               """)
