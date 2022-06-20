from fastapi import APIRouter, Security, Depends

from binocular_vision.models.doctor import Doctor
from binocular_vision.models.paginationbase import PaginationBase, PaginationPatient
from binocular_vision.models.patient import Patient, PatientCreat
from binocular_vision.services.doctor import DoctorService

router = APIRouter(
    prefix='/doctor',
    tags=['doctor']
)


@router.get('/doctor', response_model=Doctor)
def get_doctor(
        services: DoctorService = Security(DoctorService, scopes=['me_doctor'])):
    return services.get_current_doctor()


@router.post('/sing_in_patient', response_model=Patient)
def sing_in_patient(
        patient: PatientCreat,
        services: DoctorService = Security(DoctorService, scopes=['create_patient'])):
    return services.sing_up_patient(patient)


@router.get('/doctor_list_patient', response_model=PaginationPatient)
def get_my_list_patient(
        page: int, size: int,
        services: DoctorService = Security(DoctorService, scopes=['get_my_list_patient'])):
    return services.get_my_list_patient(page, size)


@router.get('/list_patient', response_model=PaginationPatient)
def get_all_list_patient(
        page: int, size: int,
        services: DoctorService = Security(DoctorService, scopes=['list_patient'])):
    return services.get_all_list_patient(page, size)

# @router.get('/')