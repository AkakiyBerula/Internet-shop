import enum
from .. import db


class Producttypes(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique = True)
    product = db.relationship('Products', backref='my_product_types', lazy=True)


class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(8), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(70), nullable=False, default='postdefault.png')
    is_on_storage = db.Column(db.Boolean(), nullable=False)
    variety = db.Column(db.Integer(), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    info = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())
    type = db.Column(db.Integer(), db.ForeignKey('producttypes.type_id'), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    ratings = db.relationship('Ratings', backref='my_ratings', lazy=True)

    def __repr__(self):
        return f"Products('{self.id}', '{self.name}', {self.variety})"

class Ratings(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    comment = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime(), default=db.func.now())

    def __repr__(self):
        return f"Ratings('{self.id}', '{self.rating}', {self.comment}, '{self.date}')"

'''class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    order = db.Column(db.String(50), nullable=False)
    variety = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=True)
    card_code  = db.Column(db.Integer(), nullable=True)
    number_phone = db.Column(db.String(14), nullable=True)
    date = db.Column(db.DateTime(), default=db.func.now())'''


