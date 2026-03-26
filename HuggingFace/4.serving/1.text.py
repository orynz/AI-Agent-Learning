import gradio as gr

# 함수 정의
def predict_sentiment(text):
    if any(word in text for word in ["좋아", "행복해"]):
        return "긍정적인 메시지입니다."
    elif any(word in text for word in ["슬픔", "외로움"]):
        return "힘내세요! 응원합니다~"
    else:
        return "평범한 메시지입니다."

# gradio 인터페이스 설정
demo = gr.Interface(
    fn= predict_sentiment,                                         # 실행할 함수
    inputs= gr.Textbox(placeholder="여기에 문장을 입력하세요..."), # 입력창
    outputs= "text",                                               # 결과창 (텍스트)
    title= "텍스트 감정 분석기",                                   # 웹페이지 제목
    description= "입력한 문장의 분위기를 AI가 분석합니다.",        # 설명
)

# 실행
if __name__ == "__main__":
    demo.launch()