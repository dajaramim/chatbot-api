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
##                   OBTENER LOS DATOS
#                    Obtener TODOS LOS DOCTORES
@router.get("/doctor")
async def get_all_doctors(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Doctor]:
    logging.info("Inside get_all_doctors function")
    try:
        # obtengo todos los elementos de campaign enlistados en un máximo de 100 elementos
        result = await db["doctor"].find().to_list(length=100)
        logging.info(f"Result: {result}")
        return [Doctor(**doctor) for doctor in result]
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

# Obtener disponibilidad Doctor (lista de fechas disponible)
@router.get("/doctor/disponibilidad/{doctor_id}")
async def get_disponibilidad(doctor_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    
    logging.info(f"get example with name: {id}")
    data = await db["doctor"].find_one({"_id": ObjectId(doctor_id)})

    if data:
        # Si el dato existe, retornar lista de fechas disponibles
        return data["disponibility"]
        # return JSONResponse(status_code=status.HTTP_200_OK, content=ExampleModel(data))

    else:
        # Si el dato no existe, retorna un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})
    
# Obtener una lista de las citas según el ID del paciente


###         SUGERENCIA
""" @router.get("/sugerencia")
async def get_sugerencia(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    
 """



##                    POBLAR DATOS

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
@router.post("/appointment")
async def create_appoinment(data: Appointment, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")

    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["appointment"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"


# ENDPOINTS QUE NOS PIDE ALLOXENTRIC
#Obtener todas las campañas


@router.put("/confirmacion/{appointment_id}")
async def update_campaign(appointment_id:str, data: Appointment, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):

#Convertir el modelo a un diccionario
    data_dict = data.dict(exclude_unset=True)
    data_dict.pop('id', None)
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with id: {id} and data: {data_dict}")

    # Actualizar el dato
    data_dict["state"] = "confirmado"
    await db["appointment"].find_one_and_update({"_id": ObjectId(appointment_id)}, {"$set": data_dict})

    # Retornar un mensaje de éxito
    return data_dict

""" 
Daniel
@router.get("/disponibilidad/{doctor_id}") LISTO
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
#  
# 1- get appointment según id paciente, doctor(muestra nombre y especialidad, centro médico
# 2- put appointment (fecha y estado)

# Confirmar multiples Citas
# 1- get appointment según id paciente
# 2- Muestra las citas una a una (CHATBOT)
 

# Cancelación espontánea
# 1- get appointment según id paciente
# 2- put cancelar
#
#   

# Reagendamiento automático
# 1- get appointment según id paciente
# 2- /disponibilidad