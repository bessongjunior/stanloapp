from flask import render_template, request, Blueprint
from shop.models import Product


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # return render_template('home.html', posts=posts)
    return render_template('main/index.html')



@main.route('/about')
def about():
    return render_template('main/about.html', title='About')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # messages = Messages(name=username, email=email, subject=subject, message=message)
        # db.session.add(messages)
        # db.session.commit()
        # print(name,email,subject,message)
        # flash('Registered successfully')
        return render_template('main/contact.html', title='contact')
    return render_template('main/contact.html', title='contact')

@main.route('/faq')
def faq():
    # return render_template('main/faq.html', title='faq')
    return 'faq page!!!'

@main.route('/terms')
def terms():
    return render_template('main/terms.html', title='terms & conditions')

@main.route('/privacy')
def privacy():
    return 'Privacy policy page!!!'

@main.route('/return-exchange')
def returnExchange():
    return 'Return Exchange page!!!'
