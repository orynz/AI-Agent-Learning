import os
import torch
import pandas as pd
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pyannote.audio import Pipeline

from dotenv import load_dotenv
import soundfile as sf   # ← torchaudio 대신 soundfile 사용

load_dotenv()

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"  # 자신이 설치한 ffmpeg 경로로 수정

def whisper_stt(
    audio_file_path: str,
    output_file_path: str = "./output.csv"
):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,  # 청크별로 타임스탬프를 반환
        chunk_length_s=10,       # 입력 오디오를 10초씩 나누기
        stride_length_s=2,       # 2초씩 겹치도록 청크 나누기
    )

    result = pipe(audio_file_path)
    df = whisper_to_dataframe(result, output_file_path)

    return result, df


def whisper_to_dataframe(result, output_file_path):
    start_end_text = []

    for chunk in result["chunks"]:
        start = chunk["timestamp"][0]
        end = chunk["timestamp"][1]
        text = chunk["text"].strip()
        start_end_text.append([start, end, text])

    df = pd.DataFrame(start_end_text, columns=["start", "end", "text"])
    df.to_csv(output_file_path, index=False, sep="|")
    return df


def speaker_diarization(
    audio_file_path: str,
    output_rttm_file_path: str,
    output_csv_file_path: str
):
    # ① Hugging Face 토큰
    hf_token = os.getenv("HF_TOKEN")
    print(">>>>>>>>>>>>> HF_TOKEN in code:", hf_token)

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token
    )

    # ② cuda 사용 여부
    if torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))
        print("cuda is available")
    else:
        print("cuda is not available")

    # ③ soundfile로 오디오 로드
    audio, sample_rate = sf.read(audio_file_path)

    # (time,) 또는 (time, channels) → (channels, time)
    if audio.ndim == 1:          # 모노
        audio = audio[None, :]   # (1, time)
    else:                        # 스테레오 이상
        audio = audio.T          # (channels, time)

    waveform = torch.from_numpy(audio).float()

    file_dict = {
        "waveform": waveform,
        "sample_rate": sample_rate,
    }

    # ④ 화자 분리 실행
    out = pipeline(file_dict)                     # DiarizeOutput 객체
    ann = out.speaker_diarization                 # Annotation 객체

    # ⑤ RTTM 형식으로 저장 (이제 ann.write_rttm 사용)
    with open(output_rttm_file_path, "w", encoding="utf-8") as rttm:
        ann.write_rttm(rttm)

    # ⑥ RTTM → DataFrame 변환 (이 아래는 그대로 사용)
    df_rttm = pd.read_csv(
        output_rttm_file_path,
        sep=" ",
        header=None,
        names=[
            "type", "file", "chnl", "start", "duration",
            "C1", "C2", "speaker_id", "C3", "C4",
        ],
    )

    df_rttm["end"] = df_rttm["start"] + df_rttm["duration"]

    df_rttm["number"] = None
    df_rttm.at[0, "number"] = 0

    for i in range(1, len(df_rttm)):
        if df_rttm.at[i, "speaker_id"] != df_rttm.at[i - 1, "speaker_id"]:
            df_rttm.at[i, "number"] = df_rttm.at[i - 1, "number"] + 1
        else:
            df_rttm.at[i, "number"] = df_rttm.at[i - 1, "number"]

    df_rttm_grouped = df_rttm.groupby("number").agg(
        start=pd.NamedAgg(column="start", aggfunc="min"),
        end=pd.NamedAgg(column="end", aggfunc="max"),
        speaker_id=pd.NamedAgg(column="speaker_id", aggfunc="first"),
    )

    df_rttm_grouped["duration"] = (
        df_rttm_grouped["end"] - df_rttm_grouped["start"]
    )

    df_rttm_grouped.to_csv(
        output_csv_file_path,
        index=False,
        encoding="utf-8",
    )

    return df_rttm_grouped


if __name__ == "__main__":
    # 같은 폴더에 있는 agent_output.mp3 사용
    audio_file_path = "./agent_output.mp3"              # 원본 오디오 파일

    # 출력 파일들도 굳이 chap05 폴더 말고, 현재 폴더에 두셔도 됩니다.
    stt_output_file_path = "./agent_output_stt.csv"     # STT 결과 파일
    rttm_file_path = "./agent_output.rttm"              # 화자 분리 RTTM 파일
    rttm_csv_file_path = "./agent_output_rttm.csv"      # 화자 분리 CSV 파일

    # ① Whisper STT 실행 (주석 해제 후 사용)
    # result, df = whisper_stt(
    #     audio_file_path,
    #     stt_output_file_path
    # )
    # print(df)

    # ② 화자 분리 실행
    df_rttm = speaker_diarization(
        audio_file_path,
        rttm_file_path,
        rttm_csv_file_path
    )

    print(df_rttm)
