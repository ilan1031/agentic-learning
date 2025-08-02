import streamlit as st
import os
from utils.rag import PolicyAssistant
from utils.loader import load_document
import time

# Page configuration
st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize assistant
@st.cache_resource
def init_assistant():
    return PolicyAssistant()

assistant = init_assistant()

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #f5f9fc;
    }
    .stChatFloatingInputContainer {
        background-color: white;
    }
    .policy-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .source-badge {
        background-color: #e6f7ff;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: 0.8em;
        margin-top: 10px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Policy Upload
st.sidebar.title("📂 Policy Management")
uploaded_file = st.sidebar.file_uploader(
    "Upload HR Policy (PDF/DOCX)", 
    type=["pdf", "docx"],
    help="Upload your company HR policy document"
)

# Load policy if uploaded
if uploaded_file:
    # Save to data directory
    if not os.path.exists("data"):
        os.makedirs("data")
    
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load policy into assistant
    with st.spinner("Processing policy document..."):
        assistant.load_policy(file_path)
    st.sidebar.success(f"✅ Policy loaded: {uploaded_file.name}")

# Main Chat Interface
st.title("🤖 HR Policy Assistant")
st.caption("Ask questions about company HR policies")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your HR policy assistant. Upload a policy document to get started."}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if available
        if "sources" in message:
            with st.expander("Sources Used"):
                for source in message["sources"]:
                    st.caption(source["source"])
                    st.markdown(f"```\n{source['content'][:200]}...\n```")

# Accept user input
if prompt := st.chat_input("Ask about HR policies..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Searching policies..."):
            # Retrieve relevant sections
            results = assistant.search(prompt)
            
            # Format context
            context = "\n\n".join([
                f"Source: {r['source']}\nContent: {r['content']}" 
                for r in results
            ])
            
            # Generate response
            response = assistant.generate_response(prompt, context)
            
        # Stream the response
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        # Show sources
        with st.expander("Policy References"):
            for r in results:
                st.caption(r["source"])
                st.markdown(f"```\n{r['content'][:200]}...\n```")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "sources": results
    })