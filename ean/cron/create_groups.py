import logging

from ean.external.recipe import suggest_recipes
from ean.database import db


def create_groups():
    with db:
        with db.cursor() as cursor:
            cursor.execute(" SELECT middleman.id as user_1_id, users.id as user_2_id, middleman.member"
                           " FROM (SELECT a.id as user_id,"
                           "    COUNT(b.id) AS group_member,"
                           "    MAX(st_distance(a.geom, b.geom)) AS max_distance,"
                           "    a.geom"
                           "  FROM users AS a"
                           "  JOIN users AS b ON st_distance(a.geom, b.geom) < 1500 AND a.token != b.token"
                           "  GROUP BY a.id, a.geom"
                           "  HAVING COUNT(b.token) > 1"
                           "    ORDER BY COUNT(b.id) DESC) AS middleman"
                           " LEFT JOIN users"
                           " ON st_distance(middleman.geom, users.geom) < 15000")

            current_middleman = None
            current_group = None
            jump = False
            group_members = []
            for item in cursor.fetchall():
                if current_middleman is not item[0]:
                    current_middleman = item[0]
                    cursor.execute(
                        "SELECT * FROM groups_rel LEFT JOIN groups ON groups.id=groups_rel.group_id WHERE day=CURRENT_DATE AND user_id=%s",
                        [current_middleman])

                    if cursor.rowcount > 0:
                        jump = True
                    else:
                        cursor.execute("INSERT INTO groups (day) VALUES (CURRENT_DATE) RETURNING id")
                        current_group = cursor.fetchone()[0]
                        jump = False

                if jump:
                    continue

                cursor.execute("INSERT INTO groups_rel (user_id, group_id) VALUES (%s, %s)", [item[1], current_group])
                group_members.append(item[1])


def suggest_all_recipes():
    with db:
        with db.cursor() as cursor:
            cursor.execute('SELECT groups.id FROM groups '
                           'LEFT JOIN group_recipes ON groups.id = group_recipes.group_id '
                           'WHERE group_recipes.group_id IS NULL AND groups.day = CURRENT_DATE')

            for row in cursor.fetchall():
                suggest_group_recipe(row[0])


def suggest_group_recipe(group_id):
    with db:
        with db.cursor() as cursor:
            logging.debug("Searching for recipes for Group #" + str(group_id))
            cursor.execute("SELECT DISTINCT product_types.name FROM groups_rel "
                           "JOIN fridge_items ON fridge_items.user_id = groups_rel.user_id "
                           "LEFT JOIN products ON fridge_items.ean = products.ean "
                           "LEFT JOIN product_types ON products.type = product_types.id "
                           "WHERE groups_rel.group_id=%s", [group_id])
            ingredients = ""
            for row in cursor.fetchall():
                ingredients += row[0] + ","
            ingredients.strip(",")
            if ingredients != "":
                for recipe in suggest_recipes(ingredients, 20):
                    cursor.execute("INSERT INTO group_recipes (group_id, recipe_id) VALUES (%s, %s)", [group_id, recipe])
