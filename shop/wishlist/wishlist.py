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
    pass


@wishlists.route('/wishlist')
def getWishlist():
    return render_template('wishlist/wishlist.html', title='wishlist')


@wishlists.route('/wishlist/<int:code>', methods=['POST'])
def updateWishlist():
    pass


@wishlists.route('/wishlist<int:id>')
def deleteWishlist():
    pass



@wishlists.route('/clearwishlist')
def clearWishlist():
    pass
