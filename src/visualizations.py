import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from typing import List
from .db.models import Progress

def create_progress_dataframe(progress_entries: List[Progress]) -> pd.DataFrame:
    """Convert progress entries to a pandas DataFrame"""
    if not progress_entries:
        return pd.DataFrame()
    
    data = [{
        'date': entry.date,
        'duration': entry.duration,
        'difficulty_level': entry.difficulty_level,
        'pain_level': entry.pain_level,
        'notes': entry.notes
    } for entry in progress_entries]
    
    return pd.DataFrame(data)

def plot_duration_chart(df: pd.DataFrame) -> None:
    """Plot exercise duration over time"""
    if df.empty:
        st.info("No duration data available yet")
        return
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('duration:Q', title='Duration (minutes)'),
        tooltip=['date', 'duration', 'notes']
    ).properties(
        title='Exercise Duration Over Time',
        width=600,
        height=300
    )
    
    st.altair_chart(chart, use_container_width=True)

def plot_metrics_chart(df: pd.DataFrame) -> None:
    """Plot pain and difficulty levels over time"""
    if df.empty:
        st.info("No metrics data available yet")
        return
    
    # Create a base chart for both metrics
    base = alt.Chart(df).encode(
        x=alt.X('date:T', title='Date')
    ).properties(
        width=600,
        height=200
    )
    
    # Pain level line
    pain_line = base.mark_line(color='red', point=True).encode(
        y=alt.Y('pain_level:Q', title='Pain Level (0-10)'),
        tooltip=['date', 'pain_level', 'notes']
    ).properties(
        title='Pain Level Over Time'
    )
    
    # Difficulty level line
    difficulty_line = base.mark_line(color='blue', point=True).encode(
        y=alt.Y('difficulty_level:Q', title='Difficulty Level (1-5)'),
        tooltip=['date', 'difficulty_level', 'notes']
    ).properties(
        title='Difficulty Level Over Time'
    )
    
    # Display charts
    st.altair_chart(pain_line, use_container_width=True)
    st.altair_chart(difficulty_line, use_container_width=True)

def show_progress_stats(df: pd.DataFrame) -> None:
    """Show summary statistics for progress"""
    if df.empty:
        st.info("No statistics available yet")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Duration",
            f"{df['duration'].mean():.1f} min",
            f"{df['duration'].std():.1f} min σ"
        )
    
    with col2:
        st.metric(
            "Average Pain Level",
            f"{df['pain_level'].mean():.1f}",
            f"{df['pain_level'].std():.1f} σ"
        )
    
    with col3:
        st.metric(
            "Average Difficulty",
            f"{df['difficulty_level'].mean():.1f}",
            f"{df['difficulty_level'].std():.1f} σ"
        )

def display_progress_visualizations(progress_entries: List[Progress]) -> None:
    """Display all progress visualizations"""
    df = create_progress_dataframe(progress_entries)
    
    if df.empty:
        st.warning("No progress data available. Record some exercise sessions to see visualizations!")
        return
    
    st.subheader("Progress Overview")
    show_progress_stats(df)
    
    st.subheader("Exercise Duration")
    plot_duration_chart(df)
    
    st.subheader("Pain and Difficulty Levels")
    plot_metrics_chart(df)