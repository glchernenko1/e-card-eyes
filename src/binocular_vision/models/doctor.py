import email

import login as login
import password as password
import pydantic
from pydantic import BaseModel, EmailStr, SecretStr, validator


class DoctorBase(BaseModel):
    full_name: str
    login: str
    email: EmailStr


class DoctorCreate(DoctorBase):
    password: str #SecretStr  # get_secret_value()

    @validator('password')
    def password_should_be_longer_eight_character(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен быть от 8 символов')
        return v


class Doctor(DoctorBase):
    id: int
    class Config:
        orm_mode = True




