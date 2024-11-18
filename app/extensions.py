from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restx import Api
from openai import OpenAI

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()
client = OpenAI()

