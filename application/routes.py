from application import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import LoginManager, logout_user, login_user, current_user, login_required
from .forms import LoginForm, RegistrationForm, CartForm
from application import models
from .models import Product, Cart, User

# route for the home page
@app.route('/')
def home():
    return render_template('home.html', title="CMPTR")


# route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # checks the password matches the one in the database
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('wrong password or email')
        else:
            # logs the user in
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)


# route for the register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data)
        user.set_password(form.password.data)
        # add the form to the database
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# route for the logout page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# route for the individual product page
@app.route('/product')
def product():
    product = Product.query.all()
    return render_template('product.html', product=product)


# route for the individual product page
@app.route('/product/<int:id>')
def productid(id):
    productid = Product.query.filter_by(id=id)
    return render_template('productid.html', productid=productid)


# route to add an item from the cart
@app.post('/add/<int:product_id>')
@login_required
def add(product_id):
    # retrieves the id of the product
    cart_item = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        # adds the id and the user id to the cart table
        db.session.add(cart_item)
        db.session.add(current_user.id)
        db.session.commit()
    return redirect(url_for('cart'))
 

# route for the cart page
@app.route('/cart')
def cart():
    u_id = current_user.id
    # queries for the product ids that match the current user in the cart able
    subquery = db.session.query(Cart.product_id).filter_by(user_id=u_id).subquery()
    # queries for the data from the product table where the id matches that which is in the cart
    cart = Product.query.filter(Product.id.in_(subquery)).all()
    return render_template('cart.html', cart=cart)


# route to delete an item from the cart
@app.post('/delete/<string:id>')
def delete():
    #queries for the id of the cart
    remove_product = Cart.query.filter_by(id=Cart.id).first()
    db.session.delete(remove_product)
    db.session.commit()
    return redirect(url_for('cart'))


# 404 ERROR page route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


#route for the cpu search filter
@app.route('/cpu')
def cpu():
    cpu = Product.query.filter(Product.category_id=="1")
    return render_template('cpu.html', cpu=cpu)


#route for the gpu search filter
@app.route('/gpu')
def gpu():
    gpu = Product.query.filter(Product.category_id=="2")
    return render_template('gpu.html', gpu=gpu)


#route for the mb search filter
@app.route('/mb')
def mb():
    mb = Product.query.filter(Product.category_id=="3")
    return render_template('mb.html', mb=mb)


#route for the ssd search filter
@app.route('/ssd')
def ssd():
    ssd = Product.query.filter(Product.category_id=="4")
    return render_template('storage.html', ssd=ssd)


#route for the ram search filter
@app.route('/ram')
def ram():
    ram = Product.query.filter(Product.category_id=="5")
    return render_template('memory.html', ram=ram)


#route for the psu search filter
@app.route('/psu')
def psu():
    psu = Product.query.filter(Product.category_id=="6")
    return render_template('psu.html', psu=psu)


#route for the case search filter
@app.route('/case')
def case():
    case = Product.query.filter(Product.category_id=="7")
    return render_template('case.html', case=case)



