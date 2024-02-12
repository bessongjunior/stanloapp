from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app
from shop import db 
from shop.models import Product
from shop.products.routes import brands, categories
import json


wishlists = Blueprint('wishlists', __name__)



def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict): 
        return dict(list(dict1.items()) + list(dict2.items()))



@wishlists.route('/wishlist', methods=['POST'])
def addWishlist():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'id': product.id, 'name':product.name,'price':float(product.price), 'quantity':quantity, 'image': product.image_1 }}
            if 'Wishlist' in session:
                print(session['Wishlist'])
                if product_id in session['Wishlist']:
                    for key, item in session['Wishlist'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Wishlist'] = MagerDicts(session['Wishlist'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Wishlist'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@wishlists.route('/wishlist')
def getWishlist():
    if 'Wishlist' not in session or len(session['Wishlist']) <= 0:
        return redirect(url_for('main.home'))
    print(session['Wishlist'])
    return render_template('wishlist/wishlist.html', title='wishlist')


@wishlists.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Wishlist' not in session or len(session['Wishlist']) <= 0:
        return redirect(url_for('main.home'))
    try:
        session.modified = True
        for key , item in session['Wishlist'].items():
            if int(key) == id:
                session['Wishlist'].pop(key, None)
                return redirect(url_for('wishlists.getWishlist'))
    except Exception as e:
        print(e)
        return redirect(url_for('wishlists.Wishlist'))


@wishlists.route('/clearwishlist')
def clearWishlist():
    try:
        session.pop('Wishlist', None)
        return redirect(url_for('main.home'))
    except Exception as e:
        print(e)
