import os
from openai import OpenAI
import urllib.request
import llama_index
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# #환경변수에 API키 설정되어 있어야 함
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# # client = OpenAI(api_key="YOUR_API_KEY")


# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "안녕하세요?"},
#     ]
# )
# print(response.choices[0].message.content)


url = "https://raw.githubusercontent.com/llama-index-tutorial/llama-index-tutorial/main/ch04/data/paul_graham_essay.txt"

# 파일 다운로드
urllib.request.urlretrieve(url, 'paul_graham_essay.txt')
print("파일 다운로드 완료!")




documents = SimpleDirectoryReader(input_files=["paul_graham_essay.txt"]).load_data()
index = VectorStoreIndex.from_documents(documents)
