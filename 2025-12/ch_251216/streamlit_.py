
import streamlit as st

# 참고 사이트 :  https://gunrestaurant.tistory.com/42 
st.title("무엇이든 물어보세요?!")

title_image_url = "/contents/title_image.png"
st.markdown(f'<div class="title><img src="{title_image_url}" alt="Title Image"></div>', unsafe_allow_html=True)

def display_chat_message(role, content, avatar_url):
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    