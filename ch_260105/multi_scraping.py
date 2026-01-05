import json
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor, as_completed
    
# 1. robots.txt 확인 (크롤링 허용 여부 확인)
def check_robots(url, user_agent = "*"): # "*" 모든 로봇 대상
    """주어진 URL의 robots.txt 확인"""    
    p = requests.utils.urlparse(url)
    base_url = f"{p.scheme}://{p.netloc}"
    
    rp = RobotFileParser()
    rp.set_url(f"{base_url}/robots.txt")
    try:
        rp.read()
        if rp.can_fetch(user_agent, url):
            print("robots.txt: 크롤링 허용됨")
            return True
        else:
            print("robots.txt: 크롤링 금지됨")
            return False
    except Exception as e:
        print(f"robots.txt 확인 실패: {e}")
        return True  # robots.txt 없을 경우 기본 허용

# 2. 메인 페이지 데이터 수집
def scrape_main_page(url, timeout: float=10):
    """메인 페이지에서 책 목록 수집"""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select("article.product_pod")

# 3. 상세 페이지 데이터 수집
def parse_detail(detail_url, timeout: float=10):
    """책 상세 페이지에서 추가 정보 추출"""
    try:
        response = requests.get(detail_url, timeout=timeout)
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
    except Exception as e:
        print(f"Error fetching {detail_url}: {e}")
        return {
            "category": "N/A",
            "description": "",
            "upc": "N/A",
            "num_reviews": "0"
        }

# 4. 메인 실행 로직
def main():
    # 기본 설정
    BASE_URL = "https://books.toscrape.com"
    TOTAL_PAGES = 5  # 전체 페이지 수

    # robots.txt 체크
    if not check_robots(BASE_URL):
        return

    # 모든 페이지 데이터 수집 (상세 정보 제외)
    all_rows = []
    for page in range(1, TOTAL_PAGES + 1):
        
        # 모든 스레드가 서로 다른 시간에 서버에 접속하게 만듭니다.
        time.sleep(random.uniform(0.1, 0.5))  # 0.1~0.5초 랜덤 지연
        
        # 페이지 URL 생성
        page_url = f"{BASE_URL}/catalogue/page-{page}.html" if page > 1 else BASE_URL
        items = scrape_main_page(page_url)

        for item in items:
            a_tag = item.select_one("h3 a")
            title = a_tag["title"]
            relative_url = a_tag["href"]
            detail_url = f"{BASE_URL}/{relative_url}"

            price = item.select_one("p.price_color").get_text(strip=True)
            availability = item.select_one("p.instock.availability").get_text(" ", strip=True)
            rating_tag = item.select_one("p.star-rating")
            rating = rating_tag["class"][1] if rating_tag else "N/A"

            all_rows.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
                "detail_url": detail_url
            })

    # 병렬 처리: 모든 상세 페이지 데이터 수집
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_index = {}
        for index, item in enumerate(all_rows):
            future = executor.submit(parse_detail, item["detail_url"])
            future_to_index[future] = index

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                detail_data = future.result()
                all_rows[index].update(detail_data)
            except Exception as e:
                print(f"Error processing {index}: {e}")

    # DataFrame 생성
    df = pd.DataFrame(all_rows)
    df["num_reviews"] = pd.to_numeric(df["num_reviews"], errors="coerce").fillna(0).astype(int)
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
            "num_reviews": int(row["num_reviews"]),
            "description": row["description"]
        }

    with open("books_scraping_llm.jsonl", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(to_llm_record(row), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()