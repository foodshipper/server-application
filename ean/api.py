from flask_restful import Api

from ean.endpoints.products import ProductAPI

api = Api()

# API Endpoints
api.add_resource(ProductAPI, '/v1/product/<string:ean>')
