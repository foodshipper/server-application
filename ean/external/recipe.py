import logging
import os

import requests

from database import db

headers = {"X-Mashape-Key": os.environ.get("MASHAPE_KEY")}


def suggest_recipes(products, number=20):
    recipe_ids = []
    req = requests.get(
        'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients'
        '?fillIngredients=false'
        '&ingredients={}'
        '&limitLicense=false'
        '&number={}'
        '&ranking=1'.format(products, number),
        headers=headers)
    if req.status_code == requests.codes.ok:
        recipes = req.json()
        for recipe in recipes:
            recipe_ids.append(get_recipe_detail(recipe['id']))
    else:
        logging.error("Request failed!")
        logging.error(req.request)
    return recipe_ids


def get_recipe_detail(external_id):
    with db:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM rec_recipes WHERE external_id=%s", [external_id])
            recipe = cursor.fetchone()
            if recipe is not None:
                print("Cached!")
                return recipe[0]
            req = requests.get(
                'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information'
                '?includeNutrition=false'.format(external_id),
                headers=headers)
            if req.status_code != requests.codes.ok:
                print("Error getting recipe")
                return

            recipe = req.json()

            cursor.execute(
                "INSERT INTO rec_recipes (external_id, title, image, duration, servings, vegetarian, vegan, cheap, instructions)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                [recipe['id'], recipe['title'], recipe['image'], recipe['readyInMinutes'],
                 recipe['servings'], recipe['vegetarian'], recipe['vegan'], recipe['cheap'], recipe['instructions']])
            recipe_id = cursor.fetchone()[0]

            for product in recipe['extendedIngredients']:
                if "id" not in product:
                    continue

                cursor.execute("SELECT product_types.id FROM product_types WHERE external_id=%s", [product['id']])
                query = cursor.fetchone()
                if query is None:
                    if not "aisle" in product:
                        product['aisle'] = None

                    cursor.execute("INSERT INTO product_types (external_id, category, name, image) VALUES "
                                   "(%s, %s, %s, %s) RETURNING id",
                                   [product['id'], product['aisle'], product['name'], product['image']])
                    product_id = cursor.fetchone()[0]
                else:
                    product_id = query[0]

                cursor.execute("INSERT INTO rec_ingredients (product_id, recipe_id, amount, unit) "
                               "VALUES (%s, %s, %s, %s)",
                               [product_id, recipe_id, product['amount'], product['unit']])
            return recipe_id
