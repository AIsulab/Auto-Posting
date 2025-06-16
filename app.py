import streamlit as st
import requests

# ▶ 무료 AI 모델: 한글과 영어 모두 지원 (HuggingFace)
MODELS = {
    "HuggingFace KoGPT2 (한글)": "skt/kogpt2-base-v2",
    "HuggingFace GPT2 (영어/글로벌)": "gpt2"
}

st.set_page_config(page_title="광고 수익형 무료 AI 블로그 자동화", layout="centered")
st.title("📝 광고 수익형 무료 AI 블로그 자동화 시스템")

st.subheader("🤖 AI 글 생성")
st.markdown("""- **강한 훅, 신뢰성, 재미, CTA가 포함된 고수익/체류형 블로그 글 자동 생성**  
- *워드프레스&네이버 자동 관리 기반, 무료 AI로 PC/모바일 어디서나 구동!*""")

# 모델 선택
model_choice = st.selectbox("AI 글 생성 무료 모델 선택", list(MODELS.keys()))

keyword = st.text_input("블로그 주제/키워드", placeholder="예) 혈압에 좋은 음식, 다이어트 성공사례, 정신건강 꿀팁 등")
if st.button("AI 블로그 글 생성"):
    if not keyword:
        st.warning("키워드를 입력해 주세요.")
    else:
        hf_api_url = f"https://api-inference.huggingface.co/models/{MODELS[model_choice]}"
        prompt = (
            f"블로그 구독자가 '{keyword}' 키워드로 검색했을 때 바로 눈길을 사로잡는 충격적 질문/경험/팩트로 시작해줘. "
            "문제의식-인사이트-전문가 정보-실제행동팁(체류/공감/신뢰/CTA/광고 유도 모두 포함). "
            "중간에 유머, 실전사례, 의심해소, 최신트렌드도 자연스럽게 곁들여. 마지막엔 '실제 행동' 권유, 댓글/공유 요청, 관련글/상품/서비스 추천도 추가! "
            "반드시 제목도 포함해 1500자 이상, 소제목/문단 구분, 한글로만 작성."
        )
        with st.spinner('무료 AI가 글을 작성 중입니다... (최대 30초 대기)'):
            headers = {}  # 무료이므로 API키 필요 X
            data = {"inputs": prompt, "max_new_tokens": 512}
            response = requests.post(hf_api_url, headers=headers, json=data)
            try:
                result = response.json()[0]['generated_text']
                st.success("AI 블로그 글 생성 완료!")
                st.text_area("생성된 블로그 글 (후킹/체류시간/CTA 반영)", result, height=400)
                st.session_state["ai_title"] = result.split('\n')[0] if result else ""
                st.session_state["ai_content"] = result
            except Exception:
                st.error("무료 HuggingFace API 호출이 일시적으로 제한됐거나, 모델 활성화 대기 중입니다. 잠시 후 다시 시도해 주세요.")

st.markdown("---")
st.subheader("📤 워드프레스 자동 업로드")
wp_url = st.text_input("워드프레스 주소 (https://로 시작)", key="wp_url")
wp_id = st.text_input("워드프레스 아이디", key="wp_user")
wp_pw = st.text_input("워드프레스 비밀번호", type="password", key="wp_pw")
post_title = st.text_input("업로드할 글 제목", value=st.session_state.get("ai_title", ""), key="wp_title")
post_content = st.text_area("업로드할 글 내용", value=st.session_state.get("ai_content", ""), key="wp_content")

if st.button("워드프레스로 글 업로드"):
    if not (wp_url and wp_id and wp_pw and post_title and post_content):
        st.warning("워드프레스 정보와 글 내용을 모두 입력해 주세요.")
    else:
        api_url = f"{wp_url}/wp-json/wp/v2/posts"
        data = {"title": post_title, "content": post_content, "status": "publish"}
        try:
            res = requests.post(api_url, json=data, auth=(wp_id, wp_pw))
            if res.status_code == 201:
                st.success("워드프레스 업로드 성공!")
            else:
                st.error(f"워드프레스 오류: {res.status_code}, {res.text}")
        except Exception as e:
            st.error(f"워드프레스를 연동하는 중 에러: {e}")

st.markdown("---")
st.subheader("📋 네이버 블로그 복사")
st.info("아래 내용을 복사해서 네이버 블로그 새 글에 붙여넣으세요!")
st.code(f"{st.session_state.get('ai_title','')}\n\n{st.session_state.get('ai_content','')}", language="markdown")
st.caption("by 대표님 광고수익형 AI 자동화 파이프라인")