import string

import requests
from flask_restful import Resource, marshal_with, abort, fields, reqparse

from ean.database import db
from ean.models import Product

product_fields = {
    'ean': fields.String,
    'name': fields.String,
    'type': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('type', required=True)


class ProductAPI(Resource):
    @marshal_with(product_fields)
    def get(self, ean):
        print(ean)
        product = Product.query.filter_by(ean=ean).first()
        if product is not None:
            return product
        else:
            result = ProductData.request_product(ean)
            if result is not None:
                db.session.add(result)
                db.session.commit()
                return result

            abort(404, message="Product with EAN {} does not exist.".format(ean))

    def put(self, ean):
        try:
            args = parser.parse_args()
            print(args)
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
            return 200


class ProductData():
    @staticmethod
    def request_product(gtin):
        req = requests.get(
            'http://pod.opendatasoft.com/api/records/1.0/search/?dataset=pod_gtin&rows=1&refine.gtin_cd={}'.format(
                gtin))
        if req.status_code == requests.codes.ok:
            print(req.json())
            product = req.json()
            if product['nhits'] == 0:
                return None
            if 'gtin_nm' not in product['records'][0]['fields']:
                return None
            result = Product(gtin, product['records'][0]['fields']['gtin_nm'], None)
            db.session.add(result)
            db.session.commit()
            return result
        else:
            return None
