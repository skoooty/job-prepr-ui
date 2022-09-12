import sqlalchemy
from db_connect import create_pool
from db_password import hash_password

def create_new_user(email: str, password: str) -> None:

    pool = create_pool()

    salt, hashed_password = hash_password(password)

    with pool.connect() as db_conn:
        try:
            db_conn.execute("INSERT INTO users (email, password, salt) VALUES (%s,%s,%s)", (email, hashed_password, salt))
        except:
            return "Email is already taken"

    return "Account created!"
