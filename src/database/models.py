from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

# Association tables for many-to-many relationships
patient_conditions = Table(
    'patient_conditions', Base.metadata,
    Column('patient_id', Integer, ForeignKey('patients.id')),
    Column('condition_id', Integer, ForeignKey('conditions.id'))
)

prescription_exercises = Table(
    'prescription_exercises', Base.metadata,
    Column('prescription_id', Integer, ForeignKey('prescriptions.id')),
    Column('exercise_id', Integer, ForeignKey('exercises.id'))
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
    progress_records = relationship("ProgressRecord", back_populates="patient")

class Condition(Base):
    __tablename__ = 'conditions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    patients = relationship("Patient", secondary=patient_conditions, back_populates="conditions")
    exercises = relationship("Exercise", back_populates="conditions")

class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    difficulty_level = Column(String)
    target_areas = Column(JSON)
    contraindications = Column(JSON)
    video_url = Column(String)
    image_url = Column(String)
    condition_id = Column(Integer, ForeignKey('conditions.id'))
    
    conditions = relationship("Condition", back_populates="exercises")
    prescriptions = relationship("Prescription", secondary=prescription_exercises, back_populates="exercises")

class Prescription(Base):
    __tablename__ = 'prescriptions'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    frequency = Column(String)
    duration = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="prescriptions")
    exercises = relationship("Exercise", secondary=prescription_exercises, back_populates="prescriptions")
    progress_records = relationship("ProgressRecord", back_populates="prescription")

class ProgressRecord(Base):
    __tablename__ = 'progress_records'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    prescription_id = Column(Integer, ForeignKey('prescriptions.id'))
    date = Column(DateTime, nullable=False)
    duration = Column(Integer)  # minutes
    difficulty_rating = Column(Integer)  # 1-5
    pain_level = Column(Integer)  # 0-10
    notes = Column(String)
    
    patient = relationship("Patient", back_populates="progress_records")
    prescription = relationship("Prescription", back_populates="progress_records")