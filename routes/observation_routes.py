from fastapi import APIRouter, Request,Depends,Form
from Models.models import Observation, ObservationComponent
from config.db import database_connection
from config.db_tables import User,Patient as pat,VitalSigns
import json
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .authentication import  is_logged_in
from sqlalchemy import or_,func, and_
from sqlalchemy.orm import aliased
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


templates = Jinja2Templates(directory="templates")

observation= APIRouter()

@observation.get("/vitals")
async def vitals(request: Request):
    try:
       return templates.TemplateResponse("Observation/vitals.html", {"request": request})
    except Exception as e:
        print(e)
         

@observation.post("/fhir/observation")
async def change_observation(
    request: Request,
    session: Session = Depends(database_connection)
    ): # Use your Observation Pydantic mo, session: Session = Depends(database_connection)# Add the o2_level field as a form parameter
    try:
        form = await request.form()
        patient_id = form.get('subject')
        O2_level=float(form.get('valueQuantity.value'))
        date = datetime.fromisoformat(form.get('effectiveDateTime'))
        hr_value = float(form.get('hrValueQuantity'))
        temp_value = float(form.get('tempValueQuantity'))
        observation = Observation(
            resourceType='Observation',
            code='http://loinc.org|20564-1',
            subject=patient_id,
            effectiveDateTime=date,
            valueQuantity=O2_level,
            component=[
                ObservationComponent(code='http://loinc.org|8867-4', valueQuantity=hr_value),
                ObservationComponent(code='http://loinc.org|8310-5', valueQuantity=temp_value),
            ]
        )
        vital_signs = VitalSigns(
            patient_id=observation.subject,
            timestamp=observation.effectiveDateTime,
            o2_level=observation.valueQuantity,
            heart_rate=hr_value,
            temperature=temp_value,
        )
        session.add(vital_signs)
        session.commit()
        session.refresh(vital_signs)
        return {"message": "Observation created successfully", "observation_id": vital_signs.id}
    except SQLAlchemyError as e:
        print(e)
        return {"error": str(e)}
    
