from flask_restful import Api

from ean.endpoints.fridge_items import FridgeItem
from ean.endpoints.fridge_items import FridgeOverview
from ean.endpoints.home_location import HomeLocation
from ean.endpoints.products import Product, ProductTypes
from ean.endpoints.user_name import UserName
from ean.endpoints.version import APIInfo
from ean.endpoints.user_firebase_token import UserFirebaseToken
from ean.endpoints.group import Group

api = Api()

# API Endpoints
api.add_resource(Product, '/v1/product/<string:ean>')
api.add_resource(ProductTypes, '/v1/types')
api.add_resource(APIInfo, '/status')
api.add_resource(FridgeOverview, '/v1/items')
api.add_resource(FridgeItem, '/v1/items/<string:ean>')
api.add_resource(HomeLocation, '/v1/user/home-location')
api.add_resource(UserFirebaseToken, '/v1/user/firebase-token')
api.add_resource(UserName, '/v1/user/name')
api.add_resource(Group, '/v1/dinner/<int:group_id>')
