from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app
from shop.models import Product, UserOrder, JsonEcodedDict
from shop.products.routes import brands, categories
import json

checkout = Blueprint('checkout', __name__)

@checkout.route('/checkout')
# @login_required
def getorder():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart
        try:
            order = UserOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('carts.getcart'))


@checkout.route('/orders/<invoice>')
# @login_required
def orders(invoice):
    # if current_user.is_authenticated:
    #     grandTotal = 0
    #     subTotal = 0
    #     customer_id = current_user.id
    #     customer = User.query.filter_by(id=customer_id).first()
    #     orders = UserOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(UserOrder.id.desc()).first()
    #     for _key, product in orders.orders.items():
    #         discount = (product['discount']/100) * float(product['price'])
    #         subTotal += float(product['price']) * int(product['quantity'])
    #         subTotal -= discount
    #         tax = ("%.2f" % (.06 * float(subTotal)))
    #         grandTotal = ("%.2f" % (1.06 * float(subTotal)))
    # else:
    #     return redirect(url_for('auth.login'))
    return render_template('checkout/checkout.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)



