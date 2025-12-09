"""
Slice 4: Excel Integration
Goal: Write extracted pattern data to Excel database
"""

import pdfplumber
import google.generativeai as genai
import pandas as pd
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def read_pdf(pdf_path):
    """Read a PDF and return all text content."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_pattern_data(pdf_text):
    """Use Gemini to extract all pattern fields from PDF text."""
    
    prompt = f"""
You are a crochet pattern data extraction expert.
Extract ALL of the following information from this crochet pattern.

Return ONLY valid JSON in this exact format:
{{
    "pattern_name": "exact name of the pattern",
    "pattern_structure": "how the pattern is constructed (e.g., 'worked in rounds', 'worked flat', 'top-down', 'granny squares joined')",
    "yarn_weight": "recommended yarn weight (e.g., 'fingering', 'sport', 'DK', 'worsted', 'bulky', 'super bulky')",
    "recommended_yarn_composition": "preferred fiber content (e.g., '100% cotton', 'acrylic blend', 'wool')",
    "hook_size_mm": "crochet hook size in mm (just the number, e.g., '4.0' or '25')",
    "difficulty_level": "skill level (beginner, easy, intermediate, advanced, or expert)",
    "materials_needed": "complete list of materials as a string",
    "recommended_colors": "number of colors or color suggestions",
    "stitches_required": "list of stitches used (e.g., 'sc, dc, hdc, sl st')"
}}

If a field is not found in the pattern, use "Not specified" as the value.

Pattern text:
{pdf_text}
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Parse JSON response
        json_text = response.text.strip()
        # Remove markdown code blocks if present
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            if json_text.startswith('json'):
                json_text = json_text[4:]
        
        data = json.loads(json_text.strip())
        return data
        
    except Exception as e:
        print(f"Error extracting with Gemini: {e}")
        return None

def add_to_excel(pattern_data, source_file, excel_path="pattern_database.xlsx"):
    """Add extracted pattern data to Excel database."""
    
    # Prepare row data
    row_data = {
        'Pattern Name': pattern_data['pattern_name'],
        'Source File': source_file,
        'Pattern Structure': pattern_data['pattern_structure'],
        'Yarn Weight': pattern_data['yarn_weight'],
        'Recommended Composition': pattern_data['recommended_yarn_composition'],
        'Hook Size (mm)': pattern_data['hook_size_mm'],
        'Difficulty Level': pattern_data['difficulty_level'],
        'Materials Needed': pattern_data['materials_needed'],
        'Recommended Colors': pattern_data['recommended_colors'],
        'Stitches Required': pattern_data['stitches_required'],
        'Date Added': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Notes': ''
    }
    
    # Check if file exists
    if os.path.exists(excel_path):
        # Load existing file
        df = pd.read_excel(excel_path)
        # Append new row
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
    else:
        # Create new file
        df = pd.DataFrame([row_data])
    
    # Save to Excel
    df.to_excel(excel_path, index=False)
    return True

if __name__ == "__main__":
    # Test with one PDF
    pdf_folder = "PDFPatterns"
    test_pdf = "Circle Cushion.pdf"
    pdf_path = os.path.join(pdf_folder, test_pdf)
    
    print(f"Testing Excel integration with: {test_pdf}\n")
    
    # Read PDF
    pdf_text = read_pdf(pdf_path)
    if not pdf_text:
        print("❌ Failed to read PDF")
        exit(1)
    
    print(f"✅ PDF read: {len(pdf_text)} characters")
    
    # Extract data
    print("Extracting pattern data...")
    pattern_data = extract_pattern_data(pdf_text)
    
    if not pattern_data:
        print("❌ Extraction failed")
        exit(1)
    
    print("✅ Data extracted")
    
    # Add to Excel
    print("\nAdding to Excel database...")
    success = add_to_excel(pattern_data, test_pdf)
    
    if success:
        print("✅ Data written to pattern_database.xlsx")
        
        # Verify by reading back
        df = pd.read_excel("pattern_database.xlsx")
        print(f"\nDatabase now has {len(df)} pattern(s)")
        print("\nLast entry:")
        print("=" * 60)
        for col in df.columns:
            print(f"{col:25s}: {df.iloc[-1][col]}")
        print("=" * 60)
        print("\n✅ Slice 4 complete: Excel integration works")
    else:
        print("❌ Failed to write to Excel")
