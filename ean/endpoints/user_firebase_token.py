from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import get_or_create_id

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
                user_id = get_or_create_id(args['token'])

                cursor.execute(u"UPDATE users SET firebase_token=%s WHERE id=%s",
                               [args['firebase_token'], user_id[0]])

                if user_id[1]:
                    return None, 201
                else:
                    return None, 200
