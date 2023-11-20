# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present juniorbesong
"""

import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
# from flask_uploads import UploadSet, con figure_uploads, IMAGES, patch_request_class
# from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate
from importlib import import_module
from .config import BaseConfig




db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
# search = Search()

login_manager = LoginManager()
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"



def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # search.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)


# Setup database
def configure_database(app):

    @app.before_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            BASE_DIR =  os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'platformdb.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)
#     mail.init_app(app)
    register_extensions(app)
    configure_database(app)

    # photos = UploadSet('photos', IMAGES)
    # configure_uploads(app, photos)
    # patch_request_class(app)

    # from flaskblog.users.routes import users
    # from flaskblog.posts.routes import posts
    from shop.main.routes import main
    from shop.error.handler import errors
    from shop.auth.routes import auth
    from shop.products.routes import product
    # app.register_blueprint(users)
    # app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(product)

    return app


































# @app.route('/cart')
# def carts():
#     return render_template('cart/carts.html')

# @app.route('/wishlist')
# def wishlist():
#     return render_template('wishlist/wishlist.html')

# @app.route('/compare')
# def compare():
#     return render_template('products/compare.html')

# @app.route('/checkout')
# def checkout():
#     return render_template('checkout/checkout.html')



# from shop.customers import routes

# @app.route('/login')
# def login():
#    return render_template('auth/customer/signin.html')
    

# @app.route('/register')
# def register():
#     return render_template('auth/customer/signup.html')
    





# @app.route('/product-details')
# def productdetails():
#     return render_template('products/product-details.html')

# @app.route('/product-list')
# def productlist():
#     return render_template('products/shop-list.html')


# import / load all routes or endpoints here! 

 