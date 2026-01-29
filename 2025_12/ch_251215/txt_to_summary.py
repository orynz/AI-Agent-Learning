import os
from openai import OpenAI
from datetime import datetime

client = OpenAI()

# 기초 단계에서는 길이 초과를 막기 위해 상한을 둠
MAX_CHARS = 12000  

def build_prompt(txt: str) -> str:
    return f"""
당신은 사용자가 제시한 글을 요약하는 어시스턴스입니다.
반드시 지정된 출력 형식으로 작성하세요.

[출력 형식]
# 제목
## 저자의 문제 인식 및 주장 (10문장 이내)
## 핵심 요약 (불릿 7개)
- ...
## 키워드 (5개, 쉼표로)
키워드1, 키워드2, 키워드3, 키워드4, 키워드5

[규칙]
- 원문에 없는 내용을 만들지 말 것.
- 불필요한 수식어를 줄이고 최대한 간결하게 작성할 것.

============== 이하 텍스트 ==============

{txt}
""".strip()

def summarize_txt(txt_path: str) -> str:
    with open(txt_path, "r", encoding="utf-8") as f:
        txt = f.read()

    txt = txt[:MAX_CHARS]  # 길이 초과 방지(간단·안정 우선)

    prompt = build_prompt(txt)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

def main() -> None:
    txt_path = input("요약할 TXT 파일명: \n> ").strip()
    if not os.path.exists(txt_path):
        print("TXT 파일을 찾을 수 없습니다.")
        return

    out_path = input("요약 폴더(기본값 .\\output):\n> ").strip() or "output"
    if not os.path.isdir(out_path):
        os.makedirs(out_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(txt_path))[0]
    summary_path = os.path.join(out_path, f"{timestamp}_{base}.md")

    summary = summarize_txt(txt_path)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"------------- [요약 완료] -------------\n{summary_path}")

if __name__ == "__main__":
    main()
