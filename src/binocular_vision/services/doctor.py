import math
from datetime import datetime

from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from sqlalchemy import func, delete

from .auth import _scopes_doctor, AuthService
from .statistic import Statistics
from ..database import get_session
from ..db_table import table
from ..models.auth import Token
from ..models.doctor import Doctor, ChangePasswordDoctor
from ..models.medical_history import CreateMedicalHistory, MedicalHistory, BaseMedicalHistory
from ..models.pagination import PaginationBase, PaginationPatient, Pagination, PaginationMedicalHistory, \
    PaginationProgressPatientOneIteration
from ..models.patient import Patient, PatientCreat, Diagnosis, TasksCreate
from ..models.progress_patient import ProgressPatientOneIteration, ProgressPatientBase, ProgressPatient

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

    @staticmethod
    def _helper_create_paginate_medical_history(
            pagination: Pagination,
            medical_histories: list[table.MedicalHistory]) -> PaginationMedicalHistory:

        medical_history_out = [MedicalHistory.from_orm(medical_history) for medical_history in medical_histories]

        return PaginationMedicalHistory(page=pagination.page, size=pagination.size, total=pagination.total,
                                        medical_history_list=medical_history_out)

    @staticmethod
    def _helper_create_paginate_progress_patient_one_iteration(
            pagination: Pagination,
            progress_patient: list[table.ProgressPatientOneIteration]) -> PaginationProgressPatientOneIteration:

        medical_history_out = [ProgressPatientOneIteration.from_orm(x) for x in progress_patient]

        return PaginationProgressPatientOneIteration(page=pagination.page, size=pagination.size, total=pagination.total,
                                                     progress_patient_one_iteration_list=medical_history_out)

    def _helper_get_current_doctor(self) -> table.Doctor:
        doctor = (self.session
                  .query(table.Doctor)
                  .filter(table.Doctor.id == self._doctor.id)
                  .first())
        return doctor

    def _helper_get_patient_by_id(self, id: int) -> table.Patient:
        patient = (self.session
                   .query(table.Patient)
                   .filter(table.Patient.id == id).first())
        if patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return patient

    def _helper_swap_doctor(self, patient: table.Patient):
        """

        :param patient:
        :return: закомитить после использования в orm
        """
        contain = patient.doctors.filter(table.Doctor.id == self._doctor.id).count()

        if contain < 1:
            _doctor = self._helper_get_current_doctor()

            patient.full_name_current_dockter = self._doctor.full_name
            patient.doctors.append(_doctor)

    def get_my_list_patient(self, page: int, size: int, ) -> PaginationPatient:

        pagination_base = self._helper_validate_PaginationBase(page, size)

        doctor = self._helper_get_current_doctor()
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

    def search_patient_login(self, login: str, ) -> list[Patient]:
        _login = login.strip().join(login.split())

        patient = (self.session
                   .query(table.Patient)
                   .filter(table.Patient.login.ilike(_login))
                   .first())

        if patient is None:
            return []
        return [Patient.from_orm(patient)]

    def get_patient_by_id(self, id: int) -> Patient:
        return Patient.from_orm(self._helper_get_patient_by_id(id))

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
        doctor = self.get_current_doctor()
        up_medical_history = table.MedicalHistory(date=datetime.now(),
                                                  doctor=doctor.full_name,
                                                  text=medical_history.text)
        patient.medical_history.append(up_medical_history)
        self.session.commit()
        return MedicalHistory.from_orm(up_medical_history)

    def get_medical_history(self, id: int, page: int, size: int, ) -> PaginationMedicalHistory:
        pagination_base = self._helper_validate_PaginationBase(page, size)
        patient = self._helper_get_patient_by_id(id)

        pagination = self._helper_create_paginate(pagination_base, patient.medical_history.count())

        medical_histories = (patient.medical_history
                             .order_by(-table.MedicalHistory.id)
                             .offset((pagination.page - 1) * pagination.size)
                             .limit(pagination.size).all())
        return self._helper_create_paginate_medical_history(pagination, medical_histories)

    def add_task_patient(self, id: int, tasks: list[TasksCreate]) -> Patient:
        patient = self._helper_get_patient_by_id(id)
        for task in tasks:
            patient.tasks.append(table.Tasks(task=task.task, quantity=task.quantity))
        self.session.commit()
        return Patient.from_orm(patient)

    def dell_task_patient(self, id: int, tasks_id: list[int]) -> Patient:
        patient: table.Patient = self._helper_get_patient_by_id(id)
        if patient.tasks is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        id_tasks_patient = [task.id for task in patient.tasks]
        for task_id in tasks_id:
            if not (task_id in id_tasks_patient):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        del_task = (delete(table.Tasks)
                    .where(table.Tasks.id.in_(tasks_id)))
        self.session.execute(del_task)
        self.session.commit()
        return Patient.from_orm(patient)

    def get_progress_patient_one_iteration(self,
                                           id: int,
                                           page: int, size: int) -> PaginationProgressPatientOneIteration:
        pagination_base = self._helper_validate_PaginationBase(page, size)
        patient = self._helper_get_patient_by_id(id)
        pagination = self._helper_create_paginate(pagination_base, patient.progress_patient.count())
        progress_patient = (patient.progress_patient
                            .order_by(-table.ProgressPatientOneIteration.id)
                            .offset((pagination.page - 1) * pagination.size)
                            .limit(pagination.size).all())
        return self._helper_create_paginate_progress_patient_one_iteration(pagination, progress_patient)

    def change_password_doctor(self, password: ChangePasswordDoctor) -> Token:
        doctor = self._helper_get_current_doctor()
        if not self.services.verify_password(password.old_password, doctor.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный пароль')
        doctor.password_hash = self.services.hash_password(password.new_password)
        self.session.commit()
        return self.services.create_token_doctor(doctor)

    def change_password_patient(self, id: int, new_password: str) -> str:
        patient = self._helper_get_patient_by_id(id)
        patient.password_hash = self.services.hash_password(new_password)
        self.session.commit()
        return 'ok'

    def statistic_two_end(self, id: int, ) -> list[ProgressPatientBase]:
        patient = self._helper_get_patient_by_id(id)
        progress_patient = (patient.progress_patient
                            .order_by(table.ProgressPatientOneIteration.id.desc())
                            .limit(2).all())
        if progress_patient is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нехватает данных')
        progress_patient_model = [ProgressPatientOneIteration.from_orm(x) for x in progress_patient]
        return Statistics.statistic_two_end(progress_patient_model)
