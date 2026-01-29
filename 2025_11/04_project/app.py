# app.py
# Streamlit 기본 'Hello World' 예제

import streamlit as st

# 제목 출력
st.title("👋 Hello, Streamlit!")

# 간단한 텍스트
st.write("이 앱은 Streamlit으로 만든 첫 번째 웹앱입니다.")

# 버튼 눌러보기
if st.button("버튼 클릭"):
    st.success("버튼이 눌렸습니다! 🎉")