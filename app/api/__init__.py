from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api import concept, learning, memory

from . import routes 