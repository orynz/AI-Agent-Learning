from openai import OpenAI


client = OpenAI()


def qusestionFn():
    prompt = input("[일반질문] >>> ")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"user", "content":prompt},
            {"role":"system", "content": "너는 사용자의 질의에 도움을 주는 어시스턴스야."}
        ]
    )
    
    print(response.choices[0].message.content)

def surmmuryFn():
    prompt = input("[요약질문] >>> ")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"user", "content":prompt},
            {"role":"system", "content": "너는 사용자의 질의에 3문장으로 요약하는 요약 봇이야."}
        ]
    )
    
    print(response.choices[0].message.content)
    
def toneChangeFn():
    prompt = input("[어조변경] >>> ")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"user", "content":prompt},
            {"role":"system", "content": "너는 사용자의 질의에 격식있는 어조로 변경해주는 작문 어시스터야."}
        ]
    )
    
    print(response.choices[0].message.content)

def main():
    while True:
        print("********* 메뉴 선택 *********")
        print("1. 일반 질의문")
        print("2. 텍스트 요약")
        print("3. 격식있는 어조로 변경")
        print("0. 종료")
        
        choice = input("[질문] >>> ")
        
        if choice == "0":
            print("프로그램 종료")
            break
        
        elif choice == "1":
            qusestionFn()
        elif choice == "2":
            surmmuryFn()
        elif choice == "3":
            toneChangeFn()

if __name__ == "__main__":
    main()
    