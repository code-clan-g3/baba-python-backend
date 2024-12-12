from flask_restx import fields

from app.extensions import api

parser = api.parser()
parser.add_argument(
    'Authorization',
    type=str,
    location='headers',
    required=True,
    help='Bearer Token',
)


new_message_model = api.model("NewMessage", {
    "message": fields.String(required=True, example="Hello World!"),
})