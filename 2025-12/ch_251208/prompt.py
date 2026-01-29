import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")
clitet = OpenAI(api_key=API_KEY)


with open("prompt.txt", "r", encoding="utf-8") as f:
    query = f.read()
    
message = [
    {"role": "user", "content": query}
]

response = clitet.chat.completions.create(messages=message, model="gpt-3.5-turbo")
chat = response.choices[0].message.content
print(chat)





