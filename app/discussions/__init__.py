from flask import Blueprint

bp = Blueprint("discussions", __name__, template_folder='templates')

from app.discussions import routes