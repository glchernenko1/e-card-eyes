import login as login
from pydantic import BaseModel


class PatientBase(BaseModel):
    full_name: str
    login: str
    full_name_current_dockter: str
    correct_diagnosis: str | None
    confirmed_diagnosis: bool | None


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
        correct_dockter = 'ignore'


class PatientCreat(PatientBase):
    password: str
