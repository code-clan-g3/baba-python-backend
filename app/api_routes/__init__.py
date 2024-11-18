from flask import Blueprint

from app.api_routes.v1.resources.auth import auth_ns
from app.extensions import api
from openai import OpenAI

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)

api.add_namespace(auth_ns, path='/auth')

