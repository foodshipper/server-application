import os

import psycopg2
import os.path, logging

db = psycopg2.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASS"),
                      database=os.environ.get("DB_NAME"))

db_version_file = ".db_version"


def db_upgrade(installed_version):
    logging.debug("Database Upgrade from " + str(installed_version))
    if installed_version < 5:
        create_tables()
        installed_version = 5
    if installed_version == 5:
        with db:
            with db.cursor() as cursor:
                cursor.execute("ALTER TABLE group_recipes ADD COLUMN upvotes SMALLINT DEFAULT 0;")
                cursor.execute("ALTER TABLE group_recipes ADD COLUMN veto BOOLEAN DEFAULT FALSE;")
                installed_version = 6

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

            upgraded_version = str(db_upgrade(int(installed_version)))

            with open(db_version_file, "w") as f:
                f.write(upgraded_version)


def create_tables():
    with db:
        with db.cursor() as cursor:
            logging.info("Creating Database Tables")
            if os.path.isfile("conf/database.sql"):
                with open("conf/database.sql", "r") as f:
                    if f.readable():
                        long_stmt = ""
                        for stmt in f.readlines():
                            long_stmt += stmt
                        cursor.execute(long_stmt)


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