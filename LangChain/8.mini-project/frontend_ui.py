import streamlit as st 
import requests, time
import pandas as pd
from io import BytesIO
from gtts import gTTS
from langsmith import Client

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
BASE_DIR = Path(__file__).parent 
DATA_DIR = BASE_DIR / "data"

def now() -> str:
    # 년월일_시분초
    return time.strftime("%Y%m%d_%H%M%S") 
    
@st.cache_resource
def get_langsmith_client():
    """LangSmith 클라이언트를 싱글톤으로 캐싱"""
    return Client()

langsmith_client = get_langsmith_client()

@st.cache_data(show_spinner="음성을 생성 중입니다...")
def get_tts_audio(text):
    """텍스트를 음성으로 변환하고 바이너리 데이터를 캐싱"""
    if not text:
        return None
    
    tts = gTTS(text=text[:300], lang="ko")
    v_buf = BytesIO()
    tts.write_to_fp(v_buf)
    return v_buf.getvalue() # 바이너리 데이터 반환

# UI --------------------------------------------------------------------------
st.set_page_config(page_title="Expert Admin V13", layout="wide")

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "last_answer" not in st.session_state: st.session_state.last_answer = None
if "stats_log" not in st.session_state: st.session_state.stats_log = []

# 사이드바 관리 메뉴
with st.sidebar:
    st.header("🎛️ 에이전트 설정")
    menu = st.selectbox("메뉴 선택", ["전문가 상담실", "운영 통계 대쉬보드"])
    st.divider()
    if st.button("모든 로그 초기화"):
        st.session_state.chat_history = [];
        st.session_state.stats_log = []; 
        st.session_state.last_answer = None
        st.rerun()

if menu == "전문가 상담실":
    st.title("👨‍⚕️ 실시간 통합 상담 센터")
    
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(content)
        
    if prompt := st.chat_input(placeholder="질문을 입력하세요..."):
        st.session_state.chat_history.append(("user", prompt))
        
        with st.chat_message("user"): 
            st.write(prompt)
            
        with st.spinner("백엔드 엔진에서 지식을 추출중..."):
            res = requests.post("http://127.0.0.1:8000/ask", params={"query": prompt})
            if res.status_code == 200:
                data = res.json()
                st.session_state.last_answer = data["answer"]
                st.session_state.chat_history.append(("assistant", data["answer"]))
                st.session_state.stats_log.append(data["stats"])
                st.rerun()
    
    if st.session_state.last_answer:
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "📑 AI 전문가 최종 리포트",
                st.session_state.last_answer,
                file_name=f"report_{now()}.md"
            )
            
        with col2:
            audio_data = get_tts_audio(st.session_state.last_answer[:300])
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

                st.download_button(
                    label="🔊 MP3 [다운로드]", 
                    data=audio_data, 
                    file_name=f"voice_{now()}.mp3",
                    mime="audio/mp3",
                    key="btn_audio_down"
                )
                            
elif menu == "운영 통계 대쉬보드":
    st.title("📊 통합 운영 관제")

    if st.session_state.stats_log:
        df = pd.DataFrame(st.session_state.stats_log)

        m1, m2, m3 = st.columns(3)
        m1.metric("평균 응답 시간", f"{df['latency'].mean():.2f}s", delta=f"{df['latency'].iloc[-1] - df['latency'].mean():.2f}s", delta_color="inverse")
        m2.metric("총 토근 사용량", f"{df['total_tokens'].sum()}")
        m3.metric("총 비용", f"{df['total_cost'].sum():.4f}$")
        
        st.divider()
        
        # [시각화 강화] 처리 속도 및 토큰 소모량 그래프
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("⏱️ 응답 시간 추이 (Latency)")
            st.line_chart(df.set_index("timestamp")["latency"])
            st.caption("질문별 소요 시간의 변화를 보여줍니다.")

        with col_right:
            st.subheader("🪙 토큰 사용 효율성")
            st.bar_chart(df.set_index("timestamp")["total_tokens"])
            st.caption("요청당 소모된 토큰량을 비교합니다.")

        #  상세 세션 로그 리포트 테이블 / 비용 요약
        st.dataframe(df, use_container_width=True)
        st.info(f"💡 현재까지 총 {len(df)}건의 요청을 처리했으며, 평균 비용은 요청당 ${df['total_cost'].mean():.6f} 입니다.")
        
    else:
        st.info("통계 데이터가 없습니다.")
