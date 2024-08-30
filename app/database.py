import psycopg2
from psycopg2.extras import RealDictCursor
import time


while True:
    try:
        conn = psycopg2.connect(host='localhost', user='postgres', password='12345',
                                database='books-store', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Successfully connected to the database")
        break
    except Exception as err:
        print("Fail to connect")
        print("Error", err)
        time.sleep(2)
