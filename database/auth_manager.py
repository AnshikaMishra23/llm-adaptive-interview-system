import sqlite3
import hashlib

def create_connection():

    return sqlite3.connect(
        "assessment_history.db",
        check_same_thread=False
    )


def create_users_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT
        )
        """
    )

    conn.commit()

    conn.close()

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def register_user(
    username,
    password
):

    conn = create_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        conn.close()

        return True

    except Exception as e:

        print("REGISTER ERROR:")
        print(e)

        conn.close()

        return False
def login_user(
    username,
    password
):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user