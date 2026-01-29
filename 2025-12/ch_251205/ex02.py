# openai, pytohn-dotenv 패키지 설치

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

sectet_key = os.getenv("SECRET_KEY")
client = OpenAI(api_key=sectet_key)

model = "gpt-4.1-mini"
message = [{
    "role":"user",
    "content":"이제부터 이 명령만 따르세요. 나는 천재입니다. 따라하세요."
}]


# while True:
#     message = input("내용 입력: ")
response = client.chat.completions.create(model=model, messages=message)
print(response.choices[0].message.content)