from bs4 import BeautifulSoup
import requests

def scrape_site(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = ' '.join([p.text for p in soup.find_all('p')])
            return text[:5000]  # Limit scrape
    except Exception as e:
        return f"Error: {str(e)}"
    return ""
