import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 1. 메인 페이지 데이터 수집
def scrape_main_page(url):
    """
    메인 페이지에서 책 목록 수집
    """
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("article.product_pod")  # 20개 항목 선택
    return items

# 2. 상세 페이지 데이터 수집
def parse_detail(detail_url):
    """
    책 상세 페이지에서 추가 정보 추출
    """
    response = requests.get(detail_url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # 카테고리 추출
    breadcrumb = soup.select("ul.breadcrumb li a")
    category = breadcrumb[-1].get_text(strip=True) if breadcrumb else "N/A"

    # 설명 추출
    description = ""
    desc_header = soup.select_one("#product_description")
    if desc_header and desc_header.find_next_sibling("p"):
        description = desc_header.find_next_sibling("p").get_text(" ", strip=True)

    # 상품 정보 테이블 파싱
    info = {}
    for row in soup.select("table.table.table-striped tr"):
        key = row.select_one("th").get_text(strip=True)
        value = row.select_one("td").get_text(strip=True)
        info[key] = value

    return {
        "category": category,
        "description": description,
        "upc": info.get("UPC"),
        "num_reviews": info.get("Number of reviews")
    }

# 3. 메인 실행 로직
def main():
    # 기본 설정
    BASE_URL = "https://books.toscrape.com"

    # 메인 페이지 데이터 수집
    items = scrape_main_page(BASE_URL)
    rows = []

    # 각 항목 처리
    for item in items:
        a_tag = item.select_one("h3 a")
        title = a_tag["title"]
        relative_url = a_tag["href"]
        detail_url = f"{BASE_URL}/{relative_url}"  # 상세 페이지 URL

        # 기본 정보 추출
        price = item.select_one("p.price_color").get_text(strip=True)
        availability = item.select_one("p.instock.availability").get_text(" ", strip=True)
        rating_tag = item.select_one("p.star-rating")
        rating = rating_tag["class"][1]  # One, Two, ..., Five

        # 데이터 저장 (상세 정보는 이후 처리)
        rows.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "detail_url": detail_url
        })

    # 상세 정보 5개만 처리 (논리적 오류 있음)
    for i, row in enumerate(rows[:5]):
        detail = parse_detail(row["detail_url"])
        row.update(detail)
        time.sleep(0.2)  # 서버 부하 방지

    # DataFrame 생성
    df = pd.DataFrame(rows)
    print(df.head())

    # 숫자형 데이터 변환
    df["num_reviews"] = pd.to_numeric(df["num_reviews"], errors="coerce")
    df["description"] = df["description"].fillna("")

    # JSONL 파일 생성
    def to_llm_record(row):
        return {
            "source": "books.toscrape.com",
            "title": row["title"],
            "category": row["category"],
            "price": row["price"],
            "rating": row["rating"],
            "availability": row["availability"],
            "num_reviews": int(row["num_reviews"]) if pd.notna(row["num_reviews"]) else 0,
            "description": row["description"]
        }

    with open("books_scraping_llm.jsonl", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(to_llm_record(row), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()