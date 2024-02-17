import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Krishnas5#@localhost/FastAPI_database'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    # `db = session_local()` is creating a local session to connect to the database. It is using the
    # `session_local` function to create a new session object. This session object is then used to
    # interact with the database within the `get_db` function. The `yield` keyword is used to return
    # the session object as a generator, allowing it to be used within a `with` statement. Finally,
    # the `finally` block ensures that the session is closed after it is no longer needed.
    db = session_local()
    try:
        yield db
    finally:
        db.close()



def connect_database():
    try:
        conn = psycopg2.connect(host='localhost', port=5432, database='FastAPI database', user='postgres', password='Krishnas5#',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established!!")
        return conn, cursor
    except Exception as error:
        print("Database connection error")
        print("error: %s" % error)
        time.sleep(2)
        