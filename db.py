import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "vindmolle"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "secret"),
        cursor_factory=RealDictCursor
    )
    return conn