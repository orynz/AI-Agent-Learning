from openai import OpenAI
from dotenv import load_dotenv
import os
import csv

# --------------------------------------
# 1) 자치구 코드 매핑 (행정동코드 앞 5자리)
# --------------------------------------
GU_CODE_PREFIX = {
    "종로구": "11110",
    "중구": "11140",
    "용산구": "11170",
    "성동구": "11200",
    "광진구": "11215",
    "동대문구": "11230",
    "중랑구": "11260",
    "성북구": "11290",
    "강북구": "11305",
    "도봉구": "11320",
    "노원구": "11350",
}

# --------------------------------------
# 2) CSV에서 특정 구(자치구)의 인구 합계 계산
#    - 서울열린데이터광장 seoul_population.csv 구조에 맞춘 버전입니다.
# --------------------------------------
def load_population_by_gu(csv_path: str, gu_name: str) -> float:
    """행정동코드 앞 5자리 기준으로 특정 구의 생활인구 합계를 계산합니다."""
    prefix = GU_CODE_PREFIX.get(gu_name)
    if prefix is None:
        raise ValueError(f"{gu_name}은(는) 지원되지 않는 구 이름입니다.")

    total = 0.0

    # 서울열린데이터광장 CSV는 보통 euc-kr 인코딩을 사용합니다.
    with open(csv_path, "r", encoding="euc-kr") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["행정동코드"].strip()
            if code.startswith(prefix):
                val = row["생활인구합계"].strip()
                # 비공개 구간은 '*' 로 표기될 수 있으므로 예외 처리합니다.
                try:
                    total += float(val)
                except ValueError:
                    continue

    return total

# --------------------------------------
# 3) Assistant에게 질문하는 함수
#    - client와 assistant_id를 인자로 받습니다.
# --------------------------------------
def ask_about_gu(client: OpenAI, assistant_id: str, gu_name: str):
    population = load_population_by_gu("seoul_population.csv", gu_name)

    # 1) Thread 생성입니다.
    thread = client.beta.threads.create()

    # 2) 사용자 메시지 작성입니다.
    user_message = (
        f"다음은 서울시 {gu_name}의 생활인구 합계입니다.\n\n"
        f"- 구 이름: {gu_name}\n"
        f"- 생활인구 합계: {population:,.0f}명\n\n"
        "이 수치를 바탕으로, 이 구의 인구 규모를 설명해 주세요. "
        "서울의 다른 구들과 비교했을 때 대략 어느 정도 수준인지도 함께 설명해 주세요."
    )

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

    # 3) Assistant 실행 및 완료까지 대기합니다.
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # 4) 답변 메시지 조회입니다.
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            for c in msg.content:
                if c.type == "text":
                    print("\n[assistant]")
                    print(c.text.value)
            break

# --------------------------------------
# 4) 메인 실행부
# --------------------------------------
if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 1) 여기서 Assistant를 실제로 생성합니다.
    assistant = client.beta.assistants.create(
        name="서울시 인구 전문가",
        instructions=(
            "당신은 서울시 각 구의 생활인구 통계를 이해하기 쉽게 설명해 주는 전문가입니다. "
            "사용자가 전달하는 숫자 데이터를 바탕으로 한국어로 자세히 설명해 주세요."
        ),
        model="gpt-4.1-mini",
    )

    print("생성된 Assistant id:", assistant.id)

    # 2) 바로 종로구를 질문해 봅니다.
    ask_about_gu(client, assistant.id, "종로구")

 
