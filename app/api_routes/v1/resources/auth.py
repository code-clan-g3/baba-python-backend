from venv import create

from flask import request
from flask_restx import Namespace, Resource

from app.extensions import bcrypt, db
from app.api_routes.v1.schema.auth_docs import sign_up_model, login_model
from app.models import SignUpForm, User, LoginForm, Chat
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import client

auth_ns = Namespace('auth', description='Auth endpoints')


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(sign_up_model)
    def post(self):
        form = SignUpForm(data=request.get_json())

        if not form.validate():
            print(form.errors)
            for error in form.errors:
                return {"error": f"{error}:{form.errors[error]}"}, 400

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            return {"error": "email already in use"}, 400

        new_user = User(
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            full_name=form.full_name.data
        )

        db.session.add(new_user)
        db.session.commit()



        new_thread = client.beta.threads.create(
            metadata={
                "user_id": str(new_user.id),
            }
        )

        new_chat = Chat(
            user_id=new_user.id,
            thread_id=new_thread.id,
        )
        db.session.add(new_chat)
        db.session.commit()

        token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)

        return {'message': 'successfully registered', 'token': str(token), 'refresh_token': str(refresh_token), "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "full_name": new_user.full_name,
        },
                "chat": {
                    "thread_id": str(new_chat.thread_id),
                }
                }, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        form = LoginForm(data=request.get_json())

        if not form.validate():
            print(form.errors)
            for error in form.errors:
                return {"error": f"{error}:{form.errors[error]}"}, 400

        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return {"error": "user doesn't exist"}, 400

        if not bcrypt.check_password_hash(user.password, form.password.data):
            return {"error": "wrong password"}, 400

        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        new_thread = client.beta.threads.create(
            metadata={
                "user_id": str(user.id),
            }
        )

        new_chat = Chat(
            user_id=user.id,
            thread_id=new_thread.id,
        )

        db.session.add(new_chat)
        db.session.commit()

        return {
            "message": "successfully logged in",
            "token": token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
            },
            "chat": {
                "thread_id": str(new_chat.thread_id),
            }
        }



