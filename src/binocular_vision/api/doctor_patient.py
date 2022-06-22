from fastapi import APIRouter, Security, status

from ..models.medical_history import MedicalHistory, CreateMedicalHistory
from ..models.pagination import PaginationMedicalHistory, PaginationProgressPatientOneIteration
from ..models.patient import Patient, Diagnosis, TasksCreate
from ..models.progress_patient import ProgressPatientBase
from ..services.doctor import DoctorService

router = APIRouter(
    prefix='/patient',
)


@router.get('/{id}', response_model=Patient)
def get_patient_by_id(
        id: int,
        services: DoctorService = Security(DoctorService, scopes=['get_patient_by_id'])):
    return services.get_patient_by_id(id)


@router.patch('/{id}', response_model=Patient)
def update_current_correct_diagnosis(
        id: int,
        diagnosis: Diagnosis,
        services: DoctorService = Security(DoctorService, scopes=['update_diagnosis'])):
    return services.update_current_correct_diagnosis(id, diagnosis)


@router.post('/{id}/medical_history', response_model=MedicalHistory)
def add_new_medical_history(
        id: int,
        medical_history: CreateMedicalHistory,
        services: DoctorService = Security(DoctorService, scopes=['add_medical_history'])):
    return services.add_new_medical_history(id, medical_history)


@router.get('/{id}/medical_history/{page}', response_model=PaginationMedicalHistory)
def get_medical_history(
        id: int,
        page: int, size: int,
        services: DoctorService = Security(DoctorService, scopes=['get_medical_history'])):
    return services.get_medical_history(id, page, size)


@router.post('/{id}/tasks', response_model=Patient)
def add_task_patient(
        id: int,
        tasks: list[TasksCreate],
        services: DoctorService = Security(DoctorService, scopes=['add_tasks'])):
    return services.add_task_patient(id, tasks)


@router.delete('/{id}/tasks', response_model=Patient)
def dell_task_patient(
        id: int,
        tasks_id: list[int],
        services: DoctorService = Security(DoctorService, scopes=['delete_tasks'])):
    return services.dell_task_patient(id, tasks_id)


@router.get('/{id}/progress/{page}', response_model=PaginationProgressPatientOneIteration)
def get_progress_patient(
        id: int,
        page: int, size: int,
        services: DoctorService = Security(DoctorService, scopes=['get_progress_patient'])):
    return services.get_progress_patient_one_iteration(id, page, size)


@router.patch('/{id}/change_password', response_model=str)
def change_password_patient(
        id: int,
        password: str,
        services: DoctorService = Security(DoctorService, scopes=['change_password_patient'])):
    return services.change_password_patient(id, password)


@router.get('/{id}/statistic_two_end', response_model=list[ProgressPatientBase])
def statistic_two_end(
        id: int,
        services: DoctorService = Security(DoctorService, scopes=['get_statistic_patient'])):
    return services.statistic_two_end(id)
