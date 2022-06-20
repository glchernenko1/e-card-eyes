import login as login
from pydantic import BaseModel, validator
from enum import Enum


class TypeTasks(str, Enum):
    CLASSIC = 'classic'
    NO_CLASSIC = 'no_classic'


class TasksBase(BaseModel):
    task: TypeTasks
    quantity: int


class Tasks(TasksBase):
    id: int


class TasksCreate(TasksBase):
    pass


class PatientBase(BaseModel):
    full_name: str
    login: str
    full_name_current_dockter: str
    correct_diagnosis: str | None
    confirmed_diagnosis: bool | None

    @validator('full_name', 'full_name_current_dockter')
    def full_name_validator(cls, v: str) -> str:
        v = v.strip().join(v.split())
        return v


class Diagnosis(BaseModel):
    correct_diagnosis: str
    confirmed_diagnosis: bool


class Patient(PatientBase):
    id: int
    tasks: list[Tasks] | None

    class Config:
        orm_mode = True


class PatientCreat(PatientBase):
    password: str

    class Config:
        full_name_current_dockter = 'ignore'
