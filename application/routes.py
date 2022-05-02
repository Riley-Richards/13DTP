from application import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import LoginManager, logout_user, login_user, current_user, login_required
from .forms import LoginForm, RegistrationForm
from application import models


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


# 404 ERROR page route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


# about page route
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gpus')
def gpu():
    return render_template('gpu.html')


@app.route('/cpus')
def cpu():
    return render_template('cpu.html')


@app.route('/motherboard')
def mb():
    return render_template('mb.html')


@app.route('/memory')
def memory():
    return render_template('memory.html')


@app.route('/storage')
def storage():
    return render_template('storage.html')


@app.route('/psus')
def psu():
    return render_template('psu.html')


@app.route('/case')
def case():
    return render_template('case.html')