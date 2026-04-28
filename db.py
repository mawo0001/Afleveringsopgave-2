import os

try:
    import pyodbc
except ImportError as e:
    raise ImportError(
        "pyodbc is required for Azure SQL connection. Install it with 'pip install pyodbc'."
    ) from e


def get_db_connection():
    server = "stud.ek.dk"
    database = "akse3585"
    username = os.getenv("AZURE_SQL_USER", "akse3585@stud.ek.dk")
    password = os.getenv("AZURE_SQL_PASSWORD")
    if not password:
        raise RuntimeError(
            "Please set AZURE_SQL_PASSWORD environment variable with your Azure SQL password"
        )
    driver = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=5;"
    )

    return pyodbc.connect(connection_string)
