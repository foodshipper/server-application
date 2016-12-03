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
                cursor.execute("INSERT INTO users (token) VALUES (%s) RETURNING id", [token])
                return cursor.fetchone()[0]


def token_exists(token):
    return id_from_token(token) is not None


def get_or_create_id(token):
    user_id = id_from_token(token)
    if user_id is None:
        user_id = register_user(token)
    return user_id
