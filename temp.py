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

# BLOGGER_PERSONAS 테스트
BLOGGER_PERSONAS = {
    "건강관리사_김민지": {"age": 32, "job": "병원 영양사", "location": "서울 강남구", "experience": "7년차"},
    "헬스트레이너_박준호": {"age": 28, "job": "개인 PT 트레이너", "location": "부산 해운대구", "experience": "5년차"},
    "약사_이수현": {"age": 35, "job": "동네 약국 약사", "location": "대구 수성구", "experience": "10년차"},
}

# get_free_images 함수 테스트
def get_free_images(keyword, count=3):
    """키워드별 실시간 이미지 검색 및 생성"""
    images = []
    for i in range(count):
        images.append({
            "url": f"https://picsum.photos/600/400?random={random.randint(1, 1000)}",
            "alt": f"{keyword} 관련 이미지 {i+1}"
        })
    return images

# 현재 계절 함수
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
st.write("✅ 로그인 완료!")
st.write("✅ BLOGGER_PERSONAS 로딩 완료!")
st.write("✅ get_free_images 함수 로딩 완료!")

# 함수 테스트
test_images = get_free_images("AI", 2)
st.write("이미지 테스트:", test_images)