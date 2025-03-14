from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Patient, Condition, Exercise, Prescription, ProgressRecord

def create_patient(db: Session, name: str, age: int, risk_factors: List[str], goals: List[str]) -> Patient:
    db_patient = Patient(
        name=name,
        age=age,
        risk_factors=risk_factors,
        goals=goals
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def create_prescription(
    db: Session, 
    patient_id: int,
    exercise_ids: List[int],
    frequency: str,
    duration: str,
    notes: str
) -> Prescription:
    db_prescription = Prescription(
        patient_id=patient_id,
        frequency=frequency,
        duration=duration,
        notes=notes
    )
    
    # Get exercises
    exercises = db.query(Exercise).filter(Exercise.id.in_(exercise_ids)).all()
    db_prescription.exercises = exercises
    
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def create_progress_record(
    db: Session,
    patient_id: int,
    prescription_id: int,
    date: datetime,
    duration: int,
    difficulty_rating: int,
    pain_level: int,
    notes: str
) -> ProgressRecord:
    db_record = ProgressRecord(
        patient_id=patient_id,
        prescription_id=prescription_id,
        date=date,
        duration=duration,
        difficulty_rating=difficulty_rating,
        pain_level=pain_level,
        notes=notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_patient_progress(db: Session, patient_id: int) -> List[ProgressRecord]:
    return db.query(ProgressRecord).filter(ProgressRecord.patient_id == patient_id).all()

def get_exercises_for_condition(db: Session, condition_name: str) -> List[Exercise]:
    condition = db.query(Condition).filter(Condition.name == condition_name).first()
    return condition.exercises if condition else []