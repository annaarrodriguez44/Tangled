"""
Slice 1: Basic PDF Reading
Goal: Read one PDF and extract raw text to understand structure
"""

import pdfplumber
import os

def read_pdf(pdf_path):
    """Read a PDF and return all text content."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"PDF has {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- PAGE {i} ---\n{page_text}"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    # Test with one PDF
    pdf_folder = "PDFPatterns"
    test_pdf = "Circle Cushion.pdf"
    pdf_path = os.path.join(pdf_folder, test_pdf)
    
    print(f"Testing with: {test_pdf}\n")
    
    text = read_pdf(pdf_path)
    
    if text:
        print("\n=== EXTRACTED TEXT ===")
        print(text[:2000])  # First 2000 characters
        print("\n...")
        print(f"\nTotal characters extracted: {len(text)}")
        print("\n✅ Slice 1 complete: PDF reading works")
    else:
        print("❌ Failed to extract text")
