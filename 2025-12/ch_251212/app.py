import time
import numpy as np
import pandas as pd
import streamlit as st



st.title("세션 상태 예제 1")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("메시지 입력")

if st.button("추가"):
    st.session_state.messages.append(user_input)

st.write("대화 기록:")
for msg in st.session_state.messages:
    st.write("-", msg)

# st.divider()
# st.title("세션 상태 예제 2")
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.user_input = ""

# def enterFn():
#     text = st.session_state.user_input
#     st.session_state.messages.append(text)
#     st.session_state.user_input = ""
    
# st.text_input("메시지 입력", key="user_input", on_change = enterFn,)

# st.write("대화 누적 기록:")
# for msg in st.session_state.messages:
#     st.write("-", msg)




# user_input = st.text_input("메시지 입력", value=st.session_state.txt,)
#                         #    on_change=enterFn)


# if st.session_state.enter:
#     st.session_state.message.append(user_input)
#     st.session_state.txt = ""

# st.write("대화 기록:")
# for msg in st.session_state.message:
#     st.write("-", msg)




st.title("레이아웃 구성 예제")

st.header("버튼을 가로로 배치했어요")
left, middle, right = st.columns(3)

if left.button("일반 버튼", width="stretch"):
    left.markdown("You clicked")

if middle.button("이모지 버튼", width="stretch", icon="😃"):
    middle.markdown("emoji clicked")
    
if right.button("Material button", icon=":material/mood:", width="stretch"):
    right.markdown("You clicked Matetial button.")
    


with st.sidebar:
    st.header("사이드바")
    model_name = st.selectbox("모델 선택", ["gpt-4.1-mini", "gpt-4.1"])


col1, col2 = st.columns(2)

with col1:
    st.write("왼쪽 영역")
    question = st.text_input("질문", width="stretch")

with col2:
    st.write("오른쪽 영역")
    st.write(f"선택한 모델: {model_name}")


st.write(f"사용자: {question}")
_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)

st.header('st.latex')
st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')



st.title('st.file_uploader')

st.subheader('Input CSV')
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file, encoding='CP949')
  st.subheader('DataFrame')
  st.write(df)
  st.subheader('Descriptive Statistics')
  st.write(df.describe())
else:
  st.info('☝️ Upload a CSV file')
  
  
st.title("입력 박스")
animal_shelter = ['고래', '강아지', '토끼', '새']

animal = st.text_input('고래, 강아지, 토끼, 새 중 입력 해보세요.')

if st.button('클릭!!'):
    have_it = animal.lower() in animal_shelter
    '정답' if have_it else '오답'

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    falg = False if st.session_state.clicked else True
    st.session_state.clicked = falg
    
st.button('Click me ㅋㅋㅋ', on_click=click_button)
st.markdown("---")
if st.session_state.clicked:
    st.write("슬라이딩 바")
    st.slider("선택")
else:
    pass
    

