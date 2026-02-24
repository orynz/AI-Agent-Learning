# AI-Agent-Learning 🤖

AI 에이전트 개발과 데이터 분석, 웹 개발 학습 기록 저장소입니다.
날짜별로 진행한 학습 내용과 실습 코드를 정리하고 있습니다.

---

## 📚 프로젝트 개요

- **목표**: AI 에이전트, LLM, 웹 크롤링, 데이터 분석 등 다양한 분야의 실무 기술 습득
- **주요 주제**: Python, FastAPI, Streamlit, LLM 활용, 데이터 처리, 웹 개발
- **학습 기간**: 2025년 11월 ~ 현재

---

## 🛠️ 기술 스택

### 백엔드

- **Python**: 메인 프로그래밍 언어
- **FastAPI**: 고성능 웹 API 프레임워크
- **Flask**: 웹 애플리케이션 프레임워크
- **Streamlit**: 데이터 시각화 및 웹앱 프레임워크

### 데이터 처리

- **Pandas**: 데이터 프레임 처리
- **NumPy**: 수치 계산
- **Matplotlib, Seaborn**: 데이터 시각화
- **BeautifulSoup**: 웹 크롤링

### LLM & AI

- **LangChain**: LLM 애플리케이션 개발
- **Ollama**: 로컬 LLM 실행
- **OpenAI API**: GPT 활용

### 기타

- **MySQL**: 데이터베이스
- **SQLAlchemy**: ORM
- **Whisper**: 음성 인식
- **ChromaDB**: 벡터 DB

---

## 📅 2026년 학습 내용

### LangChain/8.mini-project (2월 23일)

> 통합 상담 센터 미니 프로젝트 (FastAPI + Streamlit + LangGraph)

- **Backend (FastAPI & LangGraph)**:
  - FAISS 기반 로컬 지식 검색(PDF 문서) 및 Tavily 웹 검색 툴을 활용하는 에이전트 구축
  - `StateGraph`를 통한 워크플로우 구성 및 FastAPI 서빙 (`backend_api.py`)
- **Frontend (Streamlit)**:
  - 실시간 채팅 UI 및 다운로드 가능한 TTS(음성 변환) 리포트 제공 (`frontend_ui.py`)
  - 통계 데이터 수집 및 대시보드 시각화(응답 시간, 토큰 사용량) 구현

### LangChain/03_RAG, 6.Graph, 7.FastAPI (2월 20일)

> FAISS 기반 RAG 시스템 및 LangGraph 시각화 워크플로우 통제, FastAPI 유저 모델 관리 실습

- **RAG 및 벡터 DB 활용 (FAISS)**
  - 기초 문서 분할(`RecursiveCharacterTextSplitter`) 및 임베딩(`OpenAIEmbeddings`) 데이터 FAISS 저장소 활용 (`4-1.faissdb_text.py`)
  - 웹 데이터를 크롤링하고 정제하여 FastAPI 컨텍스트 기반 QA 서비스 구축 (`7.FastAPI/rag_server.py`)
- **LangGraph 기반 병렬 및 조건부 워크플로우 구현**
  - 기획, 제작, 검수, 배달, 에러 처리 등의 노드로 구성된 협업 시뮬레이션 (`6-1.failsystemupdate.py`, `7-1.Parallel.py`)
  - `Pillow`를 통해 상태 바인딩 다이어그램 경로 시각화 및 Streamlit UI 적용
- **FastAPI 백엔드 개발 (CRUD)**
  - Pydantic 모델 검증 및 SQLite 연동을 통해 사용자(User) 데이터 관리 API 작성 (`7.FastAPI/routers/users.py`)

### LangChain/7.FastAPI & 6.Graph (2월 19일)

> FastAPI 기초 및 LangGraph 심화 기능

- **LangGraph Advanced**:
  - **Trace**: Agent 실행 경로 추적 및 시각화 (`4.trace.py`)
  - **Scoring**: 단계별 점수 산정 및 평가 시스템 (`5.score.py`)
  - **Error Handling**: 에러 발생 시 조건부 분기 및 위기관리부 운영 (`6.fail-system.py`)
