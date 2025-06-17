import streamlit as st
import requests
import json
import time
import random
import urllib.parse

# 페이지 설정 (맨 처음에)
st.set_page_config(
    page_title="AI 블로그 자동화 Pro", 
    page_icon="🚀",
    layout="wide"
)

# 로그인 정보
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("🚀 AI 블로그 자동화 Pro")
    st.markdown("### 진수 대표님 전용 시스템")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_id = st.text_input("아이디", value="aisulab")
        user_pw = st.text_input("비밀번호", value="!js44358574", type="password")
        
        if st.button("🔑 로그인", use_container_width=True):
            if user_id == VALID_ID and user_pw == VALID_PW:
                st.session_state['login_ok'] = True
                st.success("✅ 로그인 성공!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    st.stop()

# 메인 화면
st.title("🚀 AI 블로그 자동화 Pro")
st.markdown("### 💰 수익화 최적화 + 📈 SEO 자동화 + 🔄 자동 게시")

# 로그아웃 버튼
if st.button("🚪 로그아웃"):
    st.session_state['login_ok'] = False
    st.rerun()

st.success("✅ 기본 시스템 로딩 완료!")
st.info("💡 다음 단계: 블로그 생성 엔진 추가 예정")