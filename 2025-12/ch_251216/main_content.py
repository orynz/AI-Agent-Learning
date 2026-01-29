# main_content.py
from llm_utils import ask_llm
from prompt_templates import AD_TEMPLATE

prompt = AD_TEMPLATE.format(
    product = "AI 학습 플랫폼 LearnX",
    message = "누구나 쉽게 AI를 배울 수 있다. 5문장으로!",
    tone = "까칠한 문체"
)

result = ask_llm(prompt)
print(result)
