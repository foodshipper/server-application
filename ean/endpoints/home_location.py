from flask_restful import Resource, abort, reqparse

from ean.database import db
from ean.user import id_from_token

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)
parser.add_argument('lon', required=True)
parser.add_argument('lat', required=True)


class HomeLocation(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except Exception as e:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                id = id_from_token(args['token'])
                if id is None:
                    cursor.execute("INSERT INTO users (token, location) VALUES (%s, ST_MakePoint(%s, %s))",
                                   [args['token'], args['lon'], args['lat']])
                    return None,201
                else:
                    cursor.execute("UPDATE users SET location=ST_MakePoint(%s, %s) WHERE id=%s",
                                   [args['lon'], args['lat'], id])
                    return None,200
