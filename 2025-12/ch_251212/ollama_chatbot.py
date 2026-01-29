import streamlit as st
import requests

st.title("온디바이스(로컬) 챗봇: Streamlit + Ollama")

# 1) 대화 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2) 이전 대화 출력
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 3) 사용자 입력
user_text = st.chat_input("메시지를 입력하세요")

def ollama_chat(messages, model="qwen3:4b"):
    # Ollama 기본 엔드포인트(로컬)
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]

# 4) 응답 생성
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("로컬 모델이 답변 생성 중입니다..."):
            reply = ollama_chat(st.session_state.messages)
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
