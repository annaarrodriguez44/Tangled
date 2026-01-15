"""
Project Tracker
Track your work-in-progress (WIP) and completed crochet projects
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Crochet-themed styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Nunito:wght@400;700;800&display=swap');
    
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
    page_title="Project Tracker - Tangled",
    page_icon="📝",
    layout="wide"
)

# File paths
PROJECTS_FILE = "projects.xlsx"
PATTERNS_FILE = "pattern_database.xlsx"

def load_projects():
    """Load projects from Excel file"""
    if os.path.exists(PROJECTS_FILE):
        try:
            return pd.read_excel(PROJECTS_FILE)
        except:
            return create_empty_projects()
    else:
        return create_empty_projects()

def create_empty_projects():
    """Create empty projects DataFrame"""
    return pd.DataFrame(columns=[
        'Project_Name', 'Pattern_Name', 'Start_Date', 'Target_End_Date', 
        'Actual_End_Date', 'Status', 'Progress_Percent', 'Yarn_Used',
        'Hook_Size', 'Notes', 'Hours_Worked', 'Difficulty_Rating', 'Date_Created'
    ])

def save_projects(df):
    """Save projects to Excel file"""
    df.to_excel(PROJECTS_FILE, index=False)

def load_patterns():
    """Load available patterns"""
    if os.path.exists(PATTERNS_FILE):
        try:
            df = pd.read_excel(PATTERNS_FILE)
            return df['Pattern_Name'].dropna().unique().tolist()
        except:
            return []
    return []

# Initialize session state
if 'projects_df' not in st.session_state:
    st.session_state.projects_df = load_projects()

# Header
st.title("📝 Project Tracker")
st.markdown("Keep track of your crochet projects from start to finish!")

# Sidebar
with st.sidebar:
    st.header("Quick Stats")
    
    if not st.session_state.projects_df.empty:
        df = st.session_state.projects_df
        
        wip_count = len(df[df['Status'] == 'In Progress'])
        completed_count = len(df[df['Status'] == 'Completed'])
        planned_count = len(df[df['Status'] == 'Planned'])
        
        st.metric("🚧 Work in Progress", wip_count)
        st.metric("✅ Completed", completed_count)
        st.metric("📅 Planned", planned_count)
        
        if wip_count > 0:
            avg_progress = df[df['Status'] == 'In Progress']['Progress_Percent'].mean()
            st.metric("📊 Avg. Progress", f"{avg_progress:.0f}%")
    else:
        st.info("No projects yet. Start tracking your first project!")
    
    st.divider()
    
    view_mode = st.radio(
        "View",
        ["All Projects", "In Progress", "Completed", "Planned", "On Hold"]
    )

# Main tabs
tab1, tab2, tab3 = st.tabs(["📋 Projects", "➕ New Project", "📊 Statistics"])

with tab1:
    st.header("Your Projects")
    
    # Filter projects based on view mode
    if st.session_state.projects_df.empty:
        st.info("No projects yet. Create your first project in the 'New Project' tab!")
    else:
        filtered_df = st.session_state.projects_df.copy()
        
        if view_mode != "All Projects":
            filtered_df = filtered_df[filtered_df['Status'] == view_mode]
        
        if filtered_df.empty:
            st.warning(f"No projects with status: {view_mode}")
        else:
            # Display projects as cards
            for idx, project in filtered_df.iterrows():
                # Status emoji
                status_emoji = {
                    'Planned': '📅',
                    'In Progress': '🚧',
                    'On Hold': '⏸️',
                    'Completed': '✅',
                    'Abandoned': '❌'
                }.get(project['Status'], '📝')
                
                with st.expander(f"{status_emoji} {project['Project_Name']} ({project['Progress_Percent']:.0f}%)"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Pattern:** {project['Pattern_Name']}")
                        st.write(f"**Status:** {project['Status']}")
                        st.write(f"**Started:** {project['Start_Date']}")
                        
                        if pd.notna(project['Target_End_Date']):
                            st.write(f"**Target completion:** {project['Target_End_Date']}")
                        
                        if pd.notna(project['Actual_End_Date']):
                            st.write(f"**Completed on:** {project['Actual_End_Date']}")
                        
                        if pd.notna(project['Yarn_Used']):
                            st.write(f"**Yarn:** {project['Yarn_Used']}")
                        
                        st.write(f"**Hook size:** {project['Hook_Size']}")
                        
                        if pd.notna(project['Hours_Worked']) and project['Hours_Worked'] > 0:
                            st.write(f"**Time invested:** {project['Hours_Worked']:.1f} hours")
                        
                        if pd.notna(project['Notes']):
                            st.write(f"**Notes:** {project['Notes']}")
                    
                    with col2:
                        # Progress bar
                        st.write("**Progress:**")
                        st.progress(project['Progress_Percent'] / 100)
                        st.write(f"{project['Progress_Percent']:.0f}%")
                        
                        # Quick actions
                        st.write("**Quick Actions:**")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if st.button("✏️ Edit", key=f"edit_{idx}"):
                                st.session_state.edit_project_idx = idx
                                st.rerun()
                        
                        with col_b:
                            if st.button("🗑️ Delete", key=f"del_{idx}"):
                                st.session_state.projects_df = st.session_state.projects_df.drop(idx).reset_index(drop=True)
                                save_projects(st.session_state.projects_df)
                                st.success("Project deleted!")
                                st.rerun()
                        
                        # Update progress for WIP projects
                        if project['Status'] == 'In Progress':
                            new_progress = st.slider(
                                "Update progress",
                                0, 100,
                                int(project['Progress_Percent']),
                                key=f"progress_{idx}"
                            )
                            
                            if st.button("💾 Save Progress", key=f"save_prog_{idx}"):
                                st.session_state.projects_df.at[idx, 'Progress_Percent'] = new_progress
                                
                                if new_progress == 100:
                                    st.session_state.projects_df.at[idx, 'Status'] = 'Completed'
                                    st.session_state.projects_df.at[idx, 'Actual_End_Date'] = datetime.now().strftime("%Y-%m-%d")
                                
                                save_projects(st.session_state.projects_df)
                                st.success("Progress updated!")
                                st.balloons()
                                st.rerun()

with tab2:
    st.header("Start a New Project")
    
    # Load available patterns
    available_patterns = load_patterns()
    
    with st.form("new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name*", placeholder="e.g., Blue Baby Blanket")
            
            if available_patterns:
                pattern_name = st.selectbox("Pattern*", ["Custom/Other"] + available_patterns)
            else:
                pattern_name = st.text_input("Pattern Name*")
            
            start_date = st.date_input("Start Date*", value=datetime.now())
            target_end_date = st.date_input("Target End Date", value=datetime.now() + timedelta(days=30))
            
            status = st.selectbox("Status*", ["Planned", "In Progress", "On Hold"])
            progress = st.slider("Current Progress (%)", 0, 100, 0)
        
        with col2:
            yarn_used = st.text_input("Yarn Used", placeholder="e.g., Drops Cotton Merino - Navy")
            hook_size = st.text_input("Hook Size*", placeholder="e.g., 4.0mm")
            hours_worked = st.number_input("Hours Worked So Far", min_value=0.0, value=0.0, step=0.5)
            difficulty = st.select_slider(
                "Difficulty Rating",
                options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"],
                value="Medium"
            )
            notes = st.text_area("Notes", placeholder="Any notes about this project...")
        
        submitted = st.form_submit_button("🚀 Create Project")
        
        if submitted:
            if project_name and pattern_name and hook_size:
                new_project = {
                    'Project_Name': project_name,
                    'Pattern_Name': pattern_name,
                    'Start_Date': start_date.strftime("%Y-%m-%d"),
                    'Target_End_Date': target_end_date.strftime("%Y-%m-%d"),
                    'Actual_End_Date': None,
                    'Status': status,
                    'Progress_Percent': progress,
                    'Yarn_Used': yarn_used,
                    'Hook_Size': hook_size,
                    'Notes': notes,
                    'Hours_Worked': hours_worked,
                    'Difficulty_Rating': difficulty,
                    'Date_Created': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.session_state.projects_df = pd.concat(
                    [st.session_state.projects_df, pd.DataFrame([new_project])],
                    ignore_index=True
                )
                
                save_projects(st.session_state.projects_df)
                st.success(f"✅ Project '{project_name}' created!")
                st.balloons()
            else:
                st.error("Please fill in all required fields (marked with *)")

with tab3:
    st.header("📊 Project Statistics")
    
    if st.session_state.projects_df.empty:
        st.info("Create projects to see statistics!")
    else:
        df = st.session_state.projects_df
        
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", len(df))
        
        with col2:
            completed = len(df[df['Status'] == 'Completed'])
            st.metric("Completed", completed)
        
        with col3:
            total_hours = df['Hours_Worked'].sum()
            st.metric("Total Hours", f"{total_hours:.1f}h")
        
        with col4:
            if completed > 0:
                avg_time = df[df['Status'] == 'Completed']['Hours_Worked'].mean()
                st.metric("Avg. Time", f"{avg_time:.1f}h")
            else:
                st.metric("Avg. Time", "N/A")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Projects by Status")
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            st.subheader("Most Used Patterns")
            pattern_counts = df['Pattern_Name'].value_counts().head(5)
            st.bar_chart(pattern_counts)
        
        st.divider()
        
        # Recent completions
        completed_projects = df[df['Status'] == 'Completed'].copy()
        
        if not completed_projects.empty:
            st.subheader("🎉 Recently Completed")
            completed_projects = completed_projects.sort_values('Actual_End_Date', ascending=False).head(5)
            
            for _, proj in completed_projects.iterrows():
                st.write(f"✅ **{proj['Project_Name']}** - Completed on {proj['Actual_End_Date']}")
        
        # Longest running WIP
        wip_projects = df[df['Status'] == 'In Progress'].copy()
        
        if not wip_projects.empty:
            st.subheader("⏱️ Longest Running WIP")
            wip_projects['Days_Active'] = (datetime.now() - pd.to_datetime(wip_projects['Start_Date'])).dt.days
            longest_wip = wip_projects.nlargest(3, 'Days_Active')
            
            for _, proj in longest_wip.iterrows():
                st.write(f"🚧 **{proj['Project_Name']}** - {proj['Days_Active']} days ({proj['Progress_Percent']:.0f}% complete)")

# Footer
st.divider()
st.caption("💡 Tip: Update your progress regularly to track how long projects actually take!")
