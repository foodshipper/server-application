import os

import psycopg2
import os.path, logging

db = psycopg2.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASS"),
                      database=os.environ.get("DB_NAME"))

db_version_file = ".db_version"


def db_upgrade(installed_version):
    logging.debug("Database Upgrade from " + str(installed_version))
    if installed_version < 1:
        create_tables()
        return 4
    elif installed_version == 1:
        with db:
            with db.cursor() as cursor:
                cursor.execute("ALTER TABLE users ADD COLUMN firebase_token VARCHAR(255)")
                return 2
    elif installed_version == 2:
        with db:
            with db.cursor() as cursor:
                cursor.execute("ALTER TABLE users ALTER COLUMN firebase_token SET DEFAULT NULL")
                cursor.execute("ALTER TABLE users ALTER COLUMN name SET DEFAULT NULL")
                return 3
    elif installed_version == 3:
        with db:
            with db.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS notification_log "
                    "(id SERIAL PRIMARY KEY,"
                    "user_id SERIAL REFERENCES users(id),"
                    "type VARCHAR(15),"
                    "time TIMESTAMP DEFAULT NOW(),"
                    "success BOOL DEFAULT FALSE,"
                    "msg TEXT)"
                )
                return 4

    return installed_version


def check_db():
    with db:
        with db.cursor() as cursor:
            # Check for current DB Version
            installed_version = 0
            if os.path.isfile(db_version_file):
                with open(db_version_file, "r") as f:
                    if f.readable():
                        content = f.readlines()
                        if len(content) > 0:
                            installed_version = content[0]
                        logging.info("Installed DB Version: " + str(installed_version))

            with open(db_version_file, "w") as f:
                f.write(str(db_upgrade(int(installed_version))))


def create_tables():
    with db:
        with db.cursor() as cursor:
            logging.info("Creating Database Tables")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS product_types "
                "(name VARCHAR(30) PRIMARY KEY )")

            cursor.execute("SELECT * FROM product_types")
            if cursor.fetchone() is None:
                #  Initial Type setup
                types = ['milk', 'water', 'tomato', 'flour', 'pork', 'chicken', 'beef', 'undefined']
                values = ','.join(cursor.mogrify("(%s)", (t,)).decode('utf-8') for t in types)
                cursor.execute("INSERT INTO product_types (name) VALUES " + values)

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS products "
                "(ean VARCHAR(13) PRIMARY KEY, name VARCHAR(100), type VARCHAR(30) REFERENCES product_types(name))")

            # User Table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users "
                "(id SERIAL PRIMARY KEY,"
                " token VARCHAR(64),"
                " firebase_token VARCHAR(255) DEFAULT NULL, "
                " longitude DOUBLE PRECISION,"
                " latitude DOUBLE PRECISION,"
                " geom GEOGRAPHY (POINT,4326),"
                " name VARCHAR(30) DEFAULT NULL)")
            cursor.execute(
                "CREATE OR REPLACE FUNCTION set_user_geom()"
                " RETURNS TRIGGER AS $set_user_geom$"
                " BEGIN"
                "   NEW.geom := st_makepoint(NEW.latitude, NEW.longitude);"
                "   RETURN NEW;"
                " END;"
                "$set_user_geom$ LANGUAGE plpgsql;")
            cursor.execute("SELECT tgname FROM pg_trigger WHERE NOT tgisinternal AND tgrelid = 'users'::REGCLASS")
            trigger = cursor.fetchone()
            if trigger is None or trigger[0] != "user_geom":
                cursor.execute(
                    "CREATE TRIGGER user_geom "
                    "BEFORE INSERT OR UPDATE ON users"
                    " FOR EACH ROW EXECUTE PROCEDURE set_user_geom();")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS fridge_items "
                "(id SERIAL PRIMARY KEY, ean VARCHAR(13) REFERENCES products(ean), user_id SERIAL REFERENCES users(id))")

            # Group Table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS groups "
                "(id SERIAL PRIMARY KEY,"
                " day DATE)")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS groups_rel "
                "(id SERIAL PRIMARY KEY,"
                "user_id SERIAL REFERENCES users(id),"
                "group_id SERIAL REFERENCES groups(id),"
                "invited BOOL DEFAULT FALSE,"
                "accepted BOOL DEFAULT FALSE)")

            cursor.execute(
                "CREATE OR REPLACE FUNCTION unique_group_member()"
                " RETURNS TRIGGER AS $unique_group_member$"
                " BEGIN"
                "   IF EXISTS(SELECT TRUE FROM groups_rel LEFT JOIN groups ON groups_rel.group_id=groups.id WHERE day=CURRENT_DATE AND user_id=NEW.user_id) THEN"
                "    RAISE EXCEPTION 'Group Member can not be in two groups on the same day';"
                "   END IF;"
                "   RETURN NEW;"
                " END;"
                " $unique_group_member$ LANGUAGE plpgsql;")
            cursor.execute("SELECT tgname FROM pg_trigger WHERE NOT tgisinternal AND tgrelid = 'groups_rel'::REGCLASS")
            trigger = cursor.fetchone()
            if trigger is None or trigger[0] != "groups_rel_unique":
                cursor.execute(
                    "CREATE TRIGGER groups_rel_unique "
                    "BEFORE INSERT ON groups_rel"
                    " FOR EACH ROW EXECUTE PROCEDURE unique_group_member();")

            # Notification Log Table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS notification_log "
                "(id SERIAL PRIMARY KEY,"
                "user_id SERIAL REFERENCES users(id),"
                "type VARCHAR(15),"
                "time TIMESTAMP DEFAULT NOW(),"
                "success BOOL DEFAULT FALSE,"
                "msg TEXT)"
            )


# NEVER (!) call this on a productive server
def teardown():
    with db:
        with db.cursor() as cursor:
            if int(os.environ.get("PRODUCTIVE", 1)) != 0:
                raise Exception("Teardown called on productive Server")
            cursor.execute("DROP TABLE fridge_items")
            cursor.execute("DROP TABLE products")
            cursor.execute("DROP TABLE product_types")

            cursor.execute("DROP TABLE groups_rel")
            cursor.execute("DROP TABLE groups")
            cursor.execute("DROP TABLE notification_log")
            cursor.execute("DROP TABLE users")

            if os.path.isfile(db_version_file):
                os.remove(db_version_file)


# NEVER (!) call this on a productive server
def install_testdata():
    with db:
        with db.cursor() as cursor:
            if int(os.environ.get("PRODUCTIVE", 1)) != 0:
                raise Exception("Testdata install called on productive Server")

            if os.path.isfile("sampledata/test_data.sql"):
                with open("sampledata/test_data.sql", "r") as f:
                    if f.readable():
                        for stmt in f.readlines():
                            if len(stmt) > 10:
                                cursor.execute(stmt)