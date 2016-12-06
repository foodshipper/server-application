from ean.database import db
from external.firebase_service import push_service


def send_invitations():
    with db:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT users.firebase_token, groups_rel.group_id, CURRENT_DATE as day, groups_rel.id, users.id FROM groups "
                "INNER JOIN groups_rel ON groups.id = groups_rel.group_id AND groups_rel.invited IS FALSE "
                "INNER JOIN users ON groups_rel.user_id = users.id AND users.firebase_token IS NOT NULL "
                "WHERE groups.day=CURRENT_DATE")
            for user in cursor.fetchall():
                data_message = {
                    "status": "invited",
                    "group_id": user[1],
                    "date": str(user[2])
                }
                result = push_service.notify_single_device(registration_id=user[0], data_message=data_message)
                if result[0]['success']:
                    cursor.execute("UPDATE groups_rel SET invited=TRUE WHERE id=%s", [user[3]])
                cursor.execute("INSERT INTO notification_log (user_id, type, success, msg) "
                               "VALUES (%s, %s, %s, %s)", [user[4], 'invitation', bool(result[0]['success']), None])