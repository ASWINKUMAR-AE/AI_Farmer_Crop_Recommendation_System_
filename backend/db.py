import pymysql
import pymysql.cursors
from backend.config import Config


def get_db_connection(use_db=True):
    """
    Establish a connection to MySQL.
    """
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME if use_db else None,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            charset='utf8mb4'
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"[DB ERROR] Failed to connect to MySQL: {e}")
        raise e


def execute_query(query, params=None, fetchone=False, fetchall=False, insert=False):
    """
    Execute a query and manage cursor and connection lifecycle.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if insert:
                last_id = cursor.lastrowid
                return last_id
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return cursor.rowcount
    finally:
        conn.close()
