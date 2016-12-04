from flask_restful import Resource, reqparse, abort

from ean.database import db
from ean.endpoints.products import Product
from ean.user import get_or_create_id, id_from_token

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)


class FridgeOverview(Resource):
    def get(self):
        try:
            args = parser.parse_args()
        except Exception:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = get_or_create_id(args['token'])

                cursor.execute(
                    "SELECT fridge_items.ean, products.name, products.type FROM fridge_items"
                    " JOIN products ON products.ean=fridge_items.ean"
                    " WHERE fridge_items.user_id=%s",
                    [user_id[0]])
                response = []
                for item in cursor.fetchall():
                    response.append({'ean': item[0],
                                     'name': item[1],
                                     'type': item[2]})
                return response, 200


class FridgeItem(Resource):
    def put(self, ean):
        try:
            args = parser.parse_args()
        except Exception:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = get_or_create_id(args['token'])

                cursor.execute(
                    "SELECT products.name, products.type FROM fridge_items"
                    " JOIN products ON products.ean=fridge_items.ean"
                    " WHERE fridge_items.user_id=%s AND fridge_items.ean=%s",
                    [user_id[0], ean])
                query = cursor.fetchone()
                if query is None:
                    p = Product.get(ean)  # Produces 404 if not exists
                    cursor.execute("INSERT INTO fridge_items (ean, user_id) VALUES (%s, %s)", [ean, user_id[0]])
                    return p, 201
                else:
                    return {
                        "name": query[0],
                        "type": query[1]
                    }, 200

    def delete(self, ean):
        try:
            args = parser.parse_args()
        except Exception:
            return abort(400, message="Invalid arguments")
        with db:
            with db.cursor() as cursor:
                user_id = id_from_token(args['token'])

                cursor.execute("DELETE FROM fridge_items WHERE ean=%s AND fridge_items.user_id=%s", [ean, user_id])
                if cursor.rowcount == 1:
                    return None, 200
                else:
                    abort(404, message="Fridge item does not exist")
