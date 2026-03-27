import gradio as gr
import torch
from PIL import Image

from transformers import ViTImageProcessor, ViTForImageClassification

model_name = "google/vit-base-patch16-224"
processor = ViTImageProcessor.from_pretrained(model_name) # 전처리기
model = ViTForImageClassification.from_pretrained(model_name) # 분류기

def classify_image(img):
    if isinstance(img, torch.Tensor):
        img = img.numpy()

    img = Image.fromarray(img)
    inputs = processor(images=img, return_tensors="pt")

    # 모델예측
    with torch.no_grad(): # 자동 미분 엔진 비활성 -> 메모리 절약 및 속도 향상
        output = model(**inputs)
        logits = output.logits # 가공되지 않은 예측값(마지막 계층을 통과한 직후의 값, 확률로 변환되기 전 상태)

    # 확률로 변환
    # probs = torch.nn.functional.softmax(logits, dim=-1)[0]
    probs = torch.softmax(logits, dim=-1)
    # 상위 3개 클래스 추출
    top3_prob, top3_indices = torch.topk(probs[0], 3)

    results = {}
    for i in range(3):
        # 클래스 인덱스를 실제 라벨 이름으로 변환
        label = model.config.id2label[top3_indices[i].item()]
        # 라벨과 해당 확률을 딕셔너리에 저장
        results[label] = float(top3_prob[i])

    # 최종 결과 반환
    return results

# gradio 인터페이스 설정
demo = gr.Interface(
    fn= classify_image, # 실행할 함수
    inputs= gr.Image(
        type="numpy",
        sources=["upload"],
        label="이미지를 업로드하거나 드래그 하세요",
    ),
    outputs= gr.Label(num_top_classes=2), # 결과창 (분류 라벨 수치 표시)
    title= "이미지 분석 분석기", # 웹페이지 제목
    description="환경에 설치된 torch와 transformers를 사용합니다. 이미지 - 드래그 앤 드롭!",
)

# 실행
if __name__ == "__main__":
    demo.launch(inbrowser=True)

