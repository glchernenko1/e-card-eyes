from pydantic import BaseModel, EmailStr, SecretStr, validator


class DoctorBase(BaseModel):
    full_name: str
    login: str
    email: EmailStr

    @validator('full_name')
    def full_name_validator(cls, v: str) -> str:
        v = v.strip().join(v.split())
        return v


class DoctorCreate(DoctorBase):
    password: str  # SecretStr  # get_secret_value()

    @validator('password')
    def password_should_be_longer_eight_character(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен быть от 8 символов')
        return v


class ChangePasswordDoctor(BaseModel):
    old_password: str
    new_password: str  # SecretStr  # get_secret_value()

    @validator('new_password')
    def password_should_be_longer_eight_character(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен быть от 8 символов')
        return v


class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True
