import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 문서 로딩
def load_docs(path="docs"):
    files = os.listdir(path)
    docs = []
    for f in files:
        with open(os.path.join(path, f), "r", encoding="utf-8") as fp:
            docs.append(fp.read())
    return docs

def retrieve(query, docs, top_k=1):
    vect = TfidfVectorizer()
    tfidf = vect.fit_transform([query] + docs)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    idx = scores.argsort()[::-1][:top_k]
    return [docs[i] for i in idx]

if __name__ == "__main__":
    docs = load_docs()
    q = "프로젝트 제출 규칙을 알려줘"
    retrieved = retrieve(q, docs)
    print("[검색된 문서 조각]")
    print(retrieved[0])
