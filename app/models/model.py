from bson import ObjectId
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Patient(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    first_name: str
    last_name: str
    rut: str
    email: str
    address: str
    phone: str
    updated_at: Optional[datetime]
    created_at: datetime = datetime.now()
   
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Doctor(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    first_name: str
    last_name: str
    specialty: str
    disponibility: bool 
    updated_at: Optional[datetime]
    created_at: datetime = datetime.now()
   
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Centre (BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    address: str
    updated_at: Optional[datetime]
    created_at: datetime = datetime.now()
   
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Appointment (BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    patient_id: str
    centre_id: str
    doctor_id: str
    state: str # si se agendó, canceló, reagendó, ya se hizo la cita
    updated_at: Optional[datetime]
    created_at: datetime = datetime.now()
   
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }




