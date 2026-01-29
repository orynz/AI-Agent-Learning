import os
from datetime import datetime

# PyMuPDF 라이브러리의 구버전과 호환성을 주기 위한 처리 방식
# 환경에 따라 pymupdf / fitz가 다를 수 있음
try:
    import pymupdf as fitz  # 최신 권장 방식
except Exception:
    import fitz             # 구버전 호환

HEADER_HEIGHT = 80
FOOTER_HEIGHT = 80
PAGE_SEP = "\n[PAGE_BREAK]\n"

def pdf_to_text_basic(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    full_text = ""
    
    # 현재 페이지의 글자들을 뽑아내서 (page.get_text())
    # 준비된 상자(full_text)에 계속 뒤에 붙여 넣어요.
    for page in doc:
        full_text += page.get_text()
        
    # # PDF 전처리(헤더/푸터 제거) 후 TXT 변환 : 헤더와 푸터의 높이가 일정할때 유용
    # HEADER_HEIGHT = 80            # 헤더 높이
    # FOOTER_HEIGHT = 80            # 푸터 높이
    # PAGE_SEP = "\n[PAGE_BREAK]\n" # 페이지 구분
    # for page in doc:
    #     rect = page.rect
    #     body = page.get_text(
    #         clip=(0, HEADER_HEIGHT, rect.width, rect.height - FOOTER_HEIGHT)
    #     )
    #     full_text += body + PAGE_SEP
    
    return full_text

def main() -> None:
    pdf_path = input(f"PDF 파일명: {os.getcwd()}\\ :\n> ").strip()
    
    if not os.path.exists(pdf_path):
        print("PDF 파일을 찾을 수 없습니다.")
        return

    out_dir = input("출력 폴더(기본값 .\\output):\n> ").strip() or "output"
        
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = os.path.join(out_dir, f"{timestamp}_{base}.txt")

    text = pdf_to_text_basic(pdf_path)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"------------- [변화 완료] -------------\n{txt_path}")

if __name__ == "__main__":
    main()
