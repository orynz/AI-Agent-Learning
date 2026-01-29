import requests
import os

url = "https://factchat-cloud.mindlogic.ai/v1/api/openai/chat/completions"

# API 키를 코드에 직접 넣기보다 환경 변수에서 불러오는 것을 권장합니다.
# os.environ["API_KEY"] = "..."  # 실행 환경에서 사전 설정


API_KEY = os.getenv("MINDLOGIC_API_KEY")
if API_KEY is None:
    raise ValueError("환경 변수 FACTCHAT_API_KEY 가 설정되어 있지 않습니다.")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5-mini",
    "messages": [
        {"role": "user", "content": "Say this is a test!"},
    ]
}

print(headers)
print(data)

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:")
print(f"Text:\n{response.text}")
print(f"Data:\n{response.json()}")
