from http.client import HTTPException
import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.auth import get_db
from app.models.model import Patient
from app.models.model import Doctor
from app.models.model import Centre
from app.models.model import Appointment

router = APIRouter(
    tags=["agendamiento"],
    responses={404: {"description": "Not found"}},
)
##                  POBLAR DATOS

#Ingresar Doctor
@router.post("/doctor")
async def create_doctor(data: Doctor, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")
    
    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["doctor"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

#Ingresar Paciente
@router.post("/patient")
async def create_patient(data: Patient, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")
    
    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["patient"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

#Ingresar centro médico
@router.post("/centre")
async def create_centre(data: Centre, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")
    
    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["centre"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

#Crear una cita
@router.post("/appoinment")
async def create_appoinment(data: Appointment, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")
    
    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["appoinment"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"




# ENDPOINTS QUE NOS PIDE ALLOXENTRIC
#Obtener todas las campañas
""" @router.get("/disponibilidad/{doctor_id}")

# Obtener una campaña según un id
@router.post("/agendar")

#Crear una campaña
@router.put("/reagendar")

#Editar una campaña
@router.put("/confirmacion")

#Eliminar una campaña
@router.put("/cancelar")

@router.put("/sugerencia")

@router.get("/lista_de_espera") """
