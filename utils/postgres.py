import pg8000.native as pg8000
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

def getconn() -> pg8000.Connection:
    with Connector() as connector:
        conn = connector.connect(
            "le-wagon-bootcamp-356711:europe-west1:jobprepr",
            "postgres",
            user="postgres",
            password="V]9{-tqAu2,dJO*_",
            db="jobprepr"
        )
    return conn

# # create connection pool
# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://",
#     creator=getconn,
# )

# # insert statement
# insert_stmt = sqlalchemy.text(
#     "INSERT INTO my_table (id, title) VALUES (:id, :title)",
# )

# interact with Cloud SQL database using connection pool
# with pool.connect() as db_conn:
#     # insert into database
#     db_conn.execute(insert_stmt, id="book1", title="Book One")

#     # query database
#     result = db_conn.execute("SELECT * from my_table").fetchall()

#     # Do something with the results
#     for row in result:
#         print(row)

if __name__ == "__main__":
    conn = getconn()
    print(conn)
