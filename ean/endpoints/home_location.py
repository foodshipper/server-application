from flask_restful import Resource, abort, reqparse

from ean.database import db
from ean.user import get_or_create_id

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)
parser.add_argument('lon', required=True)
parser.add_argument('lat', required=True)


class HomeLocation(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except Exception:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = get_or_create_id(args['token'])
                cursor.execute("UPDATE users SET longitude=%s, latitude=%s WHERE id=%s",
                               [args['lon'], args['lat'], user_id[0]])
                if user_id[1]:
                    return None, 201
                else:
                    return None, 200
