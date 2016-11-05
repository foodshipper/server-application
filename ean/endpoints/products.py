import requests
from flask_restful import Resource, marshal_with, abort, fields

from ean.database import db
from ean.models import Product

product_fields = {
    'ean': fields.Integer,
    'name': fields.String,
    'type': fields.String
}


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
            return result
        else:
            return None
