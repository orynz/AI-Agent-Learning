from dotenv import load_dotenv
from openai import OpenAI
import os
import hsutils

load_dotenv()
# api_key = os.getenv("API_KEY")
client = OpenAI()
question = "AI가 사회를 어떻게 변화시킬까요?"
for temp in [0.0, 0.7, 1.2]:
    print(f"\n=== temperature = {temp} ===\n")

    reply = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": question}],
        temperature=temp,
    )
    content = reply.choices[0].message.content
    print(content)


# tiktoken 패키지에서 특정 모델에 맞는 토크나이저(encoder)를 불러오는 함수
import tiktoken

try:
    # "gpt-4o-mini" 모델에서 사용되는 토큰 인코딩 방식을 로드
    # 각 모델은 서로 다른 토크나이저 규칙을 가질 수 있으므로 모델명을 지정해야 합니다.
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
except KeyError:
    # 모델을 찾을 수 없는 경우 기본 인코딩(cl100k_base)으로 대체합니다.
    # cl100k_base는 gpt-4, gpt-3.5-turbo 등 대부분의 최신 모델에 사용됩니다.
    encoding = tiktoken.get_encoding("cl100k_base")
        
# # 토큰화할 입력 텍스트 정의
text = "안녕하세요. tiktoken 패키지를 사용하여 토큰수를 확인합니다."

# 텍스트를 토큰 ID의 리스트 형태로 변환
# 토큰화(Tokenization)는 모델이 텍스트를 처리할 수 있도록 숫자 단위로 변환하는 과정임
encoded = encoding.encode(text)
tokens = len(encoded)
# 
print(f"변환된 토큰 ID 리스트를 출력:\n{encoded}")
print(f"'{text}'의 토큰 수: {tokens}")
