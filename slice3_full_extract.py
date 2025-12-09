"""
Slice 3: Extract All Pattern Fields Using Gemini
Goal: Extract all 9 fields from the pattern as structured JSON
"""

import pdfplumber
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

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
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response:\n{response.text}")
        return None
    except Exception as e:
        print(f"Error extracting with Gemini: {e}")
        return None

if __name__ == "__main__":
    # Test with one PDF
    pdf_folder = "PDFPatterns"
    test_pdf = "Circle Cushion.pdf"
    pdf_path = os.path.join(pdf_folder, test_pdf)
    
    print(f"Testing full extraction with: {test_pdf}\n")
    
    # Read PDF
    pdf_text = read_pdf(pdf_path)
    if not pdf_text:
        print("❌ Failed to read PDF")
        exit(1)
    
    print(f"✅ PDF read: {len(pdf_text)} characters\n")
    
    # Extract all fields
    print("Sending to Gemini for full extraction...")
    result = extract_pattern_data(pdf_text)
    
    if result:
        print("\n✅ Extraction successful!\n")
        print("=" * 60)
        for key, value in result.items():
            print(f"{key:30s}: {value}")
        print("=" * 60)
        print("\n✅ Slice 3 complete: All fields extracted")
    else:
        print("❌ Extraction failed")
