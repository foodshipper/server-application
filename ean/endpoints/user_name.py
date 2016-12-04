from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token, get_or_create_id

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)
parser.add_argument('name', required=False)


class UserName(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        if args['name'] is None:
            return abort(400, message="Invalid Arguments")

        name = args['name']

        with db:
            with db.cursor() as cursor:
                user_id = get_or_create_id(args['token'])
                cursor.execute("UPDATE users SET name=%s WHERE id=%s",
                               [name, user_id[0]])
                if user_id[1]:
                    return None, 201
                else:
                    return None, 200

    def get(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                cursor.execute("SELECT name FROM users WHERE id=%s", [id_from_token(args['token'])])
                query = cursor.fetchone()
                if query is None:
                    return None, 404
                else:
                    return {
                        "name": query[0]
                    }
