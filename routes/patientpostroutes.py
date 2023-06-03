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

#getting names of patients
@patient.post("/fhir/patient")
@is_logged_in
async def create_patient(request: Request, session: Session = Depends(database_connection)):
    try:
        form = await request.form()
        identifier_values = [form.get("identifier1"), form.get("identifier2")]
        given_name = form.get("given")
        family_name = form.get("family")
        phone_number = form.get("telecom")
        gender = form.get("gender")
        birth_date = form.get("birthDate")
        city = form.get("city")
        state = form.get("state")
        country = form.get("country")
        assigned_to = form.get("assigned")
        print(assigned_to)
        
        patient = Patient(
            identifier=[
                {"value": identifier_values[0]},
                {"value": identifier_values[1]}
            ],
            name=[
                {
                    "given": [given_name],
                    "family": family_name
                }
            ],
            telecom=[
                {
                    "system": "phone",
                    "value": phone_number
                }
            ],
            gender=gender,
            birthDate=birth_date,
            address=[
                {
                    "city": city,
                    "state": state,
                    "country": country
                }
            ]
        )
        
        primary_key_uuid = str(uuid4())
        patient.id = primary_key_uuid
        
        patient_json = json.dumps(patient.dict(by_alias=True), cls=DateEncoder)
        if assigned_to== "self": 
            print("ok")
            session_data_json = request.cookies.get("session_data") 
            session_data = json.loads(session_data_json)
            user_id = session_data.get("user_id")  
            print(user_id)
            patient_model = pat(id=primary_key_uuid, patient=patient_json,user_id=user_id,treatment_in_progress=True)
            print(patient_model)
        else:
            patient_model = pat(id=primary_key_uuid, patient=patient_json,treatment_in_progress=True)
        
        session.add(patient_model)
        session.commit()
        print("sucess")
        return templates.TemplateResponse("success.html", {"request": request})
    
    except Exception as e:
        print(e)
        return e

@patient.get("/createpatient")
@is_logged_in
async def create_patient(request: Request):
    try:
       return templates.TemplateResponse("patients/createpatient.html", {"request": request})
    except Exception as e:
        print(e)


@patient.get("/fhir/patient")
@is_logged_in
async def get_all_patient(request: Request,session: Session = Depends(database_connection)):
    try:
        # session: Session = connection.session
        row = session.query(pat)
        print(type(row))
        names = []       #try whether you can directly query only the names of the patients
        for row in row:
            patient_data = json.loads(row.patient) if row and row.patient else {}
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            names.append(name)
        return templates.TemplateResponse("patients/patient.html", {"request": request, "names": names})

    except Exception as e:
        print("Error")
        print("Error retrieving patient names:", e)
        return e
        






# @patient.get("/patient")
# async def get_all_patient(request: Request,session: Session = Depends(database_connection)):
#     try:
#         # session: Session = connection.session
#         row = session.query(pat)
