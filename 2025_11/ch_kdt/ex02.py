# from openai import OpenAI
# import os

# # 환경변수에 API키를 설정한 경우 사용
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# # AIP키를 직접 입력해서 사용하는 경우
# # os.environ["OPENAI_API_KEY"] = "Your API Key"

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "안녕하세요?"},
#     ]
# )
# print(response.choices[0].message.content)


import urllib.request # URL을 다루기 위한 모듈 : urllib
url = "https://raw.githubusercontent.com/llama-index-tutorial/llama-index-tutorial/main/ch04/data/paul_graham_essay.txt"

# 파일 다운로드
urllib.request.urlretrieve(url, 'Attention_Is_All_You_Need.pdf')
print("다운로드 완료!")

# import llama_index
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# documents = SimpleDirectoryReader(input_files=["paul_graham_essay.txt"]).load_data()
# index = VectorStoreIndex.from_documents(documents)

# query_engine = index.as_query_engine()
# response = query_engine.query("작가의 청소년 시절은 어떠했는지 한글로 설명하세요.")
# print(response)