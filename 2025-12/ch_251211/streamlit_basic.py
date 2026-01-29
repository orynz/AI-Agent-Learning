import streamlit as st
from openai import OpenAI
import os

# # 사이드바에서 API 키 가져오기
with st.sidebar:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # 필요하다면 직접 입력 방식으로 바꿀 수 있음
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    
    
st.title("왜 왔어? 까필한 상담사!👋")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role" : "system", "content" : "당신은 다른 불필요한 설명은 하지 않지만, 그 안에 상대방을 존중하고 배려하며 공감하는 30년 경력의 매우 까칠한 상담사입니다. 최대한 짧게 무조건 반말로 답하세요!"},
        {"role": "assistant", "content": "왜왔니? 뭐가 문제야?"}
    ]

# (2) 기존 대화 내용을 화면에 출력
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# (3) 사용자 입력을 받아 대화에 추가하고 OpenAI로부터 응답 받기
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 사용자 메시지를 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 누적된 대화 내용을 모두 전달하여 응답 생성
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages,
    )
    msg = response.choices[0].message.content

    # AI 응답을 대화 기록에 추가하고 화면에 출력
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
