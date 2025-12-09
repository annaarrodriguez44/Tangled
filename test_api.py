"""
Test script to verify Gemini API key is working correctly.
Run this after adding your API key to .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

# Check if key exists
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("Please add your API key to the .env file:")
    print("GEMINI_API_KEY=your_key_here")
    exit(1)

# Check if key looks valid (basic format check)
if not api_key.startswith('AIza'):
    print("⚠️  WARNING: API key doesn't look like a valid Gemini key")
    print("Gemini keys typically start with 'AIza'")
    print(f"Your key starts with: {api_key[:10]}...")

print("✅ API key found in .env file")
print(f"Key preview: {api_key[:10]}...{api_key[-4:]}")

# Try to import and initialize Gemini
try:
    import google.generativeai as genai
    print("✅ google.generativeai library imported successfully")
    
    # Configure the API
    genai.configure(api_key=api_key)
    print("✅ API configured successfully")
    
    # List available models
    print("\nAvailable models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    # Try a simple test with the correct model name
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'API test successful' if you can read this.")
    
    print("\n✅ API CONNECTION SUCCESSFUL!")
    print(f"Test response: {response.text}")
    
except ImportError as e:
    print("❌ ERROR: google.generativeai not installed")
    print("Run: pip install google-generativeai")
    
except Exception as e:
    print(f"❌ ERROR: API test failed")
    print(f"Error: {str(e)}")
    print("\nPossible issues:")
    print("- Invalid API key")
    print("- No internet connection")
    print("- API quota exceeded")
    print("- API key not activated yet")
