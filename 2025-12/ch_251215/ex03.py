from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

topic = input("설명할 주제를 입력하세요: ")

formats = {
    "문장형": "2~3문장의 짧은 단락으로 설명하시오.",
    "목록형": "bullet 목록으로 4줄 이내로 설명하시오.",
    "표 형식": "선택한 내용을 2열 표 형식으로 정리하시오. (항목 | 설명)",
    "JSON": "다음을 JSON 형식으로 출력하시오. { '요약': '', '핵심포인트': [] }",
}

for fmt_name, fmt_instruction in formats.items():
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "출력 형식을 정확히 지키는 AI입니다."},
            {"role": "user", "content": f"{topic}를 {fmt_instruction}"}
        ]
    )

    print(f"\n=== Format: {fmt_name} ===")
    print(resp.choices[0].message.content)
