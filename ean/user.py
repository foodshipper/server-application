from ean.database import db


def id_from_token(token):
    with db:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE token=%s", [token])
            user = cursor.fetchone()
            if user is not None:
                return user[0]
            return None


def register_user(token):
    with db:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE token=%s", [token])
            user = cursor.fetchone()
            if user is not None:
                raise Exception("Token already registered")
            else:
                cursor.execute("INSERT INTO users (token) VALUES (%s)", [token])
            return cursor.lastrowid


def token_exists(token):
    return id_from_token(token) is not None


def get_or_create_id(token):
    id = id_from_token(token)
    if id is None:
        id = register_user(token)
    return id
