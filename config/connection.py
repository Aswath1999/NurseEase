import psycopg2
from psycopg2 import Error
from decouple import config
from uuid import uuid4

class DatabaseManager:
    def __init__(self):
        self.conn = self.connect_database()
    
    #Connect to the database
    def connect_database(self):
        try:    
            host = 'balarama.db.elephantsql.com'
            database = config("DATABASE")
            user = config("user")  #USER for codespaces
            password = config("PASSWORD")

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

    #Create tables if it does not exist
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Vitals (
                id UUID PRIMARY KEY,
                vitals JSONB
            )
            '''
            cursor.execute(create_table_query)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Patient (
                id UUID PRIMARY KEY,
                patient JSONB
            )
            '''
            cursor.execute(create_table_query)
            self.conn.commit()
            print("Created tables")
        except Error as e:
            print(e)
    
    #Delete tables if necessary
    def delete_table(self,table_name):
        try:
            cursor = self.conn.cursor()
            drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_table_query)
            self.conn.commit()
            print(f"The table Patient has been deleted successfully.")
        except Error as e:
            print(e)

    #Close the connection
    def close_connection(self):
        if self.conn:
            self.conn.close()


# Usage example:
db_manager = DatabaseManager()
db_manager.create_tables()
# db_manager.delete_table('Patient')
db_manager.close_connection()
