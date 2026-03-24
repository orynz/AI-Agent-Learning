import streamlit as st
from transformers import pipeline
import torch
import matplotlib.pyplot as plt
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="감정 분석 및 시각화", page_icon="😊", layout="wide")

# matplotlib 한글 폰트 설정 (선택 사항, 필요시)
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 모델 로드 (캐싱을 통해 속도 향상)
@st.cache_resource
def load_classifier():
    return pipeline(
        task="text-classification",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=(0 if torch.cuda.is_available() else -1)
    )

def main():
    st.title("🎭 Hugging Face 감정 분석기 & 시각화")
    st.info("문장을 입력하면 AI가 1(부정)에서 5(긍정) 사이의 별점으로 감정을 분석하고, 전체 분포를 시각화합니다.")

    # 사용자 입력 UI
    st.subheader("분석할 문장 입력")
    user_input = st.text_area(
        "분석하고 싶은 문장들을 입력하세요. (한 줄에 한 문장씩 입력)",
        placeholder="예시:\n이 영화 정말 재미있어요!\n배송이 너무 늦어서 실망했습니다.\n그냥 평범한 하루였습니다.",
        height=200
    )

    # 분석 버튼
    if st.button("분석 및 시각화 시작"):
        if not user_input.strip():
            st.warning("분석할 내용을 입력해주세요.")
            return

        # 문장 분리 및 전처리
        sentences = [s.strip() for s in user_input.split('\n') if s.strip()]
        
        with st.spinner("AI가 감정을 분석 중입니다..."):
            classifier = load_classifier()
            results = classifier(sentences)

        # 데이터 준비
        star_counts = [int(r['label'].split()[0]) for r in results]
        
        # UI 레이아웃 분할 (결과 목록과 시각화를 나란히 배치)
        col_results, col_viz = st.columns([1, 1])

        with col_results:
            st.subheader("상세 분석 결과")
            for i, (sentence, result) in enumerate(zip(sentences, results), start=1):
                label = result['label']  # 예: "1 star", "5 stars"
                score = result['score']  # 신뢰도 확률
                
                # 별점에 따른 이모지 설정
                star_count = int(label.split()[0])
                stars = "⭐" * star_count
                
                # 결과 박스
                with st.expander(f"{i}. {sentence[:30]}...", expanded=True):
                    st.write(f"**문장:** {sentence}")
                    st.write(f"**결과:** {stars} ({label})")
                    st.write(f"**확률:** {score:.2%}")

        with col_viz:
            st.subheader("종합 통계 및 시각화")
            
            # 요약 정보
            average_score = sum(star_counts) / len(star_counts)
            st.metric(label="전체 평균 별점", value=f"{average_score:.1f} / 5.0")

            # Matplotlib 시각화
            st.markdown("### 감정 별점 분포")
            
            # 별점별 빈도수 계산
            data = pd.DataFrame({'star': [1, 2, 3, 4, 5], 'count': [0, 0, 0, 0, 0]})
            for s in star_counts:
                data.loc[data['star'] == s, 'count'] += 1

            fig, ax = plt.subplots(figsize=(8, 5))
            
            # 별점에 따른 색상 설정 (부정->긍정: 빨강->초록 계열)
            colors = ['#ff9999', '#ffb3b3', '#ffff99', '#99ff99', '#66ff66']
            bars = ax.bar(data['star'], data['count'], color=colors, edgecolor='grey')

            # 그래프 세부 설정
            ax.set_title("감정 별점 분포", fontsize=16)
            ax.set_xlabel("별점 (1: 매우 부정 ~ 5: 매우 긍정)", fontsize=12)
            ax.set_ylabel("문장 개수", fontsize=12)
            ax.set_xticks([1, 2, 3, 4, 5])
            
            # 막대 위에 숫자 표시
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=10)
            
            # 스트림릿에 그래프 출력
            st.pyplot(fig)

if __name__ == "__main__":
    main()