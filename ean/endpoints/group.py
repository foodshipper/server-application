import os

import requests
from flask_restful import Resource, reqparse, abort
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)

putParser = reqparse.RequestParser()
putParser.add_argument('token', required=True)
putParser.add_argument('accept', required=True)


class Group(Resource):
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

                cursor.execute("SELECT day, COUNT(CASE WHEN invited THEN 1 END) AS invited, "
                               "COUNT(CASE WHEN accepted THEN 1 END) AS accepted, "
                               # Only if user is Group Member this will be 1
                               "COUNT(CASE WHEN user_id=%s THEN 1 END) = 1 AS allowed "
                               "FROM groups "
                               "JOIN groups_rel ON groups.id = groups_rel.group_id "
                               "WHERE groups.id=%s "
                               "GROUP BY groups.id ", [user_id, group_id])
                group = cursor.fetchone()
                if group is None:
                    return abort(404, message="Group not found")
                if not group[3]:
                    return abort(403, message="Token is not allowed to view this group")

                return {
                    'invited': group[1],
                    'accepted': group[2],
                    'day': str(group[0]),
                }

    def put(self, group_id):
        try:
            args = putParser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        with db:
            with db.cursor() as cursor:
                user_id = id_from_token(args['token'])
                if user_id is None:
                    return abort(403, message="Token is not allowed to view this group")

                cursor.execute("SELECT id FROM groups_rel WHERE user_id=%s AND groups_rel.group_id=%s",
                               [user_id, group_id])
                rel = cursor.fetchone()
                if rel is None:
                    return abort(404, message="Group not found")

                cursor.execute("UPDATE groups_rel SET accepted=%s WHERE id=%s", [args['accept'], rel[0]])
                return 200