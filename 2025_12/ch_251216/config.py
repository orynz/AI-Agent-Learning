from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from openai import BaseModel
from dataclasses import dataclass
import logging

"""
프로젝트에서 사용하는 상수값과 데이터 모델을 정의 -
전체 코드의 일정한 데이터 구조를 유지하며 및 특정 설정값을 관리한다.
"""

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnvType(str, Enum):
    """환경 유형 정의"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    
class Models(str, Enum):
    GPT4 = "gpt-4"
    GPT4o = "gpt-4o"

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class PromptUnit(BaseModel):
    title: str
    prompt: List[ChatMessage]
    response: Optional[Union[Any, List, Dict]]    


class DatabaseConfig:
    """데이터베이스 연결 설정"""
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5432,
                 user: str = "admin",
                 password: str = "password",
                 name: str = "mydb"):
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        
@dataclass
class FeatureFlags:
    """기능 토글 관리"""
    enable_chatgpt: bool = True
    enable_dalle: bool = False
    enable_codex: bool = True
    enable_whisper: bool = False

class BaseConfig(BaseModel):
    """모든 환경별 설정의 기본 클래스"""
    env: EnvType = EnvType.DEVELOPMENT
    debug: bool = False
    feature_flags: FeatureFlags = FeatureFlags()
    
    class Config:
        arbitrary_types_allowed = True

class DevelopmentConfig(BaseConfig):
    """개발 환경 설정"""
    openai: OpenAIConfig = OpenAIConfig(timeout=30, max_retries=1)
    database: DatabaseConfig = DatabaseConfig(
        host="dev-db.example.com",
        name="dev_db"
    )
    # 개발 환경 특화 설정
    allow_insecure_requests: bool = True

class ProductionConfig(BaseConfig):
    """운영 환경 설정"""
    openai: OpenAIConfig = OpenAIConfig(timeout=60, max_retries=5)
    database: DatabaseConfig = DatabaseConfig(
        host="prod-db.example.com",
        name="prod_db",
        user="prod_user"
    )
    # 운영 환경 특화 설정
    enable_rate_limiting: bool = True
    log_level: str = "INFO"

# 현재 환경에 따른 설정 로드
def get_config(env: Optional[EnvType] = None) -> BaseConfig:
    """환경에 따른 적절한 설정 반환"""
    env = env or os.getenv("APP_ENV", EnvType.DEVELOPMENT)
    
    if env == EnvType.PRODUCTION:
        return ProductionConfig(env=env, debug=False)
    elif env == EnvType.TESTING:
        return BaseConfig(env=env, debug=True)
    else:
        return DevelopmentConfig(env=env, debug=True)