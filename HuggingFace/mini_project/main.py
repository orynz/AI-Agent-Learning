import os
import json
import asyncio
import httpx
from typing import TypedDict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph

# [1] 설정 로드: API 키와 환경 변수 관리
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# [2] FastAPI 서비스 객체 생성 및 정적 경로 설정
app = FastAPI()
# static 폴더 안의 CSS 파일을 브라우저가 읽을 수 있게 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# [3] AI 모델 초기화 (속도와 정확도의 밸런스가 좋은 gpt-4o-mini)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# [4] 데이터 통로 정의 (에이전트가 들고 다닐 바구니)
class AgentState(TypedDict):
    user_input: str      # 사용자 질문
    emotion: dict        # 분석된 감정 데이터
    genre: int           # 결정된 영화 장르 코드
    recommendations: list # 최종 추천 리스트

import re
# [5] 감정 분석 도구: 심리학자 페르소나 강화
@tool
async def emotion_tool(text: str) -> dict:
    """사용자의 심리를 분석하여 따뜻한 공감 문장을 생성합니다."""
    
    # 1. 프롬프트 최적화 (구조화 및 명확성)
    prompt = f"""
        Role: 30-year experience Psych PhD and Movie Therapist.
        Task: Analyze the emotional state from the input text and provide a comforting message using movie metaphors or reasoning.
        Input Text: <text>{text}</text>
        
        Style: 
        - Short-breath, vertical-friendly sentences.
        - Warm, professional yet empathetic tone.
        
        Constraint: 
        - Output MUST be a valid JSON object ONLY.
        - No conversational filler before or after the JSON.
        - Language: Korean.

        TMDB genre codes: 
        28=Action, 12=Adventure, 16=Animation, 35=Comedy, 80=Crime,
        99=Documentary, 18=Drama, 10751=Family, 14=Fantasy, 36=History,
        27=Horror, 10402=Music, 9648=Mystery, 10749=Romance, 878=Science Fiction,
        10770=TV Movie, 53=Thriller, 10752=War, 37=Western,
        
        US Certification: G(전체), PG(7세+), PG-13(13세+), R(17세+)
        
        Output: valid JSON ONLY
        {{
            "감정": "행복|슬픔|분노|설렘|기본",
            "공감멘트": "따뜻한 공감 문장 (2-3줄)",
            "age_group": "어린이|청소년|성인|전체" or null,
            "certification": "G|PG|PG-13|R" or null,
            "themes": ["테마1", "테마2"],
            "genre_codes": [장르코드1, 장르코드2],
            "sort_by": "popularity.desc|vote_average.desc|primary_release_date.desc",
            "vote_average_gte": 평점(10점 만점)
        }}
    """
    
    try:
        res = await llm.ainvoke(prompt)
        content = res.content.strip()

        # 2. 정규표현식을 이용한 JSON 추출 (코드 블록 방어)
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            print(json_str)
            return json.loads(json_str)
        else:
            raise ValueError("No JSON found in response")

    except Exception as e:
        print(f"Error in emotion_tool: {e}")
        # 3. 사용자 경험을 위한 기본 공감 멘트 설정
        return {
            "감정": "기본", 
            "공감멘트": "마음이 머무는 곳을 찬찬히 살펴보고 있어요.\n당신의 이야기에 귀를 기울이고 있답니다."
        }

# [6] 영화 추천 도구: 고득점 명작 위주
@tool
async def recommend_tool(genre: int, emotion: dict) -> list:
    """TMDB에서 검증된 명작 5편을 가져옵니다."""
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://api.themoviedb.org/3/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_genres": genre,
                "vote_average.gte": 7.0,      # 평점 7점 이상만
                "sort_by": "popularity.desc",  # 인기순 정렬
                "vote_count.gte": 200, # 최소 투표수  
            }
        )
        data = res.json()
        # 프론트엔드 디자인을 위해 데이터를 정제해서 보냄
        return [{
            "title": m["title"],
            "desc": m.get("overview", "설명 없음"),
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
            "rating": round(m.get("vote_average", 0), 1),
            "sentiment": emotion.get("감정", "기본"),
            "reason": emotion.get("공감멘트", "당신에게 어울리는 영화를 찾았어요.")
        } for m in data.get("results", [])[:3]]

# [7] 에이전트 노드 구성 (생략 없이 연결)
async def emotion_node(state: AgentState):
    return {**state, "emotion": await emotion_tool.ainvoke({"text": state["user_input"]})}

async def genre_node(state: AgentState):
    emotion_data = state["emotion"]
    
    # LLM이 이미 genre_codes를 반환 → 매핑 불필요
    genre_codes = emotion_data.get("genre_codes", [12])
    
    # 여러 장르를 OR 조건으로 결합 (TMDB: | 구분자)
    genre_str = "|".join(str(g) for g in genre_codes)
    
    return {**state, "genre": genre_str}

async def recommend_node(state: AgentState):
    emotion = state["emotion"]
    
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ko-KR",
        "with_genres": state["genre"],
        "vote_average.gte": emotion.get("vote_average_gte", 7.0),
        "vote_count.gte": 200,          # 낚시 영화 방지
        "sort_by": emotion.get("sort_by", "popularity.desc"),
    }
    
    # 나이 등급 필터 (7세 아이 → G 또는 PG)
    if emotion.get("certification"):
        params["certification_country"] = "US"
        params["certification.lte"] = emotion["certification"]
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://api.themoviedb.org/3/discover/movie",
            params=params
        )
        data = res.json()
        return {**state, "recommendations": [{
            "title": m["title"],
            "desc": m.get("overview", "설명 없음"),
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
            "rating": round(m.get("vote_average", 0), 1),
            "sentiment": emotion.get("감정", "기본"),
            "themes": emotion.get("themes", []),
            "reason": emotion.get("공감멘트", "")
        } for m in data.get("results", [])[:5]]}

# [8] 그래프 빌드: 시작 -> 감정분석 -> 장르결정 -> 영화추천 -> 종료
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("emotion", emotion_node)
    workflow.add_node("genre", genre_node)
    workflow.add_node("recommend", recommend_node)
    workflow.set_entry_point("emotion")
    workflow.add_edge("emotion", "genre")
    workflow.add_edge("genre", "recommend")
    workflow.set_finish_point("recommend")
    return workflow.compile()

graph = build_graph()

# [9] 웹 라우팅 설정
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat_stream")
async def chat_stream(prompt: str):
    async def generator():
        result = await graph.ainvoke({"user_input": prompt})
        # SSE(Server-Sent Events) 형식으로 데이터를 실시간 전송
        yield f"data: {json.dumps({'status':'processing', 'data':result['recommendations']}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'status':'complete'})}\n\n"
    return StreamingResponse(generator(), media_type="text/event-stream")
