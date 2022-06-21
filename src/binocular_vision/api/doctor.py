from fastapi import APIRouter, Security, Depends

from ..models.auth import Token
from ..models.doctor import Doctor, ChangePasswordDoctor
from ..models.pagination import PaginationPatient
from ..models.patient import Patient, PatientCreat
from ..services.doctor import DoctorService
from .doctor_patient import router as doctor_patient

router = APIRouter(
    prefix='/doctor',
    tags=['doctor']
)

router.include_router(doctor_patient)


@router.get('/', response_model=Doctor)
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


@router.get('/search_patient_full_name', response_model=list[Patient])
def search_patient_full_name(
        patient_name: str,
        services: DoctorService = Security(DoctorService, scopes=['search_patient'])):
    return services.search_patient_full_name(patient_name)


@router.get('/search_patient_login', response_model=list[Patient])
def search_patient_full_name(
        patient_login: str,
        services: DoctorService = Security(DoctorService, scopes=['search_patient'])):
    return services.search_patient_login(patient_login)


@router.patch('/change_password', response_model=Token)
def change_password_doctor(
        password: ChangePasswordDoctor,
        services: DoctorService = Security(DoctorService, scopes=['change_my_password_doctor'])):
    return services.change_password_doctor(password)
