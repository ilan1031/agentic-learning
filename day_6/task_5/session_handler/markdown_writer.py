import os

def export_markdown(session_name, history):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{session_name}.md", 'w') as f:
        for turn in history:
            f.write(f"**User:** {turn['user']}\n\n")
            f.write(f"**Agent:** {turn['agent']}\n\n")
