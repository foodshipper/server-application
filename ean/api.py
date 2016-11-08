from flask_restful import Api

from ean.endpoints.products import ProductAPI, ProductTypes
from ean.endpoints.version import APIInfo

api = Api()

# API Endpoints
api.add_resource(ProductAPI, '/v1/product/<string:ean>')
api.add_resource(ProductTypes, '/v1/types')
api.add_resource(APIInfo, '/status')