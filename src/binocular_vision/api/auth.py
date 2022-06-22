import current as current
from fastapi import APIRouter, Depends, Security

from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import Token
from ..models.doctor import (
    DoctorCreate,
    Doctor,
)
from ..services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/sign_up_doctor', response_model=Token)
def sing_up_doctor(
        doctor_data: DoctorCreate,
        services: AuthService = Depends()
):
    '''
    Регистрация доктора
    - **doctor_data**: Схема доктора.
    \f
    :param doctor_data:
    :param services:
    :return:
    '''
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


@router.post('/sing_in_patient', response_model=Token)
def sing_in_patient(
        from_data: OAuth2PasswordRequestForm = Depends(),
        services: AuthService = Depends(), ):
    return services.authenticated_patient(
        from_data.username,
        from_data.password,
    )
