"""
Pattern Notes & Ratings
Personal notes, modifications, and ratings for each pattern
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Crochet-themed styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sacramento&family=Nunito:wght@400;700;800&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background-color: #FFF5F7;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(232,129,156,.03) 35px, rgba(232,129,156,.03) 70px),
            repeating-linear-gradient(-45deg, transparent, transparent 35px, rgba(244,168,184,.03) 35px, rgba(244,168,184,.03) 70px);
    }
    html, body, [class*="css"], p, div, span {
        font-family: Georgia, serif !important;
    }
    h1, h2, h3 {
        font-family: 'Sacramento', cursive !important;
        color: #D66B87;
    }
    .stat-number { font-family: 'Nunito', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Pattern Notes & Ratings - Tangled",
    page_icon="⭐",
    layout="wide"
)

# File paths
RATINGS_FILE = "pattern_ratings.xlsx"
NOTES_FILE = "pattern_notes.xlsx"
PATTERNS_FILE = "pattern_database.xlsx"

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        try:
            return pd.read_excel(RATINGS_FILE)
        except:
            return pd.DataFrame(columns=[
                'Pattern_Name', 'Overall_Rating', 'Difficulty_vs_Listed', 
                'Would_Make_Again', 'Completed_Date', 'Time_Taken_Hours', 
                'Review_Text', 'Date_Added'
            ])
    return pd.DataFrame(columns=[
        'Pattern_Name', 'Overall_Rating', 'Difficulty_vs_Listed', 
        'Would_Make_Again', 'Completed_Date', 'Time_Taken_Hours', 
        'Review_Text', 'Date_Added'
    ])

def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            return pd.read_excel(NOTES_FILE)
        except:
            return pd.DataFrame(columns=[
                'Pattern_Name', 'Note_Type', 'Note_Text', 'Hook_Size_Used',
                'Yarn_Substitution', 'Modifications_Made', 'Tips', 'Date_Added'
            ])
    return pd.DataFrame(columns=[
        'Pattern_Name', 'Note_Type', 'Note_Text', 'Hook_Size_Used',
        'Yarn_Substitution', 'Modifications_Made', 'Tips', 'Date_Added'
    ])

def load_patterns():
    if os.path.exists(PATTERNS_FILE):
        try:
            df = pd.read_excel(PATTERNS_FILE)
            return sorted(df['Pattern_Name'].dropna().unique().tolist())
        except:
            return []
    return []

# Initialize session state
if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df = load_ratings()

if 'notes_df' not in st.session_state:
    st.session_state.notes_df = load_notes()

# Header
st.title("⭐ Pattern Notes & Ratings")
st.markdown("Track your experience with each pattern - what worked, what didn't, and what you'd do differently!")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 My Notes", "⭐ Rate a Pattern", "📊 Overview"])

with tab1:
    st.header("Pattern Notes")
    
    available_patterns = load_patterns()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if available_patterns:
            selected_pattern = st.selectbox("Select Pattern", ["All Patterns"] + available_patterns)
        else:
            st.warning("No patterns found in database")
            selected_pattern = None
    
    with col2:
        if st.button("➕ Add New Note", type="primary"):
            st.session_state.show_note_form = True
    
    # Show note form
    if st.session_state.get('show_note_form', False):
        st.subheader("Add Pattern Note")
        
        if not available_patterns:
            st.warning("No patterns found in database. Please add patterns first.")
        else:
            with st.form("add_note_form"):
                note_pattern = st.selectbox("Pattern", available_patterns)
                note_type = st.selectbox("Note Type", ["General", "Modification", "Yarn Substitution", "Hook Size Change", "Tip"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    note_text = st.text_area("Note*", placeholder="What do you want to remember about this pattern?")
                    hook_used = st.text_input("Hook Size Used", placeholder="e.g., 4.0mm")
                
                with col2:
                    yarn_sub = st.text_area("Yarn Substitution", placeholder="What yarn did you use instead?")
                    modifications = st.text_area("Modifications Made", placeholder="How did you change the pattern?")
                
                tips = st.text_area("Tips for Next Time", placeholder="What would you do differently?")
                
                col1, col2 = st.columns([1, 5])
                
                with col1:
                    submitted = st.form_submit_button("💾 Save Note")
                
                with col2:
                    cancel = st.form_submit_button("❌ Cancel")
                
                if cancel:
                    st.session_state.show_note_form = False
                    st.rerun()
            
            if submitted and note_text:
                new_note = {
                    'Pattern_Name': note_pattern,
                    'Note_Type': note_type,
                    'Note_Text': note_text,
                    'Hook_Size_Used': hook_used,
                    'Yarn_Substitution': yarn_sub,
                    'Modifications_Made': modifications,
                    'Tips': tips,
                    'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.session_state.notes_df = pd.concat(
                    [st.session_state.notes_df, pd.DataFrame([new_note])],
                    ignore_index=True
                )
                
                st.session_state.notes_df.to_excel(NOTES_FILE, index=False)
                st.success("✅ Note saved!")
                st.session_state.show_note_form = False
                st.rerun()
    
    # Display notes
    st.divider()
    
    if st.session_state.notes_df.empty:
        st.info("No notes yet. Add your first note about a pattern!")
    else:
        display_df = st.session_state.notes_df.copy()
        
        if selected_pattern and selected_pattern != "All Patterns":
            display_df = display_df[display_df['Pattern_Name'] == selected_pattern]
        
        if display_df.empty:
            st.info(f"No notes for {selected_pattern}")
        else:
            # Sort by date, newest first
            display_df = display_df.sort_values('Date_Added', ascending=False)
            
            for idx, note in display_df.iterrows():
                with st.expander(f"📝 {note['Pattern_Name']} - {note['Note_Type']} ({note['Date_Added'][:10]})"):
                    st.write(f"**{note['Note_Text']}**")
                    
                    if pd.notna(note['Hook_Size_Used']) and note['Hook_Size_Used']:
                        st.write(f"🪝 **Hook Used:** {note['Hook_Size_Used']}")
                    
                    if pd.notna(note['Yarn_Substitution']) and note['Yarn_Substitution']:
                        st.write(f"🧶 **Yarn Substitution:** {note['Yarn_Substitution']}")
                    
                    if pd.notna(note['Modifications_Made']) and note['Modifications_Made']:
                        st.write(f"✂️ **Modifications:** {note['Modifications_Made']}")
                    
                    if pd.notna(note['Tips']) and note['Tips']:
                        st.write(f"💡 **Tips:** {note['Tips']}")
                    
                    if st.button("🗑️ Delete Note", key=f"del_note_{idx}"):
                        st.session_state.notes_df = st.session_state.notes_df.drop(idx).reset_index(drop=True)
                        st.session_state.notes_df.to_excel(NOTES_FILE, index=False)
                        st.success("Note deleted!")
                        st.rerun()

with tab2:
    st.header("Rate a Pattern")
    
    available_patterns = load_patterns()
    
    if not available_patterns:
        st.warning("No patterns available to rate")
    else:
        # Show existing ratings
        st.subheader("Your Ratings")
        
        if st.session_state.ratings_df.empty:
            st.info("No patterns rated yet. Rate your first pattern below!")
        else:
            for idx, rating in st.session_state.ratings_df.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    stars = "⭐" * int(rating['Overall_Rating'])
                    st.write(f"**{rating['Pattern_Name']}** {stars}")
                
                with col2:
                    would_make = "✅ Yes" if rating['Would_Make_Again'] else "❌ No"
                    st.caption(f"Make again: {would_make}")
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_rating_{idx}"):
                        st.session_state.ratings_df = st.session_state.ratings_df.drop(idx).reset_index(drop=True)
                        st.session_state.ratings_df.to_excel(RATINGS_FILE, index=False)
                        st.rerun()
        
        st.divider()
        st.subheader("Add New Rating")
        
        # Check which patterns already have ratings
        rated_patterns = st.session_state.ratings_df['Pattern_Name'].tolist()
        unrated_patterns = [p for p in available_patterns if p not in rated_patterns]
        
        if not unrated_patterns:
            st.info("You've rated all available patterns!")
        else:
            with st.form("rating_form"):
                pattern_to_rate = st.selectbox("Select Pattern*", unrated_patterns)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    overall_rating = st.slider("Overall Rating*", 1, 5, 5, help="How much did you like this pattern?")
                    
                    difficulty_vs_listed = st.select_slider(
                        "Difficulty vs. Listed*",
                        options=["Much Easier", "Easier", "As Expected", "Harder", "Much Harder"],
                        value="As Expected"
                    )
                    
                    would_make_again = st.checkbox("Would make again", value=True)
                
                with col2:
                    completed_date = st.date_input("When did you complete it?", value=datetime.now())
                    time_taken = st.number_input("Time taken (hours)", min_value=0.0, value=0.0, step=0.5)
                
                review_text = st.text_area("Review (optional)", placeholder="Share your thoughts about this pattern...")
                
                submitted = st.form_submit_button("⭐ Submit Rating")
                
                if submitted:
                    new_rating = {
                        'Pattern_Name': pattern_to_rate,
                        'Overall_Rating': overall_rating,
                        'Difficulty_vs_Listed': difficulty_vs_listed,
                        'Would_Make_Again': would_make_again,
                        'Completed_Date': completed_date.strftime("%Y-%m-%d"),
                        'Time_Taken_Hours': time_taken,
                        'Review_Text': review_text,
                        'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    
                    st.session_state.ratings_df = pd.concat(
                        [st.session_state.ratings_df, pd.DataFrame([new_rating])],
                        ignore_index=True
                    )
                    
                    st.session_state.ratings_df.to_excel(RATINGS_FILE, index=False)
                    st.success(f"✅ Rating saved for {pattern_to_rate}!")
                    st.balloons()
                    st.rerun()

with tab3:
    st.header("Overview & Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Ratings Statistics")
        
        if st.session_state.ratings_df.empty:
            st.info("No ratings yet")
        else:
            df = st.session_state.ratings_df
            
            # Summary metrics
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Patterns Rated", len(df))
                avg_rating = df['Overall_Rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}⭐")
            
            with col_b:
                would_make_pct = (df['Would_Make_Again'].sum() / len(df)) * 100
                st.metric("Would Make Again", f"{would_make_pct:.0f}%")
                
                if df['Time_Taken_Hours'].sum() > 0:
                    avg_time = df['Time_Taken_Hours'].mean()
                    st.metric("Avg. Time", f"{avg_time:.1f}h")
            
            # Top rated patterns
            st.write("**⭐ Top Rated Patterns**")
            top_rated = df.nlargest(5, 'Overall_Rating')[['Pattern_Name', 'Overall_Rating']]
            for _, row in top_rated.iterrows():
                stars = "⭐" * int(row['Overall_Rating'])
                st.write(f"• {row['Pattern_Name']} {stars}")
            
            # Difficulty feedback
            st.write("**📈 Difficulty Feedback**")
            diff_counts = df['Difficulty_vs_Listed'].value_counts()
            st.bar_chart(diff_counts)
    
    with col2:
        st.subheader("📝 Notes Statistics")
        
        if st.session_state.notes_df.empty:
            st.info("No notes yet")
        else:
            df = st.session_state.notes_df
            
            # Summary metrics
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Total Notes", len(df))
                patterns_with_notes = df['Pattern_Name'].nunique()
                st.metric("Patterns with Notes", patterns_with_notes)
            
            with col_b:
                most_common_type = df['Note_Type'].mode()[0] if not df.empty else "N/A"
                st.metric("Most Common Type", most_common_type)
            
            # Notes by type
            st.write("**📋 Notes by Type**")
            type_counts = df['Note_Type'].value_counts()
            st.bar_chart(type_counts)
            
            # Most documented patterns
            st.write("**📚 Most Documented Patterns**")
            pattern_notes = df['Pattern_Name'].value_counts().head(5)
            for pattern, count in pattern_notes.items():
                st.write(f"• {pattern} ({count} notes)")

# Footer
st.divider()
st.caption("💡 Tip: Keep detailed notes to help yourself and others who might use the same patterns!")
