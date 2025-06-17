import streamlit as st
import requests
import json
import time
import random

st.set_page_config(page_title="AI 블로그 자동화", layout="centered")

# 로그인 관련 변수들
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

st.title("📝 AI 블로그 자동화 시스템")
st.write("로그인 테스트")

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

st.write("로그인 완료! 메인 화면입니다.")