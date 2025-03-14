from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models

def list_all_patients(db: Session) -> List[models.Patient]:
    """List all patients in the database"""
    try:
        patients = db.query(models.Patient).order_by(models.Patient.id.desc()).all()
        print(f"Found {len(patients)} patients in database")
        for patient in patients:
            print(f"Patient ID: {patient.id}, Name: {patient.name}")
        return patients
    except Exception as e:
        print(f"Error listing patients: {str(e)}")
        db.rollback()
        raise

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

def get_prescription(db: Session, prescription_id: int) -> Optional[models.Prescription]:
    """Get a prescription by ID"""
    return db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()

def record_progress(
    db: Session,
    patient_id: int,
    prescription_id: int,
    date: datetime,
    duration: int,
    difficulty_level: int,
    pain_level: int,
    notes: str
) -> models.Progress:
    """Record a progress entry"""
    db_progress = models.Progress(
        patient_id=patient_id,
        prescription_id=prescription_id,
        date=date,
        duration=duration,
        difficulty_level=difficulty_level,
        pain_level=pain_level,
        notes=notes
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_patient_progress(
    db: Session,
    patient_id: int
) -> List[models.Progress]:
    """Get all progress entries for a patient"""
    return db.query(models.Progress).filter(
        models.Progress.patient_id == patient_id
    ).order_by(models.Progress.date.desc()).all()

def record_progress(
    db: Session,
    patient_id: int,
    prescription_id: int,
    date: datetime,
    duration: int,
    difficulty_level: int,
    pain_level: int,
    notes: str
) -> models.Progress:
    """Record a progress entry"""
    db_progress = models.Progress(
        patient_id=patient_id,
        prescription_id=prescription_id,
        date=date,
        duration=duration,
        difficulty_level=difficulty_level,
        pain_level=pain_level,
        notes=notes
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_patient_progress(
    db: Session,
    patient_id: int
) -> List[models.Progress]:
    """Get all progress entries for a patient"""
    return db.query(models.Progress).filter(
        models.Progress.patient_id == patient_id
    ).order_by(models.Progress.date.desc()).all()
