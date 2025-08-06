#!/usr/bin/env python3
"""
Setup script for Google Gemini API Key
"""
import os
from pathlib import Path

def setup_env():
    """Guide user through setting up the .env file"""
    print("🔧 Setting up Google Gemini API Key")
    print("=" * 50)
    
    # Check if .env exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_gemini_api_key_here" in content:
                print("⚠️  Please update your API key in the .env file")
            else:
                print("✅ API key appears to be configured")
    else:
        print("📝 Creating .env file...")
        api_key = input("Enter your Google Gemini API key: ").strip()
        
        if api_key and api_key != "your_gemini_api_key_here":
            with open(env_file, 'w') as f:
                f.write(f"GOOGLE_API_KEY={api_key}\n")
            print("✅ .env file created successfully!")
        else:
            print("❌ Invalid API key. Please run this script again with a valid key.")
            return False
    
    print("\n🚀 You can now run: streamlit run app.py")
    return True

if __name__ == "__main__":
    setup_env() 