from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,String,Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
from sqlalchemy.sql.expression import text


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

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=str(uuid4()))
    email = Column(String, unique= True, nullable=False)
    password = Column(String,nullable=False)
    is_verified = Column(Boolean, default =False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default = text('now()'))

# have to still create observation table with patient id as foreign key