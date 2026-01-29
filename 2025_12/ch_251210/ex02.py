from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client  =OpenAI()

model = "gpt-4.1-mini"

long_text = ""
with open("ex02_long_text.txt", "r", encoding="utf-8") as f:
    long_text = f.read()
    
    
print(long_text)


prompt = f"다음 긴 글의 핵심 내용을 두세줄로 요약하세요.\n---\n{long_text}"

response = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"user", "content": prompt}
        ]
    )

content = response.choices[0].message.content
def save(f_name, txt):
    with open(f_name, "w", encoding="utf-8")  as f:
        f.write(txt)
        
save("ex02_result_text.txt", content)
print(content)

    
