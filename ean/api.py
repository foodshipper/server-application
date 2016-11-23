from flask_restful import Api

from endpoints.fridge_items import FridgeItem
from endpoints.fridge_items import FridgeOverview
from endpoints.home_location import HomeLocation
from endpoints.products import Product, ProductTypes
from endpoints.user_name import UserName
from endpoints.version import APIInfo

api = Api()

# API Endpoints
api.add_resource(Product, '/v1/product/<string:ean>')
api.add_resource(ProductTypes, '/v1/types')
api.add_resource(APIInfo, '/status')
api.add_resource(FridgeOverview, '/v1/items')
api.add_resource(FridgeItem, '/v1/items/<string:ean>')
api.add_resource(HomeLocation, '/v1/user/home-location')
api.add_resource(UserName, '/v1/user/name')
