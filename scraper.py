import requests
from bs4 import BeautifulSoup


def fetch_website_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style"]):
            element.decompose()

        return soup.get_text(separator=" ", strip=True)

    except requests.RequestException as e:
        print(f"Could not fetch {url}: {e}")
        return None

websites = [
    "https://perific.com",
    "https://carpenova.se",
    "https://swedrive.se",
    "https://sparv.io",
    "https://cetasol.com",
    "https://octanorm.se",
    "https://adway.ai",
    "https://photonsports.se",
    "https://welandsolutions.se",
    "https://qurant.se",
]

for website in websites:
    print(f"\n--- {website} ---")

    text = fetch_website_text(website)

    if text:
        print(text[:500])