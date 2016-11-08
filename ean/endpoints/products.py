import requests
from flask_restful import Resource, marshal_with, abort, reqparse

from ean.database import db

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('type', required=True)


class ProductAPI(Resource):
    def get(self, ean):
        print(ean)
        cursor = db.cursor()
        cursor.execute("SELECT name, type FROM products WHERE ean=%s", (ean,))
        product = cursor.fetchone()
        if product is not None:
            return {
                "ean": ean,
                "name": product[0],
                "type": product[1]
            }
        else:
            result = ProductData.request_product(ean)
            if result is not None:
                self.addProduct(result['ean'], result['name'], result['type'])
                return result

            abort(404, message="Product with EAN {} does not exist.".format(ean))

    '''def put(self, ean):
        try:
            args = parser.parse_args()
        except Exception as e:
            print(e)
            return abort(400, message="Invalid arguments")

        if len(args['name']) == 0 or len(args['type']) == 0:
            return abort(400, message="Invalid arguments")

        p = Product.query.filter_by(ean=ean).first()
        if p is None:
            p = Product(ean, args['name'], args['type'])
            db.session.add(p)
            db.session.commit()
            return 201
        else:
            p.name = args['name']
            p.type = args['type']
            db.session.add(p)
            db.session.commit()
            return 200'''

    def addProduct(self, ean, name, type):
        cur = db.cursor()
        cur.execute("INSERT INTO products (ean, name, type) VALUES (%s, %s, %s)", (ean, name, type))
        db.commit()
        cur.close()


class ProductData():
    @staticmethod
    def request_product(gtin):
        req = requests.get(
            'http://pod.opendatasoft.com/api/records/1.0/search/?dataset=pod_gtin&rows=1&refine.gtin_cd={}'.format(
                gtin))
        if req.status_code == requests.codes.ok:
            product = req.json()
            if product['nhits'] == 0:
                return None
            if 'gtin_nm' not in product['records'][0]['fields']:
                return None
            return {
                "ean": gtin,
                "name": product['records'][0]['fields']['gtin_nm'],
                "type": None
            }
        else:
            return None
