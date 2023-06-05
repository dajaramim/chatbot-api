from fastapi import APIRouter
from app.resources.campaign import router as resources_router_campaign
from app.resources.category import router as resources_router_category
from app.resources.subcategory import router as resources_router_subcategory


router = APIRouter()
router.include_router(resources_router_campaign, prefix="/campaign", tags=["campaign"])
router.include_router(resources_router_category, prefix="/category", tags=["category"])
router.include_router(resources_router_subcategory, prefix="/subcategory", tags=["subcategory"])
