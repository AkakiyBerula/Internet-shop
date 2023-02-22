from .. import db, SQLAlchemy, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import enum

class UserType(enum.Enum):
    User = 1
    Moderator = 2
    Admin = 3

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    lastname = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(70), nullable=False, default = 'default.png')
    about_me = db.Column(db.Text, default="Добавте інформацію про себе")
    number_phone = db.Column(db.String(14), nullable=True)
    usertype = db.Column(db.Enum(UserType), default="User")
    rating = db.relationship('Ratings', backref='my_backref_types', lazy=True)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __init__(self, username, name, lastname, email, password, number_phone, usertype = "User"):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)  
        self.number_phone = number_phone 
        self.usertype = usertype 
       

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)