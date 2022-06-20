from pydantic import BaseModel, validator

from binocular_vision.models.patient import Patient


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