- **FastAPI Basics**:
  - 기본 서버 구동 및 데이터 모델링 (Pydantic, TypedDict) (`fa-01` ~ `fa-06`)
  - HTTP 예외 처리 및 데이터 검증 (`fa-07`)

### LangChain/99_homework (2월 14일)

> LangGraph Advanced: Parallel Execution & Error Handling

- **Parallel Execution**: 기획(Planner) 이후 요리(Cook)와 홍보(Marketing)의 병렬 처리 구현 (`studyEx03.py`)
- **Error Handling**: 제작부의 에러(재료 부족) 발생 시 위기관리부(Error Handler)를 통한 복구 및 재시도 루프
- **Visualization**: Streamlit을 활용한 실시간 로그 모니터링 및 Mermaid 워크플로우 시각화

### LangChain/6.Graph (2월 13일)

> LangGraph Basics: Visualization & Conditional Edges

- **Custom Visualization**: `PIL`을 활용하여 에이전트 실행 경로와 점수를 시각적으로 표현 (`7.parallel.py`)
- **Conditional Logic**: `lambda` 함수를 이용한 동적 분기(Error Handler vs Reviewer) 처리

### LangChain/6.Graph (2월 12일)

> LangGraph State Management & Workflow

- **StateGraph**: `StateGraph`를 활용한 상태 기반 애플리케이션 구조 설계 (`1.plantest.py`)
- **Multi-Agent Flow**: 기획 -> 제작 -> 검수 부서로 이어지는 멀티 에이전트 워크플로우 구현 (`2.payment.py`)
- **Conditional Edge**: `add_conditional_edges`를 활용한 피드백 루프 및 조건부 라우팅 (Retry/Finish) (`3.feedback.py`)

### LangChain/05_Agent (2월 11일)

> LangChain Agent 기초: Tool Binding, Reasoning, Execution

- **Agent Basics**: `create_openai_functions_agent`를 활용한 에이전트 생성 및 실행 (`1.cal.py`, `2.binding.py`)
- **Reasoning**: 에이전트의 사고 과정(Chain of Thought) 이해 (`3.thought.py`)
- **Custom Tools**: `@tool` 데코레이터를 활용한 요리 도구 정의 (`5.cook_tool.py`)
- **Planning**: 복잡한 작업(요리 계획 등)을 수행하는 에이전트 실습 (`4.cook_plan.py`)

### LangChain/04_Multi_Modal_RAG (2월 10일)

> 멀티모달(이미지) 데이터 처리 및 RAG

- **Image Processing**: 이미지 파일 로딩 및 분석 (`1-1.image_read.py`)
- **Image RAG**: 이미지를 포함한 질문에 대한 답변 생성 및 정보 검색 (`1-2.image_rag.py`)

### LangChain/03_RAG (2월 10일)

> RAG(Retrieval-Augmented Generation) 파이프라인 구축 기초

- **Document Loading**: PDF 문서 로드 및 전처리 (`1.read_pdf.py`, `SamsungMemoryReaderPDF.py`)
- **Text Splitting**: 효율적인 검색을 위한 문서 분할 전략 (`2.splittest.py`)
- **Embedding & Vector Store**: 텍스트 임베딩 생성 및 FAISS 벡터 DB 구축 (`3.text_embedding.py`, `4.faissdb*.py`)

### LangChain/02_Memory (2월 9일)

> Streamlit을 활용한 대화형 에이전트 및 RAG 기초

- **Streamlit 통합**: Streamlit을 활용하여 Chat Interface 구축 (`9.streamlit.py`, `10.userselect.py`)
- **Runnable & History**: `RunnableWithMessageHistory`를 활용한 대화 기록 관리 심화 (`7.runnalbewithchathistory.py`)
- **유틸리티**: TOML 설정 파일 관리 및 공통 함수 분리 (`8.convert_toml.py`, `callfunction.py`)

