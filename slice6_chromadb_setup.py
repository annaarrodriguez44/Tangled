"""
Slice 6: ChromaDB Setup
Goal: Initialize vector database and store pattern content with metadata
"""

import chromadb
from chromadb.config import Settings
import pdfplumber
import os
import pandas as pd

def initialize_chromadb(persist_directory="./chroma_db"):
    """Initialize ChromaDB client and create/get collection."""
    
    # Create client with persistence
    client = chromadb.PersistentClient(path=persist_directory)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="crochet_patterns",
        metadata={"description": "Crochet pattern embeddings and metadata"}
    )
    
    return client, collection

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

def add_pattern_to_vectordb(collection, pattern_row, pdf_folder="PDFPatterns"):
    """Add a single pattern to the vector database."""
    
    # Read PDF content
    pdf_path = os.path.join(pdf_folder, pattern_row['Source File'])
    pdf_text = read_pdf(pdf_path)
    
    if not pdf_text:
        return False
    
    # Create unique ID
    doc_id = pattern_row['Source File'].replace('.pdf', '').replace(' ', '_')
    
    # Prepare metadata (ChromaDB metadata must be simple types)
    metadata = {
        'pattern_name': str(pattern_row['Pattern Name']),
        'difficulty': str(pattern_row['Difficulty Level']),
        'yarn_weight': str(pattern_row['Yarn Weight']),
        'hook_size': str(pattern_row['Hook Size (mm)']),
        'structure': str(pattern_row['Pattern Structure']),
        'stitches': str(pattern_row['Stitches Required']),
        'source_file': str(pattern_row['Source File'])
    }
    
    # Add to collection
    collection.add(
        documents=[pdf_text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    
    return True

def load_all_patterns_to_vectordb(excel_path="pattern_database.xlsx"):
    """Load all patterns from Excel into vector database."""
    
    # Initialize ChromaDB
    client, collection = initialize_chromadb()
    
    # Load Excel data
    df = pd.read_excel(excel_path)
    
    print(f"Loading {len(df)} patterns into vector database...")
    
    success_count = 0
    failed = []
    
    for idx, row in df.iterrows():
        try:
            if add_pattern_to_vectordb(collection, row):
                success_count += 1
                print(f"✓ {row['Pattern Name']}")
            else:
                failed.append(row['Source File'])
                print(f"✗ {row['Pattern Name']} (failed to read PDF)")
        except Exception as e:
            failed.append(row['Source File'])
            print(f"✗ {row['Pattern Name']} ({str(e)})")
    
    return collection, success_count, failed

if __name__ == "__main__":
    print("=" * 60)
    print("CHROMADB INITIALIZATION")
    print("=" * 60)
    print()
    
    # Load all patterns into vector database
    collection, success, failed = load_all_patterns_to_vectordb()
    
    print()
    print("=" * 60)
    print("LOADING COMPLETE")
    print("=" * 60)
    print(f"\n✅ Successfully loaded: {success} patterns")
    
    if failed:
        print(f"❌ Failed to load: {len(failed)} patterns")
        for f in failed:
            print(f"   - {f}")
    
    # Verify collection
    print(f"\n📊 Vector database stats:")
    print(f"   Total documents: {collection.count()}")
    
    # Test retrieval by ID
    print("\n🔍 Testing retrieval by ID...")
    test_id = "Circle_Cushion"
    result = collection.get(ids=[test_id])
    
    if result['ids']:
        print(f"✅ Successfully retrieved: {result['metadatas'][0]['pattern_name']}")
        print(f"   Difficulty: {result['metadatas'][0]['difficulty']}")
        print(f"   Yarn weight: {result['metadatas'][0]['yarn_weight']}")
        print(f"   Content preview: {result['documents'][0][:200]}...")
    else:
        print(f"❌ Could not retrieve test pattern")
    
    print("\n✅ Slice 6 complete: ChromaDB setup and storage works")
