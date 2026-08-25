from scraper import fetch_website_text
from qualifier import qualify_company

text = fetch_website_text("https://perific.com")

if text:
    result = qualify_company(text)
    print(result)