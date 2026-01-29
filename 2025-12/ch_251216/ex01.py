from openai import OpenAI
import os

# client = OpenAI()

# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     stream=True,
#     messages=[
#         {"role": "user", "content": "생성형 AI의 개념을 간단히 10문장으로 설명해 주세요."}
#     ]
# )

# def print_tokens(tk):
#     print(tk.completion_tokens)
#     print(tk.prompt_tokens)
#     print(tk.total_tokens)


# for chunk in stream:
#     delta = chunk.choices[0].delta
#     # print_tokens(chunk.usage)
    
#     # delta가 dict가 아니라 ChoiceDelta 객체라서 delta["content"]처럼 대괄호 인덱싱 안 됨.
#     content = getattr(delta, "content", None)
#     if content:
#         print(content, end="", flush=True)



from typing import Optional

class User:
    def __init__(self, name: str, middle_name: Optional[str] = None):
        self.name = name
        self.middle_name = middle_name

    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.name} {self.middle_name}"
        return self.name

u = User(name="hong", middle_name="test")
print(u.full_name())