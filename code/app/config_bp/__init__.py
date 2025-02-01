from flask import Blueprint

config_blueprint = Blueprint('config_bp', __name__, template_folder='templates')

from . import routes
