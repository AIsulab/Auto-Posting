import streamlit as st
import requests
import json
import time

# 무료 AI 모델 설정
FREE_AI_MODELS = {
    "Hugging Face - GPT2": "gpt2",
    "Hugging Face - DialoGPT": "microsoft/DialoGPT-medium", 
    "Cohere 무료 모델": "command-light",
    "OpenAI GPT-3.5": "gpt-3.5-turbo"
}

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
            time.sleep(1)  # 1초 대기
            st.rerun()  # 페이지 새로고침
        else:
            st.error("아이디/비밀번호가 틀렸습니다.")
    st.stop()

# 메인 화면
st.title("📝 AI 블로그 자동화 시스템")
st.markdown("### 🤖 AI 글 생성 | 📤 워드프레스 업로드 | 📋 네이버 블로그 복사")

# AI 모델 선택
st.markdown("---")
st.subheader("🤖 AI 모델 선택")

selected_model = st.selectbox(
    "사용할 AI 모델을 선택하세요",
    list(FREE_AI_MODELS.keys()),
    help="무료 모델 우선 추천!"
)

# 선택된 모델 안내
if selected_model == "OpenAI GPT-3.5":
    st.warning("💳 OpenAI는 API 키 + 요금 발생")
    openai_key = st.text_input("OpenAI API 키", type="password")
else:
    st.success("✅ 무료 AI 모델 선택됨!")
    openai_key = ""

# 키워드 입력
st.markdown("---")
st.subheader("📝 블로그 글 생성")

keyword = st.text_input("블로그 주제/키워드", placeholder="예: 혈압에 좋은 음식, 다이어트 비법")

# 훅킹 옵션
hook_style = st.selectbox(
    "글 스타일 선택 (체류시간 최적화)",
    ["충격적 사실로 시작", "질문으로 시작", "개인 경험담", "최신 연구 결과"]
)

# AI 글 생성 함수
def generate_with_free_ai(model_name, keyword, hook_style):
    """무료 AI 모델로 글 생성"""
    
    # 훅킹 프롬프트 설정
    hook_prompts = {
        "충격적 사실로 시작": f"충격! {keyword}에 대해 90%가 모르는 놀라운 사실부터 시작해서",
        "질문으로 시작": f"{keyword} 때문에 고민이세요? 이 글을 읽고 나면 해답을 찾을 수 있습니다.",
        "개인 경험담": f"제가 직접 {keyword}를 경험해보니 정말 놀라운 변화가 있었습니다.",
        "최신 연구 결과": f"2024년 최신 연구에서 밝혀진 {keyword}의 진실을 공개합니다."
    }
    
    # 체류시간 최적화 프롬프트
    prompt = f"""
    {hook_prompts[hook_style]}
    
    {keyword} 주제로 블로그 독자가 끝까지 읽을 수밖에 없는 매력적인 글을 써주세요.
    
    필수 포함 사항:
    - 눈에 띄는 제목 (클릭 유도)
    - 흥미진진한 도입부 (훅킹)
    - 3-4개 소제목으로 구성
    - 구체적인 팁과 실용 정보
    - 중간중간 궁금증 유발 문장
    - 마지막에 행동 유도(댓글, 공유 요청)
    
    1500자 이상, 한국어로 작성.
    """
    
    return prompt

# 무료 AI API 호출 함수
def call_huggingface_api(model_name, prompt):
    """Hugging Face 무료 API 호출"""
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    headers = {}  # 무료 사용
    payload = {
        "inputs": prompt[:500],  # 프롬프트 길이 제한
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '생성 실패')
            return str(result)
        else:
            return f"API 오류: {response.status_code} - 잠시 후 다시 시도해주세요"
    except Exception as e:
        return f"네트워크 오류: {str(e)}"
    
    # AI 블로그 글 생성 버튼
if st.button("🚀 AI 블로그 글 생성", type="primary"):
    if not keyword:
        st.warning("⚠️ 키워드를 입력해주세요!")
    else:
        with st.spinner("AI가 매력적인 블로그 글을 작성 중입니다... 📝"):
            
            if selected_model == "OpenAI GPT-3.5":
                if not openai_key:
                    st.error("OpenAI API 키를 입력해주세요!")
                else:
                    # OpenAI API 호출
                    prompt = generate_with_free_ai(selected_model, keyword, hook_style)
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
                        st.success("✅ AI 블로그 글 생성 완료!")
                        st.text_area("생성된 블로그 글", ai_content, height=400)
                        st.session_state['generated_content'] = ai_content
                    else:
                        st.error(f"OpenAI API 오류: {response.text}")
            
            else:
                # 무료 AI 모델 사용
                model_id = FREE_AI_MODELS[selected_model]
                prompt = generate_with_free_ai(selected_model, keyword, hook_style)
                
                result = call_huggingface_api(model_id, prompt)
                
                if "오류" in result:
                    st.error(f"❌ {result}")
                    st.info("💡 잠시 후 다시 시도하거나 다른 모델을 선택해보세요.")
                else:
                    st.success("✅ 무료 AI로 블로그 글 생성 완료!")
                    st.text_area("생성된 블로그 글", result, height=400)
                    st.session_state['generated_content'] = result

                    # 워드프레스 자동 업로드
st.markdown("---")
st.subheader("📤 워드프레스 자동 업로드")

wp_url = st.text_input("워드프레스 주소", placeholder="https://yoursite.com")
wp_id = st.text_input("워드프레스 아이디")
wp_pw = st.text_input("워드프레스 비밀번호", type="password")

# 생성된 글이 있을 때만 업로드 가능
if 'generated_content' in st.session_state:
    if st.button("📤 워드프레스에 업로드"):
        if wp_url and wp_id and wp_pw:
            api_url = f"{wp_url}/wp-json/wp/v2/posts"
            
            # 제목 추출 (첫 번째 줄)
            content = st.session_state['generated_content']
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip() if lines else keyword
            
            data = {
                "title": title,
                "content": content,
                "status": "publish"
            }
            
            try:
                response = requests.post(api_url, json=data, auth=(wp_id, wp_pw))
                if response.status_code == 201:
                    st.success("🎉 워드프레스 업로드 성공!")
                else:
                    st.error(f"업로드 실패: {response.status_code}")
            except Exception as e:
                st.error(f"오류 발생: {e}")
        else:
            st.warning("모든 정보를 입력해주세요!")

# 네이버 블로그 복사
st.markdown("---")
st.subheader("📋 네이버 블로그 복사")

if 'generated_content' in st.session_state:
    st.info("📝 아래 내용을 복사해서 네이버 블로그에 붙여넣으세요!")
    st.code(st.session_state['generated_content'])
    
    if st.button("📋 클립보드에 복사"):
        st.success("✅ 클립보드에 복사되었습니다! (수동으로 Ctrl+C 해주세요)")

st.markdown("---")
st.caption("💡 by 대표님의 AI 블로그 자동화 시스템")
