from bs4  import BeautifulSoup
from datetime import datetime
import requests
import os
import json

# 기사 제목/원문 url 저장
def news_save(path, data):
    
   with open(f"{path}.jsonl", "a", encoding="utf-8") as f:
       
       f.write(f'{json.dumps(data, ensure_ascii=False)}\n')
# 이미지 저장
def image_download(url, file_name):
    res = requests.get(url)
    if res.status_code == 200:
        
        with open(file_name,"wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        print("Error: ", res.status_code)

urls = [
    {"url":"https://news.naver.com/section/100", "section":"정치"},
    {"url":"https://news.naver.com/section/101", "section":"경제"},
    {"url":"https://news.naver.com/section/102", "section":"사회"},
    {"url":"https://news.naver.com/section/103", "section":"생활_문화"},
    {"url":"https://news.naver.com/section/104", "section":"세계"},
    {"url":"https://news.naver.com/section/105", "section":"IT_과학"},
]

news_data = {"sections" : list()}

# 폴더 생성
path = datetime.now().strftime(f"news_%Y%m%d")
if not os.path.isdir(path):
    os.makedirs(path)
        
for i, url in enumerate(urls):
    # 요청
    res = requests.get(url["url"])
    res.raise_for_status()
    
    news_data["sections"].append({f"section_{i}": url["section"]})
    news_data["sections"][i]["news"] = []
    
    # 요청 성공시
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.select("div.sa_item_flex._LAZY_LOADING_WRAP")
        
        for j, quote in enumerate(quotes):
            
            # 헤드라인 뉴스 5개만!
            if j > 4: break
            
            file_name = datetime.now().strftime(f"{path}/%Y%m%d_%H%M%S{j}.jpg")
            img_url = quote.select_one("img._LAZY_LOADING._LAZY_LOADING_INIT_HIDE") # 이미지
            news_title = quote.select_one("strong.sa_text_strong")                  # 제목
            news_url = quote.select_one("a.sa_thumb_link._NLOG_IMPRESSION")         # 기사 원본 URL
            
            
            if img_url and news_title and news_url:
                image_download(img_url["data-src"], file_name) # 이미지(썸네일) 다운로드
                
            if news_title and news_url:
                news_data["sections"][i]["news"].append({
                    "title": news_title.text,
                    "url": news_url["data-imp-url"]
                })
                
    else:
        print("Error: ", res.status_code)
        
news_save(path + "/news", news_data) # 뉴스 제목 저장

