from openai import OpenAI
from dotenv import load_dotenv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import fitz
from PyPDF2 import PdfReader

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def load_docs(path="docs"):
    files = os.listdir(path)
    docs = []
    for f in files:
        
        if os.path.splitext(f)[-1] == ".pdf":
            
            reader = PdfReader(os.path.join(path, f))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            docs.append(text)
        else:
            with open(os.path.join(path, f), "r", encoding="utf-8") as fp:
                docs.append(fp.read())
    return docs

def retrieve(query, docs, top_k=1):
    vect = TfidfVectorizer()
    tfidf = vect.fit_transform([query] + docs)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    idx = scores.argsort()[::-1][:top_k]
    return [docs[i] for i in idx]

def rag_answer(question):
    docs = load_docs()
    retrieved = retrieve(question, docs)[0]

    prompt = f"""
            당신은 RAG 기반 답변 생성기입니다.
            아래 '검색 결과'의 내용만 참조하여 답변을 작성할 수 있습니다.
            '검색 결과'에 없는 답변은 생성하지 않으며, 참조 답변시 출처를 표시하세요.
            
            ---
            
            검색 결과:            
            {retrieved}
            
            ---

            질문:
            {question}
        """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    # q = "인공지능을 공부하려면 어떻게 해야해?"
    q = "프롬프트 엔지니어링 기법에 대해 정리해줘."
    print("\n[RAG 기반 답변]")
    print(rag_answer(q))
    
    