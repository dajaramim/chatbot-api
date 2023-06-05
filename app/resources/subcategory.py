import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.auth import get_db
from app.models.model import Subcategory
from app.resources.category import delete_category


router = APIRouter(
    tags=["subcategory"],
    responses={404: {"description": "Not found"}},
)

#Obtener todas las subcategorias
@router.get("/subcategories")
async def get_all_subcategories(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Subcategory]:
    return await db["subcategory"].find().to_list(length=100)

#Obtener una lista de subcategorias según el id de una categoria
@router.get("/subcategories/{category_id}")
async def get_subcategory(category_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Subcategory]:
    
    logging.info(f"get example with category id: {category_id}")
    cursor = db["subcategory"].find({"category_id": category_id})

    data = await cursor.to_list(length=100)

    if data:
        # Si el dato existe, retornarlo
        return data
        # return JSONResponse(status_code=status.HTTP_200_OK, content=ExampleModel(data))

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Data not found"})

#Crear una subcategoria
@router.post("/subcategories")
async def create_subcategory(data: Subcategory, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop('id', None)

    logging.info(f"post example with: {data}")
    new_data = await db["subcategory"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"
 

#Editar una subcategoria
@router.put("/subcategories/{subcategory_id}")
async def update_subcategory(subcategory_id: str, data: Subcategory, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    data_dict = data.dict(exclude_unset=True)
    data_dict.pop("id")
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with id: {subcategory_id} and data: {data_dict}")

    data_dict['updated_at'] = datetime.now()
    await db["subcategory"].find_one_and_update({"_id": ObjectId(subcategory_id)}, {"$set": data_dict})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data updated successfully"})

#Eliminar una subcategoria
@router.delete("/subcategories")
async def delete_subcategory(id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    logging.info(f"delete subcategory with id: {id}")

    # Obtener la subcategory antes de eliminarla
    subcategory = await db["subcategory"].find_one({"_id": ObjectId(id)})
    category_id = subcategory["category_id"]

    # Eliminar la subcategory
    await db["subcategory"].find_one_and_delete({"_id": ObjectId(id)})

    # Verificar si la category asociada no tiene más subcategories
    subcategories_count = await db["subcategory"].count_documents({"category_id": category_id})
    if subcategories_count == 0:
        # Si no hay más subcategories, eliminar la category
        await delete_category(category_id, db)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Data deleted successfully"})




