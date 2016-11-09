from flask_restful import Api

from ean.endpoints.products import Product, ProductTypes
from ean.endpoints.version import APIInfo
from endpoints.fridge_items import FridgeOverview, FridgeItem

api = Api()

# API Endpoints
api.add_resource(Product, '/v1/product/<string:ean>')
api.add_resource(ProductTypes, '/v1/types')
api.add_resource(APIInfo, '/status')
api.add_resource(FridgeOverview, '/v1/items')
api.add_resource(FridgeItem, '/v1/items/<string:ean>')
