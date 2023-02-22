from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_blueprint = Blueprint('main', __name__, template_folder="templates/main")

from . import views