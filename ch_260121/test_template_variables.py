from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model="gpt-5-mini", temperature=0.2)

# 프롬프트에 변수 사용
prompt = PromptTemplate.from_template(
    "한국어로 3줄의 하이쿠를 작성해줘.\n"
    "topic: {topic}\n"
    "style: {style}"
)

# invoke에서는 dict(json형식)로 변수 전달. key를 문자열로 사용.
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic":"AI", "style":"경쾌하고 발랄하게"})
print(result)
