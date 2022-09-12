import pg8000.native as pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os
from google.oauth2 import service_account
import streamlit as st


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

def getconn() -> pg8000.Connection:
    with Connector(credentials=credentials) as connector:
        conn = connector.connect(
            os.environ.get('INSTANCE'),
            'pg8000',
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            db=os.environ.get('DB')
        )
    return conn


def create_pool():
    conn = getconn()

    # create connection pool
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    return pool
