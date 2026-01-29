from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)


def build_advanced_prompt() -> str:
    prompt = """
[역할] AI 교육을 담당하는 데이터 과학 강사입니다.

[요청]
기업에서 AI 윤리 교육이 중요한 이유를 3가지로 설명하세요.

[예시1 입력]
"클라우드 컴퓨팅의 장점"

[예시1 출력]
{
  "summary": "클라우드 컴퓨팅은 확장성과 비용 효율성 때문에 다양한 산업에서 폭넓게 도입되는 기술입니다.",
  "keywords": ["#확장성", "#비용효율", "#유연성"],
  "importance": "기업 운영의 민첩성과 서비스 확장을 빠르게 지원하는 핵심 인프라 역할을 합니다.",
  "level": "5단계 중 2단계"
}

[예시2 입력]
"데이터 시각화의 의의"

[예시2 출력]
{
  "summary": "데이터 시각화는 복잡한 정보를 시각적으로 표현하여 빠른 이해와 통찰을 돕는 분석 기법입니다.",
  "keywords": ["#시각화", "#정보해석", "#통찰"],
  "importance": "의사결정 과정에서 핵심 패턴을 빠르게 파악하도록 지원합니다.",
  "level": "5단계 중 1단게"
}

[출력 스키마]
아래 JSON 형식에 맞추어 출력하시오.

{
  "summary": "",
  "keywords": ["", "", ""],
  "importance": "",
  "level": ""
}

[제약]
- 스키마 외 문장 출력 금지
- summary는 한 문장으로 작성
- keywords는 정확히 3개
- level은 “기초·중급·고급” 중 하나로 지정
- 새로운 사실 추가 금지
- 학술적이고 간결한 표현 유지

[검증 규칙]
summary, keywords, importance, level 네 항목 중 하나라도 누락되면
“누락 발견 → 전체 재작성”을 수행하시오.
스키마 형태가 틀리면 동일 구조로 다시 작성하시오.
"""
    return prompt.strip()


# template = """
# [역할] {role}
# [요청] {task}
# [출력 형식] {format}
# [제약] {constraints}

# 위 조건에 따라 답하시오.
# """

# prompt = template.format(
#     role="데이터 과학 강사",
#     task="정규화(normalization)의 개념을 설명하라.",
#     format="1) 개념 2) 예시 3) 적용 상황 4) 주의점",
#     constraints="간결하게 작성"
# )

# print(prompt)


def call_llm(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # 첫 번째 출력 텍스트만 가져온다.
    message = response.output[0].content[0].text
    return message


def main():
    prompt = build_advanced_prompt()
    print("===== 전송된 프롬프트 =====")
    # print(prompt)
    print("\n===== LLM 응답(JSON) =====")
    result = call_llm(prompt)
    print(result)


if __name__ == "__main__":
    main()
