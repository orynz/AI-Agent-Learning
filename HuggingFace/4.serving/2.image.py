import gradio as gr
import numpy as np


# 함수 정의
def classify_image(img):
    avg_brightness = np.mean(img) # 0 ~ 255
    
    if avg_brightness > 127:
        return {"밝은 이미지": 1.0, "어두운 이미지": 0.0}
    else:
        return {"밝은 이미지": 0.0, "어두운 이미지": 1.0}

# gradio 인터페이스 설정
demo = gr.Interface(
    fn= classify_image,                               # 실행할 함수
    inputs= gr.Image(placeholder="이미지 업로드..."), # 입력창
    outputs= gr.Label(num_top_classes=2),             # 결과창 (분류 라벨 수치 표시)
    title= "이미지 분석 분석기",                      # 웹페이지 제목
)

# 실행
if __name__ == "__main__":
    demo.launch()