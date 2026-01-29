from openai import OpenAI
from config import Models, ChatMessage, PromptUnit
import time


client = OpenAI()

def ask_llm(prompt: str,
            model: str = "gpt-4o-mini",
            temperature: float = 0.7) -> str:
    """단일 프롬프트를 받아 LLM 응답 텍스트를 반환하는 기본 함수입니다."""
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def ask_llm_2(prompt: str,
            model: str = "gpt-4o-mini",
            temperature: float = 0.7,
            max_retries: int = 3,
            retry_delay: float = 2.0) -> str:
    """LLM 호출에 대한 기본 함수로, 예외 처리와 재시도 로직을 포함합니다."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[오류 발생] 시도 {attempt}/{max_retries}: {e}")
            if attempt == max_retries:
                return "죄송합니다. 현재 AI 응답을 가져오는 데 실패했습니다. 잠시 후 다시 시도해 주세요."
            time.sleep(retry_delay)
            
def run_chat_completion(
    prompt_unit: PromptUnit,
    model: Models = Models.GPT4o,
    temperature: float = 0.7,
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> PromptUnit:
    
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model = model.value,
                messages = prompt_unit.prompt,
                temperature = temperature
            )
            prompt_unit.response = completion.choices[0].message.content or ""
            return prompt_unit
        
        except Exception as e:
            print(f"[오류 발생] 재시도 {attempt+1}/{max_retries}: {e}")
            if attempt == max_retries:
                return prompt_unit
            time.sleep(retry_delay)

prompt_unit = PromptUnit(
    title="간단한 요약 설명",
    prompt=[
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="인공지능의 역사")
    ],
    response=None
)

# if __name__ == "__main__":
#     question = input("AI에게 물어볼 내용을 입력하세요: ")
#     answer = ask_llm_2(question)
#     print("\n[AI 응답]")
#     print(answer)
    
# prompt_unit = run_chat_completion(prompt_unit)
# print(prompt_unit.response)