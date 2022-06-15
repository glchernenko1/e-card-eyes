import doctor as doctor
import sqlalchemy as sa
from sqlalchemy import null
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import date

Base = declarative_base()

doctors_patients = sa.Table('doctor_patient',
                            Base.metadata,
                            sa.Column('patient_id', sa.ForeignKey('patient.id'), primary_key=True),
                            sa.Column('doctor_id', sa.ForeignKey('doctor.id'), primary_key=True),
                            )


class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date: date = sa.Column(sa.Date, nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('patient.id'))

    def __repr__(self):
        return f'MedicalHistory(id={self.id}, date={self.date}, text={self.text}, patient_id={self.patient_id})'


class Patient(Base):
    __tablename__ = 'patient'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    full_name = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, nullable=False, unique=True)
    password_hash = sa.Column(sa.Text, nullable=False)

    full_name_current_dockter = sa.Column(sa.String, nullable=False)
    correct_diagnosis = sa.Column(sa.String)
    confirmed_diagnosis = sa.Column(sa.Boolean)
    doctors = relationship('Doctor', secondary=doctors_patients, back_populates='patients', lazy='dynamic')
    medical_history = relationship('MedicalHistory', lazy='dynamic')

    def __repr__(self):
        return f'Patient(id={self.id}, full_name={self.full_name}, login={self.login}, ' \
               f'password_hash={self.password_hash}, full_name_current_dockter= {self.full_name_current_dockter},' \
               f'correct_diagnosis={self.correct_diagnosis}, confirmed_diagnosis={self.confirmed_diagnosis},' \
               f'doctors = {self.doctors}, medical_history = {self.medical_history})'


class Doctor(Base):
    __tablename__ = 'doctor'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    full_name = sa.Column(sa.String, nullable=False)
    login = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.Text, nullable=False)
    patients = relationship('Patient', secondary=doctors_patients, back_populates='doctors', lazy='dynamic')

    def __repr__(self):
        return f'Doctor(id={self.id}, full_name={self.full_name}, login={self.login}, email={self.email}, ' \
               f'password_hash={self.password_hash}, patients= {self.patients})'
