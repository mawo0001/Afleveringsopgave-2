import os
try:
    import psycopg2
except ImportError as e:
    raise ImportError(
        "psycopg2 is required for PostgreSQL connection. Install it with 'pip install psycopg2-binary'."
    ) from e

def get_db_connection():
    """Establish PostgreSQL database connection."""
    host = os.getenv("POSTGRES_HOST", "postgresql")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "vindmolle_db")
    username = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD")
    
    if not password:
        raise RuntimeError(
            "POSTGRES_PASSWORD environment variable is not set. Please set it with your PostgreSQL password."
        )
    
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=username,
        password=password
    )
    
    return connection