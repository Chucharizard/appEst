from flask import Blueprint

graficos_bp = Blueprint('graficos', __name__)

from . import routes
