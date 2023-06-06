from http.client import HTTPException
import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.auth import get_db
from app.models.model import Campaign


router = APIRouter(
    tags=["campaign"],
    responses={404: {"description": "Not found"}},
)
#Obtener todas las campañas
@router.get("/campaigns")
async def get_all_campanias(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Campaign]:
    logging.info("Inside get_all_campanias function")
    try:
        # obtengo todos los elementos de campaign enlistados en un máximo de 100 elementos
        result = await db["campaign"].find().to_list(length=100)
        logging.info(f"Result: {result}")
        return [Campaign(**campaign) for campaign in result]
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Obtener una campaña según un id
@router.get("/campaigns/{id}")
async def get_campania(rut: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> Campaign:
    
    logging.info(f"get example with name: {id}")
    data = await db["campaign"].find_one({"rut": rut})

    if data:
        # Si el dato existe, retornarlo
        return data
        # return JSONResponse(status_code=status.HTTP_200_OK, content=ExampleModel(data))

    else:
        # Si el dato no existe, retorna un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})
#Crear una campaña
@router.post("/campaigns")
async def create_campaign(data: Campaign, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop("id")
    
    logging.info(f"post example with: {data_dict}")

    # Buscar si el dato ya existe
    db_data = await db["campaign"].find_one({"name": data_dict['name']})
    if db_data:
        # Si el dato ya existe, retornar un error
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"message": "Data already exists"})
    
    #si no existe lo inserto a la base de datos 
    new_data = await db["campaign"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"


#Editar una campaña
@router.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id:str, data: Campaign, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict(exclude_unset=True)
    data_dict.pop('id', None)
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with id: {id} and data: {data_dict}")

    # Actualizar el dato
    data_dict['updated_at'] = datetime.now()
    await db["campaign"].find_one_and_update({"_id": ObjectId(campaign_id)}, {"$set": data_dict})

    # Retornar un mensaje de éxito
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "Data updated successfully"})

#Eliminar una campaña
@router.delete("/campaigns")
async def delete_campaign(id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    logging.info(f"delete campania with id: {id}")

    # Eliminar la campania
    await db["campaign"].find_one_and_delete({"_id": ObjectId(id)})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Data deleted successfully"})