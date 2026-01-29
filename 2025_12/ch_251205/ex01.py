from openai import OpenAI
import os

# .env 파일의 변수 사용하기
# pip install dotenv : 패키지 설치
'''

'''

import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 사용
secret_key= os.getenv("SECRET_KEY")
naver_url = os.getenv("NAVER_URL")
debug_mode = bool(os.getenv("DEBUG"))


print(f"Secret Key: {secret_key}")
print(f"Naver URL: {naver_url}")

# 환경 변수는 항상 문자열로 읽히므로 필요시 형 변환이 필요합니다.
print(f"Debug Mode: {debug_mode}", type(debug_mode)) 

f = open("newfile.txt", 'r')
# f.write("Hello World")
text = f.read()
f.close()
print(text) # 출력: Hello, python!

# client = OpenAI(api_key=value)



# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# response = client.responses.create(
#     model="gpt-5-nano",
#     input="우주의 나이는 얼마나될까?",
#     store=True
# )

# print(response.output_text)

