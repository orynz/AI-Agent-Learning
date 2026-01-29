from gpt_yf_functions import (
    get_current_time,
    get_yf_stock_info,
    get_yf_stock_history,
    get_yf_stock_recommendations,
    tools
)
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )
    return response

st.title("💬 Function Calling 자동화 챗봇")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 금융·정보 상담사다."}
    ]

for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = ai_response.choices[0].message
    print(ai_message)

    tool_calls = ai_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            arguments = json.loads(tool_call.function.arguments)

            if tool_name == "get_current_time":
                result = get_current_time(timezone=arguments["timezone"])
            elif tool_name == "get_yf_stock_info":
                result = get_yf_stock_info(ticker=arguments["ticker"])
            elif tool_name == "get_yf_stock_history":
                result = get_yf_stock_history(
                    ticker=arguments["ticker"],
                    period=arguments["period"]
                )
            elif tool_name == "get_yf_stock_recommendations":
                result = get_yf_stock_recommendations(
                    ticker=arguments["ticker"]
                )
            else:
                result = "지원하지 않는 도구입니다."

            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": result,
            })

        st.session_state.messages.append({
            "role": "system",
            "content": "이제 함수 실행 결과를 바탕으로 사용자에게 답변하라."
        })

        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message.content
    })

    st.chat_message("assistant").write(ai_message.content)


tools =[
    {
        "type": "function",
        "function":{
            "name": "함수명",
            "description":"함수관련 설명",
            "parameters":{
                    "type": "objet",
                    "properties":{
                        "ticker:"{
                            "type": "string"
                            "descriptions":"변수 설명(에)"                                                            
                        }
                    }
            }
        }
    }
]