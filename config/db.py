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

# from fhirclient.models import patient
# from fhirclient.models.fhirdate import FHIRDate


# # Create a patient object
# my_patient = patient.Patient()

# # Set the patient's birth date
# birth_date = FHIRDate('1905-08-23')
# my_patient.birthDate = birth_date
# print()

# # Print the birth date as a FHIR date string
# print(my_patient.birthDate.isostring())

# from fhir.resources.patient import Patient as FhirPatient
# from pydantic import BaseModel, validator,Field
# from pydantic import ValidationError
# from datetime import date
# import datetime
# from fhirclient.models.fhirdate import FHIRDate
# import certifi
# from typing import List,Optional
# from pymongo.mongo_client import MongoClient


# uri = "mongodb+srv://cskaswath:acchu999@cluster0.a3nj9yv.mongodb.net/test1?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, tlsCAFile=certifi.where())
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# print(client.list_database_names())
# db=client.test1
# print(db.list_collection_names())
# collections=db.python


# class PatientCreate(BaseModel):
#     resourceType: str = "Patient"
#     id: Optional[str] = Field(None)
#     identifier: List[str]
#     name: str
#     gender: str
#     birthDate: Optional[datetime.datetime]
#     address: str
    # @validator('birthDate', pre=True)
    # def validate_birthdate(cls, v):
    #     if isinstance(v, str):
    #         return datetime.datetime.strptime(v, '%Y-%m-%d')
    #     elif isinstance(v, date):
    #         return datetime.datetime.combine(v, datetime.datetime.min.time())
    #     else:
    #         return v
#     # @validator('birthDate')
#     # def validate_birthdate(cls, v):
#     #     return v.isoformat() if v else None

#     # @validator('birthDate')
#     # def validate_birthdate(cls, v):
#     #     if not v or not isinstance(v.date, date):
#     #         raise ValueError('Invalid birthDate format. Must be a valid date string in the format YYYY-MM-DD.')
#     #     return v.date.isoformat()
    # class Config:
    #     arbitrary_types_allowed = True


# try:
    # patient_data = {
    #     "resourceType": "Patient",
    #     "identifier": ["123456"],
    #     "name": "John soem",
    #     "gender": "male",
    #     "birthDate": "1980-01-01",
    #     "address": "123 Main St."
    # }
#     patient_data['birthDate']= datetime.datetime.strptime(patient_data['birthDate'], "%Y-%m-%d")
#     patient_data['birthDate'] = datetime.datetime.combine(patient_data['birthDate'], datetime.datetime.min.time())
#     patient = PatientCreate(**patient_data)
# except ValidationError as e:
#     print(e)
# import datetime



# try:
#     # patient.birthDate = datetime.datetime.combine(patient.birthDate, datetime.time.min)
#     # patient.birthDate=patient.birthDate.strftime('%Y-%m-%d')
#     # patient.birthDate=datetime.datetime.strptime(patient.birthDate,"%Y-%m-%d")
#     # try:
#     #     patient.birthDate= datetime.datetime.strptime(patient.birthDate, "%Y-%m-%d")
#     # except Exception as e:
#     #     print(e)
#     # try:
#     #     patient.birthDate = datetime.datetime.combine(patient.birthDate, datetime.datetime.min.time())
#     # except Exception as e:
#     #     print(e)

    # fhir_patient = FhirPatient(identifier=[{"value": value} for value in patient.identifier],
    #         name=[{"text": patient.name}],
    #         gender=patient.gender,
    #         address=[{"text": patient.address}])
#     fhir_patient_json = fhir_patient.dict(by_alias=True)
#     fhir_patient_json['birthDate']=patient.birthDate
#     print(fhir_patient_json)
#     result = collections.insert_one(fhir_patient_json)
#     print({"id": str(result.inserted_id)})
# except Exception as e:
#     print(e)


# import datetime

# date_str = "2023-05-12"
# # The format of the date string is "%Y-%m-%d", which means
# # year-month-day. You need to pass the same format string to
# # the strptime() method.
# date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
# try:
#     print(FHIRDate(date_obj.isoformat()))
# except Exception as e:
#     print('error')

# print(date_obj)