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
    # Convertir los submodelos a diccionarios
    data_dict['doctor'] = data.doctor.dict()
    data_dict['patient'] = data.patient.dict()
    data_dict['centre'] = data.centre.dict()

    logging.info(f"post example with: {data_dict}")
    
    new_data = await db["appointment"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"


@router.post("/agendar/{date}")
async def agendar(date:str,doctor_id:str,id_patient:str, data:Appointment ,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    data_dict_appointment = data.dict()
    data_dict_appointment.pop("id")

    #ingresa el diccionario doctor al objeto doctor dentro de la clase appointment
    data_dict_appointment["doctor"] = data.doctor.dict()
    #se crea la variable data_dict_doctor para utilizarla en el ingreso de variables al objeto appointment
    data_dict_doctor = data_dict_appointment["doctor"]

    #ingresa el diccionario doctor al objeto patient dentro de la clase appointment
    data_dict_appointment["patient"] = data.patient.dict()
    #se crea la variable data_dict_patient para utilizarla en el ingreso de variables al objeto appointment
    data_dict_patient = data_dict_appointment["patient"]


    doctor_user = await db["doctor"].find_one({"_id":ObjectId(doctor_id)})
    patient_user = await db["patient"].find_one({"_id":ObjectId(id_patient)})
    data_dict_appointment["date"] = date
    data_dict_appointment["state"] = "agendado"

    #Se ingresan los datos de doctor_user a data_dict_doctor

    data_dict_doctor["id"] = doctor_user["_id"]
    data_dict_doctor["first_name"] = doctor_user["first_name"]
    data_dict_doctor["last_name"] = doctor_user["last_name"]
    data_dict_doctor["specialty"] = doctor_user["specialty"]
    data_dict_doctor["disponibility"] = doctor_user["disponibility"]

    #Se ingresan los datos de patient_user a data_dict_patient

    data_dict_patient["id"] =  patient_user["_id"]
    data_dict_patient["first_name"] = patient_user["first_name"]
    data_dict_patient["last_name"] = patient_user["first_name"]
    data_dict_patient["rut"] = patient_user["rut"]
    data_dict_patient["email"] = patient_user["email"]
    data_dict_patient["address"] = patient_user["address"]
    data_dict_patient["phone"] = patient_user["phone"]
    

    await db["appointment"].insert_one(data_dict_appointment)

    return "Agendamiento exitoso"
    
@router.post("/paciente/ingresarSistema/{rut}") ###
async def create_new_patient(rut:str,data: Patient, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict_patient = data.dict()
    # Elimino el id que genera pydantic
    data_dict_patient.pop("id")

    buscador = await db["patient"].find_one({"rut": rut})
    if buscador is None:
        data_dict_patient["rut"] = rut
        new_data_patient = await db["patient"].insert_one(data_dict_patient)
        return f"{new_data_patient.inserted_id}"
        
    else:
        
        return "existe"

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
    
# Obtener la disponibilidad más cercana según especialidad
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

@router.get("/especialidad/citasDisponibles/{specialty_name}")  ####
async def get_disponibilidad_specialty(specialty_name:str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    
    logging.info(f"get example with name: {id}")
    data = await db["doctor"].find_one({"specialty": specialty_name})
    disponibility = data["disponibility"]
    if data:
        # Si el dato existe, retornar lista de fechas disponibles
        return disponibility,
        # return JSONResponse(status_code=status.HTTP_200_OK, content=ExampleModel(data))

    else:
        # Si el dato no existe, retorna un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})

#Cambia el estado de una cita a confirmado 
@router.put("/confirmacion/{appointment_id}")
async def confirm_appointment(appointment_id:str, data: Appointment, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):

    #Convertir el modelo a un diccionario
    data_dict = data.dict(exclude_unset=True)
     # Elimino el id que genera pydantic
    data_dict.pop('id', None)
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with id: {id} and data: {data_dict}")

    # Actualizar el dato
    data_dict["state"] = "confirmado"
    await db["appointment"].find_one_and_update({"_id": ObjectId(appointment_id)}, {"$set": data_dict})

    # Retornar un mensaje de éxito
    return data_dict


#Cambia el estado de una cita a cancelado 
@router.put("/cancelar/{appointment_id}")
async def cancel_appointment(appointment_id:str, data: Appointment, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):

    #Convertir el modelo a un diccionario
    data_dict = data.dict(exclude_unset=True)
    # Elimino el id que genera pydantic
    data_dict.pop('id', None)
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with id: {id} and data: {data_dict}")

    # Actualizar el dato
    data_dict["state"] = "cancelado"
    await db["appointment"].find_one_and_update({"_id": ObjectId(appointment_id)}, {"$set": data_dict})

    # Retornar un mensaje de éxito
    return data_dict

@router.put("/reagendar/{appointment_id}")
async def reschedule(date:str,appointment_id:str,data: Appointment,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    
    #Convertir el modelo a un diccionario
    data_dict_appointment = data.dict(exclude_unset=True)
    # Elimino el id que genera pydantic
    data_dict_appointment.pop('id', None)
    
    data_dict_appointment["date"] = date
    data_dict_appointment["state"] = "reagendado"

    await db["appointment"].find_one_and_update({"_id": ObjectId(appointment_id)}, {"$set": data_dict_appointment})

    return data_dict_appointment



    

 
    


    




""" 
Daniel
@router.get("/disponibilidad/{doctor_id}") LISTO
@router.get("/sugerencia")
@router.get("/lista_de_espera") 

Nico

@router.put("/reagendar")

Ricardo


"""



# confirmar una cita  
# 1- get appointment según id paciente, doctor(muestra nombre y especialidad, centro médico
# 2- put appointment (fecha y estado)

# Confirmar multiples Citas
# 1- get appointment según id paciente
# 2- Muestra las citas una a una (CHATBOT)
# 3- put confirmacion
 

# Cancelación espontánea
# 1- get appointment según id paciente
# 2- put cancelar
#
#   

# Reagendamiento automático
# 1- get appointment según id paciente
# 2- /disponibilidad

# Bloques de Agenda
# 1- get appointment suspendida
# 2- get appointment nueva
# 3- put confirmacion

# Lista de espera
# get lista de espera
# put confirmar

# Derivaciones 
# get paciente
# 
# 
# # 
