import streamlit as st

# 1. session_state 초기화
# 'my_text_input_value'라는 키로 세션 상태에 기본값을 설정합니다.
if 'my_text_input_value' not in st.session_state:
    st.session_state['my_text_input_value'] = '기본 텍스트'

# 2. 값 업데이트를 위한 콜백 함수 정의
# 이 함수는 버튼이 클릭될 때 호출되며, 세션 상태의 값을 변경합니다.
def update_text_value():
    st.session_state['my_text_input_value']
    # 콜백 함수 내에서 st.rerun()은 일반적으로 필요하지 않지만, 
    # 특정 복잡한 로직에서는 필요할 수 있습니다. 여기서는 생략합니다.

# 3. st.text_input 위젯 생성 및 session_state와 연결
# 위젯의 value를 session_state 값으로 설정하고, key를 지정합니다.
st.text_input(
    label='텍스트 입력', 
    key='my_text_input', # 위젯 자체의 키
    value=st.session_state['my_text_input_value'] # 세션 상태의 값을 초기값으로 사용
)

# 4. 값 변경을 트리거할 버튼 생성 (콜백 함수 연결)
st.button('텍스트 입력 값 변경', on_click=update_text_value)

# 현재 입력된 값 확인 (사용자가 입력한 값 또는 변경된 값)
st.write('현재 입력된 값:', st.session_state['my_text_input'])

# # session_state 초기화
# if 'text_input_value' not in st.session_state:
#     st.session_state['text_input_value'] = '초기값'

# # 텍스트 입력값 업데이트를 위한 콜백 함수
# def update_value():
#     st.session_state['text_input_value'] = '업데이트된 새로운 값'

# # 텍스트 입력값 초기화를 위한 콜백 함수
# def clear_value():
#     st.session_state['text_input_value'] = ''

# # key를 사용하여 text_input을 session_state와 연결
# st.text_input(
#     '텍스트를 입력하세요',
#     key='text_input_value', # session_state 키와 동일하게 설정
# )

# st.write(f"현재 입력된 값: {st.session_state['text_input_value']}")

# # 버튼 클릭 시 콜백 함수 실행
# st.button('값 업데이트', on_click=update_value)
# st.button('값 비우기', on_click=clear_value)