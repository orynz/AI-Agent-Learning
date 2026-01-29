from openai import OpenAI


clitent = OpenAI()

prompt = [
    "AI 교육의 필요성을 설명하라",
    "AI 교육의 필요성을 세 가지 핵심을 이유를 불릿 형식으로 작성하라",
    "AI 교육 전문가의 관점에서 고등학생에게 설명하듯 쉽게 설명하라"
]

MODEL = "gpt-5-nano"
for i, p in enumerate(prompt):
    response = clitent.chat.completions.create(
        model=MODEL,        
        messages=[
            {"role": "user", "content": p},
            {"role": "system", "content": "당신은 유능한 AI 교육 전문가입니다."}
        ],
        # temperature=0.7
    )
    print(f"Prompt {i+1}: {p}")
    print("Response:", response.choices[0].message.content)
    print()