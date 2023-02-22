from os import environ, path
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'thesecretkey132'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = "6LcI6yEjAAAAALFm0sXu5fJS7yPfLt98Gz9VMCFn"
    RECAPTCHA_PRIVATE_KEY = "6LcI6yEjAAAAADhd7NpdvF6qD-8wYkpp4WNbGMnD"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'vlad5dyakun@gmail.com'
    MAIL_PASSWORD = 'txllkyvyukajvuhe'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')
    RECAPTCHA_PUBLIC_KEY = "6LcI6yEjAAAAALFm0sXu5fJS7yPfLt98Gz9VMCFn"
    RECAPTCHA_PRIVATE_KEY = "6LcI6yEjAAAAADhd7NpdvF6qD-8wYkpp4WNbGMnD"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'vlad5dyakun@gmail.com'
    MAIL_PASSWORD = 'txllkyvyukajvuhe'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"


class ProdConfig(Config):
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'site.db')
    RECAPTCHA_PUBLIC_KEY = "6LcI6yEjAAAAALFm0sXu5fJS7yPfLt98Gz9VMCFn"
    RECAPTCHA_PRIVATE_KEY = "6LcI6yEjAAAAADhd7NpdvF6qD-8wYkpp4WNbGMnD"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'vlad5dyakun@gmail.com'
    MAIL_PASSWORD = 'txllkyvyukajvuhe'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig
}