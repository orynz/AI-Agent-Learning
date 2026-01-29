# app_no_function_calling.py
# Function Calling(도구 호출) 없이 실행되는 비교용 Streamlit 챗봇 예제

from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import requests

load_dotenv()


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_seoul_weather",
            "description": "서울(대한민국)의 현재 날씨를 조회하여 요약해서 반환합니다.",
            "parameters": {"type": "object", "properties": {}},
        },
    }
]

def get_seoul_weather() -> str:
    openweather_api = os.getenv("OPEN_WEATHER_API")
    if not(openweather_api):
        return "Invaild OpenWeather API Key."
    
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_api}"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Seoul,KR",
        "appid": openweather_api,
        "units": "mettic",
        "lang": "kr",
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        
        if r.status_code != 200:
            return f"OpenWeather API 오류: {r.status_code} / {r.text}"
        
        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"][0]["temp"]
        feels = data["main"][0]["feels_like"]
        hum = data["main"][0]["humidity"]
        wind = data["wind"][0]["speed"]
        
        return f"서울 현재 날씨: {desc}, 기온 {temp:.1f}°C(체감 {feels:.1f}°C), 습도 {hum}%, 풍속 {wind:.1f}m/s"
    except Exception as e:
        return f"날씨 조회 예외: {type(e).__name__}: {e}"



def get_ai_response(messages):
    # tools 파라미터를 사용하지 않음(= Function Calling 비활성)
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

st.title("Chatbot (No Function Calling)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "너는 도우미이다. 외부 함수나 도구를 호출할 수 없다. 사용자가 시간을 물어보면 일반적인 설명만 하고, 실제 현재 시각을 확정해서 말하지 않는다."
        }
    ]

# 이전 대화 출력
for msg in st.session_state.messages:
    if msg["role"] in ("assistant", "user"):
        st.chat_message(msg["role"]).write(msg.get("content", ""))

# 사용자 입력 처리
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 단일 호출로 답변 생성(도구 호출 없음)
    resp = get_ai_response(st.session_state.messages)
    ai_msg = resp.choices[0].message

    st.session_state.messages.append(ai_msg.model_dump())
    st.chat_message("assistant").write(ai_msg.content)