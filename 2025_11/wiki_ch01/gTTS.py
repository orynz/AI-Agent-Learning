# gTTS 라이브러리 선언
from gtts import gTTS

# 저장하지 않고 바로 메모리에서 재생을 하고 싶을 때
from io import BytesIO

# 텍스트 정의
text_to_speak = "안녕하세요. \
    무료 TTS 실습 예제입니다. \
    만나서 반가워요~"
    
# 언어설정 (한국어 = ko)
# 영어 = en, 일본어 = ja, 중어어 zh-ch
language = 'ko'

# gTTS 생성
tts = gTTS(text=text_to_speak, lang=language)

# 음성 파일로 저장(파일명 : hello.mp3)
file_name = "hello.mp3"
# tts.save(file_name)

tts.stream()


# # 메모리 버퍼 생성
# mp3_fp = BytesIO()

# # gTTS 객체 생성
# tts = gTTS(text=text_to_speak, lang=language)

# # 버퍼에 오디오 데이터 쓰기
# tts.write_to_fp(mp3_fp)


