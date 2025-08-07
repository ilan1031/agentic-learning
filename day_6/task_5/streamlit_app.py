import streamlit as st
from agents.math_web_agent import run_agent
from session_handler.session_handler import save_session, load_sessions, load_session
from session_handler.markdown_writer import export_markdown

st.set_page_config(layout="wide")
st.sidebar.title("💬 AI Assistant")

if "session_history" not in st.session_state:
    st.session_state.session_history = []

st.sidebar.subheader("Saved Sessions")
saved_sessions = load_sessions()
selected_session = st.sidebar.selectbox("Choose a session to load", ["New"] + saved_sessions)

if selected_session != "New":
    st.session_state.session_history = load_session(selected_session)
    st.sidebar.success(f"Loaded session: {selected_session}")

session_name = st.sidebar.text_input("Session Name", value="session1")

user_input = st.text_input("Enter your question or task")
if st.button("Run Agent"):
    agent_response = run_agent(user_input)
    st.session_state.session_history.append({"user": user_input, "agent": agent_response})

st.subheader("Conversation")
for turn in st.session_state.session_history:
    st.markdown(f"**User:** {turn['user']}")
    st.markdown(f"**Agent:** {turn['agent']}")

if st.button("💾 Save Session"):
    save_session(session_name, st.session_state.session_history)
    st.success("Session saved!")

if st.button("📤 Export to Markdown"):
    export_markdown(session_name, st.session_state.session_history)
    st.success("Markdown exported!")
