from fastapi import APIRouter, Request,Depends,Form,status, Query
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
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
import random 

from faker import Faker
def get_faker_instance():
    return Faker()

templates = Jinja2Templates(directory="templates")

observation= APIRouter()

@observation.get("/vitals/{id}")
async def vitals(id: str, request: Request):
    try:
        return templates.TemplateResponse("Observation/vitals.html", {"request": request, "id": id})
    except Exception as e:
        print(e)

         
"""
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
            id=str(uuid4()),  # Generate a new unique id
            patient_id=observation.subject,
            timestamp=observation.effectiveDateTime,
            o2_level=observation.valueQuantity,
            heart_rate=hr_value,
            temperature=temp_value,
        )
        session.add(vital_signs)
        session.commit()
        session.refresh(vital_signs)
        redirect_url = f"/individualpatient/{patient_id}"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        print(e)
        return {"error": str(e)}
    
"""
@observation.get("/fhir/observation")
@is_logged_in
async def get_observation_data(
    request: Request,
    id: str = Query(..., description="patientId"),
    session: Session = Depends(database_connection)
):
    try:
        today = date.today()
        vitals_today = session.query(VitalSigns).filter(
            VitalSigns.timestamp >= datetime.combine(today, datetime.min.time()),
            VitalSigns.timestamp < datetime.combine(today, datetime.max.time()),
            VitalSigns.patient_id == id
        ).all()
        vitals = session.query(VitalSigns).filter(VitalSigns.patient_id == id).order_by(VitalSigns.timestamp).all()
        if vitals:
            # Extract the oxygen level and heart rate from each vital sign record
            timestamps = [vital.timestamp.isoformat() for vital in vitals]
            o2_levels = [vital.o2_level for vital in vitals]
            temperatures=[vital.temperature for vital in vitals]
            heart_rates = [vital.heart_rate for vital in vitals]
            o2_levels_today = [vital.o2_level for vital in vitals_today]
            time_today= [vital.timestamp.isoformat() for vital in vitals_today]
            heart_rates_today = [vital.heart_rate for vital in vitals_today]
            temp_today = [vital.temperature for vital in vitals_today]
            return {
                "timestamps": timestamps,
                "o2_levels": o2_levels,
                "heart_rates": heart_rates,
                "temperatures": temperatures,
                "time_today": time_today,
                "temperature_today":temp_today,
                "heart_rates_today": heart_rates_today,
                "o2_levels_today": o2_levels_today

            }
        else:
            return {
                "timestamps": [],
                "o2_levels": [],
                "heart_rates": [],
                "temperatures":[],
                "time_today":[],
                "temperature_today":[],
                "heart_rates_today":[],
                "o2_levels_today":[],
            }
    except SQLAlchemyError as e:
        print("Error retrieving observation data:", e)
        return e




@observation.post("/fhir/observation/{patient_id}")
async def change_observation(
    patient_id: str,  # Extract patient ID from URL using a path parameter
    session: Session = Depends(database_connection),
    faker: Faker = Depends(get_faker_instance)  # Create a dependency for Faker
):
    try:
        # Generate fake data using Faker
        o2_level = faker.random_int(min=90, max=95)
        hr_value = faker.random_int(min=60, max=120)
        temp_value = round(random.uniform(95.0, 105.0), 1)
        
        vital_signs = VitalSigns(
            id=str(uuid4()),  # Generate a new unique id
            patient_id=patient_id,  # Use patient ID from URL
            timestamp=datetime.now(),
            # timestamp=faker.date.recent(),
            o2_level=o2_level,
            heart_rate=hr_value,
            temperature=temp_value,
        )
        session.add(vital_signs)
        session.commit()
        session.refresh(vital_signs)
        return {"success": True}
    except SQLAlchemyError as e:
        return {"error": str(e)}

"""
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Real-time Data</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>Real-time Data</h1>
    <div id="data-container"></div>

    <script>
        // Function to update the data container with the received data
        function updateDataContainer(data) {
            // Update the HTML content of the data container
            $('#data-container').html(data);
        }

        // Function to send the AJAX request and update the data container
        function fetchData() {
            $.ajax({
                url: '/real-time-data',  // URL of the FastAPI route handler
                type: 'POST',
                success: function(response) {
                    // Update the data container with the received data
                    updateDataContainer(response);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching data:', error);
                }
            });
        }

        // Schedule the AJAX request to be executed every 5 seconds
        setInterval(fetchData, 5000);

        // Initial data fetch
        fetchData();
    </script>
</body>
</html>

"""
"""
// Function to send a POST request to generate and save random data
function sendObservationData(patientId) {
  $.ajax({
    url: `/fhir/observation/${patientId}`,
    type: 'POST',
    success: function(response) {
      console.log('Data generated and saved successfully');
    },
    error: function(xhr, status, error) {
      console.error('Error generating and saving data:', error);
    }
  });
}

// Function to send a GET request to retrieve the latest data for visualization
function getObservationData(patientId) {
  $.ajax({
    url: `/fhir/observation/${patientId}`,
    type: 'GET',
    success: function(response) {
      // Update the visualization with the retrieved data
      // (You will need to write the code to update the visualization here)
      console.log('Data retrieved successfully');
    },
    error: function(xhr, status, error) {
      console.error('Error retrieving data:', error);
    }
  });
}

// Example usage: Trigger the POST and GET requests at the specified intervals
setInterval(function() {
  const urlParts = window.location.href.split('/');
  const patientId = urlParts[urlParts.length - 1];
  sendObservationData(patientId);
}, 5000); // 5 seconds interval

setInterval(function() {
  const urlParts = window.location.href.split('/');
  const patientId = urlParts[urlParts.length - 1];
  getObservationData(patientId);
}, 10000); // 10 seconds interval
"""