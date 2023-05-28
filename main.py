from fastapi import FastAPI
from routes.patientpostroutes import patient
from routes.auth_routes import auth

app=FastAPI(debug=True)
app.include_router(auth)
app.include_router(patient)

