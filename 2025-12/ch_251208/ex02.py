import os
from dotenv import load_dotenv
import openai as OpenAI


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client  = OpenAI.Client(api_key=API_KEY)

message =[
    {"role":"user", "content":"인공지능이 뭐야?"},
    {"role":"system", "content":"한 줄로 인사!"}
    ]

response = client.chat.completions.create(messages=message, model="gpt-5")
print(response.choices[0].message.content)
