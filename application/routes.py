from application import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import LoginManager, logout_user, login_user, current_user, login_required
from .forms import LoginForm, RegistrationForm, CartForm
from application import models
from .models import Product, Cart, User

@app.route('/')
def home():
    return render_template('home.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('wrong password or email')
        else:
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/product/<int:id>')
def productid(id):
    productid = Product.query.filter_by(id=id)
    return render_template('productid.html', productid=productid)

@app.post('/<int:product_id>/add/')
@login_required
def add(product_id):
    cart_item = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        new_cart = request.form['id']
        cart.product=new_cart
        db.session.add(cart_item)
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('cart'))
 

@app.route('/cart')
def cart():
    u_id = current_user.id
    subquery = db.session.query(Cart.product_id).filter_by(user_id=u_id).subquery()
    cart = Product.query.filter(Product.id.in_(subquery)).all()
    return render_template('cart.html', cart=cart)


@app.post('/delete/<string:id>')
def delete(id):
    remove_product = Cart.query.filter_by(id=int(id)).first()
    db.session.delete(remove_product)
    db.session.commit()
    return redirect(url_for('cart'))




# 404 ERROR page route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


# about page route
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/cpu')
def cpu():
    cpu = Product.query.filter(Product.category_id=="1")
    return render_template('cpu.html', cpu=cpu)


@app.route('/gpu')
def gpu():
    gpu = Product.query.filter(Product.category_id=="2")
    return render_template('gpu.html', gpu=gpu)


@app.route('/mb')
def mb():
    mb = Product.query.filter(Product.category_id=="3")
    return render_template('mb.html', mb=mb)


@app.route('/ssd')
def ssd():
    ssd = Product.query.filter(Product.category_id=="4")
    return render_template('storage.html', ssd=ssd)


@app.route('/ram')
def ram():
    ram = Product.query.filter(Product.category_id=="5")
    return render_template('memory.html', ram=ram)


@app.route('/psu')
def psu():
    psu = Product.query.filter(Product.category_id=="6")
    return render_template('psu.html', psu=psu)


@app.route('/case')
def case():
    case = Product.query.filter(Product.category_id=="7")
    return render_template('case.html', case=case)


@app.route('/product')
def product():
    product = Product.query.all()
    return render_template('product.html', product=product)
