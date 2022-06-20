import math
from datetime import datetime

from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from starlette import status

from .auth import _scopes_doctor, AuthService
from ..database import get_session
from ..db_table import table
from ..models.doctor import Doctor
from ..models.medical_history import CreateMedicalHistory, MedicalHistory, BaseMedicalHistory
from ..models.paginationbase import PaginationBase, PaginationPatient, Pagination
from ..models.patient import Patient, PatientCreat, Diagnosis, TasksCreate

oauth2_schem_doctor = OAuth2PasswordBearer(
    tokenUrl='auth/sing_in_doctor',
    scheme_name="sing_in_doctor"
)


class DoctorService:
    def __init__(self, security_scopes: SecurityScopes, token: str = Depends(oauth2_schem_doctor),
                 services: AuthService = Depends(), session: Session = Depends(get_session)):
        self.session = session
        self.security_scopes = security_scopes
        self.services = services
        self.token = token
        self._doctor = services.validate_token_doctor(security_scopes, token)

    def get_current_doctor(self, ) -> Doctor:
        return self._doctor

    def sing_up_patient(self, patient: PatientCreat) -> Patient:
        return self.services.register_new_patient(self._doctor, patient)

    @staticmethod
    def _helper_validate_PaginationBase(_page: int, _size: int, ) -> PaginationBase:
        try:
            pagination = PaginationBase(page=_page, size=_size)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Страница и размер должны быть больше 0'
            )
        return pagination

    @staticmethod
    def _helper_create_paginate(pagination: PaginationBase, patients_count: int) -> Pagination:

        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if patients_count == 0:
            raise exception

        page = math.ceil(patients_count / pagination.size)
        if page < pagination.page:
            raise exception

        return Pagination(page=pagination.page, size=pagination.size, total=page)

    @staticmethod
    def _helper_create_paginate_patients(pagination: Pagination, patients: list[table.Patient]) -> PaginationPatient:

        patients_out = [Patient.from_orm(patient) for patient in patients]

        return PaginationPatient(page=pagination.page, size=pagination.size, total=pagination.total,
                                 patient_list=patients_out)

    def get_my_list_patient(self, page: int, size: int, ) -> PaginationPatient:

        pagination_base = self._helper_validate_PaginationBase(page, size)

        doctor: table.Doctor = (self.session
                                .query(table.Doctor)
                                .filter(table.Doctor.id == self._doctor.id)
                                .first())

        pagination = self._helper_create_paginate(pagination_base, doctor.patients.count())

        patients = (doctor.patients
                    .order_by(-table.Patient.id)
                    .offset((pagination.page - 1) * pagination.size)
                    .limit(pagination.size).all())

        return self._helper_create_paginate_patients(pagination, patients)

    def get_all_list_patient(self, page: int, size: int, ) -> PaginationPatient:

        pagination_base = self._helper_validate_PaginationBase(page, size)

        pagination = self._helper_create_paginate(pagination_base, self.session.query(table.Patient).count())

        patients = (self.session.query(table.Patient)
                    .order_by(-table.Patient.id)
                    .offset((pagination.page - 1) * pagination.size)
                    .limit(pagination.size).all())

        return self._helper_create_paginate_patients(pagination, patients)

    def search_patient_full_name(self, full_name: str, ) -> list[Patient]:
        _full_name = full_name.strip().join(full_name.split())

        patients = (self.session
                    .query(table.Patient)
                    .filter(table.Patient.full_name.ilike(_full_name))
                    .all())
        patients_out = [Patient.from_orm(patient) for patient in patients]
        return patients_out

    def search_patient_login(self, login: str, ) -> Patient:
        _login = login.strip().join(login.split())

        patient = (self.session
                   .query(table.Patient)
                   .filter(table.Patient.full_name.ilike(_login))
                   .first())
        return Patient.from_orm(patient)

    def _helper_get_patient_by_id(self, id: int) -> table.Patient:
        patient = (self.session
                   .query(table.Patient)
                   .filter(table.Patient == id).first())
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return patient

    def get_patient_by_id(self, id: int) -> Patient:
        return Patient.from_orm(self._helper_get_patient_by_id(id))

    def _helper_swap_doctor(self, patient: table.Patient):
        contain = patient.doctors.filter(table.Doctor.id == self._doctor.id).count()

        if contain < 1:
            _doctor = (self.session
                       .query(table.Doctor)
                       .filter(table.Doctor.id == self._doctor.id)
                       .first())

            patient.full_name_current_dockter = self._doctor.full_name
            patient.doctors.append(_doctor)

    def update_current_correct_diagnosis(self, id: int, diagnosis: Diagnosis) -> Patient:
        patient = self._helper_get_patient_by_id(id)
        self._helper_swap_doctor(patient)
        patient.correct_diagnosis = diagnosis.correct_diagnosis
        patient.confirmed_diagnosis = diagnosis.confirmed_diagnosis
        self.session.commit()
        return Patient.from_orm(patient)

    def add_new_medical_history(self, id: int, medical_history: CreateMedicalHistory) -> MedicalHistory:
        patient: table.Patient = self._helper_get_patient_by_id(id)
        self._helper_swap_doctor(patient)
        up_medical_history = table.MedicalHistory(date=datetime.now(), text=medical_history.text)
        patient.medical_history.append(up_medical_history)
        self.session.commit()
        return MedicalHistory.from_orm(up_medical_history)

    def get_medical_history(self, id: int, page: int, size: int, ) -> list[MedicalHistory]:
        pagination_base = self._helper_validate_PaginationBase(page, size)
        patient = self._helper_get_patient_by_id(id)

        pagination = self._helper_create_paginate(pagination_base, patient.medical_history.count())

        medical_histories = (patient.medical_history
                             .order_by(-table.Patient.id)
                             .offset((pagination.page - 1) * pagination.size)
                             .limit(pagination.size).all())
        patients_out = [MedicalHistory.from_orm(medical_history) for medical_history in medical_histories]
        return patients_out

    def add_task_patient(self, id: int, tasks: list[TasksCreate]) -> Patient:
        patient = self._helper_get_patient_by_id(id)
        patient.tasks.append(tasks)
        self.session.commit()
        return Patient.from_orm(patient)

    def dell_task_patient(self, id: int, tasks_id: list[int]) -> Patient:
        patient: table.Patient = self._helper_get_patient_by_id(id)
        if patient.tasks is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        id_del_tasks = [task.id for task in patient.tasks]
        for task_id in tasks_id:
            if not (tasks_id in tasks_id):
                HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        del_task = (self.session
                    .query(table.Tasks)
                    .filter(table.Tasks.id in tasks_id)
                    .all())
        self.session.delete(del_task)
        return Patient.from_orm(patient)
