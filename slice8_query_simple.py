"""
Slice 8 Alternative: Query Agent without excessive API calls
Goal: Query patterns directly from database
"""

import chromadb
import pandas as pd

def initialize_chromadb(persist_directory="./chroma_db"):
    """Initialize ChromaDB client and get collection."""
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(name="crochet_patterns")
    return client, collection

def load_excel_data(excel_path="pattern_database.xlsx"):
    """Load pattern data from Excel."""
    return pd.read_excel(excel_path)

def query_by_difficulty(df, difficulty):
    """Find patterns by difficulty level."""
    return df[df['Difficulty Level'].str.contains(difficulty, case=False, na=False)]

def query_by_yarn_weight(df, yarn_weight):
    """Find patterns by yarn weight."""
    return df[df['Yarn Weight'].str.contains(yarn_weight, case=False, na=False)]

def query_by_structure(df, structure):
    """Find patterns by structure."""
    return df[df['Pattern Structure'].str.contains(structure, case=False, na=False)]

def semantic_search(collection, query, n_results=5):
    """Search patterns semantically."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def display_patterns(df, title="Results"):
    """Display pattern results nicely."""
    print(f"\n{title}: {len(df)} patterns found")
    print("=" * 80)
    
    if len(df) == 0:
        print("No patterns match your criteria")
        return
    
    for idx, row in df.iterrows():
        print(f"\n{row['Pattern Name']}")
        print(f"  Difficulty: {row['Difficulty Level']}")
        print(f"  Yarn: {row['Yarn Weight']}")
        print(f"  Hook: {row['Hook Size (mm)']}mm")
        print(f"  Structure: {row['Pattern Structure']}")
        print(f"  Stitches: {row['Stitches Required']}")
    
    print("=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("CROCHET PATTERN QUERY SYSTEM")
    print("=" * 80)
    
    # Initialize
    client, collection = initialize_chromadb()
    df = load_excel_data()
    
    print(f"\n✅ Loaded {len(df)} patterns from database")
    print(f"✅ Vector database has {collection.count()} unique patterns\n")
    
    # Example queries
    print("\n" + "=" * 80)
    print("QUERY 1: Beginner patterns")
    print("=" * 80)
    beginner = query_by_difficulty(df, "beginner")
    display_patterns(beginner, "Beginner Patterns")
    
    print("\n" + "=" * 80)
    print("QUERY 2: Worsted weight patterns")
    print("=" * 80)
    worsted = query_by_yarn_weight(df, "worsted")
    display_patterns(worsted, "Worsted Weight Patterns")
    
    print("\n" + "=" * 80)
    print("QUERY 3: Granny square patterns")
    print("=" * 80)
    granny = query_by_structure(df, "granny square")
    display_patterns(granny, "Granny Square Patterns")
    
    print("\n" + "=" * 80)
    print("QUERY 4: Semantic search - 'amigurumi stuffed animals'")
    print("=" * 80)
    search_results = semantic_search(collection, "amigurumi stuffed animals", n_results=3)
    
    print(f"\nTop 3 matches:")
    print("=" * 80)
    for i, (metadata, distance) in enumerate(zip(
        search_results['metadatas'][0],
        search_results['distances'][0]
    ), 1):
        print(f"\n{i}. {metadata['pattern_name']}")
        print(f"   Difficulty: {metadata['difficulty']}")
        print(f"   Yarn: {metadata['yarn_weight']}")
        print(f"   Structure: {metadata['structure']}")
        print(f"   Similarity: {(1 - distance) * 100:.1f}%")
    
    print("\n" + "=" * 80)
    print("✅ Slice 8 complete: Query system works without excessive API calls")
    print("=" * 80)
