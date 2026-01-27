from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

prompt_1 = PromptTemplate.from_template(
    "다음 주제에 대해 핵심 키워드 5개를 한국어로 뽑으세요.\n주제: {topic}\n출력: 쉼표로 구분"
)

prompt_2 = PromptTemplate.from_template(
    "다음 키워드를 활용해 3문장 요약을 한국어로 작성하세요.\n키워드: {keywords}"
)

chain_keywords = prompt_1 | llm | StrOutputParser()
chain_summary = prompt_2 | llm | StrOutputParser()

keywords = chain_keywords.invoke({"topic": "AI 에이전트"})
summary = chain_summary.invoke({"keywords": keywords})

print("[키워드]")
print(keywords)
print("\n[요약]")
print(summary)
