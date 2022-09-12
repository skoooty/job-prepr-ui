import streamlit as st
from utils.db_connect import create_pool
from utils.db_password import hash_password, check_password

def create_new_user(email: str, password: str) -> None:

    pool = create_pool()

    salt, hashed_password = hash_password(password)

    with pool.connect() as db_conn:
        try:
            db_conn.execute("INSERT INTO users (email, password, salt) VALUES (%s,%s,%s)", (email, hashed_password, salt))
        except:
            return 0

    return 1

def login_user(email: str, password: str) -> bool:

    if email and password:
        pool = create_pool()

        with pool.connect() as db_conn:
            result = db_conn.execute("SELECT password, salt FROM users WHERE email = %s", (email)).fetchall()

        if not result or len(result) == 0:
            return 0

        hashed_password, salt = result[0]

        if check_password(password, salt, hashed_password):
            return 1

        return 0
