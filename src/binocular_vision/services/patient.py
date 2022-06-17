from typing import List, Optional

from sqlalchemy import exc
from fastapi import (
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from ..database import get_session
from ..db_table.table import Patient
from ..models.patient import PatientCreat


class PatientService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_list_patients(self, ) -> List[Patient]:
        return self.session.query(Patient).all()

    def get_patient(self, id: int) -> Patient:
        response = self.session.query(Patient).filter(Patient.id == id).first()
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return response

    def create_patient(self, patient: PatientCreat) -> Patient:
        patient_db = Patient(**patient.dict())
        try:
            self.session.add(patient_db)
            self.session.commit()
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Логин уже занят")
        return patient_db
