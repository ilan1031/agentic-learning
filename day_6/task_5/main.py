import streamlit as st
from session_handler.session_handler import save_session, load_session
from session_handler.markdown_writer import export_markdown
from agent_executor import run_agent

st.set_page_config(layout="wide", page_title="🧠 AI Research Agent")

# Sidebar: session controls
st.sidebar.title("🧠 Sessions")
session_id = st.sidebar.text_input("Enter session name", value="default")
if st.sidebar.button("Start New Session"):
    st.session_state["messages"] = []
    session_id = session_id.strip() or "default"

if "messages" not in st.session_state:
    try:
        st.session_state["messages"] = load_session(session_id)
    except Exception:
        st.session_state["messages"] = []

# Main Interface
st.title("LangChain Research Agent")
user_input = st.text_input("Ask a question")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = run_agent(user_input)
    st.session_state.messages.append({"role": "ai", "content": response})
    save_session(session_id, st.session_state.messages)

# Chat History Display
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Export Markdown
if st.button("Export Session to Markdown"):
    export_markdown(session_id, st.session_state.messages)
    st.success("Markdown saved to output/{session_id}.md")
