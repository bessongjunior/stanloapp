from flask import Blueprint, render_template, session, request, redirect,url_for, flash, current_app
from shop import db
from shop.models import Category,Brand,Product
from shop.forms import Addproducts
import secrets
import os

product = Blueprint('product', __name__)

def brands():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Product,(Category.id == Product.category_id)).all()
    return categories


# @product.route('/shop/<int:page_num>')
# def shop(page_num):
#     products =  Product.query.paginate(per_page=8, page=page_num, error_out=True) #Product.query.all()
#     return render_template('products/shop-list.html', title='shop listing', products=products)


@product.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/shop-list.html', title='shop listing', products=products, brands=brands(),categories=categories())



# @app.route('/result')
# def result():
#     searchword = request.args.get('q')
#     products = Product.query.msearch(searchword, fields=['name','desc'] , limit=6)
#     return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@product.route('/product_details/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template('products/product-details.html', title='product details', product=product,brands=brands(),categories=categories())


@product.route('/search_result')
def search_results():
    # searchword = request.args.get('q')
    return render_template('products/search-results.html')


