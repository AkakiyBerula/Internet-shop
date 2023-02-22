from flask import Blueprint, Flask, url_for, render_template, abort, make_response, request, session
from sqlalchemy import MetaData 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound

auth_blueprint = Blueprint('auth', __name__, template_folder="templates/auth")

from . import views