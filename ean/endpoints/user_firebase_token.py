from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token

parser = reqparse.RequestParser()
parser.add_argument('firebase_token', required=True)
parser.add_argument('token', required=True)


class UserFirebaseToken(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = id_from_token(args['token'])

                if user_id is None:
                    cursor.execute(u"INSERT INTO users (token, firebase_token) VALUES (%s, %s)",
                                   [args['token'], args['firebase_token']])
                    return None, 201
                else:
                    cursor.execute(u"UPDATE users SET firebase_token=%s WHERE id=%s",
                                   [args['firebase_token'], user_id])
                    return None, 200