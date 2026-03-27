import gradio as gr
import torch
from PIL import Image
from transformers import (
    ViTImageProcessor, ViTForImageClassification,
    BlipProcessor, BlipForConditionalGeneration
)
from deep_translator import GoogleTranslator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

vit_model_name = "google/vit-base-patch16-224"
vit_processor = ViTImageProcessor.from_pretrained(vit_model_name)
vit_model = ViTForImageClassification.from_pretrained(vit_model_name).to(device)

blip_model_name = "Salesforce/blip-image-captioning-base"
blip_processor = BlipProcessor.from_pretrained(blip_model_name)
blip_model = BlipForConditionalGeneration.from_pretrained(blip_model_name).to(device)

translator = GoogleTranslator(source='en', target='ko')

def analyze_all(img, user_prompt):
    if img is None:
        return "이미지를 업로드해주세요.", "", ""

    pil_img = Image.fromarray(img)

    # --- [Step 1: ViT 정밀 분류] ---
    vit_inputs = vit_processor(images=pil_img, return_tensors="pt").to(device)
    with torch.no_grad():
        vit_outputs = vit_model(**vit_inputs)
        probs = torch.softmax(vit_outputs.logits, dim=-1)
        top1_prob, top1_idx = torch.topk(probs[0], 1)

    obj_name_en = vit_model.config.id2label[top1_idx[0].item()]
    obj_conf = top1_prob[0].item()

    # --- [Step 2: BLIP 상황 묘사] ---
    prompt = user_prompt.strip() if user_prompt and user_prompt.strip() else None

    if prompt:
        # ✅ 핵심 수정: BLIP conditional generation
        # 프롬프트를 text로 넘기면 BLIP이 이를 prefix로 붙여 생성함
        # → 출력에서 prefix를 반드시 제거해야 함
        blip_inputs = blip_processor(
            images=pil_img, text=prompt, return_tensors="pt"
        ).to(device)
    else:
        blip_inputs = blip_processor(images=pil_img, return_tensors="pt").to(device)

    with torch.no_grad():
        blip_out = blip_model.generate(
            **blip_inputs,
            max_new_tokens=100,
            num_beams=5
        )

    # decode 전체 결과 (프롬프트 포함 가능성 있음)
    caption_full = blip_processor.decode(blip_out[0], skip_special_tokens=True)

    # ✅ 핵심 수정: 프롬프트 제거 로직 강화
    if prompt:
        caption_en = _remove_prompt_prefix(caption_full, prompt)
    else:
        caption_en = caption_full.strip()

    if not caption_en:
        caption_en = "No description generated."

    # --- [Step 3: 번역 및 통합 추론 생성] ---
    try:
        obj_name_ko = translator.translate(obj_name_en)
        caption_ko = translator.translate(caption_en)

        final_insight = (
            f"🔍 **핵심 피사체:** 이 이미지의 주요 객체는 '{obj_name_ko}'({obj_conf*100:.1f}% 확신)입니다.\n\n"
            f"📝 **상황 묘사:** 현재 {caption_ko} 상황인 것으로 추론됩니다."
        )
    except Exception:
        final_insight = f"분류: {obj_name_en}\n설명: {caption_en}"

    return final_insight, f"{obj_conf*100:.1f}%", caption_en


def _remove_prompt_prefix(caption: str, prompt: str) -> str:
    """
    BLIP 출력에서 입력 프롬프트 prefix를 제거합니다.
    대소문자, 앞뒤 공백, 구두점 차이를 모두 처리합니다.
    """
    caption_stripped = caption.strip()
    prompt_stripped = prompt.strip()

    # 1차: 단순 소문자 비교로 시작 부분 제거
    if caption_stripped.lower().startswith(prompt_stripped.lower()):
        result = caption_stripped[len(prompt_stripped):].strip()
        # 남은 앞부분이 구두점/공백으로 시작하면 제거
        result = result.lstrip(" ,.:;-")
        return result

    # 2차: 프롬프트 단어들이 앞에 포함된 경우 (단어 단위 매칭)
    prompt_words = prompt_stripped.lower().split()
    caption_words = caption_stripped.lower().split()
    if caption_words[:len(prompt_words)] == prompt_words:
        original_words = caption_stripped.split()
        result = " ".join(original_words[len(prompt_words):]).strip()
        return result

    # 3차: 제거 불필요 (프롬프트가 포함 안 된 경우) → 그대로 반환
    return caption_stripped


# Gradio 대시보드
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🏢 AI 시각 통합 분석 대시보드")
    gr.Markdown("ViT와 BLIP 모델이 협력하여 이미지를 분석합니다.")

    with gr.Row():
        with gr.Column(scale=2):
            input_image = gr.Image(label="분석 대상 이미지", type="numpy")
            prompt_input = gr.Textbox(
                label="추론 프롬프트 (영문 권장)",
                placeholder="예: 'The color of the car is', 'What is the weather like?', 'A photo of'"
            )
            submit_btn = gr.Button("종합 분석 실행", variant="primary")

        with gr.Column(scale=3):
            with gr.Group():
                gr.Markdown("### 🧠 AI 통합 분석 리포트")
                output_final = gr.Markdown("이미지를 분석하면 결과가 여기에 표시됩니다.")

            with gr.Row():
                output_conf = gr.Textbox(label="객체 인식 신뢰도")
                output_en_raw = gr.Textbox(label="BLIP 원문 (En)")

    # ✅ 핵심 수정: Examples 컬럼 수를 inputs 수와 맞춤 (1개)
    gr.Examples(
        examples=[
            ["A photo of a"],
            ["This image shows"],
            ["The color of the main object is"],
        ],
        inputs=[prompt_input],
        label="프롬프트 예시 (클릭하면 자동 입력)"
    )

    submit_btn.click(
        fn=analyze_all,
        inputs=[input_image, prompt_input],
        outputs=[output_final, output_conf, output_en_raw],
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True)