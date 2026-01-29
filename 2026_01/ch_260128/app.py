import os
import streamlit as st
from typing import List, Dict, Any

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 설정
IS_STREAMING = True
PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "rag_docs"

# OpenAI 설정
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# LLM 초기화
answer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, streaming=IS_STREAMING)
rewrite_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# 프롬프트 템플릿
answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "문서 기반 질의응답 도우미입니다. 컨텍스트에 포함된 내용만으로 답변합니다. "
     "추정, 상상, 일반상식 보강을 금지합니다. "
     "컨텍스트에 근거 문장이 없으면 '문서에서 확인되지 않았습니다.'라고 답변합니다. "
     "답변은 항목형으로 6줄 이내로 작성합니다."),
    ("user", "질문: {question}\n\n컨텍스트:\n{context}\n\n답변:")
])

rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "# Role"
        "orean Search Query Optimizer"

        "# Objective"
        "Refine user input into specific search keywords for a Korean database."

        "# Rules"
        "1. Remove conversational fillers."
        "2. Resolve ambiguity and expand context."
        "3. **Translate and output strictly in KOREAN.**"
        "4. Output ONLY the refined query string."
    ),
    ("user", "원 질문: {q}\n재작성 질문:")
])

# 파서
parser = StrOutputParser()

# 체인 구성
answer_chain = answer_prompt | answer_llm | parser
rewrite_chain = rewrite_prompt | rewrite_llm | parser

# 문서 포맷팅 및 출처 추출
def format_docs(docs: List[Any]) -> str:
    """문서 리스트를 검색 컨텍스트 문자열로 변환"""
    lines = []
    for d in docs:
        src = d.metadata.get("source", "알 수 없음")
        page = d.metadata.get("page", "알 수 없음")
        lines.append(f"(source={src}, page={page}) {d.page_content}")
    return "\n\n".join(lines)

def build_sources(docs: List[Any]) -> List[Dict[str, Any]]:
    """중복된 출처를 제거하고 유일한 출처 목록 생성"""
    seen = set()
    sources = []
    for d in docs:
        src = d.metadata.get("source", "")
        page = d.metadata.get("page", "")
        key = (src, page)
        if key not in seen:
            seen.add(key)
            sources.append({"source": src, "page": page})
    return sources

# 메인 애플리케이션
def main():
    st.set_page_config(page_title="RAG 문서 기반 챗봇", layout="wide")
    st.title("RAG 문서 기반 챗봇")

    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY 환경변수가 필요합니다.")
        st.stop()

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 사용자 입력
    if user_input := st.chat_input("질문을 입력하세요."):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # 질문 재작성
        try:
            expanded_query = rewrite_chain.invoke({"q": user_input}).strip()
            if not expanded_query:
                raise ValueError("재작성 질문이 비어 있습니다.")
        except Exception as e:
            expanded_query = user_input  # 실패 시 원본 사용
            st.warning(f"질문 재작성 실패: {e}")

        # 검색
        try:
            docs = retriever.invoke(expanded_query)
            if not docs:
                context = ""
                st.warning("검색 결과가 없습니다.")
            else:
                context = format_docs(docs)
        except Exception as e:
            st.error(f"검색 중 오류 발생: {e}")
            context = ""

        # 답변 생성
        with st.chat_message("assistant"):
            st.caption(f"재작성 질문: {expanded_query}")

            if IS_STREAMING:
                placeholder = st.empty()
                tokens = []
                try:
                    for chunk in answer_chain.stream({"question": expanded_query, "context": context}):
                        tokens.append(chunk)
                        placeholder.write("".join(tokens))
                    answer = "".join(tokens)
                except Exception as e:
                    answer = "답변 생성 중 오류가 발생했습니다."
                    st.error(f"답변 생성 오류: {e}")
            else:
                try:
                    answer = answer_chain.invoke({"question": expanded_query, "context": context})
                except Exception as e:
                    answer = "답변 생성 중 오류가 발생했습니다."
                    st.error(f"답변 생성 오류: {e}")

            st.session_state.messages.append({"role": "assistant", "content": answer})

        # 출처 표시
        if "문서에서 확인되지 않았습니다." not in answer:
            sources = build_sources(docs)
            st.write("🔍 **자료 출처:**")
            if sources:
                st.dataframe(sources, use_container_width=True)
            else:
                st.write("출처 정보가 없습니다.")

    # 하단 정보 표시
    st.caption(f"📦 컬렉션 이름: {vectorstore._collection.name}")
    st.caption(f"📄 컬렉션 문서 수: {vectorstore._collection.count()}")
    st.caption(f"📁 persist 경로(절대): {os.path.abspath(PERSIST_DIR)}")

if __name__ == "__main__":
    main()