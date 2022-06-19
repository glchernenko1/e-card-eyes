from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from .auth import _scopes_doctor, AuthService
from ..database import get_session
from ..models.doctor import Doctor
from ..models.patient import Patient, PatientCreat

oauth2_schem_doctor = OAuth2PasswordBearer(
    tokenUrl='auth/sing_in_doctor',
    scheme_name="sing_in_doctor"
)


class DoctorService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def get_current_doctor(security_scopes: SecurityScopes, token: str = Depends(oauth2_schem_doctor),
                           services: AuthService = Depends()) -> Doctor:
        return services.validate_token_doctor(security_scopes, token)

    @staticmethod
    def sing_up_patient(
            patient: PatientCreat,
            doctor: Doctor = Security(get_current_doctor, scopes=['create_patient']),
            services: AuthService = Depends(AuthService)
    ):
        return services.register_new_patient(doctor, patient)
