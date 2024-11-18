from flask_restx import fields

from app.extensions import api

sign_up_model = api.model('SignUp', {
    "full_name": fields.String(required=True, example="<NAME>"),
    'email': fields.String(description='Email address', example='<EMAIL>'),
    'password': fields.String(description='Password', example='<PASSWORD>'),
})

login_model = api.model('Login', {
    "email": fields.String(description='Email address', example='<EMAIL>'),
    "password": fields.String(description='Password', example='<PASSWORD>'),
})