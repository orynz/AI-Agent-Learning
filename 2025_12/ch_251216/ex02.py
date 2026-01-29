from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def streaming_chatbot():
    print("=== 스트리밍 기반 챗봇 ===")
    print("종료하려면 '/quit' 을 입력하세요.\n")

    messages = [
        {"role": "system", "content": "당신은 친절하고 설명을 잘하는 AI 강사입니다."}
    ]

    while True:
        user_msg = input("\n[사용자] ")

        if user_msg.strip() == "/quit":
            print("\n대화를 종료합니다.")
            break

        # 사용자 메시지 추가
        messages.append({"role": "user", "content": user_msg})

        # 스트리밍 호출
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            stream=True,
            messages=messages
        )

        print("[AI] ", end="", flush=True)
        ai_response = ""

        for chunk in stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                text = content
                ai_response += text
                print(text, end="", flush=True)

        # 응답 전체를 messages에 저장하여 다음 대화에 활용
        messages.append({"role": "assistant", "content": ai_response})


if __name__ == "__main__":
    streaming_chatbot()
