from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError,IntegerField,FloatField, DecimalField, SelectField
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from .models import User, Admin

class UserRegistrationForm(FlaskForm):
    # name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    # password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm_password', message=' Both password must match! ')])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm_password', message=' Both password must match! ')])
    confirm_password = PasswordField('Repeat Password: ', [validators.DataRequired()])
    # terms = BooleanField('Terms of service and Privacy')
    terms = BooleanField('I accept the terms of the Services & Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class UserBillingForm(FlaskForm):
    pass
#     firstname = StringField('Name: ')
#     lastname = StringField('Username: ', [validators.DataRequired()])
#     email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
#     country = StringField('Country: ', [validators.DataRequired()])
#     city_state = StringField('City: ', [validators.DataRequired()])
#     contact = StringField('Contact: ', [validators.DataRequired()])
#     address = StringField('Address: ', [validators.DataRequired()])
#     zipcode = StringField('Zip code: ', [validators.DataRequired()])



class UserUpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    


class UserLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


   


class UserDeliveryForm(FlaskForm):
    pass


class Addproducts(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_4 = FileField('Image 4', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_5 = FileField('Image 5', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=80)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', validators=[DataRequired()])
# colors = StringField('Colors', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)  # to be populated with categories from the database
    brand = SelectField('Brand', coerce=int)  # to be populated with brands from the database
    # image_1 = StringField('Image 1', default='image1.jpg')
    # image_2 = StringField('Image 2', default='image2.jpg')
    # image_3 = StringField('Image 3', default='image3.jpg')
    # image_4 = StringField('Image 4', default='image4.jpg')
    # image_5 = StringField('Image 5', default='image5.jpg')
    image_1 = FileField('Image 1')
    image_2 = FileField('Image 2')
    image_3 = FileField('Image 3')
    image_4 = FileField('Image 4')
    image_5 = FileField('Image 5')
    submit = SubmitField('Submit')

class AdminRegistrationForm(FlaskForm):
    '''admin registration  form'''

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

        
    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            

class AdminLoginForm(FlaskForm):
    '''admin login  form '''
    # email = StringField('Email Address', [validators.Length(min=6, max=35)])
    # password = PasswordField('New Password', [validators.DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')