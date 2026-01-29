from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


def get_current_time(format: str = "%Y_%m_%d_%H%M%S") -> str:
    """현재 시간을 지정된 형식의 문자열로 반환합니다. 기본값: YYYY_MM_DD_HHMMSS
    """
    return datetime.now().strftime(format)

def generate_timestamped_filename(filename: str) -> str:
    """파일명 앞에 타임스탬프를 붙여 반환하는 함수"""
    return f"{get_current_time}_{filename}"