from flask import Blueprint

tablas_bp = Blueprint('tablas', __name__)

from . import routes
