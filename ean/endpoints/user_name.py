from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token

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

        args['name'] = str(args['name'])

        with db:
            with db.cursor() as cursor:
                id = id_from_token(args['token'])

                if id is None:
                    cursor.execute("INSERT INTO users (token, name) VALUES (%s, %s)",
                                   [args['token'], args['name']])
                    return None, 201
                else:
                    cursor.execute("UPDATE users SET name=%s WHERE id=%s",
                                   [args['name'], id])
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
