from pydantic import BaseModel, Field, validator
from typing import List,Optional
import datetime
from datetime import date
from fhirclient.models.fhirdate import FHIRDate

class PatientCreate(BaseModel):
    resourceType: str = "Patient"
    id: Optional[str] = Field(None)
    identifier: List[str]
    name: str
    gender: str
    birthDate: Optional[FHIRDate]
    address: str
    @validator('birthDate', pre=True)
    def validate_birthdate(cls, v):
        if isinstance(v, str):
            return datetime.datetime.strptime(v, '%Y-%m-%d')
        elif isinstance(v, date):
            return datetime.datetime.combine(v, datetime.datetime.min.time())
        else:
            return v
    class Config:
        arbitrary_types_allowed = True

    