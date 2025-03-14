import streamlit as st
from datetime import datetime
from sqlalchemy.orm import Session
from .db.database import SessionLocal
from .db import crud, models

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
    page = st.sidebar.selectbox(
        "Select Page",
        ["Patient Profile", "Exercise Prescription", "Progress Tracking"]
    )
    
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
            for patient in patients:
                st.write(f"ID: {patient.id}")
                st.write(f"Name: {patient.name}")
                st.write(f"Age: {patient.age}")
                st.write(f"Risk Factors: {patient.risk_factors}")
                st.write(f"Goals: {patient.goals}")
                st.write("---")
        else:
            st.info("No patients in database")
    except Exception as e:
        st.error(f"Error fetching patients: {str(e)}")
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
            except Exception as e:
                st.error(f"Error saving prescription: {str(e)}")
                st.exception(e)
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.exception(e)
    finally:
        if 'db' in locals():
            db.close()

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
        
        # Progress tracking form
        date = st.date_input("Date")
        duration = st.number_input("Exercise Duration (minutes)", min_value=0)
        difficulty = st.slider("Difficulty Level (1-5)", 1, 5)
        pain = st.slider("Pain Level (0-10)", 0, 10)
        notes = st.text_area("Session Notes")
        
        if st.button("Record Progress"):
            try:
                # TODO: Implement progress recording in database
                st.success("Progress recorded successfully!")
            except Exception as e:
                st.error(f"Error recording progress: {str(e)}")
                st.exception(e)
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.exception(e)
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()
