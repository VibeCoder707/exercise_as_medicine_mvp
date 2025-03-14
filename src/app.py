import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from typing import List
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db import crud, models

@dataclass
class Exercise:
    name: str
    description: str
    difficulty_level: str
    target_areas: List[str]

def get_exercises_for_condition(condition: str) -> List[Exercise]:
    """Get recommended exercises for a specific condition."""
    exercise_library = {
        "fall_prevention": [
            Exercise(
                name="Balance Walking",
                description="Walk heel to toe, as if on a tightrope. Take 20 steps forward.",
                difficulty_level="Beginner",
                target_areas=["Balance", "Core stability"]
            ),
            Exercise(
                name="Single Leg Stand",
                description="Stand on one leg for 30 seconds, then switch.",
                difficulty_level="Beginner",
                target_areas=["Balance", "Lower body strength"]
            )
        ],
        "pain_management": [
            Exercise(
                name="Gentle Stretching",
                description="Perform gentle full-body stretches, holding each for 15-30 seconds.",
                difficulty_level="Beginner",
                target_areas=["Flexibility", "Pain relief"]
            ),
            Exercise(
                name="Water Walking",
                description="Walk in chest-deep water for 10-15 minutes.",
                difficulty_level="Beginner",
                target_areas=["Cardiovascular", "Joint mobility"]
            )
        ],
        "diabetes_management": [
            Exercise(
                name="Brisk Walking",
                description="Walk at a brisk pace for 15-20 minutes.",
                difficulty_level="Moderate",
                target_areas=["Cardiovascular", "Blood sugar control"]
            ),
            Exercise(
                name="Resistance Band Exercises",
                description="Perform upper and lower body exercises with resistance bands.",
                difficulty_level="Moderate",
                target_areas=["Strength", "Metabolic health"]
            )
        ],
        "weight_management": [
            Exercise(
                name="Circuit Training",
                description="Alternate between cardio and strength exercises for 20 minutes.",
                difficulty_level="Advanced",
                target_areas=["Full body", "Cardiovascular"]
            ),
            Exercise(
                name="HIIT Walking",
                description="Alternate between 1 minute fast walking and 2 minutes normal pace.",
                difficulty_level="Moderate",
                target_areas=["Cardiovascular", "Weight loss"]
            )
        ]
    }
    
    return exercise_library.get(condition, [])

def get_db_session():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        raise

def main():
    st.title("Exercise as Medicine MVP")
    
    # Sidebar for navigation
    if 'page' not in st.session_state:
        st.session_state['page'] = "Patient Profile"
    
    page = st.sidebar.selectbox(
        "Select Page",
        ["Patient Profile", "Exercise Prescription", "Progress Tracking"],
        index=["Patient Profile", "Exercise Prescription", "Progress Tracking"].index(st.session_state['page'])
    )
    
    # Update session state when page changes
    st.session_state['page'] = page
    
    if page == "Patient Profile":
        show_patient_profile()
    elif page == "Exercise Prescription":
        show_exercise_prescription()
    else:
        show_progress_tracking()

def show_patient_profile():
    """Show patient profile page"""
    st.header("Patient Profile")
    
    # Show existing patients first
    try:
        db = get_db_session()
        patients = crud.list_all_patients(db)
        if patients:
            st.subheader("Existing Patients")
            
            # Create columns for layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create a selection box for patients
                patient_options = {f"{p.name} (ID: {p.id})": p.id for p in patients}
                selected_patient = st.selectbox(
                    "Select a patient to view or edit",
                    options=list(patient_options.keys()),
                    key="patient_selector"
                )
            
            with col2:
                # Add button to create prescription
                if st.button("Create Prescription", key="create_prescription"):
                    selected_patient_id = patient_options[selected_patient]
                    st.session_state['current_patient_id'] = selected_patient_id
                    st.session_state['page'] = "Exercise Prescription"
                    st.rerun()
            
            if selected_patient:
                # Display patient details
                selected_patient_id = patient_options[selected_patient]
                patient = next(p for p in patients if p.id == selected_patient_id)
                with st.expander("Patient Details", expanded=True):
                    st.write(f"Name: {patient.name}")
                    st.write(f"Age: {patient.age}")
                    st.write(f"Risk Factors: {', '.join(patient.risk_factors) if patient.risk_factors else 'None'}")
                    st.write(f"Goals: {', '.join(patient.goals) if patient.goals else 'None'}")
        else:
            st.info("No patients in database")
    except Exception as e:
        st.error(f"Error fetching patients: {str(e)}")
        st.exception(e)  # This will show the full error trace
    finally:
        if 'db' in locals():
            db.close()
    
    # Form for adding new patient
    st.subheader("Add New Patient")
    
    # Basic patient information form
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    
    # Risk factors
    risk_factors = st.multiselect(
        "Select Risk Factors",
        ["High Blood Pressure", "Diabetes", "Heart Disease", "Osteoporosis"]
    )
    
    # Goals
    goals = st.multiselect(
        "Select Goals",
        ["Improve Balance", "Reduce Pain", "Increase Strength", "Weight Loss"]
    )
    
    if st.button("Save Profile"):
        if name and age:
            try:
                db = get_db_session()
                patient = crud.create_patient(
                    db=db,
                    name=name,
                    age=age,
                    risk_factors=risk_factors,
                    goals=goals
                )
                st.success(f"Patient profile saved successfully! ID: {patient.id}")
                st.session_state['current_patient_id'] = patient.id
            except Exception as e:
                st.error(f"Error saving patient profile: {str(e)}")
                st.exception(e)
            finally:
                db.close()
        else:
            st.error("Please fill in all required fields")

