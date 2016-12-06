from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest

from ean.database import db
from ean.user import id_from_token, get_or_create_id

parser = reqparse.RequestParser()
parser.add_argument('token', required=True)
parser.add_argument('resend_all', required=False)


class UserGroups(Resource):
    def put(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return abort(400, message="Invalid arguments")

        if 'resend_all' not in args:
            return abort(200, message="")

        if args['resend_all']:
            with db:
                with db.cursor() as cursor:
                    user_id = id_from_token(args['token'])
                    if user_id is None:
                        return abort(400, message="Invalid arguments")
                    cursor.execute("UPDATE groups_rel SET invited=FALSE WHERE id = (SELECT groups_rel.id FROM groups_rel "
                                   "JOIN groups ON groups_rel.group_id = groups.id "
                                   "WHERE groups_rel.user_id=%s AND groups.day = CURRENT_DATE)",
                                   [user_id])
                    return 200