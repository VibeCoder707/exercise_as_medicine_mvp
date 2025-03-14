from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from .database import Base

# Association tables
patient_conditions = Table(
    'patient_conditions', Base.metadata,
    Column('patient_id', Integer, ForeignKey('patients.id')),
    Column('condition_id', Integer, ForeignKey('conditions.id'))
)

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    risk_factors = Column(JSON)
    goals = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conditions = relationship("Condition", secondary=patient_conditions, back_populates="patients")
    prescriptions = relationship("Prescription", back_populates="patient")
    progress_entries = relationship("Progress", back_populates="patient")

class Condition(Base):
    __tablename__ = 'conditions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    patients = relationship("Patient", secondary=patient_conditions, back_populates="conditions")

class Prescription(Base):
    __tablename__ = 'prescriptions'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    exercises = Column(JSON)  # Store as JSON for simplicity in MVP
    frequency = Column(String)
    duration = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="prescriptions")
    progress_entries = relationship("Progress", back_populates="prescription")

class Progress(Base):
    __tablename__ = 'progress'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    prescription_id = Column(Integer, ForeignKey('prescriptions.id'))
    date = Column(DateTime)
    duration = Column(Integer)  # in minutes
    difficulty_level = Column(Integer)
    pain_level = Column(Integer)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="progress_entries")
    prescription = relationship("Prescription", back_populates="progress_entries")
