from fastapi import APIRouter
from Models.models import Patient,DateEncoder
from config.connection import DatabaseManager
import json
from uuid import uuid4


patient= APIRouter()

#post route for creating a new Patient
@patient.post("/fhir/patient")
async def create_patient(patient: Patient):
    try:
        connection=DatabaseManager()
        with connection.conn.cursor() as cursor:
            primary_key_uuid = str(uuid4())
            patient.id = primary_key_uuid
            patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)
            insert_query = "INSERT INTO Patient (id, patient) VALUES (%s, %s)"
            cursor.execute(insert_query, (primary_key_uuid, patient_json))
            connection.conn.commit()
            print("success")
    except Exception as e:
        print(e)
        return e
    finally:
        if connection:
            connection.close_connection()
            return "Connection closed"
    


@patient.get("/patient")
async def get_all_patient():
    try:
        connection=DatabaseManager()
        with connection.conn.cursor() as cursor:
            query = "SELECT patient->'name' FROM Patient"
            cursor.execute(query)
            result = cursor.fetchall()
            patients=[]
            for row in result:
                patient_name_json = json.dumps(row)
                print(patient_name_json)
                # name=patient_name_json['given']
                # print(name)
                patient_name_data = json.loads(patient_name_json)
                print(patient_name_json)
                patients.append(patient_name_data[0][0]['given'])
    except Exception as e:
        print("Error retrieving patient names:", e)
    finally:
        if connection:
            if patients:
                connection.close_connection()
                return patients
            connection.close_connection()



"""
@patient.post("/fhir/patient")
async def create_patient(patient: PatientCreate):
    fhir_patient = FhirPatient(identifier=[{"value": value} for value in patient.identifier],
        name=[{"text": patient.name}],
        gender=patient.gender,
        address=[{"text": patient.address}])
    fhir_patient_json = fhir_patient.dict(by_alias=True)
    fhir_patient_json['birthDate']=patient.birthDate
    result = collection.insert_one(fhir_patient_json)
    return {"id": str(result.inserted_id)}
"""

