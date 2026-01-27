import os
from dotenv import load_dotenv
from openai import OpenAI

# 환견변수 로드
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
print(API_KEY)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "user", "content": "안녕!"}
    ]
)

print(response.choices[0].message.content)