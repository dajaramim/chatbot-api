from http.client import HTTPException
import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.auth import get_db
from app.models.model import Appointment

router = APIRouter(
    tags=["agendamiento"],
    responses={404: {"description": "Not found"}},
)
##                   OBTENER LOS DATOS
#                    Obtener TODOS LOS DOCTORES
@router.get("/appoinment")
async def get_all_doctors(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Appointment]:
    logging.info("Inside get_all_doctors function")
    try:
        # obtengo todos los elementos de campaign enlistados en un máximo de 100 elementos
        result = await db["appointment"].find().to_list(length=100)
        logging.info(f"Result: {result}")
        return [Appointment(**appointment) for appointment in result]
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

##                    POBLAR DATOS

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

""" 
Daniel
@router.get("/disponibilidad/{doctor_id}")
@router.get("/sugerencia")
@router.get("/lista_de_espera") 

Nico
@router.post("/agendar")
@router.put("/reagendar")

Ricardo
@router.put("/confirmacion")
@router.put("/cancelar")

"""

# confirmar una cita
# 1- get paciente
# 2- get appointment según id paciente
# 3- get doctor(muestra nombre y especialidad)
# 4- get centro médico con el id del doctor
# 5- put appointment (fecha)
# 
# 
# 
# 
# 
# 
# ##
# #
