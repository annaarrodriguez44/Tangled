"""
Project Photo Gallery
Upload and showcase your finished crochet projects
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)
import io

st.set_page_config(
    page_title="Photo Gallery - Tangled",
    page_icon="📸",
    layout="wide"
)

# File paths
GALLERY_FILE = "project_gallery.xlsx"
PHOTOS_DIR = "project_photos"
PATTERNS_FILE = "pattern_database.xlsx"

# Ensure photos directory exists
os.makedirs(PHOTOS_DIR, exist_ok=True)

def load_gallery():
    """Load photo gallery metadata"""
    if os.path.exists(GALLERY_FILE):
        try:
            return pd.read_excel(GALLERY_FILE)
        except:
            return create_empty_gallery()
    else:
        return create_empty_gallery()

def create_empty_gallery():
    """Create empty gallery DataFrame"""
    return pd.DataFrame(columns=[
        'Photo_ID', 'Pattern_Name', 'Project_Name', 'Photo_Filename',
        'Upload_Date', 'Completion_Date', 'Yarn_Used', 'Hook_Size',
        'Caption', 'Tags', 'Rating'
    ])

def save_gallery(df):
    """Save gallery to Excel file"""
    df.to_excel(GALLERY_FILE, index=False)

def load_patterns():
    """Load available patterns"""
    if os.path.exists(PATTERNS_FILE):
        try:
            df = pd.read_excel(PATTERNS_FILE)
            return df['Pattern_Name'].dropna().unique().tolist()
        except:
            return []
    return []

def save_uploaded_photo(uploaded_file, photo_id):
    """Save uploaded photo to disk"""
    try:
        # Read image
        image = Image.open(uploaded_file)
        
        # Resize if too large (max 1200px width)
        max_width = 1200
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save as JPEG
        filename = f"{photo_id}.jpg"
        filepath = os.path.join(PHOTOS_DIR, filename)
        image.convert('RGB').save(filepath, 'JPEG', quality=85)
        
        return filename
    except Exception as e:
        st.error(f"Error saving photo: {e}")
        return None

def load_photo(filename):
    """Load photo from disk"""
    try:
        filepath = os.path.join(PHOTOS_DIR, filename)
        if os.path.exists(filepath):
            return Image.open(filepath)
    except:
        pass
    return None

# Initialize session state
if 'gallery_df' not in st.session_state:
    st.session_state.gallery_df = load_gallery()

# Header
st.title("📸 Project Photo Gallery")
st.markdown("Showcase your beautiful finished projects!")

# Tabs
tab1, tab2, tab3 = st.tabs(["🖼️ Gallery", "📤 Upload Photo", "🔍 Search"])

with tab1:
    st.header("Your Project Gallery")
    
    if st.session_state.gallery_df.empty:
        st.info("No photos yet. Upload your first finished project in the 'Upload Photo' tab!")
    else:
        # Filter options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["Newest First", "Oldest First", "Highest Rated", "Pattern Name"]
            )
        
        with col2:
            view_mode = st.selectbox("View", ["Grid", "List"])
        
        # Sort gallery
        df = st.session_state.gallery_df.copy()
        
        if sort_by == "Newest First":
            df = df.sort_values('Upload_Date', ascending=False)
        elif sort_by == "Oldest First":
            df = df.sort_values('Upload_Date', ascending=True)
        elif sort_by == "Highest Rated":
            df = df.sort_values('Rating', ascending=False)
        elif sort_by == "Pattern Name":
            df = df.sort_values('Pattern_Name')
        
        # Display gallery
        if view_mode == "Grid":
            # Grid view (3 columns)
            cols_per_row = 3
            for i in range(0, len(df), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for col_idx, col in enumerate(cols):
                    row_idx = i + col_idx
                    if row_idx < len(df):
                        row = df.iloc[row_idx]
                        
                        with col:
                            # Load and display photo
                            photo = load_photo(row['Photo_Filename'])
                            
                            if photo:
                                st.image(photo, use_container_width=True)
                            else:
                                st.warning("Photo not found")
                            
                            # Project details
                            st.markdown(f"**{row['Project_Name']}**")
                            st.caption(f"Pattern: {row['Pattern_Name']}")
                            
                            # Rating
                            if pd.notna(row['Rating']) and row['Rating'] > 0:
                                stars = "⭐" * int(row['Rating'])
                                st.caption(stars)
                            
                            # View details button
                            if st.button("👁️ View Details", key=f"view_{row_idx}"):
                                st.session_state.selected_photo = row_idx
                                st.rerun()
        
        else:
            # List view
            for idx, row in df.iterrows():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    photo = load_photo(row['Photo_Filename'])
                    if photo:
                        st.image(photo, use_container_width=True)
                    else:
                        st.warning("Photo not found")
                
                with col2:
                    st.subheader(row['Project_Name'])
                    st.write(f"**Pattern:** {row['Pattern_Name']}")
                    st.write(f"**Completed:** {row['Completion_Date']}")
                    
                    if pd.notna(row['Rating']) and row['Rating'] > 0:
                        stars = "⭐" * int(row['Rating'])
                        st.write(f"**Rating:** {stars}")
                    
                    if pd.notna(row['Caption']):
                        st.write(f"*{row['Caption']}*")
                    
                    if pd.notna(row['Yarn_Used']):
                        st.caption(f"Yarn: {row['Yarn_Used']}")
                    
                    if pd.notna(row['Tags']):
                        tags = row['Tags'].split(',')
                        tag_str = " ".join([f"`{tag.strip()}`" for tag in tags])
                        st.markdown(tag_str)
                
                st.divider()

with tab2:
    st.header("Upload New Project Photo")
    
    available_patterns = load_patterns()
    
    with st.form("upload_photo_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a photo",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a photo of your finished project"
            )
            
            project_name = st.text_input("Project Name*", placeholder="e.g., My Cozy Blanket")
            
            if available_patterns:
                pattern_name = st.selectbox("Pattern Used*", ["Custom/Other"] + available_patterns)
            else:
                pattern_name = st.text_input("Pattern Name*")
            
            completion_date = st.date_input("Completion Date", value=datetime.now())
        
        with col2:
            yarn_used = st.text_input("Yarn Used", placeholder="e.g., Drops Cotton - Navy")
            hook_size = st.text_input("Hook Size", placeholder="e.g., 4.0mm")
            rating = st.slider("How happy are you with the result?", 1, 5, 5)
            caption = st.text_area("Caption", placeholder="Tell us about this project...")
            tags = st.text_input("Tags (comma-separated)", placeholder="e.g., blanket, blue, gift")
        
        submitted = st.form_submit_button("📤 Upload Photo")
        
        if submitted:
            if uploaded_file and project_name and pattern_name:
                # Generate unique photo ID
                photo_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save photo
                filename = save_uploaded_photo(uploaded_file, photo_id)
                
                if filename:
                    # Add to gallery
                    new_entry = {
                        'Photo_ID': photo_id,
                        'Pattern_Name': pattern_name,
                        'Project_Name': project_name,
                        'Photo_Filename': filename,
                        'Upload_Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'Completion_Date': completion_date.strftime("%Y-%m-%d"),
                        'Yarn_Used': yarn_used,
                        'Hook_Size': hook_size,
                        'Caption': caption,
                        'Tags': tags,
                        'Rating': rating
                    }
                    
                    st.session_state.gallery_df = pd.concat(
                        [st.session_state.gallery_df, pd.DataFrame([new_entry])],
                        ignore_index=True
                    )
                    
                    save_gallery(st.session_state.gallery_df)
                    st.success("✅ Photo uploaded successfully!")
                    st.balloons()
                else:
                    st.error("Failed to save photo. Please try again.")
            else:
                st.error("Please fill in all required fields and upload a photo")

with tab3:
    st.header("🔍 Search Gallery")
    
    if st.session_state.gallery_df.empty:
        st.info("No photos to search yet.")
    else:
        search_term = st.text_input("Search by project name, pattern, or tags", placeholder="Type to search...")
        
        if search_term:
            df = st.session_state.gallery_df.copy()
            
            # Search in multiple fields
            mask = (
                df['Project_Name'].str.contains(search_term, case=False, na=False) |
                df['Pattern_Name'].str.contains(search_term, case=False, na=False) |
                df['Tags'].str.contains(search_term, case=False, na=False) |
                df['Caption'].str.contains(search_term, case=False, na=False)
            )
            
            results = df[mask]
            
            if results.empty:
                st.warning(f"No results found for '{search_term}'")
            else:
                st.success(f"Found {len(results)} photo(s)")
                
                # Display results
                for idx, row in results.iterrows():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        photo = load_photo(row['Photo_Filename'])
                        if photo:
                            st.image(photo, use_container_width=True)
                    
                    with col2:
                        st.subheader(row['Project_Name'])
                        st.write(f"**Pattern:** {row['Pattern_Name']}")
                        st.write(f"**Completed:** {row['Completion_Date']}")
                        
                        if pd.notna(row['Caption']):
                            st.write(f"*{row['Caption']}*")
                    
                    st.divider()
        else:
            # Show recent photos
            st.subheader("Recently Added")
            recent = st.session_state.gallery_df.sort_values('Upload_Date', ascending=False).head(6)
            
            cols = st.columns(3)
            for idx, (_, row) in enumerate(recent.iterrows()):
                with cols[idx % 3]:
                    photo = load_photo(row['Photo_Filename'])
                    if photo:
                        st.image(photo, use_container_width=True)
                        st.caption(row['Project_Name'])

# Photo detail modal (if selected)
if 'selected_photo' in st.session_state:
    row = st.session_state.gallery_df.iloc[st.session_state.selected_photo]
    
    with st.expander("📷 Photo Details", expanded=True):
        photo = load_photo(row['Photo_Filename'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if photo:
                st.image(photo, use_container_width=True)
        
        with col2:
            st.subheader(row['Project_Name'])
            st.write(f"**Pattern:** {row['Pattern_Name']}")
            st.write(f"**Completed:** {row['Completion_Date']}")
            st.write(f"**Uploaded:** {row['Upload_Date']}")
            
            if pd.notna(row['Rating']):
                stars = "⭐" * int(row['Rating'])
                st.write(f"**Rating:** {stars}")
            
            if pd.notna(row['Yarn_Used']):
                st.write(f"**Yarn:** {row['Yarn_Used']}")
            
            if pd.notna(row['Hook_Size']):
                st.write(f"**Hook:** {row['Hook_Size']}")
            
            if pd.notna(row['Caption']):
                st.write(f"\n*{row['Caption']}*")
            
            if pd.notna(row['Tags']):
                st.write(f"\n**Tags:** {row['Tags']}")
            
            if st.button("❌ Close"):
                del st.session_state.selected_photo
                st.rerun()

# Footer
st.divider()
st.caption("📸 Tip: Take photos in good lighting to showcase your beautiful work!")
