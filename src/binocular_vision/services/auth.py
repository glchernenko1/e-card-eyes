from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import SecretStr
from passlib.hash import bcrypt
from jose import jwt, JWTError
from sqlalchemy import exc
from sqlalchemy.orm import Session

from ..database import get_session
from ..db_table import table
from ..models.doctor import Doctor, DoctorCreate
from ..settings import settings
from ..models.auth import Token

oauth2_schem = OAuth2PasswordBearer(tokenUrl='/auth/sing_in_doctor')


def get_current_doctor(token: str = Depends(oauth2_schem)) -> Doctor:
    return AuthService.validate_token_doctor(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, password_hash: str) -> bool:
        return bcrypt.verify(plain_password, password_hash)

    @classmethod
    def has_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    @classmethod
    def validate_token_doctor(cls, token: str) -> Doctor:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        doctor_data = payload.get('doctor_data')
        try:
            doctor = Doctor.parse_obj(doctor_data)
        except ValueError:
            raise exception from None
        return doctor

    @classmethod
    def create_token_doctor(cls, doctor: table.Doctor) -> Token:
        doctor_data = Doctor.from_orm(doctor)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(hours=settings.jwt_expiration),
            'sub': str(doctor_data.id),
            'doctor_data': doctor_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_doctor(self, doctor_data: DoctorCreate) -> Token:
        doctor = table.Doctor(
            full_name=doctor_data.full_name,
            login=doctor_data.login,
            email=doctor_data.email,
            password_hash=self.has_password(doctor_data.password)
        )
        try:
            self.session.add(doctor)
            self.session.commit()
        except exc.IntegrityError as e:
            if 'email' in str(e.orig):
                detail = 'Email уже зарегистрирован'
            else:
                detail = 'Логин уже используется'
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

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
