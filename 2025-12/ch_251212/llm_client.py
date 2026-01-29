# llm_client.py
from openai import OpenAI
from dotenv import load_dotenv
import os

def load_config() -> dict:
    """환경별 설정을 한 번에 읽어오는 함수입니다."""
    env = os.getenv("APP_ENV", "dev")
    
    load_dotenv(f".env.{env}")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL", "gpt-4o-mini")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

    return {
        "env": env,
        "api_key": api_key,
        "model": model,
    }

def create_client(config: dict) -> OpenAI:
    """설정 정보를 받아 OpenAI 클라이언트를 생성합니다."""
    return OpenAI(api_key=config["api_key"])

def ask_llm(prompt: str) -> str | None:
    """
    ① 설정 로딩 → ② 클라이언트 생성 → ③ LLM 호출을 한 번에 수행합니다.
    """
    config = load_config()
    client = create_client(config)

    try:
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": f"{config['env']} 환경용 어시스턴트입니다."},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content
    
    except Exception as e:
        # 최소한의 오류 메시지만 반환하거나, 로깅 모듈과 연동할 수 있습니다.
        return f"[오류] LLM 호출에 실패했습니다: {e}"

