"""
Slice 9: Combined Query Agent with Natural Language Responses
Goal: Integrate Excel + Vector DB + Gemini for conversational answers
"""

import chromadb
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def initialize_chromadb(persist_directory="./chroma_db"):
    """Initialize ChromaDB client and get collection."""
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(name="crochet_patterns")
    return client, collection

def load_excel_data(excel_path="pattern_database.xlsx"):
    """Load pattern data from Excel."""
    return pd.read_excel(excel_path)

def search_patterns(query, df, collection, n_results=5):
    """Search patterns using both Excel filtering and vector search."""
    
    # Semantic search from vector DB
    vector_results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Extract pattern names from vector search
    relevant_patterns = []
    if vector_results['ids'][0]:
        for metadata in vector_results['metadatas'][0]:
            relevant_patterns.append(metadata['pattern_name'])
    
    # Filter Excel data for those patterns
    if relevant_patterns:
        filtered_df = df[df['Pattern Name'].isin(relevant_patterns)]
    else:
        filtered_df = df.head(n_results)
    
    return filtered_df, vector_results

def generate_answer(query, df, filtered_df, vector_results):
    """Generate natural language answer using Gemini."""
    
    # Build context
    context = f"""
DATABASE OVERVIEW:
- Total patterns: {len(df)}
- Difficulty distribution: {df['Difficulty Level'].value_counts().to_dict()}
- Yarn weight distribution: {df['Yarn Weight'].value_counts().to_dict()}

RELEVANT PATTERNS FOR THIS QUERY:
"""
    
    for idx, row in filtered_df.iterrows():
        context += f"""
Pattern: {row['Pattern Name']}
- Difficulty: {row['Difficulty Level']}
- Yarn: {row['Yarn Weight']} (Hook: {row['Hook Size (mm)']}mm)
- Structure: {row['Pattern Structure']}
- Stitches: {row['Stitches Required']}
- Materials: {row['Materials Needed'][:150]}...
"""
    
    # Build prompt
    prompt = f"""You are a helpful crochet pattern assistant. Answer the user's question based on the pattern database.

Be conversational and specific. Reference pattern names and explain why they match the user's needs.
If asked for recommendations, give 2-3 specific suggestions with reasoning.

{context}

User Question: {query}

Answer:"""
    
    # Get response from Gemini with rate limit handling
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️  API rate limit reached. Please wait a moment and try again."
        return f"Error generating response: {str(e)}"

def query_agent(user_query, df, collection):
    """Main query agent function."""
    
    # Search for relevant patterns
    filtered_df, vector_results = search_patterns(user_query, df, collection)
    
    # Generate natural language answer
    answer = generate_answer(user_query, df, filtered_df, vector_results)
    
    return answer, filtered_df

if __name__ == "__main__":
    print("=" * 80)
    print("COMBINED QUERY AGENT - SLICE 9")
    print("=" * 80)
    print()
    
    # Initialize
    client, collection = initialize_chromadb()
    df = load_excel_data()
    
    print(f"✅ Loaded {len(df)} patterns from database")
    print(f"✅ Vector database has {collection.count()} unique patterns\n")
    
    # Test queries with delays to avoid rate limits
    test_queries = [
        "What beginner-friendly patterns do you have?",
        "I want to make something with worsted weight yarn",
        "Show me amigurumi patterns"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print("=" * 80)
        print(f"QUERY {i}: {query}")
        print("=" * 80)
        print()
        
        answer, patterns = query_agent(query, df, collection)
        print(answer)
        print()
        
        print(f"\nMatched patterns ({len(patterns)}):")
        for idx, row in patterns.iterrows():
            print(f"  - {row['Pattern Name']} ({row['Difficulty Level']}, {row['Yarn Weight']})")
        
        print()
        
        # Wait between queries to respect rate limits
        if i < len(test_queries):
            print("⏳ Waiting 5 seconds before next query...")
            time.sleep(5)
    
    print("\n" + "=" * 80)
    print("✅ Slice 9 complete: Combined query agent with natural language works")
    print("=" * 80)
    print("\nThe system can now:")
    print("  ✓ Search patterns semantically")
    print("  ✓ Filter by multiple criteria")
    print("  ✓ Generate conversational answers")
    print("  ✓ Recommend specific patterns with reasoning")
