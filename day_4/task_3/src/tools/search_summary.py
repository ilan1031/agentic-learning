from bs4 import BeautifulSoup
import requests

def search_summary(book_title):
    search_urls = {
        "wikipedia": f"https://en.wikipedia.org/wiki/{book_title.replace(' ', '_')}",
        "sparknotes": f"https://www.sparknotes.com/search?q={book_title.replace(' ', '+')}",
        "goodreads": f"https://www.goodreads.com/search?q={book_title.replace(' ', '+')}",
    }
    return search_urls
