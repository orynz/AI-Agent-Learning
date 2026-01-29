# import requests
# from bs4 import BeautifulSoup
# import re

# def get_headers():
#     return {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }

# # 지저분한 공백과 줄 바꿈을 깔끔하게 정리
# def clean_text(text):
#     # 1. 연속된 줄 바꿈을 하나로 줄임
#     text = re.sub(r'\n\s*\n', '\n', text)
#     # 2. 연속된 공백을 하나로 줄임
#     text = re.sub(r'\s+', ' ', text)
#     return text.strip()

# # [일반 웹페이지용] 광고, 메뉴, 스크립트 같은 쓰레기를 버리고 본문만 남깁니다.
# def extract_general_content(soup):
#     # 1. 불필요한 태그 제거 (청소 단계)
#     # script: 자바스크립트 코드 / style: 꾸미기 코드 / header, footer, nav: 메뉴와 바닥글
#     for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'noscript', 'form']):
#         tag.decompose() # 태그를 삭제합니다.

#     # 2. 남은 것 중에서 텍스트만 추출
#     # body 태그가 있으면 body에서, 없으면 전체에서 추출
#     target = soup.body if soup.body else soup
#     return clean_text(target.get_text(separator=' '))

# # [네이버 블로그용] 숨겨진 진짜 주소(iframe)를 찾아 내용만 추출
# def extract_naver_blog_content(html_text):
#     # 1. iframe src 찾기
#     match = re.search(r'src="(/PostView\.naver\?.*?)"', html_text)
#     if not match:
#         return None
    
#     # 2. 진짜 주소 완성
#     real_url = f"https://blog.naver.com{match.group(1).replace('&amp;', '&')}"
    
#     # 3. 진짜 주소로 다시 접속
#     response = requests.get(real_url, headers=get_headers())
#     if response.status_code != 200:
#         return None
        
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # 4. 블로그 본문 영역 찾기 (se-main-container 또는 view)
#     post_div = soup.find('div', class_='se-main-container') or soup.find('div', class_='view')
    
#     if post_div:
#         return clean_text(post_div.get_text(separator=' '))
#     else:
#         # 본문 영역을 못 찾으면 일반 방식처럼 전체에서 텍스트 추출 시도
#         return extract_general_content(soup)

# def main_extractor(url):
#     """대장 로봇: 주소를 보고 알맞은 방법을 선택합니다."""
#     try:
#         print(f"🔍 분석 중: {url}")
#         response = requests.get(url, headers=get_headers(), timeout=10)
        
#         # HTML 가져오기 실패 시
#         if response.status_code != 200:
#             print(f"❌ Error_Code: {response.status_code}")
#             print(response)
#             return

#         html_text = response.text

#         # 네이버 블로그인지 확인
#         if "blog.naver.com" in url:
#             print("💡 네이버 블로그 감지!")
#             content = extract_naver_blog_content(html_text)
#         else:
#             print("💡 일반 웹페이지 감지!")
#             soup = BeautifulSoup(html_text, 'html.parser')
#             content = extract_general_content(soup)

#         # 결과 출력
#         print("-" * 50)
#         if content:
#             print(f"✅ 추출 결과 (길이: {len(content)}자):")
#             print(content)
#         else:
#             print("❌ 내용을 찾을 수 없습니다.")
#         print("-" * 50)

#     except Exception as e:
#         print(f"🚫 오류 발생: {e}")

# # --- 실행 ---
# if __name__ == "__main__":
#     # 1. 네이버 블로그 테스트
#     target_blog = "https://blog.naver.com/khsbless/224104030727"
#     main_extractor(target_blog)

#     print("\n" + "="*50 + "\n")

#     # 2. 일반 웹페이지 테스트 (예: 한국경제 기사)
#     target_web = "https://www.hankyung.com/article/202511066930g"
#     main_extractor(target_web)
    
#     # 3. 위키독스 테스트(실패: 봇 크롤링 우회기능 필요)
#     target_web = "https://wikidocs.net/742"
#     main_extractor(target_web)


import requests
import time
import random
from fake_useragent import UserAgent # 가짜 신분증을 만들어주는 도구 (pip install fake-useragent)

# 1. 세션(Session) 만들기: 브라우저처럼 방문 기록(쿠키)을 기억하는 도구
session = requests.Session()

# 2. 정교한 가짜 신분증(Header) 만들기
# (fake_useragent가 없다면 직접 긴 문자열을 넣어도 됩니다)
try:
    ua = UserAgent()
    user_agent = ua.random # 매번 다른 브라우저인 척 변경
except:
    # 만약 라이브러리가 없으면 가장 일반적인 크롬 브라우저로 설정
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

headers = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/' # "구글 검색해서 들어왔어요"라고 핑계 대기
}

# 세션에 신분증 부착!
session.headers.update(headers)

def human_request(url):
    """사람처럼 행동하며 접속하는 함수"""
    print(f"🕵️ 접속 시도: {url}")
    print(f"🎭 현재 위장 신분: {session.headers['User-Agent'][:30]}...")

    try:
        # 3. 접속 전 랜덤하게 쉬기 (사람인 척 연기)
        # 1초에서 3초 사이로 무작위로 쉽니다. 로봇은 이렇게 안 쉬거든요.
        sleep_time = random.uniform(1, 3)
        print(f"☕ {sleep_time:.2f}초 동안 딴짓하는 중...")
        time.sleep(sleep_time)

        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ 문지기 통과 성공!")
            return response.text
        elif response.status_code == 403:
            print("🚫 문지기에게 들켰습니다! (403 Forbidden)")
        else:
            print(f"⚠️ 문제 발생: {response.status_code}")

    except Exception as e:
        print(f"❌ 오류: {e}")
    
    return None

# --- 실행 테스트 ---
if __name__ == "__main__":
    target_url = "https://wikidocs.net/742"
    html = human_request(target_url)
    
    # (여기서 아까 만든 BeautifulSoup 코드로 html을 분석하면 됩니다)