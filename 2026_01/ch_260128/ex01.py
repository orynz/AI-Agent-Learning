import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 환견변수 로드
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 객체 생성
llm = ChatOpenAI(
    api_key=API_KEY,
    temperature=0.2,            # 창의성 (0.0 ~ 2.0)
    max_completion_tokens=2048, # 최대 토큰수
    model="gpt-5-nano",         # 모델명
).bind(logprobs=True)

# 질의내용
question = "대한민국의 수도는 어디인가요?"
result = llm.invoke(question);

print(result)
'''출력 결과: 
content='대한민국의 수도는 서울(서울특별시)입니다. 필요하시면 서울에 대한 정보도 더 알려드릴게요.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 230, 'prompt_tokens': 15, 'total_tokens': 245, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 192, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-D2raguuYM1bqe54iJB0dHub12I7jb', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019c02e4-2113-75b2-acf9-4fbb8f9523db-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 15, 'output_tokens': 230, 'total_tokens': 245, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 192}}
'''

print(result.content)
'''출력 결과: 
대한민국의 수도는 서울(서울특별시)입니다. 필요하시면 서울에 대한 정보도 더 알려드릴게요.
'''
print(result.response_metadata)
'''
{'token_usage': {'completion_tokens': 230, 'prompt_tokens': 15, 'total_tokens': 245, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 192, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-D2raguuYM1bqe54iJB0dHub12I7jb', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}
'''

print(result.to_json())
'''출력 결과: 
{'lc': 1, 'type': 'constructor', 'id': ['langchain', 'schema', 'messages', 'AIMessage'], 'kwargs': {'content': '대한민국의 수도는 서울(서울특별시)입니다. 필요하시면 서울에 대한 정보도 더 알려드릴 게요.', 'additional_kwargs': {'refusal': None}, 'response_metadata': {'token_usage': {'completion_tokens': 230, 'prompt_tokens': 15, 'total_tokens': 245, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 192, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-D2raguuYM1bqe54iJB0dHub12I7jb', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, 'type': 'ai', 'id': 'lc_run--019c02e4-2113-75b2-acf9-4fbb8f9523db-0', 'usage_metadata': {'input_tokens': 15, 'output_tokens': 230, 'total_tokens': 245, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 192}}, 'tool_calls': [], 'invalid_tool_calls': []}}
'''

