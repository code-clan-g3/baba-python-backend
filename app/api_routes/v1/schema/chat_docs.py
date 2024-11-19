from flask_restx import fields

from app.extensions import api

new_message_model = api.model("NewMessage", {
    "message": fields.String(required=True, example="Hello World!"),
})