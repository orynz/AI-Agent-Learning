# ------------------------
# robots.txt 확인 예제
# ------------------------
import requests

url = "https://www.naver.com/robots.txt"
response = requests.get(url)
print(response.text)


# ------------------------
# robots.txt 자동 확인 예제
# ------------------------
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://www.naver.com/robots.txt")
rp.read()


"""
can_fetch() 함수는 지정한 크롤러(User-agent)가
특정 경로에 접근 가능한지를 True 또는 False로 반환합니다. 
이와 같은 자동 확인 방식은 크롤링 프로그램을 작성할 때 
사전에 접근 가능 여부를 점검하는 안전 장치로 활용할 수 있습니다.
"""
print(rp.can_fetch("*", "/"))  # 모든 봇이 루트(/) 접근 가능 여부


