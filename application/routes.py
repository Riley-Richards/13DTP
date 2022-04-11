from application import app
from flask import render_template


@app.route('/')
def home():
    return render_template('home.html', title="Home")


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