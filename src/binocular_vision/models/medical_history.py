from datetime import datetime

from pydantic import BaseModel


class BaseMedicalHistory(BaseModel):
    text: str


class MedicalHistory(BaseMedicalHistory):
    id: int
    date: datetime
    patient_id: int

    class Config:
        orm_mode = True


class CreateMedicalHistory(BaseMedicalHistory):
    pass
