from flask import request
from flask_restx import Namespace, Resource

from app.api_routes.v1 import wait_for_run_completion
from app.api_routes.v1.schema.chat_docs import new_message_model
from app.extensions import client

chat_ns = Namespace('chat', description='Chat operations')

@chat_ns.route('/chat/<string:thread_id>')
class Chat(Resource):
    def get(self, thread_id):
        messages =  client.beta.threads.messages.list(thread_id)
        return messages.to_dict()

    @chat_ns.expect(new_message_model)
    def post(self, thread_id):
        new_message = request.get_json()['message']
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=new_message)

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            model = "gpt-4o",
            assistant_id="asst_RdAYEvGJ2PmGjkV3d3HjbFqs"
        )

        return {
            "message": "success",
            "response": wait_for_run_completion(client, thread_id, run.id, sleep_time=2)
        }



