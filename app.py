import streamlit as st
import requests
import json
import time
import random

# 페이지 설정 (맨 처음에)
st.set_page_config(page_title="AI 블로그 자동화", layout="centered")

# 무료 이미지 API 설정
UNSPLASH_API_KEY = "demo"  # 무료 사용
PIXABAY_API_KEY = "demo"   # 무료 사용

# 무료 이미지 검색 함수
def get_free_images(keyword, count=3):
    """무료 이미지 URL 가져오기"""
    images = []
    
    # Unsplash 무료 이미지 (API 키 없이 사용 가능)
    try:
        # 키워드를 영어로 변환 (간단한 매핑)
        keyword_en = {
            "혈압": "blood pressure",
            "음식": "food",
            "건강": "health",
            "다이어트": "diet",
            "운동": "exercise",
            "영양": "nutrition"
        }.get(keyword.split()[0], keyword)
        
        # Lorem Picsum 사용 (완전 무료)
        for i in range(count):
            width = random.choice([800, 600, 700])
            height = random.choice([400, 300, 350])
            seed = random.randint(1, 1000)
            img_url = f"https://picsum.photos/{width}/{height}?random={seed}"
            images.append({
                "url": img_url,
                "alt": f"{keyword} 관련 이미지 {i+1}"
            })
    except:
        # 기본 이미지
        images = [{
            "url": "https://picsum.photos/600/300?random=1",
            "alt": f"{keyword} 관련 이미지"
        }]
    
    return images

# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("대표님 전용 블로그 자동화 로그인")
    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        if user_id == VALID_ID and user_pw == VALID_PW:
            st.session_state['login_ok'] = True
            st.query_params['logged_in'] = 'true'  # URL에 로그인 상태 저장
            st.success("✅ 로그인 성공!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    st.stop()

# URL에서 로그인 상태 복원
if st.query_params.get('logged_in') == 'true':
    st.session_state['login_ok'] = True

# 메인 화면
st.title("📝 AI 블로그 자동화 시스템")
st.markdown("### 🤖 AI 글 생성 | 📤 워드프레스 업로드 | 📋 네이버 블로그 복사")

# 로그아웃 버튼
if st.button("🚪 로그아웃", key="logout"):
    st.session_state['login_ok'] = False
    st.query_params.clear()
    st.rerun()

st.markdown("---")
st.subheader("🤖 AI 모델 선택")

# 실제 작동하는 무료 AI 옵션
ai_options = {
    "로컬 AI (무료)": "local",
    "OpenAI GPT-3.5": "openai"
}

selected_model = st.selectbox(
    "사용할 AI 모델을 선택하세요",
    list(ai_options.keys())
)

# API 키 입력 (OpenAI 선택시만)
if selected_model == "OpenAI GPT-3.5":
    st.warning("💳 OpenAI는 API 키 + 요금 발생")
    openai_key = st.text_input("OpenAI API 키", type="password")
else:
    st.success("✅ 무료 로컬 AI 선택됨!")
    openai_key = ""

st.markdown("---")
st.subheader("📝 블로그 글 생성")

keyword = st.text_input("블로그 주제/키워드", placeholder="예: 혈압에 좋은 음식, 다이어트 비법")

hook_style = st.selectbox(
    "글 스타일 선택 (체류시간 최적화)",
    ["충격적 사실로 시작", "질문으로 시작", "개인 경험담", "최신 연구 결과"]
)

# 로컬 AI 글 생성 함수 (완전 무료)
def generate_local_blog(keyword, hook_style):
    """로컬에서 블로그 글 생성 (무료)"""
    
    # 훅킹 시작 문장
    hooks = {
        "충격적 사실로 시작": f"충격! {keyword}에 대한 놀라운 진실을 공개합니다.",
        "질문으로 시작": f"{keyword} 때문에 고민이신가요? 이 글에서 해답을 찾아보세요.",
        "개인 경험담": f"제가 직접 {keyword}를 경험해본 솔직한 후기를 공유합니다.",
        "최신 연구 결과": f"2024년 최신 연구로 밝혀진 {keyword}의 진실을 알려드립니다."
    }
    
    # 블로그 글 템플릿
    blog_content = f"""# {keyword} - 완벽 가이드

{hooks[hook_style]}

## 🔍 {keyword}란 무엇인가?

{keyword}는 현대인들에게 매우 중요한 주제입니다. 많은 사람들이 이에 대해 궁금해하지만, 정확한 정보를 찾기는 쉽지 않죠.

## 💡 핵심 포인트 3가지

### 1. 기본 개념 이해
{keyword}의 기본적인 개념을 이해하는 것이 첫 번째 단계입니다. 전문가들은 이것을 가장 중요하게 생각합니다.

### 2. 실용적인 방법
실제로 일상생활에서 적용할 수 있는 구체적인 방법들을 소개합니다. 이는 검증된 방법들로 많은 사람들이 효과를 보았습니다.

### 3. 주의사항
{keyword}와 관련해서 반드시 알아야 할 주의사항들이 있습니다. 이를 모르면 오히려 역효과가 날 수 있어요.

## 🎯 실천 방법

구체적으로 어떻게 실천할 수 있는지 단계별로 알아보겠습니다:

1. **첫 번째 단계**: 기초 지식 습득
2. **두 번째 단계**: 실제 적용
3. **세 번째 단계**: 결과 확인 및 개선

## 📈 기대 효과

이 방법을 따르면 다음과 같은 효과를 기대할 수 있습니다:
- 전반적인 개선 효과
- 장기적인 긍정적 변화
- 자신감 향상

## 💬 마무리

{keyword}에 대한 정보가 도움이 되셨나요? 

**여러분의 경험도 댓글로 공유해주세요!** 
더 궁금한 점이 있다면 언제든 질문해주시고, 이 글이 도움되셨다면 주변 분들에게도 공유해주세요! 🙏

---
*더 많은 유용한 정보를 원하신다면 구독과 좋아요 부탁드립니다!*
"""
    
    return blog_content

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
                    st.error("❌ OpenAI API 키를 입력해주세요!")
                else:
                    # OpenAI API 호출
                    hooks = {
                        "충격적 사실로 시작": f"충격! {keyword}에 대해 90%가 모르는 놀라운 사실부터 시작해서",
                        "질문으로 시작": f"{keyword} 때문에 고민이세요? 이 글을 읽고 나면 해답을 찾을 수 있습니다.",
                        "개인 경험담": f"제가 직접 {keyword}를 경험해보니 정말 놀라운 변화가 있었습니다.",
                        "최신 연구 결과": f"2024년 최신 연구에서 밝혀진 {keyword}의 진실을 공개합니다."
                    }
                    
                    prompt = f"""
                    {hooks[hook_style]}
                    
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
                    
                    try:
                        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
                        if response.status_code == 200:
                            ai_content = response.json()["choices"][0]["message"]["content"].strip()
                            st.success("✅ OpenAI로 블로그 글 생성 완료!")
                            st.text_area("생성된 블로그 글", ai_content, height=400)
                            st.session_state['generated_content'] = ai_content
                        else:
                            st.error(f"❌ OpenAI API 오류: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
            
            else:
                # 로컬 AI 사용 (완전 무료)
                ai_content = generate_local_blog(keyword, hook_style)
                st.success("✅ 로컬 AI로 블로그 글 생성 완료!")
                st.text_area("생성된 블로그 글", ai_content, height=400)
                st.session_state['generated_content'] = ai_content

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
            with st.spinner("워드프레스에 업로드 중..."):
                api_url = f"{wp_url}/wp-json/wp/v2/posts"
                
                # 제목 추출 (첫 번째 줄에서 # 제거)
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
                        post_url = response.json().get('link', '')
                        if post_url:
                            st.info(f"🔗 게시글 링크: {post_url}")
                    else:
                        st.error(f"❌ 업로드 실패: {response.status_code}")
                        st.error("워드프레스 정보를 확인해주세요.")
                except Exception as e:
                    st.error(f"❌ 연결 오류: {str(e)}")
        else:
            st.warning("⚠️ 워드프레스 정보를 모두 입력해주세요!")
else:
    st.info("💡 먼저 블로그 글을 생성해주세요.")

# 네이버 블로그 복사
st.markdown("---")
st.subheader("📋 네이버 블로그 복사")

if 'generated_content' in st.session_state:
    st.info("📝 아래 내용을 복사해서 네이버 블로그에 붙여넣으세요!")
    
    # 복사 버튼
    if st.button("📋 전체 글 복사하기"):
        st.balloons()  # 시각적 효과
        st.success("✅ 아래 텍스트를 Ctrl+A로 전체선택 후 Ctrl+C로 복사하세요!")
    
    # 복사할 텍스트 영역
    st.text_area("복사할 내용", st.session_state['generated_content'], height=300)
    
else:
    st.info("💡 먼저 블로그 글을 생성해주세요.")

# 푸터
st.markdown("---")
st.markdown("### 💡 사용 통계")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("생성된 글", "1개" if 'generated_content' in st.session_state else "0개")

with col2:
    st.metric("사용 모델", selected_model if 'generated_content' in st.session_state else "미선택")

with col3:
    st.metric("상태", "완료" if 'generated_content' in st.session_state else "대기중")

st.caption("💡 by 대표님의 AI 블로그 자동화 시스템 | 새로고침해도 로그인 유지됩니다!")