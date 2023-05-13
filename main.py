from fastapi import FastAPI
from routes.patientpostroutes import patient

app=FastAPI(debug=True)
app.include_router(patient)

