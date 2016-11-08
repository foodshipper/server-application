import os
import psycopg2

db = psycopg2.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASS"),
                      database=os.environ.get("DB_NAME"))


def create_tables():
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS products "
        "(id SERIAL PRIMARY KEY, ean VARCHAR(13) UNIQUE, name VARCHAR(100), type VARCHAR(10))")
    db.commit()
    cur.close()
