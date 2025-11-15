
from flask import render_template
from app.products import products_bp

@products_bp.route('/')
def all_products():

    fake_products = [
        {"id": 1, "name": "Ноутбук 'Alpha'", "price": 35000},
        {"id": 2, "name": "Мишка 'Gamma'", "price": 1200},
        {"id": 3, "name": "Монітор 'Omega'", "price": 7500}
    ]
    return render_template('products/index.html', products=fake_products)

@products_bp.route('/<int:product_id>')
def product_details(product_id):

    return f"Це сторінка для товару з ID: {product_id}"