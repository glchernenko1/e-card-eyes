from typing import List

import login
from fastapi import APIRouter, Depends, Security
from pydantic.class_validators import Optional
from sqlalchemy.orm import Session

from ..database import get_session
from ..models.auth import Token
from ..models.patient import Patient, PatientCreat, Tasks
from ..models.progress_patient import ProgressPatientCreate, ProgressPatientBase

from ..services.patient import PatientService

router = APIRouter(
    prefix='/patient',
    tags=['patient']
)


@router.get('/', response_model=Patient)
def get_patient(
        services: PatientService = Security(PatientService, scopes=['me_patient'])):
    return services.get_current_patient()


@router.get('/get_current_task', response_model=list[Tasks])
def get_current_task(
        services: PatientService = Security(PatientService, scopes=['my_task'])):
    return services.get_current_task()


@router.post('/create_progress_one_iteration', response_model=str)
def create_progress_patient_one_iteration(
        services: PatientService = Security(PatientService, scopes=['create_progress'])):
    return services.create_progress_patient_one_iteration()


@router.post('/add_progress_to_last_iteration', response_model=str)
def add_progress_to_last_iteration(
        progress: ProgressPatientCreate,
        services: PatientService = Security(PatientService, scopes=['add_progress'])):
    return services.add_progress_to_last_iteration(progress)


@router.post('/add_list_progress_to_last_iteration', response_model=str)
def add_progress_to_last_iteration(
        progress: list[ProgressPatientCreate],
        services: PatientService = Security(PatientService, scopes=['add_progress'])):
    return services.add_list_progress_to_last_iteration(progress)


@router.patch('/change_password', response_model=Token)
def change_password_doctor(
        old_password: str,
        new_password: str,
        services: PatientService = Security(PatientService, scopes=['change_my_password_patient'])):
    return services.change_password(old_password, new_password)


@router.get('/statistic_two_end', response_model=list[ProgressPatientBase])
def statistic_two_end(
        services: PatientService = Security(PatientService, scopes=['get_my_statistic'])):
    return services.statistic_two_end()