### LangChain/01_Basic & 02_Memory (2월 6일)

> LangChain 프롬프트 템플릿 및 메모리 시스템 기초

- **Prompt Template**: `PromptTemplate`, `ChatPromptTemplate` 활용 및 역할(Role) 설정 (`6.prompt.py`, `7.role.py`)
- **Memory System**:
  - **Stateless vs Stateful**: 체인 비교 (`1.nomemory.py`)
  - **Memory Types**: Buffer, Window, History Class 등 다양한 메모리 유형 실습
  - **Context Injection**: `MessagesPlaceholder` 활용

### LangChain/01_Basic (2월 5일)

> LCEL(LangChain Expression Language) 기초 및 활용

- **LCEL 기초**: 프롬프트, 모델, 파서 연결 및 체인 구성 (`1.LCEL.py`)
- **데이터 전달**: `invoke`를 통한 파라미터 전달 및 딕셔너리 활용 (`3.param.py`)
- **체인 결합**: 여러 체인을 연결하여 복합적인 로직 구현 (`4.combine.py`)
- **실습**: 번역 에이전트 구현 (`5.translation.py`)

### 2026_02/ch_260204 (2월 4일)

> Express 심화: Bootstrap, MongoDB 연동 및 파일 업로드

- **Bootstrap & EJS**: Bootstrap을 활용한 UI 구성 및 Express View Engine(EJS) 연동
- **MongoDB**: In-Memory 데이터 관리를 MongoDB로 마이그레이션 (Native Driver 사용)
- **File Upload**: 이미지 업로드 기능 구현 및 정적 파일 서빙 설정 (서버 모듈 분리)

### 2026_02/ch_260203 (2월 3일)

> 🤖 자동 코치 에이전트 (Agent Coach) 시뮬레이션

- **에이전틱 워크플로우**: [Plan → Execute → Verify] 구조의 에이전트 사고 흐름 구현
- **진단 프로세스**:
  - 규칙 기반 진단: 정규표현식을 활용한 실무 실수 패턴 분석
  - Trace 시스템: 에이전트의 내부 판단 과정을 단계별로그로 시각화
  - 상태 관리: 완료(DONE), 정보 부족(NEED_INFO), 실패(FAIL) 등의 상태 처리
- **환경 구성**: Node.js, Docker 환경에서의 과제 자동 진단 시뮬레이션

### 2026_02/ch_260202 (2월 2일)

> Docker CLI 및 Express 미들웨어/EJS 기초

- **Docker**: Docker CLI 가이드 및 컨테이너 관리 명령어 실습
- **Node.js**:
  - EJS 템플릿 엔진 기초 (데이터 전달, 제어문)
  - Express 미들웨어 (Middleware) 개념 및 활용
  - Express 애플리케이션 구조 및 라우팅 실습

### 2026_01/ch_260130 (1월 30일)

> Express와 EJS를 활용한 사용자 관리 CRUD 실습

- Express Framework를 활용한 RESTful 라우팅 구현 (GET, Redirect)
- EJS 템플릿 엔진을 활용한 데이터 바인딩 및 동적 리스트 생성
- 사용자 데이터 CRUD 기능 구현:
  - **Create**: 홈 화면에서 사용자 정보 입력 및 리스트 추가
  - **Read**: 사용자 전체 목록 조회 및 상세 정보 확인
  - **Update**: 기존 사용자 정보 수정 기능
  - **Delete**: 사용자 데이터 삭제 처리
- 인메모리(Memory) 배열을 활용한 데이터 상태 관리

### 2026_01/ch_260129 (1월 29일)

> Express와 EJS를 이용한 웹 서버 실습

- Express Framework 기초 설정
- EJS 템플릿 엔진을 활용한 동적 페이지 렌더링
- Query Parameter 처리 및 응답 페이지 구성

### 2026_01/ch_260128 (1월 28일)

> Streamlit을 이용한 웹 애플리케이션 개발

- **주제**: 챗봇/에이전트 웹 인터페이스 구현
- **파일**: `app.py`, `ex01.py`, `build_db.py`

