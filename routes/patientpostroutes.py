from fastapi import APIRouter, Request
from Models.models import Patient,DateEncoder
from config.db import DatabaseManager
from config.db_tables import Patient as pat
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

patient= APIRouter()

#post route for creating a new Patient
@patient.post("/fhir/patient")
async def create_patient(patient: Patient, request: Request):
    try:
        connection=DatabaseManager()
        # with connection.conn.cursor() as cursor:
        primary_key_uuid = str(uuid4())
        patient.id = primary_key_uuid
        patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)
        # Create a new instance of the Patient model
        patient_model = pat(id=primary_key_uuid, patient=patient_json)
        # Add the patiet model to the session
        connection.session.add(patient_model)
        # Commit the changes to the database
        connection.session.commit()
        print("success")
    except Exception as e:
        print(e)
        return e  
    finally:
        if connection:                   # Close the session and connection
            connection.close_connection()
    

#getting names of patients
@patient.get("/patient")
async def get_all_patient(request: Request):
    try:
        connection = DatabaseManager()
        session: Session = connection.session
        row = session.query(pat)
        print(row)
        names = []
        for row in row:
            patient_data = json.loads(row.patient) if row and row.patient else {}
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            names.append(name)
        return templates.TemplateResponse("patients/patient.html", {"request": request, "names": names})

    except Exception as e:
            print("Error retrieving patient names:", e)
            return templates.TemplateResponse("patients/patient.html", {"request": request, "names": []})
    finally:
        if connection:
            connection.close_connection()



