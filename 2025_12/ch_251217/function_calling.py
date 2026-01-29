import json
from typing import Dict, Any

# 1. 사용할 함수들 정의
def calculate_sum(a: float, b: float) -> float:
    return a + b

def calculate_sub(a: float, b: float) -> float:
    return a - b

# 2. 함수 메타데이터 정의
FUNCTIONS = {
    "calculate_sum": {
        "description": "두 숫자 더하기",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "첫 번째 숫자"},
                "b": {"type": "number", "description": "두 번째 숫자"}
            },
            "required": ["a", "b"]
        },
        "function": calculate_sum
    },
    "calculate_sub": {
        "description": "두 숫자 빼기",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "첫 번째 숫자"},
                "b": {"type": "number", "description": "두 번째 숫자"}
            },
            "required": ["a", "b"]
        },
        "function": calculate_sub
    }
}

# 3. 간단한 규칙 기반 Function Calling 시스템
def process_request(user_input: str) -> Dict[str, Any]:
    """
    사용자 입력을 분석해 적절한 함수 선택 및 파라미터 추출
    (실제 LLM 대신 간단한 규칙 기반 시스템 사용)
    """
    # 매우 간단한 규칙 기반 매칭 (실제 LLM은 더 정교함)
    functions_to_call = []
    
    # 더하기 계산 요청 확인
    if "합" in user_input or "더하기" in user_input:
        # 숫자 추출 (간단한 경우)
        import re
        numbers = re.findall(r"-?\d+\.?\d*", user_input)
        if len(numbers) >= 2:
            a, b = map(float, numbers[:2])
            functions_to_call.append({
                "name": "calculate_sum",
                "arguments": json.dumps({"a": a, "b": b})
            })
    # 빼기 계산 요청 확인
    elif "차" in user_input or "빼기" in user_input:
        # 숫자 추출 (간단한 경우)
        import re
        numbers = re.findall(r"-?\d+\.?\d*", user_input)
        if len(numbers) >= 2:
            a, b = map(float, numbers[:2])
            functions_to_call.append({
                "name": "calculate_sub",
                "arguments": json.dumps({"a": a, "b": b})
            })
    
    if functions_to_call:
        return {"function_calls": functions_to_call}
    else:
        return {"answer": "함수 호출이 정의되지 않았습니다."}

# 4. 함수 호출 실행기
def execute_function_calls(function_calls: list) -> Dict[str, Any]:
    results = {}
    for call in function_calls:
        func_name = call["name"]
        arguments = json.loads(call["arguments"])
        
        if func_name in FUNCTIONS:
            func = FUNCTIONS[func_name]["function"]
            results[func_name] = func(**arguments)
        else:
            results[func_name] = "알 수 없는 함수"
    return results

# 5. 전체 시스템 테스트
def main():
    user_queries = [
        "3과 5을 합을 계산하세요",
        "부산의 기온을 알려주세요",
        "7.5와 2.3의 빼기는?"
    ]
    
    for query in user_queries:
        print("-" * 50)
        print(f"\n사용자 입력: {query}")
        response = process_request(query)
        
        if "function_calls" in response:
            # print("함수 호출 식별:")
            for call in response["function_calls"]:
                print(f" - {call['name']}({call['arguments']})")
                
            results = execute_function_calls(response["function_calls"])
            print("\n실행 결과:")
            for name, result in results.items():
                print(f" - {name}: {result}")
        elif "answer" in response:
            print(f"결과: {response['answer']}")
        
        print()
if __name__ == "__main__":
    main()
