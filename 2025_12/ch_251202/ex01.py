import pandas as pd

filename = "content_data.csv"
data = [
    ["AI 활용 사례", "김하늘", "2025-11-13", "AI가 미디어 산업 전반에 확산되고 있다."],
    ["생성형 AI와 콘텐츠", "이도윤", "2025-11-12", "텍스트, 이미지, 오디오를 자동으로 생성하는 기술이 주목받고 있다."],
    ["AI 교육 혁신", "박지현", "2025-11-10", "학교 현장에서 맞춤형 학습이 가능해지고 있다."]
]

df = pd.DataFrame(data, columns=["제목", "작성자", "날짜", "본문"])
df.to_csv(filename, index=False)
print(f"'{filename}' 파일 변환 및 저장이 완료되었습니다.")