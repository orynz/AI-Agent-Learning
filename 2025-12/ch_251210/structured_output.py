from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()



text = """▲
|Google Workspace Studio를 통해 AI 에이전트로 일상 업무 자동화 하기|
13P by GN⁺ 2025-12-10 13:05 | ★ favorite | 댓글과 토론
Google Workspace Studio는 업무 환경내에서 Gemini 3 기반의 AI 에이전트를 설계·관리·공유해 일상 업무를 자동화할 수 있는 플랫폼
사용자는 코딩 없이 자연어로 지시해 이메일 분류, 일정 관리, 보고서 작성 등 반복 업무를 자동화 가능
독일의 청소기기 제조업체 Kärcher는 Studio를 활용해 기능 아이디어 검토 과정을 자동화하여 초안 작성 시간을 90% 단축
에이전트는 Gmail, Drive, Chat 등 Workspace 앱과 통합되어 맥락을 이해하고, Asana·Jira·Salesforce 등 외부 앱과도 연동 가능
모든 직원이 자신만의 업무 흐름을 자동화할 수 있어, 기업 전반의 생산성과 협업 효율을 높이는 도구로 주목
Google Workspace Studio 개요
Google Workspace Studio는 Google Workspace 내에서 AI 에이전트를 설계·관리·공유할 수 있는 통합 환경
Gemini 3의 추론 및 멀티모달 이해 능력을 활용해 복잡한 워크플로를 자동화
코딩이나 전문 문법 없이 몇 분 만에 에이전트를 구축 가능
사용자는 단순 반복 작업부터 복잡한 비즈니스 프로세스까지 자동화 가능
예: 이메일 분류, 일정 조정, 보고서 생성 등
에이전트 기반 자동화의 필요성
기존 자동화 도구는 기술적 진입장벽이 높고 유연성이 부족해 일반 사용자가 활용하기 어려움
Studio는 이러한 한계를 제거해 모든 직원이 직접 에이전트를 설계할 수 있도록 지원
반복적이고 시간이 많이 소요되는 업무를 맥락을 이해하는 AI 에이전트에 위임 가능
복잡한 업무 자동화 기능
기존의 규칙 기반 자동화와 달리, Workspace 에이전트는 유연한 추론과 적응 능력을 보유
감정 분석, 콘텐츠 생성, 우선순위 지정, 알림 관리 등 고급 기능 수행
Kärcher 사례
Zoi와 협력해 Workspace Studio를 조기 도입
Chat에서 제안된 기능 아이디어를 여러 AI Gem이 단계별로 평가·작성
초안 작성 시간이 90% 단축, 수시간 걸리던 작업을 2분 내 완료
누구나 에이전트를 만들 수 있는 환경
Gemini Alpha 프로그램 참여 고객은 이미 Studio를 활용 중이며, 최근 30일간 2천만 건 이상의 작업 자동화
사용자는 템플릿을 선택하거나 자연어로 “이메일에 질문이 있으면 ‘To respond’로 라벨링하고 Chat으로 알림”과 같이 지시 가능
Gemini 3이 이메일 내용을 분석해 자동으로 규칙 생성
첨부파일에서 행동 항목, 송장 번호 등 세부 정보 추출 가능
생성된 에이전트는 Google Drive처럼 팀과 공유 가능
Workspace 및 외부 앱 통합
에이전트는 Gmail, Drive, Chat 등 Workspace 앱과 깊이 통합되어 업무 맥락을 이해
회사 정책과 프로세스에 맞는 지원 제공
사용자 톤과 스타일에 맞춘 콘텐츠 생성
Asana, Jira, Mailchimp, Salesforce 등 외부 앱과 연결 가능
Apps Script의 Custom steps를 통해 내부 도구나 Vertex AI 모델과 연동 가능
Workspace 앱의 사이드 패널에서 에이전트 활동을 직접 확인 가능
Workspace Studio 시작하기
수주 내 비즈니스 고객 대상 단계적 배포 예정
접속 후 템플릿을 선택하거나 자연어로 자동화 지시 입력 가능
추가 정보는 Workspace Studio 도움말 센터 또는 Discord 채널에서 확인 가능
Gemini Alpha 프로그램 참여 시 향후 기능과 관리자 제어 기능을 조기 체험 가능"""

class ResearchPaperExtraction(BaseModel):
    title: str
    publish_date: str
    authors: list[str]
    summury : str
    keywords: list[str]
    
response = client.responses.parse(
    model="gpt-5-nano",
    input=[
        {
            "role": "system",
            "content": "당신은 정형 데이터 추출 전문가입니다. 연구 논문에서 발췌한 비정형 텍스트를 주어진 정형 구조로 변환해야 합니다.",
        },
        {"role": "user", "content": text},
    ],
    text_format=ResearchPaperExtraction,
)
print(response.output_text)
print()
research_paper = response.output_parsed
print(f"제목: {research_paper.title}")
print(f"저자들: {', '.join(research_paper.authors)}")
print(f"출판일: {research_paper.publish_date}")
print(f"요약: {research_paper.summury}")
print(f"키워드들: {', '.join(research_paper.keywords)}")





# class Step(BaseModel):
#     explanation: str
#     output: str

# class MathReasoning(BaseModel):
#     steps: list[Step]
#     final_answer: str

# response = client.responses.parse(
#     model="gpt-5-nano",
#     input=[
#         {
#             "role": "system",
#             "content": "당신은 친절한 수학 튜터입니다. 사용자가 풀이 과정을 단계별로 이해할 수 있도록 안내해 주세요.",
#         },
#         {"role": "user", "content": "8x + 7 = -23을 어떻게 풀 수 있나요?"},
#     ],
#     text_format=MathReasoning,
# )

# print(response.output_text)
# print()
# math_reasoning = response.output_parsed
# for step in math_reasoning.steps:
#     print(f"설명: {step.explanation}")
#     print(f"출력: {step.output}")
# print(f"최종 답변: {math_reasoning.final_answer}")