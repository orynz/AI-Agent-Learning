
import streamlit as st
import os
import google.generativeai as genai
import json
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. Configuration & Setup
# -----------------------------------------------------------------------------
# API Key Setup
# You can set this in your environment variables or paste it in the sidebar
api_key = os.getenv("API_KEY")

st.set_page_config(
    page_title="SOMA4YOU All-in-One Blogging",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #B0B0B0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #4A4A4A;
    }
    .highlight {
        color: #4ECDC4;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Sidebar & Inputs
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ 설정")
    if not api_key:
        api_key = st.text_input("Gemini API Key", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API Key가 설정되었습니다.")
    else:
        st.warning("API Key를 입력해주세요.")

    st.divider()
    
    st.header("🎨 테마 선택")
    theme_options = {
        "🔵 블루-그레이": {"primary": "#1a73e8", "bg": "#f8f9fa"},
        "🌿 그린-오렌지": {"primary": "#34a853", "bg": "#f1f8e9"},
        "💜 퍼플-옐로우": {"primary": "#8e44ad", "bg": "#fdf6e3"},
        "🍵 틸-라이트그레이": {"primary": "#00796b", "bg": "#eceff1"},
        "🧱 테라코타": {"primary": "#e57373", "bg": "#fafafa"},
        "👔 클래식 블루": {"primary": "#0f4c81", "bg": "#f0f4f8"},
        "🌳 네이처 그린": {"primary": "#2e7d32", "bg": "#f1f8e9"},
    }
    selected_theme_name = st.selectbox("색상 테마", list(theme_options.keys()))
    selected_theme = theme_options[selected_theme_name]

# -----------------------------------------------------------------------------
# 3. Helper Functions (Gemini Service Logic)
# -----------------------------------------------------------------------------
def get_current_date():
    now = datetime.now()
    return now.strftime("%Y년 %m월 %d일 %A")

def generate_content(topic, theme_name, theme_colors, additional_req):
    if not api_key:
        st.error("API Key가 필요합니다.")
        return None

    model = genai.GenerativeModel('gemini-2.5-flash')
    current_date = get_current_date()
    
    # Prompt Construction (Simplified for Python)
    system_instruction = f"""
    You are an expert content creator specializing in SEO-optimized blog posts.
    Current Date: {current_date}
    Task: Create a blog post about "{topic}".
    Theme: {theme_name} (Primary Color: {theme_colors['primary']})
    
    Output Format: JSON
    The JSON must have the following structure:
    {{
        "blogPostHtml": "Full HTML content with inline styles...",
        "supplementaryInfo": {{
            "keywords": ["keyword1", "keyword2"...],
            "seoTitles": ["title1", "title2"...],
            "imagePrompt": "Description for DALL-E...",
            "altText": "Korean alt text..."
        }},
        "socialMediaPosts": {{
            "threads": "...",
            "instagram": "...",
            "facebook": "...",
            "x": "..."
        }}
    }}
    
    Requirements:
    1. Write in Korean.
    2. Use inline CSS for styling matching the theme.
    3. Include a summary card and FAQ section.
    4. {additional_req if additional_req else "No additional requests."}
    """

    try:
        response = model.generate_content(
            contents=f"Write a blog post about: {topic}",
            config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

def suggest_topics(category):
    if not api_key: return []
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Suggest 10 creative blog post topics for the category: {category}. Return as a JSON object {{'topics': ['topic1', ...]}}"
    try:
        response = model.generate_content(
            contents=prompt,
            config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(response.text).get('topics', [])
    except:
        return []

# -----------------------------------------------------------------------------
# 4. Main UI Layout
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">GPT PARK 의 올인원 블로깅 <sup style="font-size: 1rem; color: #4ECDC4;">BASIC</sup></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Python Streamlit Version</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["💡 주제 아이디어 얻기", "✨ 포스트 생성하기"])

with tab1:
    st.markdown("### 카테고리별 주제 추천")
    category = st.selectbox("카테고리 선택", [
        "재정/투자", "IT/기술", "생활/라이프스타일", "건강/자기계발", "교육/학습", "쇼핑/소비"
    ])
    
    if st.button("주제 추천받기"):
        with st.spinner("AI가 주제를 생각 중입니다..."):
            topics = suggest_topics(category)
            if topics:
                st.success("추천 주제:")
                for t in topics:
                    st.info(t)

with tab2:
    st.markdown("### 블로그 포스트 생성")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        topic_input = st.text_input("블로그 주제", placeholder="예: 2024년 최고의 AI 툴")
    with col2:
        additional_req = st.text_area("추가 요청사항", placeholder="예: 초보자가 이해하기 쉽게 써주세요.", height=100)
    
    generate_btn = st.button("🚀 포스트 생성 시작", type="primary", use_container_width=True)

    if generate_btn and topic_input:
        with st.spinner("블로그 포스트를 작성 중입니다... (약 30초 소요)"):
            result = generate_content(topic_input, selected_theme_name, selected_theme, additional_req)
            
            if result:
                st.session_state['generated_result'] = result
                st.balloons()

    # Display Results
    if 'generated_result' in st.session_state:
        res = st.session_state['generated_result']
        
        st.divider()
        st.subheader("📄 생성된 콘텐츠")
        
        # HTML Preview
        with st.expander("Web Preview (HTML)", expanded=True):
            st.components.v1.html(res['blogPostHtml'], height=800, scrolling=True)
        
        # HTML Code
        with st.expander("HTML Source Code"):
            st.code(res['blogPostHtml'], language='html')
            
        # Supplementary Info
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown("#### 🔑 SEO 키워드")
            st.write(", ".join(res['supplementaryInfo']['keywords']))
            
            st.markdown("#### 🖼️ 이미지 프롬프트")
            st.info(res['supplementaryInfo']['imagePrompt'])
            
        with col_info2:
            st.markdown("#### 🏷️ SEO 제목 제안")
            for title in res['supplementaryInfo']['seoTitles']:
                st.write(f"- {title}")

        # Social Media
        st.divider()
        st.subheader("📱 소셜 미디어 포스트")
        social = res['socialMediaPosts']
        
        s_tabs = st.tabs(["Threads", "Instagram", "Facebook", "X"])
        with s_tabs[0]: st.text_area("Threads", social['threads'], height=200)
        with s_tabs[1]: st.text_area("Instagram", social['instagram'], height=200)
        with s_tabs[2]: st.text_area("Facebook", social['facebook'], height=200)
        with s_tabs[3]: st.text_area("X", social['x'], height=200)

