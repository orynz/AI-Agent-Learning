
import matplotlib.pyplot as plt
import pandas as pd

# 한글 폰트 설정 - 맑은 고딕
plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False

# 매체별 기사 수 예시 데이터
df = pd.DataFrame({
    "media": ["A신문", "B신문", "C신문", "D신문"],
    "article_count": [25, 40, 15, 30]
})

# 막대 그래프 작성
plt.bar(df["media"], df["article_count"])

# 그래프 정보 설정
plt.title("매체별 기사 수 비교")
plt.xlabel("매체")
plt.ylabel("기사 수")

# 그래프 출력
plt.show()