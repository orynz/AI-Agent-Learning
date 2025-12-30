import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = "https://quotes.toscrape.com"
url = "/page/1/"

data = []

while url:
    response = requests.get(base_url + url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.select("div.quote")

    for quote in quotes:
        text = quote.select_one("span.text").get_text(strip=True)
        author = quote.select_one("small.author").get_text(strip=True)
        data.append({"Quote": text, "Author": author})

    next_btn = soup.select_one("li.next > a")
    url = next_btn["href"] if next_btn else None

df = pd.DataFrame(data)
df.to_csv("quotes.csv", index=False, encoding="utf-8")
print("quotes.csv 파일 저장 완료")
