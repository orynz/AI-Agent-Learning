from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

result = llm.invoke("AI를 주제로 한 한국어 하이쿠를 작성하세요.")
print(result.content)

prompt = PromptTemplate.from_template(
    "AI를 주제로 한 한국어 하이쿠를 작성하세요."
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({})
print(result)
