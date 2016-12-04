# Endpoints

# Products
## GET /product/<<string:ean>>
Returns JSON-Object with ean, name and type
Returns 404 if product is not found

#### Example: GET /product/4000406071242
```json
{
    "type": "flour",
    "ean": "4000406071242",
    "name": "Aurora Weizenvollkorn Mehl, 5er Pack (5 x 1 kg)"
}
```

## PUT /product/<<string:ean>>
_name_: Name of the product
_type_: Type of the product, must be from `/types`

Creates or updates (override) product information

# Product Types

## GET /types
Returns a JSON-Array with valid product types
#### Example: GET /types
```json
["milk", "water", "tomato", "flour", "pork", "chicken", "beef", "undefined"]
```

# Fridge Items
_token_: Unique Identification of the current user

Every request expects a valid token!

## GET /items
Returns a JSON Array with Products that are saved for the current user

#### Example: GET /items?token=5
```json
[{
    "type": "flour",
    "ean": "4000406071242",
    "name": "Aurora Weizenvollkorn Mehl, 5er Pack (5 x 1 kg)"
}]
```

## PUT /items/<<string:ean>>
Saves a specific product for the given user, returns JSON Product Object
Returns a 404 if product does not exist

## DELETE /items/<<string:ean>>
Deletes the product from the users storage
Returns a 404, if the user did not have the product

# User
_token_: Unique Identification of the current user

## PUT /user/home-location
_lon_: Longitude
_lat_: Latitude

Create or updates the user location

## GET /user/home-location
Not implemented for privacy reasons!

## PUT /user/name
_name_: Name of the user

Creates or updates the user name

## GET /user/name
Gets the name of the user

## PUT /user/firebase-token
_firebase_token_: [Firebase Token](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/auth/FirebaseToken)

Creates or updates the users Firebase token for notification

# Dinner Groups
_token_: Unique Identification of current user

## GET /dinner/<<int:group_id>>
Gets Group Information
```json
{
    "invited": 4,
    "accepted": 2,
    "day": "2016-12-04"
}
```

## PUT /dinner/<<int:group_id>>
_accept_: Boolean, whether user accepts invitation or not

## GET /dinner/<<int:group_id>>/recipes
Gets possible recipes
```json
[
{"id": 321, "title": "Chicken Curry", "desc": "Tasty chicken curry", "upvotes": 2, "veto": false}, 
{"id": 324, "title": "Pizza Funghi", "desc": "Tasty Pizza", "upvotes": 3, "veto": false},
{"id": 325, "title": "Spaghetti Carbonara", "desc": "Tasty chicken curry", "upvotes": 2, "veto": false}     
]
```