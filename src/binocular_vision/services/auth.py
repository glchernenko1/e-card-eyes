from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.hash import bcrypt
from jose import jwt, JWTError
from sqlalchemy import exc
from sqlalchemy.orm import Session

from ..database import get_session
from ..db_table import table
from ..models.doctor import Doctor, DoctorCreate
from ..models.patient import Patient, PatientCreat
from ..settings import settings
from ..models.auth import Token

_scopes_doctor = [
    'me_doctor', 'create_patient', 'get_my_list_patient',
    'list_patient', 'search_patient', 'get_patient_by_id',
    'update_diagnosis', 'add_medical_history', 'get_medical_history',
    'add_tasks', 'delete_tasks', 'get_progress_patient',
    'change_my_password_doctor', 'change_password_patient',
    'get_statistic_patient'
]
_scopes_patient = [
    'me_patient', 'my_task', 'create_progress',
    'add_progress', 'add_progress', 'change_my_password_patient',
    'get_my_statistic'
]


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, password_hash: str) -> bool:
        return bcrypt.verify(plain_password, password_hash)

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    # Handler

    @staticmethod
    def _error_handler_creating_account(e: exc.IntegrityError):
        if 'email' in str(e.orig):
            detail = 'Email уже зарегистрирован'
        else:
            detail = 'Логин уже используется'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    @staticmethod
    def _error_handler_scopes_load(security_scopes: SecurityScopes) -> [str, HTTPException]:
        """
        :return: authenticate_value, exception
        """

        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = f"Bearer"
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={"WWW-Authenticate": authenticate_value},
        )
        return authenticate_value, exception

    @staticmethod
    def _error_handler_scopes_correct(security_scopes: SecurityScopes, token_scopes: list[str],
                                      authenticate_value: str):
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )

    @classmethod
    def _handler_scopes_valid(cls, security_scopes: SecurityScopes, token: str) -> [dict, HTTPException]:
        """
        :return: payload (from jwt.decode), exception
        """
        authenticate_value, exception = cls._error_handler_scopes_load(security_scopes)
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
            token_scopes = payload.get("scopes", [])
        except JWTError:
            raise exception
        cls._error_handler_scopes_correct(security_scopes, token_scopes, authenticate_value)

        return payload, exception

    # Doctor

    @classmethod
    def validate_token_doctor(cls, security_scopes: SecurityScopes, token: str) -> Doctor:

        payload, exception = cls._handler_scopes_valid(security_scopes, token)
        try:
            doctor_data = payload.get('doctor_data')
            doctor = Doctor.parse_obj(doctor_data)
        except ValueError:
            raise exception
        return doctor

    @classmethod
    def create_token_doctor(cls, doctor: table.Doctor) -> Token:
        doctor_data = Doctor.from_orm(doctor)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(hours=settings.jwt_expiration_doctor),
            'sub': str(doctor_data.id),
            'doctor_data': doctor_data.dict(),
            'scopes': _scopes_doctor
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    # Patient

    @classmethod
    def validate_token_patient(cls, security_scopes: SecurityScopes, token: str) -> Patient:
        payload, exception = cls._handler_scopes_valid(security_scopes, token)
        try:
            patient_data = payload.get('patient_data')
            patient = Patient.parse_obj(patient_data)
        except ValueError:
            raise exception
        return patient

    @classmethod
    def create_token_patient(cls, patient: table.Patient) -> Token:
        patient_data = Patient.from_orm(patient)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(hours=settings.jwt_expiration_patient),
            'sub': str(patient_data.id),
            'patient_data': patient_data.dict(),
            'scopes': _scopes_patient
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    # Doctor

    def register_new_doctor(self, doctor_data: DoctorCreate) -> Token:
        doctor = table.Doctor(
            full_name=doctor_data.full_name,
            login=doctor_data.login,
            email=doctor_data.email,
            password_hash=self.hash_password(doctor_data.password)
        )

        patient_login_noun = (self.session
                              .query(table.Patient)
                              .filter(table.Patient.login == doctor_data.login)
                              .first())

        if not patient_login_noun is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин уже используется')

        try:
            self.session.add(doctor)
            self.session.commit()
        except exc.IntegrityError as e:
            self._error_handler_creating_account(e)

        return self.create_token_doctor(doctor)

    def authenticated_doctor(self, doctor_login: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль'
        )

        doctor = (
            self.session
            .query(table.Doctor)
            .filter(table.Doctor.login == doctor_login)
            .first()
        )
        if not doctor:
            raise exception

        if not self.verify_password(password, doctor.password_hash):
            raise exception
        return self.create_token_doctor(doctor)

    # Patient

    def register_new_patient(self, doctor: Doctor, patient: PatientCreat) -> Patient:

        doctor_login_noun = (self.session
                             .query(table.Doctor)
                             .filter(table.Doctor.login == patient.login)
                             .first())

        if not doctor_login_noun is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин уже используется')

        _doctor: table.Doctor = (self.session
                                 .query(table.Doctor)
                                 .filter(table.Doctor.id == doctor.id)
                                 .first())

        _patient = table.Patient(
            full_name=patient.full_name,
            login=patient.login,
            password_hash=self.hash_password(patient.password),
            full_name_current_dockter=_doctor.full_name,
        )

        _doctor.patients.append(_patient)

        try:
            self.session.add(_doctor)
            self.session.commit()
        except exc.IntegrityError as e:
            self._error_handler_creating_account(e)

        return Patient.from_orm(_patient)  # todo: проверить добавляется ли id

    def authenticated_patient(self, patient_login: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль'
        )

        patient: table.Patient = (
            self.session
            .query(table.Patient)
            .filter(table.Patient.login == patient_login)
            .first()
        )
        if not patient:
            raise exception

        if not self.verify_password(password, patient.password_hash):
            raise exception
        return self.create_token_patient(patient)
