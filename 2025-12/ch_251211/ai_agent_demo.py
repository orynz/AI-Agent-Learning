from openai import OpenAI
import datetime

client = OpenAI()

# 입력 내용 검열
def moderate_input(text: str) -> bool:
    result = client.moderations.create(
        model = "omni-moderation-latest",
        input = text
    )
    
    flagged = result.results[0].flagged
    return flagged

# Multi-format 콘텐츠 생성
def generate_multi_format(prompt: str)-> str:
    response = client.responses.create(
        model ="gpt-5-nano-2025-08-07",
        input = f"""
        다음 제품/서비스 설명을 바탕으로 멀티포맷 콘텐츠를 생성하라.
        
        # 설명
        {prompt}
        
        # 요구사항
        1. 15초 분량 광과 카피
        2. 유튜브 영상 스크립트 (약 1분)
        3. 인스타그램용 짧은 SNS 문구 3개
        
        각 항목에 번호를 붙여서 구부해서 작성하라.
        """
    )
    
    return response.output_text

# Embedding 생성
def create_embedding(text: str):
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    
    vector = emb.data[0].embedding
    print(f"Embedding vector length: {len(vector)}")
    return vector

# Text to Speech 변환
def text_to_speech(text: str, filename: str):
    speech = client.audio.speech.create(
        model = "gpt-4o-mini-tts",
        voice = "marin",
        input = text
    )
    
    speech.stream_to_file(filename)
    print(f"음성 파일 생성완료: {filename}")

def speech_to_text(filename: str):
    with open(filename, "rb") as audio_file:
        ressult = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print("음성 -> 텍스트 변환 완료:\n", ressult.text)
        return ressult.text
    
def main():
    print("=== AI Agent 통합 데모 ===")
    
    while True:
        # 사용자 입력 받기
        user_prompt = user_inpput()
        
        # 1. 입력 내용 검열
        if moderate_input(user_prompt):
            print("입력 내용이 검열되었습니다. 다른 내용을 시도해 주세요.")
            continue
        
        # 2. 프롬프트 실행 - 멀티포맷 콘텐츠 생성
        multi_response = generate_multi_format(user_prompt)
        print("=== 생성된 멀티포맷 콘텐츠 ===")
        print(multi_response)
        
        # 3. 임베딩 생성
        create_embedding(user_prompt)
        
        # 4. Text to Speech 변환
        filename = f"{datetime.datetime.now().strftime('audio_%H%M%S')}_{'output_audio.mp3'}"
        text_to_speech(multi_response, filename)
        
        # 5. 저장된 음성 텍스
        speech_to_text(filename)
            
def user_inpput():
    user_input = input("제품/서비스를 한 줄로 성명해 보세요: ")
    return user_input
        
if __name__ == "__main__":
    main()
    
    