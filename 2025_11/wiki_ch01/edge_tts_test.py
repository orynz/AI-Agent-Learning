# import edge_tts
# import asyncio

# async def main():
#     communicate = edge_tts.Communicate(
#         "안녕하세요, Edge TTS 실습니다.\
#             만나서 반가워요.",
#         voice = "ko-KR-SunHiNeural"
            
#     )
#     await communicate.save("hello_edge_tts.mp3")
    
# asyncio.run(main())
import edge_tts
import asyncio


# 텍스트 정의
TEXT = "안녕하세요. 이것은 Microsoft Edge TTS 테스트입니다. 목소리가 매우 자연스럽습니다."

# 목소리 지정 (한국어 여성 목소리)
# 다른 목소리 예시: en-US-AriaNeural (영어 여성), ja-JP-NanamiNeural (일본어 여성)
VOICE = "ko-KR-SunHiNeural" 

# 출력 파일명
OUTPUT_FILE = "edge_tts_output.mp3"

async def generate_speech():
    # Communicate 객체 생성
    communicate = edge_tts_test.Communicate(TEXT, VOICE)
    
    # 파일로 오디오 데이터 저장
    await communicate.save(OUTPUT_FILE)
    
    print(f"'{OUTPUT_FILE}' 파일이 저장되었습니다.")

# 비동기 함수 실행
if __name__ == "__main__":
    asyncio.run(generate_speech())