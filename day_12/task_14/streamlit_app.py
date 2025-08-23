import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Recipe Generator",
    page_icon="🍳",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
    }
    .ingredient-input {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🍳 Recipe Generator</h1>', unsafe_allow_html=True)
st.markdown("### Transform your ingredients into delicious recipes!")

# Input section
st.markdown("### What ingredients do you have?")
ingredients = st.text_area(
    "Enter ingredients (comma separated):",
    placeholder="e.g., chicken, rice, tomatoes, onions...",
    height=100
)

if st.button("Generate Recipe", type="primary"):
    if ingredients:
        with st.spinner("Cooking up your recipe... This may take a minute."):
            try:
                # Send request to Flask backend
                response = requests.post(
                    'http://localhost:5000/generate_recipe',
                    json={'ingredients': ingredients},
                    timeout=120  # Increased timeout for longer processing
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display the recipe
                    st.success("Recipe generated successfully!")
                    st.markdown("### Your Custom Recipe")
                    st.markdown(result['recipe'])
                    
                    # Show where the recipe was saved
                    st.info(f"Recipe saved to: {result['saved_file']}")
                
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
            
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the recipe server. Please make sure the Flask backend is running.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again with fewer ingredients.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    else:
        st.warning("Please enter some ingredients to generate a recipe.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>"
    "Powered by CrewAI, Gemini 1.5, Flask, and Streamlit"
    "</div>",
    unsafe_allow_html=True
)