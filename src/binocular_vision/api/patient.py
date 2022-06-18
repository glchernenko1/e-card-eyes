from typing import List

import login
from fastapi import APIRouter, Depends
from pydantic.class_validators import Optional
from sqlalchemy.orm import Session

from ..database import get_session
from ..models.patient import Patient, PatientCreat

from ..services.patient import PatientService

router = APIRouter(
    prefix='/patient',
    tags=['patient']
)


@router.get('/get-all-patients', response_model=List[Patient])
def get_patients(
        services: PatientService = Depends()):
    return services.get_list_patients()


@router.get('/get-patient', response_model=Patient)
def get_patients(
        id: int,
        services: PatientService = Depends(),
):
    return services.get_patient(id)


@router.post('/create_patient', response_model=Patient)
def create_patient(
        patient: PatientCreat,
        services: PatientService = Depends(),
):
    return services.create_patient(patient)
