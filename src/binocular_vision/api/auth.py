import current as current
from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import Token
from ..models.doctor import (
    DoctorCreate,
    Doctor,
)
from ..services.auth import AuthService, get_current_doctor

router = APIRouter(
    prefix='/auth',
)


@router.post('/sign_up_doctor', response_model=Token)
def sing_up_doctor(
        doctor_data: DoctorCreate,
        services: AuthService = Depends()
):
    return services.register_new_doctor(doctor_data)


@router.post('/sing_in_doctor', response_model=Token)
def sing_in_doctor(
        from_data: OAuth2PasswordRequestForm = Depends(),
        services: AuthService = Depends(),

):
    return services.authenticated_doctor(
        from_data.username,
        from_data.password
    )


@router.get('/doctor', response_model=Doctor)
def get_doctor(doctor: Doctor = Depends(get_current_doctor)):
    return doctor


@router.post('/sign_up_patient')
def sing_up_patient():
    pass


@router.post('/sing_in_patient')
def sing_in_patient():
    pass
