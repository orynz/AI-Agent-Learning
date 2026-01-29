
def load_text(path: str) -> str:
    with open (path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def clean_text(text: str) -> str:
    text = text.strip()
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
        
    return text

if __name__ == "__main__":
    raw = load_text("article.txt")
    print("로우 데이터 *****************")
    print(raw[:500])
    print("클린 데이터 *****************")
    cleaned  = clean_text(raw)
    print(cleaned[:500])

import re   
rrr = re.search('a', 'adab')
_, b = rrr.span()
print( b)