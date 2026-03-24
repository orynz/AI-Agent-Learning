import streamlit as st
from transformers import pipeline
import torch

from dotenv import load_dotenv
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="감정 분석 도구", page_icon="😊")

# 모델 로드 (캐싱을 통해 속도 향상)
@st.cache_resource
def load_classifier():
    return pipeline(
        task="text-classification",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=(0 if torch.cuda.is_available() else -1)
    )

def main():
    st.title("🎭 Hugging Face 감정 분석기")
    st.info("문장을 입력하면 AI가 1(부정)에서 5(긍정) 사이의 별점으로 감정을 분석합니다.")

    # 사용자 입력 UI
    st.subheader("분석할 문장 입력")
    user_input = st.text_area(
        "분석하고 싶은 문장들을 입력하세요. (한 줄에 한 문장씩 입력)",
        placeholder="예시:\n이 영화 정말 재미있어요!\n배송이 너무 늦어서 실망했습니다.",
        height=200
    )

    # 분석 버튼
    if st.button("분석 시작"):
        if not user_input.strip():
            st.warning("분석할 내용을 입력해주세요.")
            return

        # 문장 분리 및 전처리
        sentences = [s.strip() for s in user_input.split('\n') if s.strip()]
        
        with st.spinner("AI가 감정을 분석 중입니다..."):
            classifier = load_classifier()
            results = classifier(sentences)

        # 결과 출력
        st.subheader("분석 결과")
        
        for i, (sentence, result) in enumerate(zip(sentences, results), start=1):
            label = result['label']  # 예: "1 star", "5 stars"
            score = result['score']  # 신뢰도 확률
            
            # 별점에 따른 이모지 설정
            star_count = int(label.split()[0])
            stars = "⭐" * star_count
            
            # 가독성 있는 결과 박스
            with st.expander(f"{i}. {sentence[:30]}...", expanded=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**문장:** {sentence}")
                col2.write(f"**결과:** {stars}")
                col3.write(f"**확률:** {score:.2%}")

if __name__ == "__main__":
    main()