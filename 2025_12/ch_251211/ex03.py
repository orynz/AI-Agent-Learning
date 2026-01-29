from openai import OpenAI

client = OpenAI()
topic = "신규 온라인 교육 프로그램 런칭"

prompt = f"""
주제: {topic}

다음 세 가지 형식으로 각각 작성하시오.
① 광고 문구
② 유튜브 스크립트(30초 분량)
③ SNS 포스팅(감성 톤)

각 형식은 길이·말투·표현 방식이 서로 다르게 작성되도록 하시오.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

print("=== 멀티포맷 생성 결과 ===\n")
print(response.choices[0].message.content)
