import streamlit as st
import requests

st.set_page_config(page_title="AI 통합 블로그 자동화", layout="centered")
st.title("AI 자동 건강 블로그 생성 · 워드프레스 자동 업로드")

st.markdown(
    """
    #### 사용법  
    1. 포스팅 주제(키워드)만 입력하세요  
    2. 'AI 블로그 글 생성' 클릭  
    3. 글이 마음에 들면 워드프레스 업로드 or 네이버 복사  
    ---
    """
)

# 1. 사용자 입력 (키워드)
keyword = st.text_input("블로그 주제/키워드", placeholder="예: 혈압 낮추는 음식, 탈모 예방, 건강검진 준비")

# 2. OpenAI API 키 입력 (보안 때문에 직접 입력)
openai_key = st.text_input("OpenAI API 키", type="password", help="https://platform.openai.com/api-keys 에서 발급")

ai_content = ""
# 3. AI 글 생성
if st.button("AI 블로그 글 생성"):
    if not keyword or not openai_key:
        st.warning("키워드와 OpenAI API 키를 모두 입력해주세요.")
    else:
        with st.spinner("AI가 글을 작성 중입니다..."):
            prompt = (
                f"{keyword} 주제로 2024년 최신 건강정보 블로그 글을 써줘. "
                "매우 눈에 띄는 제목, 소제목 3개, 실제 전문가 조언/연구결과 인용, "
                "결론엔 실질적인 건강 팁·행동 유도(CTA) 반드시 포함. "
                "전체 분량은 1500자 이상, 문단/소제목 구분, 한국어로."
            )
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
                st.success("AI 블로그 글 생성 완료!")
                st.text_area("AI가 쓴 블로그 글", ai_content, height=400)
            else:
                st.error(f"OpenAI 에러: {response.text}")

# 4. 워드프레스 정보 입력 (자동 업로드)
st.markdown("---")
st.subheader("워드프레스 자동 업로드")

wp_url = st.text_input("워드프레스 주소 (https://로 시작)", key="wp_url")
wp_id = st.text_input("워드프레스 아이디", key="wp_user")
wp_pw = st.text_input("워드프레스 비밀번호", type="password", key="wp_pw")
auto_title = ""
auto_content = ""

# 글 제목/본문 자동 추출
if ai_content:
    # 제목: 첫 줄 혹은 "#", "**" 등으로 시작하는 부분 추출
    lines = [line.strip() for line in ai_content.split('\n') if line.strip()]
    # 소제목(~3개)와 결론도 자동 추출, 필요시 추후 고도화 가능
    auto_title = lines[0] if lines else keyword
    auto_content = ai_content

else:
    auto_title = st.text_input("업로드할 글 제목 (AI 글 생성 후 자동 입력, 직접 입력 가능)", key="wp_title")
    auto_content = st.text_area("업로드할 글 내용 (AI 글 생성 후 자동 입력, 직접 입력 가능)", key="wp_content")

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
            st.error(f"워드프레스 연동 에러: {e}")

# 5. 네이버 블로그 복붙 안내
st.markdown("---")
st.subheader("네이버 블로그: 글 복사해서 등록 (공식 API 없음)")
if ai_content:
    st.info("아래 내용 복사해서 네이버 블로그에 새 글로 붙여넣으세요!")
    st.code(auto_title + "\n\n" + auto_content, language="markdown")

st.caption("by 수랩대표님 자동화 파이프라인")