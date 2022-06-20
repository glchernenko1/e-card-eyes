from typing import List

import login
from fastapi import APIRouter, Depends, Security
from pydantic.class_validators import Optional
from sqlalchemy.orm import Session

from ..database import get_session
from ..models.patient import Patient, PatientCreat

from ..services.patient import PatientService

router = APIRouter(
    prefix='/patient',
    tags=['patient']
)


@router.get('/patient', response_model=Patient)
def get_patient(
        doctor: Patient = Security(PatientService.get_current_patient, scopes=['me_patient'])):
    return doctor


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
