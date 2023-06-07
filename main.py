from fastapi import FastAPI
from routes.patientpostroutes import patient
from routes.auth_routes import auth
from routes.observation_routes import observation
from fastapi.staticfiles import StaticFiles


app=FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth)
app.include_router(patient)
app.include_router(observation)
