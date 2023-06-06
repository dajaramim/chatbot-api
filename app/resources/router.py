from fastapi import APIRouter
from app.resources.agendamiento import router as resources_router_agendamiento

router = APIRouter()
router.include_router(resources_router_agendamiento, prefix="/agendamiento", tags=["agendamiento"])

