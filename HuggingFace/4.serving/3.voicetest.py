# ==============================
# 1. 라이브러리
# ==============================
import gradio as gr
import torch
from transformers import pipeline, M2M100ForConditionalGeneration, M2M100Tokenizer
from gtts import gTTS
import tempfile
import os
import nltk
from nltk.tokenize import sent_tokenize

# NLTK 문장 분리기 다운로드 (최초 1회)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# ==============================
# 2. 모델 설정
# ==============================
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# STT (Whisper)
stt = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=device,
    chunk_length_s=30,
    generate_kwargs={"language": "en"}
)

# 번역 (영어 → 한국어, M2M100)
model_name = "facebook/m2m100_418M"
translation_model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)
translation_tokenizer = M2M100Tokenizer.from_pretrained(model_name)


# ==============================
# 3. 핵심 함수
# ==============================

def split_into_sentence_groups(text: str, max_tokens: int = 400) -> list[str]:
    """
    문장 단위로 분리 후, 토큰 한도를 넘지 않도록 여러 문장을 하나의 그룹으로 묶음.
    - 짧은 문장들을 합쳐서 번역하면 문맥이 살아 번역 품질이 향상됨
    - 너무 길면 모델 한도를 초과하므로 토큰 수 기준으로 분할
    """
    sentences = sent_tokenize(text, language="english")
    groups = []
    current_group = []
    current_len = 0

    for sent in sentences:
        token_len = len(translation_tokenizer.encode(sent))
        # 현재 그룹에 추가 시 한도를 넘으면 현재 그룹을 저장하고 새 그룹 시작
        if current_len + token_len > max_tokens and current_group:
            groups.append(" ".join(current_group))
            current_group = [sent]
            current_len = token_len
        else:
            current_group.append(sent)
            current_len += token_len

    if current_group:
        groups.append(" ".join(current_group))

    return groups


def translate_group(text: str) -> str:
    """단일 텍스트 그룹을 번역"""
    translation_tokenizer.src_lang = "en"
    encoded = translation_tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,        # max_length 제거 → max_new_tokens 단독 사용
    ).to(device)

    generated_tokens = translation_model.generate(
        **encoded,
        forced_bos_token_id=translation_tokenizer.get_lang_id("ko"),
        max_new_tokens=512,     # 출력 토큰 수만 제어 (경고 해소)
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3
    )
    return translation_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


def process(audio):
    if audio is None:
        return "", "", None

    # 1. 음성 → 영어 텍스트 (STT)
    try:
        result = stt(audio, return_timestamps=True)
        text_en = result.get("text", "").strip()
        if not text_en:
            return "음성을 인식하지 못했습니다.", "", None
    except Exception as e:
        return f"STT 오류: {str(e)}", "", None

    # 2. 영어 → 한국어 번역 (문장 그룹 단위 분할 번역)
    try:
        # 문장 단위로 묶어서 청크 생성
        groups = split_into_sentence_groups(text_en, max_tokens=400)
        translated_chunks = [translate_group(g) for g in groups]

        # 번역된 그룹들을 자연스럽게 연결 (공백 1개)
        text_ko = " ".join(translated_chunks)

    except Exception as e:
        return text_en, f"번역 오류: {str(e)}", None

    # 3. 한국어 텍스트 → 음성 변환 (TTS)
    try:
        tts = gTTS(text=text_ko, lang="ko")
        file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(file.name)
        audio_path = file.name
    except Exception as e:
        print(f"TTS 오류: {e}")
        audio_path = None

    return text_en, text_ko, audio_path


# ==============================
# 4. UI 및 실행
# ==============================
with gr.Blocks() as demo:
    gr.Markdown("## 🎤 영어 음성 → 한국어 번역 + TTS")

    with gr.Row():
        audio_in = gr.Audio(sources=["microphone", "upload"], type="filepath", label="영어 음성 입력")
    btn = gr.Button("변환하기", variant="primary")

    with gr.Column():
        text_out_en = gr.Textbox(label="1. 영어 텍스트 결과")
        text_out_ko = gr.Textbox(label="2. 한국어 번역 결과")
        audio_out = gr.Audio(label="3. 한국어 음성 출력", type="filepath")

    btn.click(process, audio_in, [text_out_en, text_out_ko, audio_out])

if __name__ == "__main__":
    demo.launch(inbrowser=True)