import os, shutil

from flask import render_template,session, request,redirect,url_for,flash, Blueprint
from werkzeug.utils import secure_filename

from shop import db, bcrypt
from shop.forms import AdminRegistrationForm, AdminLoginForm, ProductForm
from shop.models import Product, Category, Brand, Admin
from shop.utils import brands, categories

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    return render_template('admin/dashboard.html', username=username)


@admin.route('/admina/register', methods=['GET', 'POST'])
def register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Admin(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        flash(f'Welcome {form.username.data}! Thanks for registering.', 'success')
        db.session.commit()
        return redirect(url_for('admin.login'))
    return render_template('auth/admins/register.html',title='Register user', form=form)


@admin.route('/admin/login', methods=['GET','POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            session['username'] = user.username#request.form['username']
            # flash(f'Welcome {form.email.data}! You are logged in now.', 'success')
            print(user.username)
            flash(f'Welcome {user.username}! You are logged in now.', 'success')
            return redirect(url_for('admin.dashboard'))  
        else:
            flash('Wrong email and password.', 'danger')
            # return redirect(url_for('admin.register'))
    return render_template('auth/admins/login.html', title='Admin Login Page', form=form)    


@admin.route('/admin/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('admin.login'))

@admin.route('/admin/brands', methods=['GET'])
def brands():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brands/listbrands.html', title='brands',brands=brands, username=username)


@admin.route('/admin/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The brand {getbrand} was added to your database','success')
        return redirect(url_for('admin.addbrand'))
    return render_template('admin/brands/addbrands.html', title='Add brand',brands='brands', username=username)

@admin.route('/admin/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        db.session.commit()
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        return redirect(url_for('admin.brands'))
    brand = updatebrand.name
    return render_template('admin/brands/updatebrands.html', username=username, title='Update brand',brands='brands',updatebrand=updatebrand)


@admin.route('/admin/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin.dashbord'))


@admin.route('/admin/categories', methods=['GET'])
def categories():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories/listcategories.html',username=username, title='categories',categories=categories)


@admin.route('/admin/addcategory', methods=['GET','POST'])
def addcategory():
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    if request.method =="POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        db.session.commit()
        flash(f'The brand {getcategory} was added to your database','success')
        return redirect(url_for('admin.addcategory'))
    return render_template('admin/categories/addcategories.html', username=username, title='Add category')


@admin.route('/admin/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecategory.name = category
        db.session.commit()
        flash(f'The category {updatecategory.name} was changed to {category}','success')
        return redirect(url_for('admin.categories'))
    category = updatecategory.name
    return render_template('admin/categories/updatecategories.html',username=username, title='Update cat',updatecategory=updatecategory)



@admin.route('/admin/deletecategory/<int:id>', methods=['GET','POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@admin.route('/admin/productlist', methods=['GET'])
def productlist():
    if 'email' not in session:
            flash('Login first please','danger')
            return redirect(url_for('admin.login'))
    username = session['username']
    products = Product.query.all()
    return render_template('admin/products/listproduct.html', username=username, title='Admin page',products=products)

@admin.route('/admin/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
            flash('Login first please','danger')
            return redirect(url_for('admin.login'))
    username = session['username']
    form = ProductForm()

    # Populate choices for categories and brands
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.brand.choices = [(brand.id, brand.name) for brand in Brand.query.all()]

    if form.validate_on_submit():
        # Get the Category and Brand instances from the database
        category = Category.query.get(form.category.data)
        brand = Brand.query.get(form.brand.data)

        # Create a new product instance and populate it with form data
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            discount=form.discount.data,
            stock=form.stock.data,
            # colors=form.colors.data,
            desc=form.desc.data,
            category= category, #form.category.data,
            brand= brand #form.brand.data
        )
        # Save the new product to the database
        db.session.add(new_product)
        db.session.commit()

        # Create a directory for the product in /static/uploads if it doesn't exist
        os.makedirs(os.path.join('shop/static', 'uploads', str(new_product.id)), exist_ok=True)

        # Save the images to the new directory and update the product with the image filenames
        # for i in range(1, 6):
        #     image = request.files.get(f'image_{i}')
        #     if image:
        #         filename = secure_filename(image.filename)
        #         image.save(os.path.join('static', 'uploads', str(new_product.id), filename))
        #         setattr(new_product, f'image_{i}', filename)

        # Save the images to the new directory and update the product with the image filenames
        image_1 = request.files.get('image_1')
        if image_1:
            filename = secure_filename(image_1.filename)
            image_1.save(os.path.join('static', 'uploads', str(new_product.id), filename))
            new_product.image_1 = filename
        
        image_2 = request.files.get('image_2')
        if image_2:
            filename = secure_filename(image_2.filename)
            image_2.save(os.path.join('static', 'uploads', str(new_product.id), filename))
            new_product.image_2 = filename
        
        image_3 = request.files.get('image_3')
        if image_3:
            filename = secure_filename(image_3.filename)
            image_3.save(os.path.join('static', 'uploads', str(new_product.id), filename))
            new_product.image_3 = filename

        image_4 = request.files.get('image_4')
        if image_4:
            filename = secure_filename(image_4.filename)
            image_4.save(os.path.join('static', 'uploads', str(new_product.id), filename))
            new_product.image_4 = filename

        image_5 = request.files.get('image_5')
        if image_5:
            filename = secure_filename(image_5.filename)
            image_5.save(os.path.join('static', 'uploads', str(new_product.id), filename))
            new_product.image_5 = filename

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another view
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/products/addproduct.html', username=username, form=form)

@admin.route('/admin/updateproduct/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    username = session['username']
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    # Populate choices for categories and brands
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.brand.choices = [(brand.id, brand.name) for brand in Brand.query.all()]

    if form.validate_on_submit():
        # Get the Category and Brand instances from the database
        category = Category.query.get(form.category.data)
        brand = Brand.query.get(form.brand.data)

        # Update the product instance with form data
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.desc = form.desc.data
        product.category = category
        product.brand = brand

        # Save the images to the new directory and update the product with the image filenames
        image_1 = request.files.get('image_1')
        if image_1:
            filename = secure_filename(image_1.filename)
            image_1.save(os.path.join('static', 'uploads', str(product.id), filename))
            product.image_1 = filename

        image_2 = request.files.get('image_2')
        if image_2:
            filename = secure_filename(image_2.filename)
            image_2.save(os.path.join('static', 'uploads', str(product.id), filename))
            product.image_2 = filename

        image_3 = request.files.get('image_3')
        if image_3:
            filename = secure_filename(image_3.filename)
            image_3.save(os.path.join('static', 'uploads', str(product.id), filename))
            product.image_3 = filename

        image_4 = request.files.get('image_4')
        if image_4:
            filename = secure_filename(image_4.filename)
            image_4.save(os.path.join('static', 'uploads', str(product.id), filename))
            product.image_4 = filename

        image_5 = request.files.get('image_5')
        if image_5:
            filename = secure_filename(image_5.filename)
            image_5.save(os.path.join('static', 'uploads', str(product.id), filename))
            product.image_5 = filename

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another view
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/products/updateproduct.html', username=username, form=form, product=product)

# @admin.route('/admin/updateproduct/<int:product_id>', methods=['GET', 'PATCH'])
# def update_product(product_id):
#     if 'email' not in session:
#         flash('Login first please','danger')
#         return redirect(url_for('admin.login'))
#     username = session['username']
#     product = Product.query.get_or_404(product_id)
#     form = ProductForm(obj=product)

#     # Populate choices for categories and brands
#     form.category.choices = [(category.id, category.name) for category in Category.query.all()]
#     form.brand.choices = [(brand.id, brand.name) for brand in Brand.query.all()]

#     if request.method == 'PATCH':
#         if form.validate_on_submit():
#             # Get the Category and Brand instances from the database
#             category = Category.query.get(form.category.data)
#             brand = Brand.query.get(form.brand.data)

#             # Update the product instance with form data
#             product.name = form.name.data
#             product.price = form.price.data
#             product.discount = form.discount.data
#             product.stock = form.stock.data
#             product.desc = form.desc.data
#             product.category = category
#             product.brand = brand

#             # Save the images to the new directory and update the product with the image filenames
#             image_1 = request.files.get('image_1')
#             if image_1:
#                 filename = secure_filename(image_1.filename)
#                 image_1.save(os.path.join('static', 'uploads', str(product.id), filename))
#                 product.image_1 = filename

#             image_2 = request.files.get('image_2')
#             if image_2:
#                 filename = secure_filename(image_2.filename)
#                 image_2.save(os.path.join('static', 'uploads', str(product.id), filename))
#                 product.image_2 = filename

#             image_3 = request.files.get('image_3')
#             if image_3:
#                 filename = secure_filename(image_3.filename)
#                 image_3.save(os.path.join('static', 'uploads', str(product.id), filename))
#                 product.image_3 = filename

#             image_4 = request.files.get('image_4')
#             if image_4:
#                 filename = secure_filename(image_4.filename)
#                 image_4.save(os.path.join('static', 'uploads', str(product.id), filename))
#                 product.image_4 = filename

#             image_5 = request.files.get('image_5')
#             if image_5:
#                 filename = secure_filename(image_5.filename)
#                 image_5.save(os.path.join('static', 'uploads', str(product.id), filename))
#                 product.image_5 = filename


#             # Commit the changes to the database
#             db.session.commit()

#             # Redirect to a success page or another view
#             return redirect(url_for('admin.dashboard'))

#     return render_template('admin/products/updateproduct.html', username=username, form=form, product=product)


@admin.route('/admin/deleteproduct/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('admin.login'))
    product = Product.query.get_or_404(product_id)

    # Delete the product's image directory
    shutil.rmtree(os.path.join('static', 'uploads', str(product.id)))

    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('admin.productlist'))
