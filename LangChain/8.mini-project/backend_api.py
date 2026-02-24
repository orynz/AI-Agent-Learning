
import operator, time
from typing import Annotated, TypedDict, List
from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_community.callbacks.manager import get_openai_callback
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()


from pathlib import Path
BASE_DIR = Path(__file__).parent 
DATA_DIR = BASE_DIR / "data"

app = FastAPI()
GLOBAL_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
GLOBAL_EMBEDDINGS = OpenAIEmbeddings()
VECTOR_DB = None

def initialize_vector_db():
    """FAISS 백터 DB 초기화"""
    global VECTOR_DB, GLOBAL_EMBEDDINGS
    
    index_name = DATA_DIR / "memory_cached_index"
    
    target_files = ["(요약) 2025 한국 반려동물 보고서.pdf", "2025_당뇨병_진료지침.pdf", "반려동물_알레르기_예방관리수칙.pdf"]
    
    if Path.exists(index_name):
        print("✅ 기존 FAISS 인덱스를 메모리에 로드합니다.")
        VECTOR_DB = FAISS.load_local(str(index_name), GLOBAL_EMBEDDINGS, allow_dangerous_deserialization=True )

    else:
        print("📂 신규 PDF 인덱스를 생성합니다. (최초 1회 소요)")
        
        all_docs = []
        for f in target_files:
            if Path.exists(DATA_DIR / f):
                pdf_loader = PyPDFLoader(str(DATA_DIR / f))
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,     # 조각의 최대 길이 (일반적으로 500~1000자 설정)
                    chunk_overlap=50    # 조각 간의 중첩되는 영역 : 앞 조각의 마지막 내용 일부를 뒤 조각에 포함시켜 문맥이 끊기는 것을 방지
                )
                doc = pdf_loader.load_and_split(splitter)
                all_docs.extend(doc)
            else:
                print(f"해당 경로에 '{f}' 가 없습니다. Path: {DATA_DIR / f}")    
        
        if all_docs:
            VECTOR_DB = FAISS.from_documents(all_docs, GLOBAL_EMBEDDINGS)
            VECTOR_DB.save_local(str(index_name))
            print("PDF 인덱스 생성 및 메모리 로드 완료!")
        else:
            print("PDF 파일이 없습니다.")
            
initialize_vector_db()

@tool
def search_local_knowledge(query: str):
    """로컬 지식 검색: FAISS 벡터 DB에서 관련 문서를 검색하여 반환"""
    
    if VECTOR_DB is None:
        return "로컬 지식 베이스가 로드되지 않았습니다."
    
    docs = VECTOR_DB.similarity_search(query=query, k=2)
    print("============= 로컬 지식 검색 Tool 사용중...")
    # return "\n\n".join([d.page_content for d in docs])
    return "\n\n".join([f"[출처:{d.metadata.get('page')}p] {d.page_content}" for d in docs])
    

@tool
def search_web_integrated(query: str):
    """웹 검색 및 요약: Tavily 검색 결과를 요약하여 반환"""
    search = TavilySearchResults(max_results=2)
    raw_data = search.run(query)
    refining_prompt = f"질문 {query}에 대한 핵심 내용만 검색 결과에서 3문장 요약: {raw_data}"
    summary = GLOBAL_LLM.invoke(refining_prompt).content
    print("============= 웹 검색 및 요약 Tool 사용중...")
    return summary

tools = [search_local_knowledge, search_web_integrated]
llm_with_tools = GLOBAL_LLM.bind_tools(tools=tools)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    
def call_model(state: AgentState):
    msg = SystemMessage(content="반려동물/당뇨병 전문 상담사입니다.")
    return {"messages": [llm_with_tools.invoke([msg] + state['messages'])]}

def check(state: AgentState):
    
    if state["messages"][-1].tool_calls:
        return "ACTION"
    else:
        return "END"

# 워크 플로우 구성
builder = StateGraph(AgentState)

# 작업 추가
builder.add_node("agent", call_model)
builder.add_node("action", ToolNode(tools=tools))

# 진행 순서
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    check,
    {
        "ACTION" : "action",
        "END" : END
    }
)

builder.add_edge("action", "agent")

graph_engine = builder.compile()


@app.post("/ask")
async def ask_api(query: str):
    with get_openai_callback() as cb:
        start_time = time.perf_counter()
        result = graph_engine.invoke({"messages": [HumanMessage(content=query)]})
        return {
            "answer": result["messages"][-1].content,
            "stats": {
                "latency": time.perf_counter() - start_time, # 응답 속도
                "prompt_tokens": cb.prompt_tokens,
                "completion_tokens": cb.completion_tokens,
                "total_tokens": cb.total_tokens,
                "total_cost": cb.total_cost,
                "timestamp": time.strftime("%Y%m%d_%H%M%S")
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)