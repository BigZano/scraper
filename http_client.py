import requests


def get_html(url):
    try:
        response = requests.get(url, headers={"User-agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"network error while fetching {url}: {e}")

    if response.status_code >= 400:
        raise Exception(f"got http error: {response.status_code}")

    content_type = response.headers.get("content-type", "")

    if "text/html" not in content_type:
        raise Exception(f"got non-HTML response: {content_type}")

    return response.text
