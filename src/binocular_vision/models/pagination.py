from pydantic import BaseModel, validator

from binocular_vision.models import medical_history
from binocular_vision.models.medical_history import MedicalHistory
from binocular_vision.models.patient import Patient
from binocular_vision.models.progress_patient import ProgressPatientOneIteration


class PaginationBase(BaseModel):
    """
        page
        size
    """

    page: int
    size: int

    @validator('size', 'page')
    def should_be_greater_zero(cls, v: int) -> int:
        if v < 1:
            raise ValueError('Страница и размер должны быть больше 0')
        return v


class Pagination(PaginationBase):
    total: int


class PaginationPatient(Pagination):
    """
    total.
    patient_list
    """

    patient_list: list[Patient]


class PaginationMedicalHistory(Pagination):
    medical_history_list: list[MedicalHistory]


class PaginationProgressPatientOneIteration(Pagination):
    progress_patient_one_iteration_list: list[ProgressPatientOneIteration]
