from fastapi import APIRouter
from Models.patient import PatientCreate
from fhir.resources.patient import Patient as FhirPatient
from bson import ObjectId
from config.db import collection


patient= APIRouter()


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
      
@patient.get("/")
async def get_patient():
    return 'hi'
