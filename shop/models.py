# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present juniorbesong
"""

from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer, TimedSerializer as Serializers 
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), unique = False)
    date_created = db.Column(db.DateTime, nullable =False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name
    
    def get_reset_token(self, expires_sec=3600):
        # s =  Serializer(current_app.config['SECRET_KEY'], expires_sec)
        s =  Serializers(current_app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.id}).decode('utf-8')
        return s.dumps({'user_id': self.id}, salt=current_app.config['SECURITY_PASSWORD_SALT']) #.decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        # s = Serializer(current_app.config['SECRET_KEY'])
        s = Serializers(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,salt=current_app.config['SECURITY_PASSWORD_SALT'])[' user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class UserOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


class Product(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    # colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')
    image_4 = db.Column(db.String(150), nullable=False, default='image4.jpg')
    image_5 = db.Column(db.String(150), nullable=False, default='image5.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username

# class BillingDetails(db.Model):
#     pass 

# db.create_all()

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(80), unique=True, nullable=False)
    discount_percentage = db.Column(db.Integer)
