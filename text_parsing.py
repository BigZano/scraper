from bs4 import BeautifulSoup


def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1")
    return h1_tag.get_text(strip=True) if h1_tag else ""


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")
    if main_tag:
        p_tag = main_tag.find("p")
    else:
        p_tag = soup.find("p")
    return p_tag.get_text(strip=True) if p_tag else ""
