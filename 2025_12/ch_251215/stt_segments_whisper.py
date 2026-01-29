# stt_segments_whisper.py

import os
import torch
import pandas as pd
from dotenv import load_dotenv
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# ① 환경 설정
load_dotenv()
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"  # ffmpeg 설치 경로

MODEL_ID = "openai/whisper-large-v3-turbo"


def create_asr_pipeline(model_id: str = MODEL_ID):
    """Whisper 모델과 Processor를 로드하고 STT 파이프라인을 생성합니다."""
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    ).to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    asr = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=device,
        torch_dtype=torch_dtype,
        return_timestamps=True,  # 청크별 시작/끝 시간 포함
        chunk_length_s=10,
        stride_length_s=2,
    )

    return asr


def transcribe_with_timestamps(audio_path: str, csv_path: str) -> pd.DataFrame:
    """오디오 파일을 받아 STT 결과를 (start, end, text) CSV로 저장합니다."""
    asr = create_asr_pipeline()

    print(f"[정보] STT 시작: {audio_path}")
    result = asr(audio_path)

    rows = []
    for chunk in result["chunks"]:
        start, end = chunk["timestamp"]
        text = chunk["text"].strip()
        rows.append((start, end, text))

    df = pd.DataFrame(rows, columns=["start", "end", "text"])
    df.to_csv(csv_path, index=False, sep="|", encoding="utf-8")

    print(f"[완료] CSV 저장: {csv_path}")
    return df


if __name__ == "__main__":
    # 같은 폴더에 있는 agent_output.mp3를 예시로 사용
    audio_file_path = "./agent_output.mp3"
    output_csv_path = "./agent_output_stt.csv"

    df = transcribe_with_timestamps(audio_file_path, output_csv_path)
    print(df.head())
