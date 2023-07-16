from fastapi import APIRouter
from .cars import router as cars_router
from .users import router as users_router
from .blueprints import router as blueprints_router

router = APIRouter()
router.include_router(cars_router)
router.include_router(users_router)
router.include_router(blueprints_router)