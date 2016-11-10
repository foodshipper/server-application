# Endpoints

# Products
## GET /product/<<string:ean>>
Returns JSON-Object with ean, name and type  
Returns 404 if product is not found

#### GET /product/4000406071242
```javascript
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

# Fridge Items
_user_id_: Unique Identification of the current user

Every request expects a valid user_id!

## GET /items
Returns a JSON Array with Products that are saved for the current user

## PUT /items/<<string:ean>>
Saves a specific product for the given user, returns JSON Product Object  
Returns a 404 if product does not exist

## DELETE /items/<<string:ean>>
Deletes the product from the users storage  
Returns a 404, if the user did not have the product
