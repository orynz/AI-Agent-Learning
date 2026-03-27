import torch
import gradio as gr
from gtts import gTTS
from transformers import pipeline

# 모델 설정 정보
MODELS = {
    "한국어 전용 (KoELECTRA - 6감정)": "Jinuuuu/KoELECTRA_fine_tunning_emotion",
    "다국어 지원 (GoEmotions - 28감정)": "AnasAlokla/multilingual_go_emotions"
}

# 파이프라인 캐싱을 위한 딕셔너리
pipelines = {}

def get_classifier(model_name):
    """선택된 모델에 따라 파이프라인을 로드하거나 반환합니다."""
    model_id = MODELS[model_name]
    if model_id not in pipelines:
        pipelines[model_id] = pipeline(
            task="text-classification",
            model=model_id,
            top_k=None,
            device=0 if torch.cuda.is_available() else -1
        )
    return pipelines[model_id]

def analyze_and_tts(text, model_choice, lang_choice):
    if not text or not text.strip():
        msg = "문장을 입력해주세요." if lang_choice == "ko" else "Please enter a sentence."
        return msg, None, None
    
    # 선택된 모델로 분류기 가져오기
    classifier = get_classifier(model_choice)
    results = classifier(text)[0]
    
    # 결과 가공
    prob_dict = {res['label']: float(res['score']) for res in results}
    top_result = results[0]
    
    # 결과 메시지 구성
    if lang_choice == "ko":
        result_summary = f"모델: {model_choice}\n결과: [{top_result['label']}] (신뢰도: {top_result['score']:.2%})"
    else:
        result_summary = f"Model: {model_choice}\nResult: [{top_result['label']}] (Confidence: {top_result['score']:.2%})"
    
    # TTS 생성 (선택한 언어 적용)
    try:
        tts = gTTS(text=text, lang=lang_choice)
        audio_path = f"output_{lang_choice}.mp3"
        tts.save(audio_path)
    except Exception as e:
        print(f"TTS Error: {e}")
        audio_path = None

    return result_summary, prob_dict, audio_path

def change_ui_lang(lang):
    if lang == "ko":
        return {
            title_md: "# 🌍 다국어 감정 분석 및 TTS 서비스",
            input_text: gr.update(label="분석할 문장 입력", placeholder="기분을 입력하세요..."),
            btn_analyze: gr.update(value="분석 및 음성 생성"),
            output_summary: gr.update(label="요약 결과"),
            output_label: gr.update(label="감정별 확률 분포"),
            output_audio: gr.update(label="문장 읽어주기 (TTS)")
        }
    else:
        return {
            title_md: "# 🌍 Multilingual Emotion Analysis & TTS",
            input_text: gr.update(label="Input Text", placeholder="How are you feeling?"),
            btn_analyze: gr.update(value="Analyze & Generate Speech"),
            output_summary: gr.update(label="Summary Result"),
            output_label: gr.update(label="Emotion Probability Distribution"),
            output_audio: gr.update(label="Listen to Sentence (TTS)")
        }
        
# Gradio UI 구성
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    title_md = gr.Markdown("# 🌍 다국어 감정 분석 및 TTS 서비스")
    
    with gr.Row():
        with gr.Column(scale=1):
            lang_selector = gr.Radio(
                choices=["ko", "en"], 
                value="ko", 
                label="사용 언어 선택 (Language Selection)",
                info="TTS 음성 및 UI 언어를 설정합니다."
            )
            model_selector = gr.Dropdown(
                choices=list(MODELS.keys()),
                value=list(MODELS.keys())[0],
                label="분석 모델 선택 (Select Model)"
            )
            input_text = gr.Textbox(
                label="분석할 문장 입력",
                placeholder="기분이나 생각을 입력해보세요...",
                lines=5
            )
            btn_analyze = gr.Button("분석 및 음성 생성", variant="primary")
            
        with gr.Column(scale=1):
            output_summary = gr.Textbox(label="요약 결과", interactive=False)
            output_label = gr.Label(label="감정별 확률 분포", num_top_classes=8)
            output_audio = gr.Audio(label="문장 읽어주기 (TTS)", type="filepath")

    # 언어 변경 이벤트
    lang_selector.change(
        fn=change_ui_lang, 
        inputs=lang_selector, 
        outputs=[title_md, input_text, btn_analyze, output_summary, output_label, output_audio]
    )

    # 분석 버튼 이벤트
    btn_analyze.click(
        fn=analyze_and_tts,
        inputs=[input_text, model_selector, lang_selector],
        outputs=[output_summary, output_label, output_audio]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)