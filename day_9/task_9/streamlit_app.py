import streamlit as st
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="🛍️ AI Product Recommender",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stTextArea textarea {
        min-height: 120px;
    }
    .recommendation-card {
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        background-color: #f8f9fa;
        border-left: 5px solid #4e73df;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .product-card {
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #ffffff;
        border: 1px solid #e3e6f0;
    }
    .price-badge {
        background-color: #1cc88a !important;
        color: white !important;
        font-weight: bold;
    }
    .header-section {
        background: linear-gradient(135deg, #4e73df 0%, #224abe 100%);
        padding: 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .history-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# Header section
st.markdown("""
<div class="header-section">
    <h1 style="color:white; margin:0;">🛍️ AI Product Recommendation System</h1>
    <p style="color:white; margin:0;">Get personalized recommendations with real-time information</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Sidebar
with col1:
    st.sidebar.title("🔍 Filters")
    categories = ["All", "Laptops", "Smartphones", "Headphones", "Tablets"]
    selected_category = st.sidebar.selectbox("Category", categories)
    
    price_range = st.sidebar.slider("Price Range ($)", 0, 2000, (300, 1000))
    
    st.sidebar.divider()
    st.sidebar.title("⚙️ Settings")
    show_details = st.sidebar.checkbox("Show Detailed Results", True)
    enable_web = st.sidebar.checkbox("Enable Web Search", True)
    
    if st.sidebar.button("Clear History", type="primary"):
        st.session_state.history = []
        st.rerun()

# Main content
with col2:
    # Query input
    with st.container():
        query = st.text_area(
            "What products are you looking for?",
            placeholder="Example: 'Best laptops under $1000' or 'Compare iPhone 15 and Samsung Galaxy S24'",
            key="query_input"
        )
        
        # Action buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            search_btn = st.button("🔍 Search", use_container_width=True)
        with btn_col2:
            compare_btn = st.button("⚖️ Compare", use_container_width=True)
        with btn_col3:
            recommend_btn = st.button("💡 Recommend", type="primary", use_container_width=True)

    # Process query if any button is clicked
    if search_btn or compare_btn or recommend_btn:
        if not query.strip():
            st.warning("Please enter a search query")
        else:
            st.session_state.processing = True
            st.session_state.current_query = query
            st.rerun()

    # Processing state
    if st.session_state.processing:
        with st.status("🔍 Processing your request...", expanded=True) as status:
            steps = [
                "Analyzing your query...",
                "Gathering product information...",
                "Checking current prices...",
                "Preparing recommendations..."
            ]
            
            for i, step in enumerate(steps):
                st.write(step)
                time.sleep(0.8)
                if i == len(steps) - 1:
                    try:
                        response = requests.post(
                            "http://localhost:8000/run",
                            json={"query": st.session_state.current_query},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.result = result
                            st.session_state.history.append({
                                "query": st.session_state.current_query,
                                "response": result.get("summary", "No summary available"),
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "products": result.get("rag_data", {}).get("products", []),
                                "web_results": result.get("web_data", {}).get("results", [])
                            })
                            status.update(label="✅ Processing complete!", state="complete")
                        else:
                            st.error(f"Error: {response.text}")
                            status.update(label="❌ Processing failed", state="error")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
                        status.update(label="❌ Processing failed", state="error")
            
            st.session_state.processing = False
            st.rerun()

    # Display results
    if st.session_state.get("result"):
        result = st.session_state.result
        
        # Recommendation summary
        st.markdown(f"""
        <div class="recommendation-card">
            <h3>🌟 Recommendation Summary</h3>
            <p>{result.get('summary', 'No summary available')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Product details
        if show_details and result.get("rag_data", {}).get("products"):
            st.subheader("📦 Recommended Products")
            for product in result["rag_data"]["products"]:
                with st.expander(f"{product['name']} - ${product['price']}", expanded=True):
                    st.markdown(f"""
                    <div class="product-card">
                        <p><strong>Category:</strong> {product['category']}</p>
                        <p><strong>Description:</strong> {product['description']}</p>
                        <h5>Specifications:</h5>
                        <ul>
                            {"".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in product['specs'].items()])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Web results
        if enable_web and result.get("web_data", {}).get("results"):
            st.subheader("🌐 Web Results")
            for i, res in enumerate(result["web_data"]["results"][:3]):
                st.markdown(f"""
                <div class="product-card">
                    <h5><a href="{res.get('url', '#')}" target="_blank">{res.get('title', 'No title')}</a></h5>
                    <p>{res.get('content', 'No description available')}</p>
                    {f"<span class='price-badge' style='padding: 5px 10px; border-radius: 20px; display: inline-block;'>Price: {res['price']}</span>" if res.get('price') else ""}
                </div>
                """, unsafe_allow_html=True)

    # Query history
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Query History")
        
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{entry['timestamp']}: {entry['query']}", expanded=False):
                st.markdown(f"**Response:** {entry['response']}")
                
                if entry.get("products"):
                    st.markdown("**Products:**")
                    cols = st.columns(min(3, len(entry["products"])))
                    for idx, product in enumerate(entry["products"][:3]):
                        with cols[idx % 3]:
                            st.markdown(f"""
                            <div style="padding: 10px; border-radius: 5px; background: #f0f2f6;">
                                <strong>{product['name']}</strong><br>
                                ${product['price']}<br>
                                <small>{product['category']}</small>
                            </div>
                            """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("ℹ️ This is an AI-powered recommendation system. Prices and availability may vary.")