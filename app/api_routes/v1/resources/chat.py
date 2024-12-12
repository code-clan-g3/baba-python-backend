from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from app.api_routes.v1 import wait_for_run_completion
from app.api_routes.v1.schema.chat_docs import new_message_model, parser
from app.extensions import client, db
from app.models import Chat, User

chat_ns = Namespace('chat', description='Chat operations')

@chat_ns.route("/thread")
class ChatThread(Resource):
    @jwt_required()
    @chat_ns.expect(parser)
    def get(self):
        user_id = get_jwt_identity()
        new_thread = client.beta.threads.create(
            metadata={
                "user_id": str(user_id),
            }
        )

        new_chat = Chat(
            user_id=user_id,
            thread_id=new_thread.id,
        )
        db.session.add(new_chat)
        db.session.commit()

        return {"message": "Thread created", "thread_id": str(new_thread.id)}, 201


@chat_ns.route('/<string:thread_id>')
class Chats(Resource):
    @chat_ns.expect(parser)
    @jwt_required()
    def get(self, thread_id):
        messages =  client.beta.threads.messages.list(thread_id)
        print(messages.to_dict())
        return messages.to_dict()

    @jwt_required()
    @chat_ns.expect(new_message_model, parser)
    def post(self, thread_id):
        new_message = request.get_json()['message']
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=new_message)

        chat =  Chat.query.filter_by(thread_id=thread_id).first()
        if chat.chat_name is None:
            chat.chat_name = new_message
            db.session.commit()

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            model = "gpt-4o",
            assistant_id="asst_RdAYEvGJ2PmGjkV3d3HjbFqs"
        )


        return {
            "message": "success",
            "response": wait_for_run_completion(client, thread_id, run.id, sleep_time=2)
        }

@chat_ns.route("/get_threads")
class GetChats(Resource):
    @chat_ns.expect(parser)
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        print(user_id)
        user = User.query.filter_by(id=user_id).first()
        data = []
        chats_query = user.chats

        for chat in chats_query:
            if chat.chat_name is not None:
                data.append({
                    "id": str(chat.id),
                    "chat_name": chat.chat_name,
                    "thread_id": chat.thread_id,
                })
        print(data)

        return {"message":data}










