from application import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    cartuser = db.relationship('Cart', backref='User',  primaryjoin="User.id == Cart.user_id")


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User{}>'.format(self.email)
    

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    info = db.Column(db.Text, nullable=False)
    image = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    cartitem = db.relationship('Cart', backref='Product',  primaryjoin="Product.id == Cart.product_id")


class Category(db.Model):
   __tablename__ = "category"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable=False, unique=True)
   info = db.Column(db.Text, nullable=False)
   product = db.relationship('Product', backref='Category',  primaryjoin="Category.id == Product.category_id")


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))