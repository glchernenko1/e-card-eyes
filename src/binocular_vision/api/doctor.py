from fastapi import APIRouter, Security, Depends

from binocular_vision.models.doctor import Doctor
from binocular_vision.models.patient import Patient, PatientCreat
from binocular_vision.services.doctor import DoctorService
from binocular_vision.services.patient import PatientService

router = APIRouter(
    prefix='/doctor',
    tags=['doctor']
)


@router.get('/doctor', response_model=Doctor)
def get_doctor(
        doctor: Doctor = Security(DoctorService.get_current_doctor, scopes=['me_doctor'])):
    return doctor


@router.post('/sing_in_patient', response_model=Patient)
def sing_in_patient(
        services: DoctorService = Depends(DoctorService.sing_up_patient)
):
    return services
