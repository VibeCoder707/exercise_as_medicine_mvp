import streamlit as st
from datetime import datetime
import uuid
from .data_models import Patient, Prescription, ProgressRecord
from .mock_data import get_exercises_for_condition

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

def show_all_patients():
    """Show all patients in the database"""
    with get_db() as db:
        try:
            patients = crud.list_all_patients(db)
            if patients:
                st.subheader("All Patients")
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

def show_patient_profile():
    # Show existing patients
    show_all_patients()
    
    st.markdown("---")
    st.subheader("Add New Patient")
    st.header("Patient Profile")
    
    # Basic patient information form
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    
    # Health conditions multi-select
    conditions = st.multiselect(
        "Select Health Conditions",
        ["Fall Prevention", "Pain Management", "Diabetes Management", "Weight Management"]
    )
    
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
        if name and age and conditions:
            patient = Patient(
                id=str(uuid.uuid4()),
                name=name,
                age=age,
                conditions=conditions,
                risk_factors=risk_factors,
                goals=goals
            )
            st.success("Patient profile saved successfully!")
            # In a real app, we would save this to a database
            st.session_state['current_patient'] = patient
        else:
            st.error("Please fill in all required fields")

def show_exercise_prescription():
    st.header("Exercise Prescription")
    
    if 'current_patient' not in st.session_state:
        st.warning("Please create a patient profile first")
        return
    
    patient = st.session_state['current_patient']
    st.write(f"Creating prescription for: {patient.name}")
    
    # Show recommended exercises based on conditions
    for condition in patient.conditions:
        st.subheader(f"Recommended exercises for {condition}")
        exercises = get_exercises_for_condition(condition.lower().replace(" ", "_"))
        
        for exercise in exercises:
            st.write(f"**{exercise.name}**")
            st.write(exercise.description)
            st.write(f"Difficulty: {exercise.difficulty_level}")
            st.write(f"Target Areas: {', '.join(exercise.target_areas)}")
            st.write("---")
    
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
        prescription = Prescription(
            id=str(uuid.uuid4()),
            patient_id=patient.id,
            exercises=exercises,
            frequency=frequency,
            duration=duration,
            notes=notes
        )
        st.success("Prescription generated successfully!")
        # In a real app, we would save this to a database
        st.session_state['current_prescription'] = prescription

def show_progress_tracking():
    st.header("Progress Tracking")
    
    if 'current_patient' not in st.session_state:
        st.warning("Please create a patient profile first")
        return
    
    if 'current_prescription' not in st.session_state:
        st.warning("Please generate a prescription first")
        return
    
    patient = st.session_state['current_patient']
    prescription = st.session_state['current_prescription']
    
    st.write(f"Tracking progress for: {patient.name}")
    
    # Progress tracking form
    date = st.date_input("Date")
    duration = st.number_input("Exercise Duration (minutes)", min_value=0)
    difficulty = st.slider("Difficulty Level (1-5)", 1, 5)
    pain = st.slider("Pain Level (0-10)", 0, 10)
    notes = st.text_area("Session Notes")
    
    if st.button("Record Progress"):
        progress = ProgressRecord(
            id=str(uuid.uuid4()),
            patient_id=patient.id,
            prescription_id=prescription.id,
            date=datetime.combine(date, datetime.min.time()),
            exercises_completed=[ex.id for ex in prescription.exercises],
            duration=duration,
            difficulty_rating=difficulty,
            pain_level=pain,
            notes=notes
        )
        st.success("Progress recorded successfully!")
        # In a real app, we would save this to a database

if __name__ == "__main__":
    main()
