from flask_restful import Resource, abort, reqparse

from database import db

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True)
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
                cursor.execute("SELECT location FROM users WHERE user_id=%s", [args['user_id']])
                query = cursor.fetchone()
                if query is None:
                    cursor.execute("INSERT INTO users (user_id, location) VALUES (%s, ST_MakePoint(%s, %s))",
                                   [args['user_id'], args['lon'], args['lat']])
                    return None,201
                else:
                    cursor.execute("UPDATE users SET location=ST_MakePoint(%s, %s) WHERE user_id=%s",
                                   [args['lon'], args['lat'], args['user_id']])
                    return None,200
