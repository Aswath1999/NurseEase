import psycopg2
from psycopg2 import Error
from decouple import config


#Connecting to database with postgres connection from Elephantsql
def connect_database():
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
        print('sucsss')
        return conn
    except Error as e:
        print("Error connecting to database")
        print(e)

print(connect_database())
#create tables if does not exist in the database
def create_tables():
    try:
        conn=connect_database()
        cursor = conn.cursor()
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
        conn.commit()
        print("Created tables")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


#     cur = conn.cursor()
#     # cur.execute(
#     #     "INSERT INTO Patient (patient) VALUES (%s)",
#     #     (patient_json,)
#     # )

#     conn.commit()
#     cur.close()
#     conn.close()
#     print("FHIR resource saved successfully.")
#     print('great')
# except Error as e:
#     print("Error connecting to PostgreSQL or executing the query:", e)
    
    # ...
"""
    data = {
        "temperature": 98.6,
        "heart_rate": 75,
        "blood_pressure": {
            "systolic": 120,
            "diastolic": 80
        }
    }

    # print(type(data))
    # Convert the data to JSON format
    json_data = json.dumps(data)
    # print(type(json_data))
    # Prepare the INSERT statement
    insert_query = "INSERT INTO Vitals (vitals) VALUES (%s)"
    with conn.cursor() as cursor:
        # Execute the INSERT statement
        cursor.execute(insert_query, (json_data,))
        # Commit the changes
        conn.commit()
"""
    # Close the connection
"""
# Prepare the SELECT statement
    select_query = "SELECT * FROM Vitals"

# Use the with statement to automatically close the cursor
    with conn.cursor() as cursor:
        # Execute the SELECT statement
        cursor.execute(select_query)
        # Fetch the query results
        results = cursor.fetchall()
        print(results)

        # Process the results
        for row in results:
            # The JSONB data is stored in the second column (index 1)
            vitals_json = row[1]
            print(vitals_json)
            print('ok')
            vitals_dict = vitals_json
            print(type(vitals_dict))
            
            # Convert the JSONB data to a Python dictionary
            try:
                
                print(vitals_dict)
                temperature = vitals_dict.get("temperature")
                heart_rate = vitals_dict.get("heart_rate")
                blood_pressure = vitals_dict.get("blood_pressure")

                print("Temperature:", temperature)
                print("Heart Rate:", heart_rate)
                print("Blood Pressure:", blood_pressure)

            except:
                'error occured'
                # Access and print the values
"""
    
 






"""

from pymongo.mongo_client import MongoClient
import certifi
import os
from decouple import config


mongo_password=config("MONGOPASSWORD")



uri = "mongodb+srv://cskaswath:"+mongo_password+"@cluster0.a3nj9yv.mongodb.net/test1?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db=client.test1
collection=db.python
"""


 # patient = Patient()
    # patient.id = 3  #providfe uuid
    # patient.name = [{"family": "Doe", "given": ["John"]}]
    # print('ok')
    # print(patient.name)
    # patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)