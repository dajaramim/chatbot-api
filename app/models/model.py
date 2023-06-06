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


class Appointment (BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    #paciente
    patient_name: str
    patient_rut: str
    patient_email: str
    patient_phone: str
    #doctor
    doctor_name: str
    doctor_specialty: str
    disponibility: datetime
    #centro médico
    centre_name: str
    centre_address: str
    date: datetime
    state: str # si se agendó, canceló, reagendó, ya se hizo la cita
    updated_at: Optional[datetime]
    created_at: datetime = datetime.now()
   
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }




