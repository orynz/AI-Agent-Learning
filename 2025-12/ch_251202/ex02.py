import pandas as pd
import matplotlib.pyplot as plt


# df = pd.read_csv("content_data.csv")
# print(df.head())                  # 미리보기(기본 5개)

# print("-" * 80)
# print(df["작성자"].value_counts())  # 작성자별 문서 갯수

# print("-" * 80)
# recent = df[df["날짜"] <= "2025-11-10"] # 2025-11-10 이전 데이터
# print(recent)

# print("-" * 80)
# recent = df[df["날짜"] >= "2025-11-10"]["제목"] # 2025-11-10 이전 데이터
# print(recent)

df = pd.read_csv("content_data.csv")
new_data = [["인공지능 활용", "홍길동", "2025-11-16", "멀티모달을 활용한 인공지능 교육이 확대 대고 있다."]]
df = df.apply(new_data)


df["글자수"] = df["본문"].apply(len)
print(df[["제목", "글자수"]])
print("평균 글자수:", df["글자수"].mean())

# plt.bar(df["제목"], df["글자수"])
# plt.xlabel("콘텐츠 제목")
# plt.ylabel("글자 수")
# plt.title("콘텐츠별 본문 길이 비교")
# plt.show()



