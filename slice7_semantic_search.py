"""
Slice 7: Semantic Search with Embeddings
Goal: Query the vector database to find similar patterns
"""

import chromadb
import pandas as pd

def initialize_chromadb(persist_directory="./chroma_db"):
    """Initialize ChromaDB client and get collection."""
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(name="crochet_patterns")
    return client, collection

def semantic_search(query, collection, n_results=5):
    """Search for patterns similar to the query."""
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return results

def display_search_results(results):
    """Display search results in a readable format."""
    
    if not results['ids'][0]:
        print("No results found")
        return
    
    print(f"Found {len(results['ids'][0])} results:\n")
    
    for i, (doc_id, metadata, distance) in enumerate(zip(
        results['ids'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        print(f"{i}. {metadata['pattern_name']}")
        print(f"   Difficulty: {metadata['difficulty']}")
        print(f"   Yarn: {metadata['yarn_weight']}")
        print(f"   Structure: {metadata['structure']}")
        print(f"   Similarity score: {1 - distance:.3f}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("SEMANTIC SEARCH TEST")
    print("=" * 60)
    print()
    
    # Initialize
    client, collection = initialize_chromadb()
    print(f"✅ Loaded collection with {collection.count()} patterns\n")
    
    # Test queries
    test_queries = [
        "baby blanket pattern",
        "amigurumi stuffed animals",
        "beginner friendly scarf",
        "granny square projects",
        "summer top or tank"
    ]
    
    for query in test_queries:
        print("=" * 60)
        print(f"Query: '{query}'")
        print("=" * 60)
        print()
        
        results = semantic_search(query, collection, n_results=3)
        display_search_results(results)
    
    # Test filtering by metadata
    print("=" * 60)
    print("METADATA FILTERING TEST")
    print("=" * 60)
    print()
    
    # Get all easy patterns
    easy_results = collection.get(
        where={"difficulty": "easy"}
    )
    
    print(f"Found {len(easy_results['ids'])} easy patterns:")
    for metadata in easy_results['metadatas']:
        print(f"  - {metadata['pattern_name']} ({metadata['yarn_weight']})")
    
    print()
    
    # Get worsted weight patterns
    worsted_results = collection.get(
        where={"yarn_weight": "worsted"}
    )
    
    print(f"\nFound {len(worsted_results['ids'])} worsted weight patterns:")
    for metadata in worsted_results['metadatas']:
        print(f"  - {metadata['pattern_name']} ({metadata['difficulty']})")
    
    print()
    print("✅ Slice 7 complete: Semantic search and filtering works")
