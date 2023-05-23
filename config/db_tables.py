from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,String
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4


Base = declarative_base()

class Vitals(Base):
    __tablename__ = 'vitals'
    id=Column(String, primary_key=True, default=str(uuid4()))
    vitals = Column(JSONB)

class Patient(Base):
    __tablename__ = 'patient'
    id=Column(String, primary_key=True, default=str(uuid4()))
    patient = Column(JSONB)


