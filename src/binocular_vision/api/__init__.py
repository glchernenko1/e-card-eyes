from fastapi import APIRouter

from .patient import router as patient_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(patient_router)
router.include_router(auth_router)