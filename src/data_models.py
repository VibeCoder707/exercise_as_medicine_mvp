from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Patient:
    id: str
    name: str
    age: int
    conditions: List[str]
    risk_factors: List[str]
    goals: List[str]
    created_at: datetime = datetime.now()

@dataclass
class Exercise:
    id: str
    name: str
    description: str
    difficulty_level: str  # 'beginner', 'intermediate', 'advanced'
    target_areas: List[str]
    contraindications: List[str]
    video_url: Optional[str] = None
    image_url: Optional[str] = None

@dataclass
class Prescription:
    id: str
    patient_id: str
    exercises: List[Exercise]
    frequency: str  # e.g., '3 times per week'
    duration: str   # e.g., '30 minutes'
    notes: str
    created_at: datetime = datetime.now()
    
@dataclass
class ProgressRecord:
    id: str
    patient_id: str
    prescription_id: str
    date: datetime
    exercises_completed: List[str]
    duration: int  # minutes
    difficulty_rating: int  # 1-5
    pain_level: int  # 0-10
    notes: str