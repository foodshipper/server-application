from flask_restful import Api

from ean.endpoints.products import Product, ProductTypes
from ean.endpoints.version import APIInfo
from ean.endpoints.fridge_items import FridgeOverview, FridgeItem
from ean.endpoints.home_location import HomeLocation

api = Api()

# API Endpoints
api.add_resource(Product, '/v1/product/<string:ean>')
api.add_resource(ProductTypes, '/v1/types')
api.add_resource(APIInfo, '/status')
api.add_resource(FridgeOverview, '/v1/items')
api.add_resource(FridgeItem, '/v1/items/<string:ean>')
api.add_resource(HomeLocation, '/v1/home-location')
