from openai import OpenAI

client = OpenAI()

message = [
    {"role" : "system", 
     "content" : 
        "당신은 불친절한 상담사입니다. \
        무조건 반말을 사용하고 짧고 거칠게 답하세요. \
        다른 불필요한 설명은 하지 않습니다. \
        사용자와의 대화에만 집중하세요."
    }
]


# 프롬프트 입력
def user_input():
    return input("내용을 입력하세요: ")
    
# 프롬프트 검증 함수
def moderationFn(text: str):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input = text
    )
    return response.results[0].flagged

# 프롬프트 쿼리 함수
def responsesFn(text: str):
    
    message.append({"role":"user", "content" : text})
    response = client.responses.create(
        model="gpt-5-nano",
        input = message
    )
    return response

def main():
    while True:
        
        prompt = input("사용자: ")
        print()
        
        if prompt == "exit":
            break
        
        if moderationFn(prompt):
            prompt = input("내용에 유해 컨텐츠가 포함되어 있습니다. 다시 입력하세요 : ")
            print()
            continue
        
        response = responsesFn(prompt)
        message.append({"role":"assistant", "content" : response.output_text})
        print(f"AI: {response.output_text}")
        print()
        


if __name__ == "__main__":
    main()