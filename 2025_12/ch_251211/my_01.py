"""파일관리 : 백스토어 """

from openai import OpenAI

client = OpenAI()

# 파일 업로드
# response = client.files.create(
#     # 업로드 파일(필수)
#     file = open("A_Lucky_Day.txt", "rb"),
    
#     # 사용 목적(필수)
#     purpose = 'assistants'
    
#     # 파일 만료 설정(옵션)
#     expires_after = {
#         "anchor": "create_at",
#         "seconds": 3600 * 24  # 24시간 후 만료
#     }
# )

# 업로드된 파일 리스트
response = client.files.list()
for f in response.data:
    print(f"- ID: {f.id}, 이름: {f.filename}, 목적: {f.purpose}")

# # 'file ID'로 업로드된 파일 조회
# response = client.files.retrieve("file-ID")

# # 'file ID'로 업로드된 파일 삭제
# response = client.files.delete("file-ID")
# if response.deleted: # 삭제 완료시 True 반환
#     print("파일이 성공적으로 삭제되었습니다.")
    
# 'file ID'로 파일 내용 검색 - 생성된 파일의 내용을 확인할 때 사용
response = client.files.content("file-ID")
print(response.text)  # 파일 내용 출력
