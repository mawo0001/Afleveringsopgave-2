import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="gruppe3iot",  
        database="wind_turbine_db" 
    )