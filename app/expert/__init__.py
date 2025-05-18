from flask import Blueprint

bp = Blueprint('expert', __name__)

from app.expert import routes
