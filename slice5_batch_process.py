"""
Slice 5: Batch Processing
Goal: Process all PDFs in folder and add to database with progress tracking
"""

import pdfplumber
import google.generativeai as genai
import pandas as pd
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import time

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
{pdf_text[:5000]}
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Parse JSON response
        json_text = response.text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            if json_text.startswith('json'):
                json_text = json_text[4:]
        
        data = json.loads(json_text.strip())
        return data
        
    except Exception as e:
        return None

def add_to_excel(pattern_data, source_file, excel_path="pattern_database.xlsx"):
    """Add extracted pattern data to Excel database."""
    
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
    
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
    else:
        df = pd.DataFrame([row_data])
    
    df.to_excel(excel_path, index=False)
    return True

def batch_process_pdfs(pdf_folder="PDFPatterns", excel_path="pattern_database.xlsx"):
    """Process all PDFs in folder and add to database."""
    
    # Get all PDF files
    all_files = [f for f in os.listdir(pdf_folder) if os.path.isfile(os.path.join(pdf_folder, f))]
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    
    print(f"Found {len(all_files)} files in {pdf_folder}")
    print(f"  - {len(pdf_files)} PDF files")
    print(f"  - {len(all_files) - len(pdf_files)} non-PDF files (will skip)\n")
    
    if not pdf_files:
        print("No PDF files to process")
        return
    
    # Track results
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    # Process each PDF
    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        # Read PDF
        pdf_text = read_pdf(pdf_path)
        if not pdf_text:
            results['failed'].append((pdf_file, "Failed to read PDF"))
            continue
        
        # Extract data
        pattern_data = extract_pattern_data(pdf_text)
        if not pattern_data:
            results['failed'].append((pdf_file, "Failed to extract data"))
            continue
        
        # Add to Excel
        try:
            add_to_excel(pattern_data, pdf_file, excel_path)
            results['success'].append(pdf_file)
        except Exception as e:
            results['failed'].append((pdf_file, str(e)))
        
        # Small delay to avoid API rate limits
        time.sleep(1)
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("BATCH PDF PROCESSING")
    print("=" * 60)
    print()
    
    # Process all PDFs
    results = batch_process_pdfs()
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"\n✅ Successfully processed: {len(results['success'])}")
    for file in results['success']:
        print(f"   - {file}")
    
    if results['failed']:
        print(f"\n❌ Failed to process: {len(results['failed'])}")
        for file, error in results['failed']:
            print(f"   - {file}: {error}")
    
    # Show final database stats
    if os.path.exists("pattern_database.xlsx"):
        df = pd.read_excel("pattern_database.xlsx")
        print(f"\n📊 Database now contains {len(df)} patterns")
        print(f"\nDifficulty breakdown:")
        print(df['Difficulty Level'].value_counts().to_string())
        print(f"\nYarn weight breakdown:")
        print(df['Yarn Weight'].value_counts().to_string())
    
    print("\n✅ Slice 5 complete: Batch processing works")
