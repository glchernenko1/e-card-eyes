from fastapi import APIRouter

from .patient import router as patient_router

router = APIRouter()
router.include_router(patient_router)