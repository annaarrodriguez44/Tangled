"""
Batch Pattern Processor
Process multiple PDF patterns and add them to the database
"""

import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)
import pdfplumber
from datetime import datetime

st.set_page_config(
    page_title="Add Patterns - Tangled",
    page_icon="📚",
    layout="wide"
)

# Load environment variables
load_dotenv()

# File paths
PATTERNS_DB = "pattern_database.xlsx"
PDF_FOLDER = "PDFPatterns"

# Initialize Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def load_patterns_db():
    """Load existing patterns database"""
    if os.path.exists(PATTERNS_DB):
        try:
            return pd.read_excel(PATTERNS_DB)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def get_pdf_files():
    """Get list of PDF files in PDFPatterns folder"""
    if os.path.exists(PDF_FOLDER):
        files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
        return sorted(files)
    return []

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages[:5]:  # First 5 pages
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_pattern_info_with_gemini(pdf_text, pattern_filename):
    """Extract structured information using Gemini API"""
    prompt = f"""
You are analyzing a crochet pattern document. Extract the following information in JSON format:

Pattern filename: {pattern_filename}

Text from pattern:
{pdf_text[:3000]}

Extract these fields (use "Unknown" if not found):
- Pattern Name (the title/name of the pattern)
- Pattern Structure (e.g., "worked in rounds", "worked flat", "top-down")
- Yarn Weight (e.g., "fingering", "sport", "DK", "worsted", "bulky")
- Recommended Yarn Composition (e.g., "100% cotton", "wool blend")
- Hook Size (e.g., "4.0mm", "G/6")
- Difficulty Level (beginner, easy, intermediate, advanced, expert)
- Materials Needed (list of materials)
- Recommended Colors (number of colors or color names)
- Stitches Required (list of stitches used, e.g., "sc, dc, hdc")

Return ONLY valid JSON with these exact field names.
"""
    
    try:
        import time
        import json
        
        # Try with retry logic for rate limits
        max_retries = 3
        retry_delay = 15  # seconds
        
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                # Parse JSON from response
                response_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.startswith('```'):
                    response_text = response_text[3:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                return json.loads(response_text.strip())
            
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                raise e
    
    except Exception as e:
        return {"error": str(e)}

# Header
st.title("📚 Batch Pattern Processor")
st.markdown("Add multiple crochet patterns to your database from PDFs")

# Load existing database
patterns_df = load_patterns_db()
pdf_files = get_pdf_files()

# Statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Patterns in Database", len(patterns_df) if not patterns_df.empty else 0)

with col2:
    st.metric("PDF Files Found", len(pdf_files))

with col3:
    if not patterns_df.empty:
        processed_names = patterns_df['Pattern Name'].tolist()
        unprocessed = [f for f in pdf_files if not any(name.lower() in f.lower() for name in processed_names)]
        st.metric("Unprocessed PDFs", len(unprocessed))
    else:
        st.metric("Unprocessed PDFs", len(pdf_files))

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Preview PDFs", "⚡ Batch Process", "📊 Database View"])

with tab1:
    st.header("Preview PDF Patterns")
    
    if not pdf_files:
        st.warning(f"No PDF files found in {PDF_FOLDER} folder")
    else:
        selected_pdf = st.selectbox("Select PDF to preview", pdf_files)
        
        if selected_pdf:
            pdf_path = os.path.join(PDF_FOLDER, selected_pdf)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("PDF Information")
                st.write(f"**Filename:** {selected_pdf}")
                st.write(f"**Size:** {os.path.getsize(pdf_path) / 1024:.2f} KB")
                
                if st.button("📄 Extract Text Preview"):
                    with st.spinner("Extracting text..."):
                        text = extract_text_from_pdf(pdf_path)
                        st.text_area("Extracted Text (first 1000 chars)", text[:1000], height=300)
            
            with col2:
                st.subheader("AI Extraction Preview")
                
                if st.button("🤖 Extract Pattern Info with AI", type="primary"):
                    with st.spinner("Analyzing pattern with Gemini..."):
                        text = extract_text_from_pdf(pdf_path)
                        info = extract_pattern_info_with_gemini(text, selected_pdf)
                        
                        if "error" in info:
                            st.error(f"Error: {info['error']}")
                        else:
                            st.success("✅ Information extracted!")
                            st.json(info)

with tab2:
    st.header("Batch Process Patterns")
    
    if not pdf_files:
        st.warning("No PDF files to process")
    else:
        # Get unprocessed files
        if not patterns_df.empty:
            processed_names = patterns_df['Pattern Name'].tolist()
            unprocessed_files = [f for f in pdf_files 
                               if not any(name.lower() in f.lower() for name in processed_names)]
        else:
            unprocessed_files = pdf_files
        
        if not unprocessed_files:
            st.success("✅ All PDFs have been processed!")
            st.info("If you want to reprocess a pattern, delete it from the database first.")
        else:
            st.write(f"**{len(unprocessed_files)} unprocessed PDF(s) found:**")
            
            for pdf_file in unprocessed_files:
                st.write(f"• {pdf_file}")
            
            st.divider()
            
            process_option = st.radio(
                "Processing mode",
                ["Process All Unprocessed", "Select Specific Files"],
                help="Choose how many files to process"
            )
            
            if process_option == "Select Specific Files":
                selected_files = st.multiselect(
                    "Select files to process",
                    unprocessed_files,
                    default=[]
                )
            else:
                selected_files = unprocessed_files
            
            if selected_files:
                st.info(f"📋 Ready to process {len(selected_files)} file(s)")
                
                if st.button("🚀 Start Processing", type="primary"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    errors = []
                    
                    for idx, pdf_file in enumerate(selected_files):
                        status_text.text(f"Processing {idx+1}/{len(selected_files)}: {pdf_file}")
                        
                        try:
                            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
                            
                            # Extract text
                            text = extract_text_from_pdf(pdf_path)
                            
                            # Extract info with Gemini
                            info = extract_pattern_info_with_gemini(text, pdf_file)
                            
                            if "error" not in info:
                                # Add to results
                                info['PDF_Source'] = pdf_file
                                info['Date_Added'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                results.append(info)
                            else:
                                errors.append(f"{pdf_file}: {info['error']}")
                        
                        except Exception as e:
                            errors.append(f"{pdf_file}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(selected_files))
                    
                    status_text.text("✅ Processing complete!")
                    
                    # Display results
                    if results:
                        st.success(f"✅ Successfully processed {len(results)} pattern(s)!")
                        
                        # Add to database
                        new_patterns_df = pd.DataFrame(results)
                        
                        if patterns_df.empty:
                            updated_df = new_patterns_df
                        else:
                            updated_df = pd.concat([patterns_df, new_patterns_df], ignore_index=True)
                        
                        # Save to Excel
                        updated_df.to_excel(PATTERNS_DB, index=False)
                        st.balloons()
                        
                        # Show preview
                        st.subheader("Newly Added Patterns:")
                        st.dataframe(new_patterns_df[['Pattern Name', 'Difficulty Level', 'Yarn Weight', 'Hook Size']], 
                                   hide_index=True, use_container_width=True)
                    
                    if errors:
                        st.warning(f"⚠️ {len(errors)} error(s) occurred:")
                        for error in errors:
                            st.error(error)

with tab3:
    st.header("Pattern Database View")
    
    if patterns_df.empty:
        st.info("No patterns in database yet. Process some PDFs to add patterns!")
    else:
        # Search and filter
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search = st.text_input("🔍 Search patterns", placeholder="Search by name, difficulty, or yarn...")
        
        with col2:
            sort_by = st.selectbox("Sort by", ["Pattern Name", "Difficulty Level", "Date Added"])
        
        # Apply filters
        display_df = patterns_df.copy()
        
        if search:
            mask = display_df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
            display_df = display_df[mask]
        
        if 'Date Added' in display_df.columns:
            display_df = display_df.sort_values(sort_by if sort_by != "Date Added" else "Date_Added", 
                                              ascending=(sort_by == "Pattern Name"))
        
        st.write(f"**Showing {len(display_df)} of {len(patterns_df)} patterns**")
        
        # Display table
        display_columns = ['Pattern Name', 'Difficulty Level', 'Yarn Weight', 
                          'Hook Size', 'Pattern Structure']
        
        available_columns = [col for col in display_columns if col in display_df.columns]
        st.dataframe(display_df[available_columns], hide_index=True, use_container_width=True)
        
        # Export option
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = display_df.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                "patterns_database.csv",
                "text/csv"
            )
        
        with col2:
            if st.button("🔄 Reload Database"):
                st.cache_data.clear()
                st.rerun()
        
        with col3:
            if st.button("⚠️ Clear All Patterns", type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    os.remove(PATTERNS_DB)
                    st.success("Database cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm deletion")

# Footer
st.divider()
st.caption("💡 Tip: Process patterns in small batches to monitor quality and make adjustments if needed!")
