import streamlit as st
import requests
import json
import time
import random
import urllib.parse

st.set_page_config(page_title="AI 블로그 자동화", layout="centered")

# 로그인 관련 변수들
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 기본 함수들
def get_free_images(keyword, count=3):
    images = []
    for i in range(count):
        images.append({
            "url": f"https://picsum.photos/600/400?random={random.randint(1, 1000)}",
            "alt": f"{keyword} 관련 이미지 {i+1}"
        })
    return images

def get_current_season():
    month = time.localtime().tm_mon
    if 3 <= month <= 5:
        return "봄"
    elif 6 <= month <= 8:
        return "여름"
    elif 9 <= month <= 11:
        return "가을"
    else:
        return "겨울"

# AI 블로그 생성 함수 테스트
def generate_ai_blog(keyword, current_season):
    images = get_free_images(keyword, 3)
    
    title = f"{keyword} 완전 정복! 초보자도 3일만에 마스터하는 비법"
    hook = f"{keyword} 때문에 제 인생이 바뀌었다고 해도 과언이 아니에요."
    
    blog_content = f"""# {title}

{hook}

오늘은 제가 실제로 사용해보고 효과를 본 {keyword} 활용법을 공부해드릴게요.

<img src="{images[0]['url']}" alt="{images[0]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

## 🤔 왜 {keyword}를 시작하게 되었나요?

테스트 내용입니다.
"""
    return blog_content

# 메인 함수
def generate_local_blog(keyword, hook_style):
    current_season = get_current_season()
    return generate_ai_blog(keyword, current_season)

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

st.title("📝 AI 블로그 자동화 시스템")

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("진수 대표님 전용 블로그 자동화 로그인")
    user_id = st.text_input("아이디", value="aisulab")
    user_pw = st.text_input("비밀번호", value="!js44358574", type="password")
    
    if st.button("로그인"):
        if user_id == VALID_ID and user_pw == VALID_PW:
            st.session_state['login_ok'] = True
            st.success("✅ 로그인 성공!")
            st.rerun()
        else:
            st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    st.stop()

# 메인 화면
st.write("✅ 블로그 생성 함수 테스트")

# 키워드 입력
keyword = st.text_input("키워드 입력", value="AI")

if st.button("블로그 생성 테스트"):
    if keyword:
        try:
            content = generate_local_blog(keyword, "test")
            st.success("✅ 블로그 생성 성공!")
            st.markdown(content)
            st.session_state['generated_content'] = content
        except Exception as e:
            st.error(f"❌ 에러 발생: {str(e)}")
    else:
        st.warning("키워드를 입력해주세요!")