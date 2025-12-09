"""
Pattern Ratings & Notes System
Rate patterns and add personal notes about your experience
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File paths
RATINGS_FILE = "pattern_ratings.xlsx"
NOTES_FILE = "pattern_notes.xlsx"
PATTERNS_FILE = "pattern_database.xlsx"

def load_ratings():
    """Load pattern ratings"""
    if os.path.exists(RATINGS_FILE):
        try:
            return pd.read_excel(RATINGS_FILE)
        except:
            return create_empty_ratings()
    return create_empty_ratings()

def create_empty_ratings():
    """Create empty ratings DataFrame"""
    return pd.DataFrame(columns=[
        'Pattern_Name', 'Overall_Rating', 'Difficulty_vs_Listed', 
        'Would_Make_Again', 'Completed_Date', 'Time_Taken_Hours', 
        'Review_Text', 'Date_Added'
    ])

def save_ratings(df):
    """Save ratings to Excel"""
    df.to_excel(RATINGS_FILE, index=False)

def load_notes():
    """Load pattern notes"""
    if os.path.exists(NOTES_FILE):
        try:
            return pd.read_excel(NOTES_FILE)
        except:
            return create_empty_notes()
    return create_empty_notes()

def create_empty_notes():
    """Create empty notes DataFrame"""
    return pd.DataFrame(columns=[
        'Pattern_Name', 'Note_Type', 'Note_Text', 'Hook_Size_Used',
        'Yarn_Substitution', 'Modifications_Made', 'Tips', 'Date_Added'
    ])

def save_notes(df):
    """Save notes to Excel"""
    df.to_excel(NOTES_FILE, index=False)

def load_patterns():
    """Load available patterns"""
    if os.path.exists(PATTERNS_FILE):
        try:
            df = pd.read_excel(PATTERNS_FILE)
            return df['Pattern_Name'].dropna().unique().tolist()
        except:
            return []
    return []

def get_pattern_rating(pattern_name, ratings_df):
    """Get rating for a specific pattern"""
    pattern_ratings = ratings_df[ratings_df['Pattern_Name'] == pattern_name]
    if not pattern_ratings.empty:
        return pattern_ratings.iloc[0]
    return None

def get_pattern_notes(pattern_name, notes_df):
    """Get all notes for a specific pattern"""
    return notes_df[notes_df['Pattern_Name'] == pattern_name]
