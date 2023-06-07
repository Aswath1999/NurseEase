from fastapi import APIRouter, Request,Depends
from Models.models import Patient,DateEncoder,SessionData
from config.db import database_connection
from config.db_tables import User,Patient as pat,VitalSigns
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .authentication import  is_logged_in
from sqlalchemy import or_,func, and_,select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError

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
            patient_model = pat(id=patient.id,patient=patient_json,user_id=user_id,treatment_in_progress=True)
            print(patient_model)
        else:
            try:
                print("sfjkafba")
                patient_alias = aliased(pat)
                users = session.query(User).outerjoin(patient_alias, User.patients).group_by(User.id).having(and_(User.is_online == True, func.count(patient_alias.id) < 3)).filter(User.id != user_id).all()
                if users:
                    user_id=users[0].id
                    print(user_id)
                    patient_model = pat(id=patient.id,patient=patient_json,user_id=user_id,treatment_in_progress=True)
                else:  
                   patient_model = pat(id=patient.id,patient=patient_json,treatment_in_progress=True) #leave user as empty to assign later
            except Exception as e:
                print(e)

  
        session.add(patient_model)
        session.commit()
        session.refresh(patient_model)
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
        names = []    
        ids = []    
        for row in row:
            patient_data = json.loads(row.patient) if row and row.patient else {}
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            patient_id = patient_data.get('id')
            names.append(name)
            print(names)
            ids.append(patient_id)
            print(ids)
        return templates.TemplateResponse("patients/allpatients.html", {"request": request,"names_ids": zip(names, ids)})

    except Exception as e:
        print("Error")
        print("Error retrieving patient names:", e)
        return e

from sqlalchemy.orm import aliased

@patient.get("/individualpatient/{id}")
@is_logged_in
async def get_individual_patient(request: Request, id: str,session: Session = Depends(database_connection)):
    try:
        print("s")
        # Query the patient table based on the id
        patient = session.query(pat).filter(pat.id == id).first()
        vitals = session.query(VitalSigns).filter(VitalSigns.patient_id == id).order_by(VitalSigns.timestamp).all()
        print(patient)
        if patient:
            patient_data = json.loads(patient.patient)
            # Extract the required attributes from the patient object
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            address = patient_data.get('address', [{}])[0].get('city', '')
            # Add additional attribute access as needed
            print(patient_data)
            patient_data = {
                'name': name,
                'id': id,
                'address': address,
                # Add additional attributes as needed
                # Example: 'gender': patient.gender,
                # Example: 'birth_date': patient.birth_date,
                # Example: 'phone_number': patient.phone_number
            }
            if vitals:
                # Extract the oxygen level and heart rate from each vital sign record
                timestamps = [vital.timestamp.isoformat() for vital in vitals]
                o2_levels = [vital.o2_level for vital in vitals]
                heart_rates = [vital.heart_rate for vital in vitals]
                return templates.TemplateResponse("patients/patient.html", {"request": request,"timestamps": timestamps, "patient": patient_data,"o2_levels": o2_levels, "heart_rates": heart_rates})
        else:
            return {"error": "Patient not found"}
    except SQLAlchemyError as e:
        print("Error retrieving patient:", e)
        return e


"""   
all patients in the database with attributes
@patient.get("/individualpatient/{id}")
@is_logged_in
async def get_individual_patient(request: Request, session: Session = Depends(database_connection)):
    try:
        rows = session.query(pat).all()
        patients = []
        for row in rows:
            patient_data = json.loads(row.patient) if row and row.patient else {}
            name = patient_data.get('name', [{}])[0].get('given', [None])[0]
            patient_id = patient_data.get('id')
            address = patient_data.get('address', [{}])[0].get('city', '')
            # Add additional fields as needed
            # Example: gender = patient_data.get('gender', '')
            # Example: birth_date = patient_data.get('birthDate', '')
            # Example: phone_number = patient_data.get('telecom', [{}])[0].get('value', '')
            
            patient = {
                'name': name,
                'id': patient_id,
                'address': address,
                # Add additional fields as needed
                # Example: 'gender': gender,
                # Example: 'birth_date': birth_date,
                # Example: 'phone_number': phone_number
            }
            patients.append(patient)
        return templates.TemplateResponse("patients/patient.html", {"request": request, "patients": patients})
    except Exception as e:
        print("Error retrieving patient names:", e)
        return e
"""

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



#provide all observations of a particular patient and present them in graphs