from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,String,Boolean, TIMESTAMP, ForeignKey,DateTime,Float
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
from sqlalchemy.sql.expression import text
from sqlalchemy import select
from sqlalchemy.orm import relationship


Base = declarative_base()


"""
class VitalSigns(Base):
    __tablename__ = 'vital_signs'
    id = Column(String, primary_key=True,default=str(uuid4()))
    patient_id = Column(String, ForeignKey('patient.id'))
    timestamp = Column(DateTime)
    observation = Column(JSONB)

    patient = relationship("Patient", backref="vital_signs")
"""
class VitalSigns(Base):
    __tablename__ = 'vital_signs'
    id = Column(String, primary_key=True, default=str(uuid4()))
    patient_id = Column(String, ForeignKey('patient.id'))
    timestamp = Column(DateTime)
    o2_level = Column(Float)
    patient = relationship("Patient", backref="vital_signs")

class Patient(Base):
    __tablename__ = 'patient'
    id=Column(String, primary_key=True, default=str(uuid4()))
    patient = Column(JSONB)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    treatment_in_progress = Column(String, nullable=True)
    user = relationship("User", back_populates="patients")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=str(uuid4()))
    username=Column(String, unique=True)
    email = Column(String, unique= True, nullable=False)
    password = Column(String,nullable=False)
    is_verified = Column(Boolean, default =False, nullable=False)
    is_online = Column(Boolean, default =False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default = text('now()'))
    patients = relationship("Patient", back_populates="user")


# have to still create observation table with patient id as foreign key


