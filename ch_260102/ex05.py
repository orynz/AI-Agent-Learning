# import matplotlib.pyplot as plt
# import pandas as pd


# plt.rcParams['font.family'] = "Malgun Gothic"
# plt.rcParams['axes.unicode_minus'] = False

# # API 수집 데이터 예시
# df = pd.DataFrame({
#     "views": [120, 180, 220, 260, 300, 340, 380, 420, 500, 560]
# })

# # 히스토그램 작성
# plt.hist(df["views"], bins=5)

# # 그래프 설정
# plt.title("기사 조회 수 분포")
# plt.xlabel("조회 수")
# plt.ylabel("기사 수")

# # plt.show()

# df = pd.DataFrame({
#     "media_A": [120, 200, 280, 360, 420],
#     "media_B": [80, 150, 230, 300, 390]
# })

# plt.hist(df["media_A"], bins=5, alpha=0.7, label="A신문")
# plt.hist(df["media_B"], bins=5, alpha=0.7, label="B신문")

# plt.title("매체별 조회 수 분포 비교")
# plt.xlabel("조회 수")
# plt.ylabel("기사 수")
# plt.legend(loc="upper right")

# plt.show()

# df = pd.DataFrame({
#     "media": ["A신문", "A신문", "B신문", "B신문"],
#     "views": [300, 420, 180, 260]
# })

# grouped = df.groupby("media")["views"].mean()

# grouped.plot(kind="bar", title="매체별 평균 조회 수")
# plt.xlabel("매체")
# plt.ylabel("평균 조회 수")

# # plt.figure(figsize=(10,4))

# plt.subplot(1,2,1)
# plt.hist(df["views"])
# plt.title("조회 수 분포")

# plt.subplot(1,2,2)
# grouped.plot(kind="bar")
# plt.title("매체별 평균 조회 수")

# plt.tight_layout()
# plt.show()


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta

# 한글 설정
plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False

# 재현성 유지
np.random.seed(42)

# 500개 기사 데이터 생성 (3개 미디어사)
n_articles = 500
media_list = ["A신문", "B신문", "C신문"]
categories = ["정치", "경제", "사회", "문화", "스포츠"]

# 날짜 생성 (2025년 1월 1일~3월 31일)
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 90)) for _ in range(n_articles)]

# 기사 조회 수: 미디어별 분포 차이를 반영
# A신문: 고화질 기사(평균 400, 표준편차 150)
# B신문: 중간 수준 (평균 280, 표준편차 120)
# C신문: 저조회 수 (평균 150, 표준편차 80) + 이상치 존재
views_A = np.random.normal(loc=400, scale=150, size=int(n_articles * 0.4))
views_B = np.random.normal(loc=280, scale=120, size=int(n_articles * 0.35))
views_C = np.random.normal(loc=150, scale=80, size=int(n_articles * 0.25))

# 이상치 삽입: C신문에 일부 가짜 급속 확산 기사 (5건)
fake_views_C = np.random.uniform(1200, 2500, 5)
views_C = np.concatenate([views_C, fake_views_C])

# 결합 및 매체 할당
all_views = np.concatenate([views_A, views_B, views_C])
media = np.repeat(media_list, [int(n_articles * 0.4), int(n_articles * 0.35), int(n_articles * 0.25) + 5])
category = np.random.choice(categories, size=len(all_views))
date = np.random.choice(dates, size=len(all_views))

# DataFrame 생성
df = pd.DataFrame({
    "article_id": range(1, len(all_views) + 1),
    "media": media,
    "category": category,
    "views": all_views,
    "publish_date": date
})

# 결측치 삽입 (5%)
df.loc[np.random.choice(df.index, size=int(len(df)*0.05), replace=False), "views"] = np.nan
df.loc[np.random.choice(df.index, size=int(len(df)*0.03), replace=False), "category"] = np.nan

# 중복 행 삽입 (3건)
duplicate = df.sample(n=3, random_state=42)
df = pd.concat([df, duplicate], ignore_index=True)

print(f"초기 데이터 크기: {df.shape}")
print("\n초기 데이터 샘플:")
print(df.head())
