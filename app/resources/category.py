import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.auth import get_db
from app.models.model import Category
from app.resources.campaign import delete_campaign


router = APIRouter(
    tags=["category"],
    responses={404: {"description": "Not found"}},
)

# Obtener todas las categorias
@router.get("/categories")
async def get_all_categories(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Category]:
    return await db["category"].find().to_list(length=100)

# Obtener lista de categorias según el id de la campaña
@router.get("/categories/{campaign_id}")
async def get_category(campaign_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Category]:
    
    logging.info(f"get example with campaign id: {campaign_id}")
    cursor = db["category"].find({"campaign_id": campaign_id})

    data = await cursor.to_list(length=100)

    if data:
        # Si el dato existe, retornarlo
        return data
        # return JSONResponse(status_code=status.HTTP_200_OK, content=ExampleModel(data))

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Data not found"})

# Crear una categoria
@router.post("/categories")
async def create_category(data: Category, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    
    # Convertir el modelo a un diccionario
    data_dict = data.dict()
    # Elimino el id que genera pydantic
    data_dict.pop('id', None)
    logging.info(f"post example with: {data}")
    new_data = await db["category"].insert_one(data_dict)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"
    

#Editar una categoria
@router.put("/categories/{category_id}")
async def update_category(category_id: str, data: Category, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    data_dict = data.dict(exclude_unset=True)
    if 'id' in data_dict:
        data_dict.pop('id')
    logging.info(f"put example with data: {data_dict}")
    logging.info(f"put example with category_id: {category_id} and data: {data_dict}")

    data_dict['updated_at'] = datetime.now()
    await db["category"].find_one_and_update({"_id": ObjectId(category_id)}, {"$set": data_dict})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data updated successfully"})


# Función para eliminar una categoria y la campaña si es que fuera necesario
async def delete_category(id: str, db: AsyncIOMotorClient):
    logging.info(f"delete category with id: {id}")

    # Obtener la category antes de eliminarla
    category = await db["category"].find_one({"_id": ObjectId(id)})
    campaign_id = category["campaign_id"]

    # Eliminar la category
    await db["category"].find_one_and_delete({"_id": ObjectId(id)})

    # Verificar si la campaign asociada no tiene más categories
    categories_count = await db["category"].count_documents({"campaign_id": campaign_id})
    if categories_count == 0:
        # Si no hay más categories, eliminar la campaign
        await delete_campaign(campaign_id, db)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Data deleted successfully"})
# Endpoint para eliminar categorias
@router.delete("/categories")
async def delete_category_endpoint(id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    await delete_category(id, db)