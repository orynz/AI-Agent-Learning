import os
from dotenv import load_dotenv
from openai import OpenAI

# 환견변수 로드
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
print(API_KEY)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=API_KEY)

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "user", "content": "안녕!"}
    ]
)

print(response.choices[0].message.content)