"""
Slice 2: Extract Pattern Name Using Gemini
Goal: Send PDF text to Gemini and extract just the pattern name as JSON
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

def extract_pattern_name(pdf_text):
    """Use Gemini to extract pattern name from PDF text."""
    
    prompt = f"""
You are a crochet pattern data extraction expert. 
Extract the pattern name from this crochet pattern.

Return ONLY valid JSON in this exact format:
{{
    "pattern_name": "exact name of the pattern"
}}

Pattern text:
{pdf_text[:3000]}
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Parse JSON response
        json_text = response.text.strip()
        # Remove markdown code blocks if present
        if json_text.startswith('```'):
            json_text = json_text.split('```')[1]
            if json_text.startswith('json'):
                json_text = json_text[4:]
        
        data = json.loads(json_text.strip())
        return data
        
    except Exception as e:
        print(f"Error extracting with Gemini: {e}")
        print(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
        return None

if __name__ == "__main__":
    # Test with one PDF
    pdf_folder = "PDFPatterns"
    test_pdf = "Circle Cushion.pdf"
    pdf_path = os.path.join(pdf_folder, test_pdf)
    
    print(f"Testing extraction with: {test_pdf}\n")
    
    # Read PDF
    pdf_text = read_pdf(pdf_path)
    if not pdf_text:
        print("❌ Failed to read PDF")
        exit(1)
    
    print(f"✅ PDF read: {len(pdf_text)} characters\n")
    
    # Extract pattern name
    print("Sending to Gemini for extraction...")
    result = extract_pattern_name(pdf_text)
    
    if result:
        print("\n✅ Extraction successful!")
        print(json.dumps(result, indent=2))
        print("\n✅ Slice 2 complete: Gemini extraction works")
    else:
        print("❌ Extraction failed")
