from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, validator, EmailStr
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.address import Address
from json import JSONEncoder
import re


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)

class Patient(BaseModel):
    resourceType: str = Field("Patient", const=True)
    id: Optional[str]
    identifier: Optional[List[Identifier]]
    name: Optional[List[HumanName]]
    telecom: Optional[List[ContactPoint]]
    gender: Optional[str]
    birthDate: Optional[date]
    address: Optional[List[Address]]

    @validator('birthDate', pre=True)
    def validate_birthdate(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v)
        else:
            return v

class UserCreation(BaseModel):
    id: str
    email: EmailStr
    username: str
    password: str
    is_verified: bool=False
    @validator('password')
    def validate_password(cls, password: str) -> str:
        # Password must be at least 8 characters long
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Password must contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
        return password
    
class SessionData(BaseModel):
    user_id: str

"""
patient_data = {
    "id": "123",
    "identifier": [
        {"value": "ABC123"},
        {"value": "XYZ789"}
    ],
    "name": [
        {
            "given": ["John"],
            "family": "Doe"
        }
    ],
    "telecom": [
        {
            "system": "phone",
            "value": "123-456-7890"
        }
    ],
    "gender": "male",
    "birthDate": {
        "date": "1980-01-01"
    },
    "address": [
        {
            "city": "New York",
            "state": "NY",
            "country": "USA"
        }
    ]
}
patient = Patient(**patient_data)
print(patient)
"""

