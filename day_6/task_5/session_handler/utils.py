def count_tokens(text):
    return len(text.split())

def clean_text(text):
    return text.replace('\n', ' ').strip()
