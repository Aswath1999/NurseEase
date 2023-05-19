from fastapi import APIRouter
from Models.models import Patient,DateEncoder
from config.connection import DatabaseManager
import json


patient= APIRouter()

#post route for creating a new Patient
@patient.post("/fhir/patient")
async def create_patient(patient: Patient):
    try:
        connection=DatabaseManager()
        with connection.conn.cursor() as cursor:
            patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)
            cursor.execute(
            "INSERT INTO Patient (patient) VALUES (%s)",
            (patient_json,))
            connection.conn.commit()
            print("success")
    except Exception as e:
        print(e)
        return e
    finally:
        if connection:
            print(patient_json)
            connection.close_connection()
            return "Connection closed"
    


@patient.get("/")
async def get_patient():
    return 'hi'


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

