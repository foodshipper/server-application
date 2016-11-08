from flask_restful import Api

from ean.endpoints.products import ProductAPI
from ean.endpoints.version import APIInfo

api = Api()

# API Endpoints
api.add_resource(ProductAPI, '/v1/product/<string:ean>')
api.add_resource(APIInfo, '/status')