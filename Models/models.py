from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, validator
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.address import Address
from json import JSONEncoder


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

patient_data = {
    "resourceType": "Patient",
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
    "birthDate": "1980-01-01",
    "address": [
        {
            "city": "New York",
            "state": "NY",
            "country": "USA"
        }
    ]
}
print(type(patient_data))

patient = Patient(**patient_data)
# print(patient)
patient=patient.dict(by_alias=True)
# print(patient)





'''
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
            return datetime.datetime.strptime(v, '%Y-%m-%d').date()
        # elif isinstance(v, date):
        #     return datetime.datetime.combine(v, datetime.datetime.min.time())
        else:
            return v
    class Config:
        arbitrary_types_allowed = True

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
patient = PatientCreate(**patient_data)
print(patient)

'''


'''
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fhir.resources import FHIRAbstractModel
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.address import Address
from fhir.resources.fhirprimitiveextension import FHIRPrimitiveExtension
from fhirclient.models.fhirdate import FHIRDate

    

class Patient(FHIRAbstractModel):
    resourceType = Field("Patient", const=True)
    id: Optional[str]
    identifier: Optional[List[Identifier]]
    name: Optional[List[HumanName]]
    telecom: Optional[List[ContactPoint]]
    gender: Optional[str]
    birthDate: Optional[FHIRDate]
    address: Optional[List[Address]]
   
    @classmethod
    def from_dict(cls, data: dict) -> "Patient":
        if "extension" in data:
            data["extension"] = [
                FHIRPrimitiveExtension.parse_obj(extension) for extension in data["extension"]
            ]
        return super().from_dict(data)
'''