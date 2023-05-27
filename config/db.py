from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from decouple import config
from config.db_tables import Base
from fastapi import  HTTPException




class DatabaseManager:
    def __init__(self):
        self.engine = self.connect_database()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # Connect to the database
    def connect_database(self):
        try:
            database_url = config("DATABASE_URL")
            engine = create_engine(database_url)
            print("Connected database")
            return engine
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

   # Create tables if they do not exist
    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine)
            print("Created tables")
        except Exception as e:
            print(e)

    # Delete table if necessary
    def delete_table(self, table_name):
        try:
            Base.metadata.tables[table_name].drop(self.engine)
            print(f"The table {table_name} has been deleted successfully.")
        except Exception as e:
            print(e)

    # Close the session and engine
    def close_connection(self):
        if self.session:
            print("Closing session")
            self.session.close()
        if self.engine:
            print("Closing engine")
            self.engine.dispose()

"""Function to use in Depends FastAPi"""
def database_connection():
    db_manager = DatabaseManager()
    yield db_manager.session
    db_manager.close_connection()


# Usage example:
db_manager = DatabaseManager()
db_manager.create_tables()
# db_manager.delete_table('user')
# db_manager.close_connection()



"""
from sqlalchemy import create_engine
from sqlalchemy import inspect

# Create an SQLAlchemy engine
engine = create_engine(config("DATABASE_URL"))

# Create an SQLAlchemy inspector
inspector = inspect(engine)

# Get the table names
table_names = inspector.get_table_names()

# Iterate over the table names
for table_name in table_names:
    print(f"Table: {table_name}")
    
    # Get the column names and types for each table
    columns = inspector.get_columns(table_name)
    
    # Print column information
    for column in columns:
        print(f"Column: {column['name']}, Type: {column['type']}")
    
    print("------------------------------")

"""
