import gradio as gr

from transformers import pipeline
import torch 

import os

# TensorFlow(테라플로) 라이브러리를 사용하지 않겠다고 명시적으로 설정
os.environ["TRANSFORMERS_NO_TF"] = "1"

device = 0 if torch.cuda.is_available() else -1

classifier = pipeline(
    task="text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=device,
)

def analyze_setiment(text: str):
    if not text or not text.strip():                  # 파이썬에서 빈 문자열("")은 False
        return "문장을 입력하세요", None  # 공백 제거 후 내용이 없으면 None 반환
    
    result = classifier(text)
    label = result[0]["label"]
    score = result[0]["score"]
    
    positive_score = float(score if label == "POSITIVE" else 1 - score)
    probability_dict = {
        "POSITIVE": positive_score,
        "NEGATIVE": 1 - positive_score,
    }
    result_text = f"감정결과: {label} 신뢰도: {score:.4f}"
    return result_text, probability_dict
    
with gr.Blocks() as demo:
    gr.Markdown("감정 분석 웹 서비스")
    gr.Markdown("문장을 입력하면 감정을 분석하고 확률을 그래프로 보여줍니다!")
    
    input_text = gr.Textbox(
        label= "문장을 입력하세요(English Only)",
        placeholder="e.g. I love AI",
        lines=3
    )
    
    btn_analyze = gr.Button(value="분석하기",)
    
    output_text = gr.Textbox(
        label= "분석결과",
        interactive=False,
    )
    
    output_label = gr.Label(value="감정 확률 그래프",)
    
    btn_analyze.click(
        fn=analyze_setiment,
        inputs=input_text,
        outputs=[output_text, output_label]
    )
    
    
# 실행
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)