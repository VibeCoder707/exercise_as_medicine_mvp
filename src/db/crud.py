from sqlalchemy.orm import Session
from . import models
from typing import List, Optional
from datetime import datetime

def create_patient(
    db: Session,
    name: str,
    age: int,
    risk_factors: List[str],
    goals: List[str]
) -> models.Patient:
    """Create a new patient"""
    db_patient = models.Patient(
        name=name,
        age=age,
        risk_factors=risk_factors,
        goals=goals
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int) -> Optional[models.Patient]:
    """Get a patient by ID"""
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def create_prescription(
    db: Session,
    patient_id: int,
    exercises: List[dict],
    frequency: str,
    duration: str,
    notes: str
) -> models.Prescription:
    """Create a new prescription"""
    db_prescription = models.Prescription(
        patient_id=patient_id,
        exercises=exercises,
        frequency=frequency,
        duration=duration,
        notes=notes
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def get_patient_prescriptions(
    db: Session,
    patient_id: int
) -> List[models.Prescription]:
    """Get all prescriptions for a patient"""
    return db.query(models.Prescription).filter(
        models.Prescription.patient_id == patient_id
    ).all()