from fastapi import APIRouter, Request,Depends
from Models.models import Patient,DateEncoder,SessionData
from config.db import DatabaseManager,database_connection
from config.db_tables import Patient as pat
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .authentication import  is_logged_in


templates = Jinja2Templates(directory="templates")

patient= APIRouter()

#post route for creating a new Patient
@patient.post("/fhir/patient")
async def create_patient(patient: Patient, request: Request,db_manager: DatabaseManager = Depends(database_connection)):
    try:
        primary_key_uuid = str(uuid4())
        patient.id = primary_key_uuid
        patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)
        # Create a new instance of the Patient model
        patient_model = pat(id=primary_key_uuid, patient=patient_json)
        # Add the patiet model to the session
        db_manager.session.add(patient_model)
        # Commit the changes to the database
        db_manager.session.commit()
        print("success")
    except Exception as e:
        print(e)
        return e  
    finally:
        if db_manager:                   # Close the session and connection
            db_manager.close_connection()
    
#getting names of patients

@patient.get("/fhir/patient")
@is_logged_in
async def get_all_patient(request: Request,user_id: int = Depends(is_logged_in),session: Session = Depends(database_connection)):
    try:
        # session: Session = connection.session
        if user_id is None:
            return RedirectResponse(url='/login')
        row = session.query(pat)
        names = []
        for row in row:
            patient_data = json.loads(row.patient) if row and row.patient else {}
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            names.append(name)
        return templates.TemplateResponse("patients/patient.html", {"request": request, "names": names})

    except Exception as e:
        print("Error")
        print("Error retrieving patient names:", e)
        return e
        






