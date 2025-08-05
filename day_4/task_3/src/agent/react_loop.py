from src.tools.search_summary import search_summary
from src.tools.scrape_site import scrape_site
from src.tools.generate_questions import generate_questions
from src.tools.answer_questions import answer_questions
from src.utils.token_tracker import log_token_count

import uuid

def react_agent(book_title):
    session_id = str(uuid.uuid4())
    token_total = 0
    summary_data = []

    urls = search_summary(book_title)
    for name, url in urls.items():
        text = scrape_site(url)
        if "Error" not in text:
            summary_data.append((name, text))

    questions = generate_questions(book_title).strip().split("\n")
    answers = []

    for q in questions:
        for name, text in summary_data:
            ans = answer_questions(text, q)
            token_total += len(ans.split()) + len(q.split())
            answers.append((q, ans))
            break  # stop at first successful

    log_token_count(session_id, token_total)
    return session_id, answers