### 2026_01/ch_260127 (1월 27일)

> MySQL TCL 기초, JavaScript Todo 앱

### 2026_01/ch_260126 (1월 26일)

> MySQL 조인 및 서브쿼리, JavaScript Todo 앱

### 2026_01/ch_260121 (1월 21일)

> Python 심화 학습

### 2026_01/ch_260109 (1월 9일)

> Flask를 이용한 멀티 기능 (계산기, 카운터, 채팅)

### 2026_01/ch_260108 (1월 8일)

> FastAPI AJAX 실습

### 2026_01/ch_260107 (1월 7일)

> Python 클래스 이론 및 테스트

### 2026_01/ch_260106 (1월 6일)

> FastAPI 기본 및 CRUD 실습

### 2026_01/ch_260105 (1월 5일)

> 웹 스크래핑 - 병렬 처리 및 성능 최적화

### 2026_01/ch_260102 (1월 2일)

> 데이터 시각화(Matplotlib), 뉴스 데이터 분석, HTML/CSS, Firebase 호스팅

---

## 📅 2025년 학습 내용

### 2025/ch_251231 (12월 31일)

> HTML/CSS/JavaScript 기초

### 2025/ch_251230 (12월 30일)

> 데이터 분석 및 시각화 (numpy, pandas, matplotlib, wordcloud), 웹 크롤링

### 2025/ch_251229 (12월 29일)

> 데이터 분석 기초

### 2025/ch_251226 (12월 26일)

> 데이터 처리

### 2025/ch_251224 (12월 24일)

> Python 기본 스크립트

### 2025/ch_251217

> LLM Function Calling 실습 (OpenAI GPT-4o, Streamlit)

### 2025/ch_251216

> 생성형 AI(LLM) 기초 실습, 프롬프트 엔지니어링

### 2025/ch_251215

> PDF 처리, STT(음성-텍스트 변환), 요약 파이프라인

### 2025/ch_251212

> LLM을 활용한 AI Agent 및 챗봇 구현

### 2025/ch_251211

> Streamlit을 이용한 AI Agent 데모

### 2025/ch_251210

> LLM 기반 구조화된 출력 처리

### 2025/ch_251209

> 로깅 시스템 및 채팅 기능

### 2025/ch_251208

> 프롬프트 기반 LLM 활용

### 2025/ch_251205

> 파일 처리 및 유틸리티

### 2025/ch_251204

> BeautifulSoup을 이용한 웹 크롤링

### 2025/ch_251203

> 다양한 데이터 처리 및 분석

### 2025/ch_251202

> 데이터 처리 및 분석 기초

### 2025/ch_251201

> Python 기본 학습

### 2025/ch*2511*

> 초기 프로젝트 및 연습 모음

---

## 🚀 빠른 시작

### 환경 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 실행 예제

```bash
# Streamlit 앱 실행
streamlit run 2026_01/ch_260128/app.py

# FastAPI 실행
python -m uvicorn 2026_01/ch_260106.main:app --reload

# Python 스크립트 실행
python 2025/ch_251216/main.py
```

---

## 💡 주요 학습 내용

### AI & LLM

- LangChain을 이용한 에이전트 개발
- 다양한 LLM API 활용 (OpenAI, Ollama)
- 프롬프트 엔지니어링
- 벡터 DB와 임베딩

### 웹 개발

- FastAPI: 비동기 웹 API
- Flask: 전통적 웹 프레임워크
- Streamlit: 데이터 앱 구축
- JavaScript: 프론트엔드 상호작용

### 데이터 처리

- 웹 크롤링 (BeautifulSoup, Selenium)
- 데이터 정제 및 전처리
- 병렬 처리를 통한 성능 최적화
- 데이터 시각화

### 데이터베이스

- MySQL: 관계형 데이터베이스
- SQLAlchemy: ORM 패턴
- ChromaDB: 벡터 데이터베이스
- MongoDB: NoSQL 데이터베이스

---
