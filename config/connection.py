import psycopg2
from psycopg2 import Error
from decouple import config


class DatabaseManager:
    def __init__(self):
        self.conn = self.connect_database()

    def connect_database(self):
        try:    
            host = 'balarama.db.elephantsql.com'
            database = config("database")
            user = config("user")
            password = config("password")

            # Establish the connection
            conn = psycopg2.connect(
                host=host,
                port='5432',
                database=database,
                user=user,
                password=password
            )
            return conn
        except Error as e:
            print(e)

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Vitals (
                id SERIAL PRIMARY KEY,
                vitals JSONB
            )
            '''
            cursor.execute(create_table_query)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Patient (
                id SERIAL PRIMARY KEY,
                patient JSONB
            )
            '''
            cursor.execute(create_table_query)
            self.conn.commit()
            print("Created tables")
        except Error as e:
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()


# Usage example:
db_manager = DatabaseManager()
# db_manager.create_tables()
# db_manager.close_connection()