def show_exercise_prescription():
    st.header("Exercise Prescription")
    
    if 'current_patient_id' not in st.session_state:
        st.warning("Please create a patient profile first")
        return
    
    try:
        db = get_db_session()
        patient = crud.get_patient(db, st.session_state['current_patient_id'])
        
        if not patient:
            st.error("Patient not found in database")
            return
        
        st.write(f"Creating prescription for: {patient.name}")
        
        # Exercise recommendations
        available_conditions = [
            "Fall Prevention",
            "Pain Management",
            "Diabetes Management",
            "Weight Management"
        ]
        
        selected_conditions = st.multiselect(
            "Select conditions to address",
            available_conditions
        )
        
        if selected_conditions:
            for condition in selected_conditions:
                st.subheader(f"Recommended exercises for {condition}")
                exercises = get_exercises_for_condition(condition.lower().replace(" ", "_"))
                
                if exercises:
                    for exercise in exercises:
                        st.write(f"**{exercise.name}**")
                        st.write(exercise.description)
                        st.write(f"Difficulty: {exercise.difficulty_level}")
                        st.write(f"Target Areas: {', '.join(exercise.target_areas)}")
                        st.write("---")
                else:
                    st.info(f"No exercises found for {condition}")
        
        # Prescription details
        frequency = st.selectbox(
            "Exercise Frequency",
            ["2 times per week", "3 times per week", "4 times per week", "5 times per week"]
        )
        
        duration = st.selectbox(
            "Session Duration",
            ["15 minutes", "20 minutes", "30 minutes", "45 minutes"]
        )
        
        notes = st.text_area("Additional Notes")
        
        if st.button("Generate Prescription"):
            try:
                prescription = crud.create_prescription(
                    db=db,
                    patient_id=patient.id,
                    exercises=[{"name": ex.name, "description": ex.description} for cond in selected_conditions for ex in get_exercises_for_condition(cond.lower().replace(" ", "_"))],
                    frequency=frequency,
                    duration=duration,
                    notes=notes
                )
                st.success("Prescription generated and saved successfully!")
                st.session_state['current_prescription_id'] = prescription.id
                
                # Add a button to go to Progress Tracking
                if st.button("Start Tracking Progress"):
                    st.session_state['page'] = "Progress Tracking"
                    st.rerun()
            except Exception as e:
                st.error(f"Error saving prescription: {str(e)}")
                st.exception(e)
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.exception(e)
    finally:
        if 'db' in locals():
            db.close()

from src.visualizations import display_progress_visualizations

def show_progress_tracking():
    st.header("Progress Tracking")
    
    if 'current_patient_id' not in st.session_state:
        st.warning("Please create a patient profile first")
        return
    
    if 'current_prescription_id' not in st.session_state:
        st.warning("Please generate a prescription first")
        return
    
    try:
        db = get_db_session()
        patient = crud.get_patient(db, st.session_state['current_patient_id'])
        prescription = crud.get_prescription(db, st.session_state['current_prescription_id'])
        
        if not patient or not prescription:
            st.error("Patient or prescription not found in database")
            return
        
        st.write(f"Tracking progress for: {patient.name}")
        
        # Create tabs for data entry and visualizations
        tab1, tab2 = st.tabs(["Record Progress", "View Progress"])
        
        with tab1:
            # Progress tracking form
            date = st.date_input("Date")
            duration = st.number_input("Exercise Duration (minutes)", min_value=0)
            difficulty = st.slider("Difficulty Level (1-5)", 1, 5)
            pain = st.slider("Pain Level (0-10)", 0, 10)
            notes = st.text_area("Session Notes")
            
            if st.button("Record Progress"):
                try:
                    progress = crud.record_progress(
                        db=db,
                        patient_id=patient.id,
                        prescription_id=prescription.id,
                        date=date,
                        duration=duration,
                        difficulty_level=difficulty,
                        pain_level=pain,
                        notes=notes
                    )
                    st.success("Progress recorded successfully!")
                except Exception as e:
                    st.error(f"Error recording progress: {str(e)}")
                    st.exception(e)
        
        with tab2:
            # Get all progress entries for visualization
            progress_history = crud.get_patient_progress(db, patient.id)
            display_progress_visualizations(progress_history)
            
            # Show recent entries in a table
            if progress_history:
                st.subheader("Recent Progress Entries")
                with st.expander("View Details"):
                    for entry in progress_history[:5]:  # Show last 5 entries
                        st.write(f"Date: {entry.date.strftime('%Y-%m-%d')}")
                        st.write(f"Duration: {entry.duration} minutes")
                        st.write(f"Difficulty: {entry.difficulty_level}/5")
                        st.write(f"Pain: {entry.pain_level}/10")
                        if entry.notes:
                            st.write(f"Notes: {entry.notes}")
                        st.write("---")
            
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.exception(e)
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()
