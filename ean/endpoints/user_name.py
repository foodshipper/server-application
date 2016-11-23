from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True)
parser.add_argument('name', required=False)


class UserName(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        if args['name'] is None:
            return abort(400, message="Invalid Arguments")

        with db:
            with db.cursor() as cursor:
                cursor.execute("SELECT name FROM users WHERE user_id=%s", [args['user_id']])
                query = cursor.fetchone()
                if query is None:
                    cursor.execute("INSERT INTO users (user_id, name) VALUES (%s, %s)",
                                   [args['user_id'], args['name']])
                    return None, 201
                else:
                    cursor.execute("UPDATE users SET name=%s WHERE user_id=%s",
                                   [args['name'], args['user_id']])
                    return None, 200

    def get(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                cursor.execute("SELECT name FROM users WHERE user_id=%s", [args['user_id']])
                query = cursor.fetchone()
                if query is None:
                    return None, 404
                else:
                    return {
                        "name": query[0]
                    }
