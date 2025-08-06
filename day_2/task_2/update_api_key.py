#!/usr/bin/env python3
"""
Update Google Gemini API Key
"""
import os
from pathlib import Path

def update_api_key():
    """Update the existing API key in .env file"""
    print("🔧 Updating Google Gemini API Key")
    print("=" * 50)
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found. Run setup_env.py first.")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        current_content = f.read().strip()
    
    print(f"Current API key: {current_content}")
    print("\n📝 Enter your new Google Gemini API key:")
    print("(Get it from: https://makersuite.google.com/app/apikey)")
    
    new_api_key = input("API Key: ").strip()
    
    if new_api_key and new_api_key != "your_api_key_here":
        # Update the .env file
        with open(env_file, 'w') as f:
            f.write(f"GOOGLE_API_KEY={new_api_key}\n")
        
        print("✅ API key updated successfully!")
        print("🚀 You can now run: streamlit run app.py")
        return True
    else:
        print("❌ Invalid API key. Please try again.")
        return False

if __name__ == "__main__":
    update_api_key() 