from TTS.api import TTS

# KSS 데이터셋 기반의 한국어 VITS 모델 예시
KOREAN_MODEL = "tts_models/ko/thorsten/tacotron2-DDC" 

tts = TTS(KOREAN_MODEL)

# tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)
# tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path="output.wav")
            
# 이 모델은 한국어 전용이므로, language 인수를 생략하거나 필요에 따라 다르게 사용합니다.
# XTTS와 달리, VITS 모델은 보통 speaker_wav가 필요 없습니다.
tts.tts_to_file(
    text="한국어 모델 테스트", 
    file_path="korean_output.wav"
)



