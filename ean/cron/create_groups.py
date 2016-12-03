from database import db


def create_groups():
    with db:
        with db.cursor() as cursor:
            cursor.execute(" SELECT middleman.id, users.id, middleman.member"
                           " FROM (SELECT a.id,"
                           "    COUNT(b.id) AS member,"
                           "    MAX(st_distance(a.geom, b.geom)) AS max_distance,"
                           "    a.geom"
                           "  FROM users AS a"
                           "  JOIN users AS b ON st_distance(a.geom, b.geom) < 1500 AND a.token != b.token"
                           "  GROUP BY a.id, a.geom"
                           "  HAVING COUNT(b.token) > 1"
                           "    ORDER BY COUNT(b.id) DESC) AS middleman"
                           " LEFT JOIN users"
                           " ON st_distance(middleman.geom, users.geom) < 1500")

            current_middleman = None
            current_group = None
            jump = False
            group_members = []
            for item in cursor.fetchall():
                if current_middleman is not item[0]:
                    current_middleman = item[0]
                    cursor.execute(
                        "SELECT * FROM groups_rel LEFT JOIN groups ON groups.id=groups_rel.group_id WHERE day=CURRENT_DATE AND user_id= %s",
                        [current_middleman])

                    if cursor.rowcount > 0:
                        print("Jump")
                        jump = True
                    else:
                        cursor.execute("INSERT INTO groups (day) VALUES (CURRENT_DATE) RETURNING id")
                        current_group = cursor.fetchone()[0]
                        jump = False

                if jump:
                    continue

                cursor.execute("INSERT INTO groups_rel (user_id, group_id) VALUES (%s, %s)", [item[1], current_group])
                group_members.append(item[1])
