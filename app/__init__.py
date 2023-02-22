from flask import Flask, flash, redirect, url_for, render_template
from sqlalchemy import MetaData 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_session import Session
from config import config

convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData( naming_convention = convention) 

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
mail = Mail()
sess = Session()

def create_app(config_name="default"):
    print(str(config_name))
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app,db,render_as_batch=True)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    with app.app_context():
        # Imports
        from .main import main_blueprint
        app.register_blueprint(main_blueprint, url_prefix='/')

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .post import posts_blueprint
        app.register_blueprint(posts_blueprint, url_prefix='/posts')

        from .product import products_blueprint
        app.register_blueprint(products_blueprint, url_prefix='/products')
        
        return app