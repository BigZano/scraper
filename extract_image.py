from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_images_from_html(html, base_url):
    image_urls = []

    try:
        soup = BeautifulSoup(html, "html.parser")
        images = soup.find_all("img")

        for img in images:
            src = img.get("src")
            if not src:
                continue

            absolute_url = urljoin(base_url, src)
            image_urls.append(absolute_url)
        return image_urls
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []
