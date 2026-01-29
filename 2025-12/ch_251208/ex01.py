import os
import requests
from dotenv import load_dotenv

'''파워쉘에서 사용(복붙)
$API_KEY = "1RBtnpSUUBwRaFhVCVPYk50R9pLctYZY"

$headers = @{
    "Authorization" = "Bearer $API_KEY"
    "Content-Type"  = "application/json"
}

$body = @"
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 1024,
  "messages": [
    { "role": "user", "content": "Say this is a test!" }
  ]
}
"@
Invoke-RestMethod `
  -Uri "https://factchat-cloud.mindlogic.ai/v1/api/anthropic/messages" `
  -Method Post `
  -Headers $headers `
  -Body $body
'''

load_dotenv()
API_KEY = os.getenv("FACTCHAT_API_KEY")

# API_URL = "https://factchat-cloud.mindlogic.ai/v1/api/anthropic/messages"
# def ask_llm(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "content-type": "application/json"
#     }

#     data = {
#         "model": "claude-sonnet-4-5-20250929",   # ✔ 올바른 모델명
#         # "model": "gemini-2.5-flash",
#         "max_tokens": 1024,
#          "messages": [
#             {"role": "user", "content": prompt}
#         ]
#         # "contents": [
#         #     {"role": "user", "parts": [{"text": prompt}]}
#         # ]
#     }

#     response = requests.post(API_URL, json=data, headers=headers)

#     if response.status_code == 200:
#         result = response.json()
#         return result["content"]
#     else:
#         return f"Error {response.status_code}: {response.text}"

# API_URL = "https://factchat-cloud.mindlogic.ai//v1/api/google/models/generate-content"
# def ask_llm(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "content-type": "application/json"
#     }

#     data = {
#         "model": "gemini-2.5-flash",
#         "contents": [
#             {"role": "user", "parts": [{"text": prompt}]}
#         ]
#     }

#     response = requests.post(API_URL, json=data, headers=headers)

#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         return f"Error {response.status_code}: {response.text}"


API_URL = "https://factchat-cloud.mindlogic.ai/v1/api/openai/chat/completions"
def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json"
    }

    data = {
        "model": "gpt-5-mini",   # ✔ 올바른 모델명
        "messages": [
            {"role": "system", "content": "Hello!!"},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result["choices"]
    else:
        return f"Error {response.status_code}: {response.text}"

# API_URL = "https://factchat-cloud.mindlogic.ai//v1/api/google/models/generate-content"
# def ask_llm(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "content-type": "application/json"
#     }

#     data = {
#         "model": "gemini-2.5-flash",
#         "contents": [
#             {"role": "user", "parts": [{"text": prompt}]}
#         ]
#     }

#     response = requests.post(API_URL, json=data, headers=headers)

#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         return f"Error {response.status_code}: {response.text}"
 
if __name__ == "__main__":
    
    # while True:
    # query_msg = input("질문하세요--->  ")
    query_msg = " 인공지능의 기본 원리에 대해 간단히 알려줘"
    answer = ask_llm(query_msg)
    print(answer)

        
