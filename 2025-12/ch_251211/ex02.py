from openai import OpenAI

client = OpenAI()

prompt1="AI 교육의 필요성을 설명하라"
prompt2="AI 교육의 필요성을 세 가지 핵심을 이유를 불릿 형식으로 작성하라"
prompt3="다음 예시처럼 블릿 구조를 유지하라.\
    예시:\
    - 핵심1: 기술 변화 대응\
    - 핵심2: 문제 해결 역략 향상\
    위 예시 스타일을 참고하여 AI 교육의 필요성을 3가지로 작성하라."

prompts =[prompt1, prompt2, prompt3]
MODEL = "gpt-5-nano"


for i, p in enumerate(prompts):
    response = client.chat.completions.create(
        model=MODEL,        
        messages=[
            {"role": "user", "content": p},
            {"role": "system", "content": "당신은 유능한 AI 교육 전문가입니다."}
        ],
        # temperature=0.7
    )
    print("*" * 80)
    print(f"Prompt {i+1}: {p}")
    print("Response:", response.choices[0].message.content)
    print()
    