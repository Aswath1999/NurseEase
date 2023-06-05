from fastapi import APIRouter, Request,Depends
from Models.models import Patient,DateEncoder,SessionData
from config.db import database_connection
from config.db_tables import User,Patient as pat
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .authentication import  is_logged_in
from sqlalchemy import or_,func, and_
from sqlalchemy.orm import aliased

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
        session_data_json = request.cookies.get("session_data") 
        session_data = json.loads(session_data_json)
        user_id = session_data.get("user_id")  
        if assigned_to== "self": 
            patient_model = pat(id=primary_key_uuid, patient=patient_json,user_id=user_id,treatment_in_progress=True)
            print(patient_model)
        else:
            try:
                print("sfjkafba")
                patient_alias = aliased(pat)
                users = session.query(User).outerjoin(patient_alias, User.patients).group_by(User.id).having(and_(User.is_online == True, func.count(patient_alias.id) < 3)).filter(User.id != user_id).all()
                if users:
                    user_id=users[0].id
                    print(user_id)
                    patient_model = pat(id=primary_key_uuid, patient=patient_json,user_id=user_id,treatment_in_progress=True)
                else:  
                   patient_model = pat(id=primary_key_uuid, patient=patient_json,treatment_in_progress=True) #leave user as empty to assign later
            except Exception as e:
                print(e)

  
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
        


@patient.get("/users")
async def get_users(request:Request,session: Session = Depends(database_connection) ):
    try:
        # Create an aliased instance of the Patient table for the subquery
        patient_alias = aliased(pat)

        users = session.query(User).outerjoin(patient_alias, User.patients).group_by(User.id).having(and_(User.is_online == True, func.count(patient_alias.id) < 3)).filter(User.id != '8e1ce70e-f6b4-44d5-ab78-07841044b92f').all()
        print("Users")
        return users
    except Exception as e:
        print(e)
        return e


#provide unassigned patients as well
# @patient.get("/patient")
# async def get_all_patient(request: Request,session: Session = Depends(database_connection)):
#     try:
#         # session: Session = connection.session
#         row = session.query(pat)
