from utils.db_connect import create_pool
from utils.db_password import hash_password, check_password
import json
import streamlit as st
from utils.db_connect import create_pool
from utils.db_password import hash_password, check_password

def create_new_user(email: str, password: str) -> None:
    """
    Creates a new user in the users table. Returns error message if email is already associated with an account.
    """
    pool = create_pool()

    salt, hashed_password = hash_password(password)

    with pool.connect() as db_conn:
        try:
            db_conn.execute("INSERT INTO users (email, password, salt) VALUES (%s,%s,%s)", (email, hashed_password, salt))
        except:
            return 0

    return 1

def login_user(email: str, password: str) -> bool:
    """"
    Authenticates a user's login credentials.
    """
    #pool = create_pool()
    #breakpoint()
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

def save_results(user_id: int, results: json) -> None:
    """
    Saves the results of a question response as a json object.
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        db_conn.execute("INSERT INTO results VALUES (%s, now(), %s)", (user_id, results))

    return None

def read_results(user_id: int):
    """
    Returns a user's results history
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT tstamp, results FROM results WHERE user_id = %s", (user_id)).fetchall()

    return result

def get_user_id(email: str) -> int:
    """
    Returns a user's id
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT id FROM users WHERE email = %s", (email)).fetchall()

    return result[0][0]

def get_user_email(user_id: int) -> str:
    """
    Returns a user's email
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT email FROM users WHERE id = %s", (user_id)).fetchall()

    return result[0][0]
