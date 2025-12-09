"""
Slice 8: Basic Query Agent
Goal: Natural language interface to query pattern database
"""

import chromadb
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

def query_patterns(user_question, df, collection):
    """Answer user questions about patterns using database and LLM."""
    
    # Get relevant patterns from vector search
    search_results = collection.query(
        query_texts=[user_question],
        n_results=5
    )
    
    # Build context from search results
    context_patterns = []
    if search_results['ids'][0]:
        for metadata in search_results['metadatas'][0]:
            context_patterns.append(f"- {metadata['pattern_name']}: {metadata['difficulty']} difficulty, {metadata['yarn_weight']} yarn, {metadata['structure']}")
    
    # Get database summary
    db_summary = f"""
Available patterns in database: {len(df)}
Difficulty levels: {df['Difficulty Level'].value_counts().to_dict()}
Yarn weights: {df['Yarn Weight'].value_counts().to_dict()}
"""
    
    # Build prompt for Gemini
    prompt = f"""
You are a helpful crochet pattern assistant. Answer the user's question about crochet patterns based on the database.

Database Summary:
{db_summary}

Most relevant patterns for this query:
{chr(10).join(context_patterns)}

Full pattern database (first 10 entries):
{df.head(10).to_string()}

User Question: {user_question}

Provide a helpful, conversational answer. Include specific pattern names and details when relevant.
If the user asks for recommendations, explain why each pattern is suitable.
"""
    
    # Get response from Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    
    return response.text

def interactive_query_mode():
    """Interactive mode for asking questions."""
    
    print("=" * 60)
    print("CROCHET PATTERN QUERY AGENT")
    print("=" * 60)
    print()
    
    # Initialize
    client, collection = initialize_chromadb()
    df = load_excel_data()
    
    print(f"✅ Loaded {len(df)} patterns from database")
    print(f"✅ Loaded {collection.count()} patterns in vector database")
    print()
    print("Ask me anything about your crochet patterns!")
    print("(Type 'quit' to exit)")
    print()
    
    while True:
        print("-" * 60)
        user_question = input("\nYour question: ").strip()
        
        if user_question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_question:
            continue
        
        print("\nThinking...\n")
        
        try:
            answer = query_patterns(user_question, df, collection)
            print(answer)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Test with predefined questions
    print("=" * 60)
    print("QUERY AGENT TEST")
    print("=" * 60)
    print()
    
    # Initialize
    client, collection = initialize_chromadb()
    df = load_excel_data()
    
    print(f"✅ Loaded {len(df)} patterns\n")
    
    # Test questions
    test_questions = [
        "What beginner patterns do you have?",
        "Show me patterns that use worsted weight yarn",
        "What amigurumi patterns are available?",
        "Do you have any tank top patterns?"
    ]
    
    for question in test_questions:
        print("=" * 60)
        print(f"Q: {question}")
        print("=" * 60)
        
        answer = query_patterns(question, df, collection)
        print(answer)
        print()
    
    print("\n✅ Slice 8 complete: Query agent works")
    print("\nStarting interactive mode...\n")
    
    # Start interactive mode
    interactive_query_mode()
