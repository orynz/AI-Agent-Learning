# openai, dotenv 모듈 선언
# 환경변수에서 api 키 세팅
# openai 객체 생성
# 명령 프롬프트 파일 열어서 프롬프트 세팅
# 메시지 보내기
# 작업 결과물 저장



from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("SECRET_KEY")
client = OpenAI(api_key=key)


with open("prompt.txt", 'r', encoding="utf-8") as f:
    prompt =  f.read()


model = os.getenv("MODDEL_GPT_4o_mini")
messages = [
    {"role": "system", "content": "할머니가 손녀에세 옛날이야기하듯 말해"},
    {"role": "user", "content": prompt}
    ]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)


with open("result1.txt", 'w', encoding="utf-8") as f:
    f.write(response.choices[0].message.content.strip('\n'))


