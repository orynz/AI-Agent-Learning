import os
import subprocess
import sys

def run_py(script: str) -> int:
    return subprocess.call([sys.executable, script])

def main() -> None:
    print("실행 순서")
    print("1) pdf_to_txt_preprocess.py 로 전처리 TXT 생성")
    print("2) txt_to_summary.py 로 요약 생성")

    choice = input("1부터 순서대로 실행하시겠습니까? (y/n): ").strip().lower()
    if choice != "y":
        print("종료합니다.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))

    step1 = os.path.join(base_dir, "pdf_to_txt_preprocess.py")
    step2 = os.path.join(base_dir, "txt_to_summary.py")

    if not os.path.exists(step1) or not os.path.exists(step2):
        print("필요한 스크립트 파일이 같은 폴더에 있는지 확인하세요.")
        return

    code = run_py(step1)
    if code != 0:
        print("전처리 TXT 생성 단계에서 오류가 발생했습니다.")
        return

    code = run_py(step2)
    if code != 0:
        print("요약 생성 단계에서 오류가 발생했습니다.")
        return

    print("[완료] 전 과정 실행이 종료되었습니다.")

if __name__ == "__main__":
    main()
