import os

import requests
from flask_restful import Resource, reqparse, abort
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('token', required=True)
put_parser.add_argument('action', required=True)
put_parser.add_argument('recipe_id', required=True)


class GroupRecipes(Resource):
    @staticmethod
    def get(group_id):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = id_from_token(args['token'])
                if user_id is None:
                    return abort(403, message="Token is not allowed to view this group")

                cursor.execute("SELECT id FROM groups_rel WHERE user_id=%s AND groups_rel.group_id=%s",
                               [user_id, group_id])
                group = cursor.fetchone()
                if group is None:
                    return abort(403, message="Token is not allowed to view this group")

                cursor.execute("SELECT recipe_id, title, upvotes, veto, image, cheap, vegan, vegetarian, duration FROM group_recipes "
                               "LEFT JOIN rec_recipes ON group_recipes.recipe_id = rec_recipes.id "
                               "WHERE group_id=%s", [group_id])

                recipes = []

                for recipe in cursor.fetchall():
                    recipes.append({
                        'id': recipe[0],
                        'title': recipe[1],
                        'desc': None,
                        'upvotes': recipe[2],
                        'veto': recipe[3],
                        'image': recipe[4],
                        'cheap': recipe[5],
                        'vegan': recipe[6],
                        'vegetarian': recipe[7],
                        'duration': recipe[8]
                    })
                return recipes

    @staticmethod
    def put(group_id):
        try:
            args = put_parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = id_from_token(args['token'])
                if user_id is None:
                    return abort(403, message="Token is not allowed to view this group")

                cursor.execute("SELECT id FROM groups_rel WHERE user_id=%s AND groups_rel.group_id=%s",
                               [user_id, group_id])
                group = cursor.fetchone()
                if group is None:
                    return abort(403, message="Token is not allowed to view this group")

                cursor.execute("INSERT INTO group_recipe_vote_log (grecipe_id, user_id, action) VALUES "
                               "((SELECT id FROM group_recipes WHERE group_id=%s AND group_recipes.recipe_id=%s),"
                               " %s, %s)",
                               [group_id, args['recipe_id'], user_id, args['action']])

                return None, 200
