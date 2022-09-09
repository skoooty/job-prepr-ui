import pg8000.native as pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os

def getconn() -> pg8000.Connection:
    with Connector() as connector:
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
