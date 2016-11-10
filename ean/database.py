import os
import psycopg2

db = psycopg2.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASS"),
                      database=os.environ.get("DB_NAME"))


def create_tables():
    with db:
        with db.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS product_types "
                "(name VARCHAR(30) PRIMARY KEY )")

            cursor.execute("SELECT * FROM product_types")
            if cursor.fetchone() is None:
                #  Initial Type setup
                types = ['milk', 'water', 'tomato', 'flour', 'pork', 'chicken', 'beef', 'undefined']
                values = ','.join(cursor.mogrify("(%s)", (t, )).decode('utf-8') for t in types)
                cursor.execute("INSERT INTO product_types (name) VALUES " + values)

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS products "
                "(ean VARCHAR(13) PRIMARY KEY, name VARCHAR(100), type VARCHAR(30) REFERENCES product_types(name))")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS fridge_items "
                "(id SERIAL PRIMARY KEY , ean VARCHAR(13) REFERENCES products(ean), user_id VARCHAR(64))")

