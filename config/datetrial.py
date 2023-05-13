from pymongo import MongoClient
from datetime import datetime
import certifi


uri = "mongodb+srv://cskaswath:acchu999@cluster0.a3nj9yv.mongodb.net/test1?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

print(client.list_database_names())
db=client.test1
print(db.list_collection_names())
collections=db.python


import datetime

date_string = "2022-05-11"
date_format = "%Y-%m-%d"

# print(type(date_obj))
date_obj = datetime.datetime.strptime(date_string, date_format)
print(type(date_string))
dob_datetime = datetime.datetime.combine(date_obj, datetime.datetime.min.time())


birthdate = dob_datetime
patient = {'name': 'John Doe', 'birthdate': dob_datetime}

print(type(birthdate))
# Insert patient into MongoDB
result = collections.insert_one(patient)


