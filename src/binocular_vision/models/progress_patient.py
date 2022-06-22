from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TypeProgress(str, Enum):
    ESOTROPIA = 'esotropia'  # INWARD_TURNING
    EXOTROPIA = 'exotropia'  # OUTWARD_TURNING


class ProgressPatientBase(BaseModel):
    progress_type: TypeProgress
    progress_value: int


class ProgressPatient(ProgressPatientBase):
    id: int

    class Config:
        orm_mode = True


class ProgressPatientCreate(ProgressPatientBase):
    pass


class ProgressPatientOneIteration(BaseModel):
    id: int
    date: datetime
    progress: list[ProgressPatient] | None

    class Config:
        orm_mode = True


class Password(BaseModel):
    password: str


class PasswordChange(Password):
    new_password: str
