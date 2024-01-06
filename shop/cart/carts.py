from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app
# from shop import db 
from shop.models import Product
from shop.products.routes import brands, categories
import json


carts = Blueprint('carts', __name__)

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict): 
        return dict(list(dict1.items()) + list(dict2.items()))

@carts.route('/addcart', methods=['POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'id': product.id, 'name':product.name,'price':float(product.price),'discount':product.discount,'quantity':quantity, 'image': product.image_1 }}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@carts.route('/carts')
def getcart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.home'))
    print(session['Shoppingcart'])
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount

        tax =("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))

    # if 'coupon' in session:
    #     coupon_discount = (session['coupon']['discount_percentage']/100) * subtotal
    #     subtotal -= coupon_discount

    # tax = float("%.2f" % (.06 * subtotal))
    # grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('cart/carts.html', title='cart')



@carts.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item is updated!')
                    return redirect(url_for('carts.getcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('carts.getcart'))



@carts.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('carts.getcart'))


@carts.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('main.home'))
    except Exception as e:
        print(e)


# @carts.route('/createcoupon', methods=['POST'])
# def create_coupon():
#     try:
#         coupon_code = request.form.get('coupon_code')
#         discount_percentage = float(request.form.get('discount_percentage'))
#         coupon = Coupon(coupon_code=coupon_code, discount_percentage=discount_percentage)
#         db.session.add(coupon)
#         db.session.commit()
#         flash('Coupon created successfully!')
#     except Exception as e:
#         print(e)
#     finally:
#         return redirect(request.referrer)

# @carts.route('/applycoupon', methods=['POST'])
# def apply_coupon():
#     try:
#         coupon_code = request.form.get('coupon_code')
#         coupon = Coupon.query.filter_by(coupon_code=coupon_code).first()
#         if coupon:
#             session['coupon'] = {'coupon_code': coupon.coupon_code, 'discount_percentage': coupon.discount_percentage}
#             flash('Coupon applied successfully!')
#         else:
#             flash('Invalid coupon code!')
#     except Exception as e:
#         print(e)
#     finally:
#         return redirect(request.referrer)


# if 'coupon' in session:
#     discount = (session['coupon']['discount_percentage']/100) * subtotal
#     subtotal -= discount