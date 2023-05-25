from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,String,Boolean
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

class User(Base):
    __tablename__ = 'user'
    id=Column(String, primary_key=True, default=str(uuid4()))
    username=Column(String, unique=True)
    password=Column(String(255))
    # activation = Column(Boolean, default=False)


# have to still create observation table with patient id as foreign key