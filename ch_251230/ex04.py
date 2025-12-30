"""
한 페이지 크롤링
"""
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.select("div.quote")

for i, quote in enumerate(quotes, 1):
    text = quote.select_one("span.text").get_text(strip=True)
    author = quote.select_one("small.author").get_text(strip=True)
    print(f"{i}. {text} - {author}")
