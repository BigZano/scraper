from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_urls_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, "html.parser")
        urls = []
        seen = set()
        for anchor_tag in soup.find_all("a"):
            href = anchor_tag.get("href")
            if href:
                absolute_url = urljoin(base_url, href)
                if absolute_url not in seen:
                    seen.add(absolute_url)
                    urls.append(absolute_url)
        return urls
    except Exception as e:
        print(f"Error parsing HTML for URLs: {e}")
        return []
