from datetime import datetime

from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from fastapi import (
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from .auth import AuthService
from ..database import get_session
from ..db_table import table

from ..models.auth import Token
from ..models.patient import Tasks, Patient
from ..models.progress_patient import ProgressPatientCreate, ProgressPatient, ProgressPatientBase, \
    ProgressPatientOneIteration
from ..services.statistic import Statistics

oauth2_schem_patient = OAuth2PasswordBearer(
    tokenUrl='auth/sing_in_patient',
    scheme_name="sing_in_patient"
)


class PatientService:
    def __init__(self, security_scopes: SecurityScopes, token: str = Depends(oauth2_schem_patient),
                 services: AuthService = Depends(), session: Session = Depends(get_session)):
        self.session = session
        self.security_scopes = security_scopes
        self.services = services
        self.token = token
        self._patient = services.validate_token_patient(security_scopes, token)

    def get_current_patient(self, ) -> Patient:
        return Patient.from_orm(self._helper_get_current_patient())

    def _helper_get_current_patient(self) -> table.Patient:
        patient = (self.session
                   .query(table.Patient)
                   .filter(table.Patient.id == self._patient.id)
                   .first())
        return patient

    def _helper_get_last_progress_iteration(self) -> table.ProgressPatientOneIteration:
        patient = self._helper_get_current_patient()
        last_progress_iteration = (patient.progress_patient
                                   .order_by(table.ProgressPatientOneIteration.id.desc())
                                   .first())
        if last_progress_iteration is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='создайте текущую итерацию')
        return last_progress_iteration

    def get_current_task(self) -> list[Tasks]:
        patient = Patient.from_orm(self._helper_get_current_patient())
        if patient.tasks is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return patient.tasks

    def create_progress_patient_one_iteration(self) -> str:
        patient = self._helper_get_current_patient()
        patient.progress_patient.append(table.ProgressPatientOneIteration(date=datetime.now()))
        self.session.commit()
        return 'ok'

    def add_progress_to_last_iteration(self, progress: ProgressPatientCreate) -> str:
        last_progress_iteration = self._helper_get_last_progress_iteration()
        progress_types = [prog.progress_type for prog in last_progress_iteration.progress]
        if progress.progress_type in progress_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='В одну сессию невозможно записать одинаковые типы')
        last_progress_iteration.progress.append(
            table.ProgressPatient(progress_type=progress.progress_type, progress_value=progress.progress_value))
        self.session.commit()
        return 'ok'

    def add_list_progress_to_last_iteration(self, progress_list: list[ProgressPatientCreate]) -> str:

        exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='В одну сессию невозможно записать одинаковые типы')

        progress_list_type = [progress.progress_type for progress in progress_list]

        if len(set(progress_list_type)) != len(progress_list_type):
            raise exception

        last_progress_iteration = self._helper_get_last_progress_iteration()
        progress_types = [prog.progress_type for prog in last_progress_iteration.progress]
        for progress in progress_list:
            if progress.progress_type in progress_types:
                raise exception
            last_progress_iteration.progress.append(
                table.ProgressPatient(
                    progress_type=progress.progress_type,
                    progress_value=progress.progress_value)
            )
        self.session.commit()
        return 'ok'

    def change_password(self, old_password: str, new_password: str) -> Token:
        patient = self._helper_get_current_patient()
        if not self.services.verify_password(old_password, patient.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный пароль')
        patient.password_hash = self.services.hash_password(new_password)
        self.session.commit()
        return self.services.create_token_patient(patient)

    def statistic_two_end(self) -> list[ProgressPatientBase]:
        patient = self._helper_get_current_patient()
        progress_patient = (patient.progress_patient
                            .order_by(table.ProgressPatientOneIteration.id.desc())
                            .limit(2).all())
        if progress_patient is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нехватает данных')

        progress_patient_model = [ProgressPatientOneIteration.from_orm(x) for x in progress_patient]

        return Statistics.statistic_two_end(progress_patient_model)
