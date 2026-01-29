from openai import OpenAI
import json


client = OpenAI()

def structured_output(name: str, date: str, participants: str) -> str:
    return f"\n\
        이벤트 이름: {name}\n\
        이벤트 날짜: {date}\n\
        이벤트 참가자들 : {', '.join(participants) if participants else '없음'}"

# 출력 스키마 정의 - 함수 도구 정의 
tools = [
    {
        "type": "function",
        "name": "structured_output",
        "description": "이벤트 정보를 추출합니다. 이벤트 항목은 이름, 날짜, 참가자들 입니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "이벤트 이름",
                },
                "date": {
                    "type": "string",
                    "description": "이벤트 날짜",
                },
                "participants": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "이벤트 참가자들",
                },
            },
            "required": ["name", "date"],
        },
    }
]

response = client.responses.create(
    model="gpt-5-nano",
    input=[
        {"role": "system", "content": "이벤트 정보를 추출하세요. 이벤트 항목은 이름, 날짜, 참가자들 입니다."},
        {
            "role": "user",
            "content": "과학 박람회는 금요일에 열리며, 철수와 영희가 참가합니다.",
        },
    ],
    tools=tools,
)

print("output_text: ", response.output_text)

for item in response.output:
    if item.type == "function_call":
        fn_call = item
        args = json.loads(item.arguments)
        print("call: ", fn_call)
        print("args: ", args)
        
        if fn_call.name == "structured_output":
            result = structured_output(**args)
            print(f"function call result: {result}")
        
        
         

