import os
from openai import OpenAI
import urllib.request
import llama_index
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 환경변수에 API키 설정되어 있어야 함
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "내일 오후 4시 서울 날씨 알려줘"},
#     ]
# )
# print(response.choices[0].message.content)


# url = "https://raw.githubusercontent.com/llama-index-tutorial/llama-index-tutorial/main/ch04/data/paul_graham_essay.txt"

# # 파일 다운로드
# urllib.request.urlretrieve(url, 'paul_graham_essay.txt')
# print("결과\n")




# documents = SimpleDirectoryReader(input_files=["paul_graham_essay.txt"]).load_data()
# index = VectorStoreIndex.from_documents(documents)

# query_engine = index.as_query_engine()
# response = query_engine.query("Describe what the author's teenage years were like.")
# print(f"작가의 청소년 시절은 어떠했는지 설명해 줘:\n{response}")
# response = query_engine.query("What are your plans for the future?")
# print(f"지금은 무엇을 하고 있어?:\n{response}")

# while True:
#     print("q")
    
# '''PDF 다운로드 봇'''
import llama_index
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader(input_files=["인문학의 새로운 역할에 대한 고찰.pdf"]).load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

print("-" * 24, "인문학의 새로운 역할에 대한 고찰", "-" * 24)
while True:    
    print()
    msg= input("궁금한 것을 물어보세요: ")
    response = query_engine.query(f"{msg} 결과물은 한국어로 출력하세요.")
    
    print()
    print(f"질문: {msg}\n답:{response}")
        
