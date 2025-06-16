import streamlit as st
import requests

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

# 1차 로그인
if not st.session_state['login_ok']:
    st.title("대표님 전용 블로그 자동화 로그인")
    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        if user_id == VALID_ID and user_pw == VALID_PW:
            st.session_state['login_ok'] = True
            st.success("로그인 성공! 자동화 프로그램을 시작합니다.")
            st.experimental_rerun()  # 페이지 새로 고침
        else:
            st.error("아이디/비밀번호가 틀렸습니다.")
    st.stop()

# 로그인 후 본문 코드 (AI 자동화 등)
st.set_page_config(page_title="AI 통합 블로그 자동화", layout="centered")
st.title("AI 자동 건강 블로그 생성 · 워드프레스 자동 업로드")

# 모델 선택 옵션 추가
model_choice = st.selectbox("AI 모델 선택", ["OpenAI GPT-3.5", "Claude", "로컬 AI 모델"])

st.markdown(
    """
    #### 사용법  
    1. 포스팅 주제(키워드)만 입력하세요  
    2. 'AI 블로그 글 생성' 클릭  
    3. 글이 마음에 들면 워드프레스 업로드 or 네이버 복사  
    ---
    """
)

keyword = st.text_input("블로그 주제/키워드", placeholder="예: 혈압 낮추는 음식")
openai_key = st.text_input("OpenAI API 키", type="password", help="https://platform.openai.com/api-keys 에서 발급")

ai_content = ""
if st.button("AI 블로그 글 생성"):
    if not keyword or not openai_key:
        st.warning("키워드와 OpenAI API 키를 모두 입력해주세요.")
    else:
        with st.spinner("AI가 글을 작성 중입니다..."):
            if model_choice == "OpenAI GPT-3.5":
                # OpenAI GPT API 호출
                prompt = f"{keyword} 주제로 2024년 최신 건강정보 블로그 글을 써줘."
                headers = {
                    "Authorization": f"Bearer {openai_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1800,
                    "temperature": 0.7
                }
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
                if response.status_code == 200:
                    ai_content = response.json()["choices"][0]["message"]["content"].strip()
                else:
                    st.error(f"OpenAI 에러: {response.text}")

            elif model_choice == "Claude":
                # Claude API 호출 (예시)
                st.error("Claude API 호출 기능은 아직 구현되지 않았습니다.")

            elif model_choice == "로컬 AI 모델":
                # 로컬 AI 모델 호출 (예시)
                st.error("로컬 AI 모델 호출 기능은 아직 구현되지 않았습니다.")

        if ai_content:
            st.success("AI 블로그 글 생성 완료!")
            st.text_area("AI가 쓴 블로그 글", ai_content, height=400)

st.markdown("---")
st.subheader("워드프레스 자동 업로드")

wp_url = st.text_input("워드프레스 주소 (https://로 시작)", key="wp_url")
wp_id = st.text_input("워드프레스 아이디", key="wp_user")
wp_pw = st.text_input("워드프레스를 비밀번호", type="password", key="wp_pw")

auto_title = ""
auto_content = ""
if ai_content:
    lines = [line.strip() for line in ai_content.split('\n') if line.strip()]
    auto_title = lines[0] if lines else keyword
    auto_content = ai_content
else:
    auto_title = st.text_input("업로드할 글 제목 (직접 입력/AI 글 생성 후 자동 입력)", key="wp_title")
    auto_content = st.text_area("업로드할 글 내용 (직접 입력/AI 글 생성 후 자동 입력)", key="wp_content")

if st.button("워드프레스로 글 업로드"):
    if not (wp_url and wp_id and wp_pw and (auto_title or auto_content)):
        st.warning("워드프레스 주소, 아이디, 비밀번호, 글 제목/내용을 모두 입력해주세요.")
    else:
        api_url = f"{wp_url}/wp-json/wp/v2/posts"
        data = {"title": auto_title, "content": auto_content, "status": "publish"}
        try:
            res = requests.post(api_url, json=data, auth=(wp_id, wp_pw))
            if res.status_code == 201:
                st.success("워드프레스 업로드 성공!")
            else:
                st.error(f"워드프레스 오류: {res.status_code}, {res.text}")
        except Exception as e:
            st.error(f"워드프레스를 연동하는 중 에러가 발생했습니다: {e}")

st.markdown("---")
st.subheader("네이버 블로그: 글 복사해서 등록 (공식 API 없음)")
if ai_content:
    st.info("아래 내용 복사해서 네이버 블로그에 새 글로 붙여넣으세요!")
    st.code(auto_title + "\n\n" + auto_content, language="markdown")

st.caption("by 대표님 자동화 파이프라인")