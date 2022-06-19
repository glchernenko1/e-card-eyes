from typing import List, Optional

from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from fastapi import (
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from .auth import AuthService
from ..database import get_session
from ..db_table.table import Patient

oauth2_schem_patient = OAuth2PasswordBearer(
    tokenUrl='auth/sing_in_patient',
    scheme_name="sing_in_patient"
)


class PatientService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def get_current_doctor(security_scopes: SecurityScopes, token: str = Depends(oauth2_schem_patient),
                           services: AuthService = Depends()) -> Patient:
        return services.validate_token_patient(security_scopes, token)

    def get_list_patients(self, ) -> List[Patient]:
        return self.session.query(Patient).all()

    def get_patient(self, id: int) -> Patient:
        response = self.session.query(Patient).filter(Patient.id == id).first()
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return response
