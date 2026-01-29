from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()
client = OpenAI()

# # 파일 업로드하기 
# response = client.files.create(
#   file = open("A_Lucky_Day.txt", "rb"),
#   purpose = "user_data",
#   expires_after={
#     "anchor": "created_at",
#     "seconds": 3600 * 24 # 3600초(1시간) * 24 = 86400초(24시간)
#   }
# )
# file_id = response.id # 업로드한 파일의 ID
# print(f'File ID: {response.id}\nFile Name: {response.filename}\nFile Purpose: {response.purpose}\n')
# print('---')

# # 벡터스토어 생성하기
# response = client.vector_stores.create(
#   name = "vector_store_test",
# )
# vector_store_id = response.id
# print(f'Vector Store ID: {response.id}\nVector Store Name: {response.name}\nVector Store File Counts: {response.file_counts}\n')
# print('---')

# # 백터스토어에 파일 등록
# response = client.vector_stores.files.create(
#   vector_store_id = vector_store_id,
#   file_id = file_id
# )
# print(f'Vector Store File ID: {file_id}')
# print(f'Vector Store File Vector Store ID: {response.vector_store_id}')
# print('---')


# 업로드한 파일 목록의 정보 조회
response = client.files.list()
for f in response.data:
    if f.filename == "A_Lucky_Day.txt":
        file_id = f.id
        print(f'File ID: {f.id}\nFile Name: {f.filename}\nFile Purpose: {f.purpose}\n')
        print('---')
        
        # 업로드된 파일 삭제
        # client.files.delete(file_id = f.id)
        break

# 백터스토어 목록의 정보를 조회
response = client.vector_stores.list()
for vs in response.data:
    if vs.name == "vector_store_test": 
        vector_store_id = vs.id
        print(f'Vector Store ID: {vs.id}\nVector Store Name: {vs.name}\nVector Store File Counts: {vs.file_counts}\n')
        print('---')
        
        # 벡터스토어 삭제
        # deleted_vector_store = client.vector_stores.delete(
        #     vector_store_id = vector_store_id
        # )
        break

# 임베딩 완료까지 기다리는 폴링 함수
def wait_for_embedding(vector_store_id, interval=1):
    while True:
        counts = client.vector_stores.retrieve(vector_store_id).file_counts

        print(
            f"상태 = completed:{counts.completed}, "
            f"in_progress:{counts.in_progress}, "
            f"failed:{counts.failed}, total:{counts.total}"
        )

        # 임베딩이 모두 완료되었을 때
        if counts.in_progress == 0:
            # 실패 여부 확인
            if counts.failed > 0:
                raise Exception("임베딩 실패한 파일이 있습니다.")
            return

        time.sleep(interval)

# 업로드 파일이 벡터스토어에 임베딩 될때까지 대기
wait_for_embedding(vector_store_id)

# 벡터스토어에서 문서내 관련 내용 찾기
response = client.vector_stores.search(
  vector_store_id = vector_store_id,
  query = "주인공에게 일어난 일?",
  max_num_results=3
)

print("마지막 결말에 주인공에게 일어난 사건은?")
for data in response.data:
    print(f'Search Result Content:\n {data.content[0].text[:100]}') # 앞부분 100자만 출력
    print(f'Search Result Score:\n {data.score}')
    print()
print('---')
    
response = client.responses.create(
    model="gpt-5-nano",
    input="왜 제목이 '운수 좋은 날'일까요?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 2, # 최대 2개만
    }],
    reasoning={ "effort": "low" },
    text={ "verbosity": "low" },    
)

print("왜 제목이 '운수 좋은 날'일까요?")
print(response.output_text)
print('---')