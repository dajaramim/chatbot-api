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
#Obtener todas las campañas
@router.get("/disponibilidad/{doctor_id}")

# Obtener una campaña según un id
@router.post("/agendar")

#Crear una campaña
@router.put("/reagendar")

#Editar una campaña
@router.put("/confirmacion")

#Eliminar una campaña
@router.put("/cancelar")

@router.put("/sugerencia")

@router.get("/lista_de_espera")
