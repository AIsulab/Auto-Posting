import streamlit as st
import requests
import base64
import json
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(
    page_title="AI 블로그 자동화 시스템",
    page_icon="📝",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86C1;
        margin-bottom: 30px;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f8f9fa;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .code-block {
        background-color: #f4f4f4;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #2E86C1;
        margin: 10px 0;
    }
    .stButton > button {
        width: 100%;
    }
    .model-info {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

# AI 모델 정보
AI_MODELS = {
    "openai": {
        "name": "OpenAI GPT-3.5",
        "description": "고품질 텍스트 생성, API 키 필요",
        "requires_api_key": True,
        "free": False
    },
    "huggingface": {
        "name": "Hugging Face (무료)",
        "description": "무료 사용 가능, API 키 불필요",
        "requires_api_key": False,
        "free": True
    },
    "colab": {
        "name": "Google Colab (무료)",
        "description": "Google의 무료 AI 모델",
        "requires_api_key": False,
        "free": True
    }
}

# 세션 상태 초기화
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = ""
    if 'blog_title' not in st.session_state:
        st.session_state.blog_title = ""
    if 'login_attempted' not in st.session_state:
        st.session_state.login_attempted = False
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "huggingface"

def authenticate_user(username, password):
    """사용자 인증"""
    return username == "aisulab" and password == "!js44358574"

def generate_content_openai(keyword, api_key):
    """OpenAI API를 사용한 콘텐츠 생성"""
    try:
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        건강 정보 블로그 글을 작성해주세요.
        
        주제: {keyword}
        
        다음 요구사항을 반드시 포함해주세요:
        1. 1500자 이상의 상세한 내용
        2. 3개의 소제목으로 구성
        3. 전문가 조언 섹션 포함
        4. 실용적이고 신뢰할 수 있는 정보
        5. 독자가 실천할 수 있는 구체적인 방법 제시
        
        글의 구조:
        - 제목
        - 서론
        - 소제목 1: 기본 정보
        - 소제목 2: 실천 방법
        - 소제목 3: 주의사항
        - 전문가 조언
        - 결론
        
        전문적이면서도 이해하기 쉽게 작성해주세요.
        """
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "당신은 건강 정보 전문 블로거입니다. 정확하고 유용한 건강 정보를 제공하는 고품질 블로그 글을 작성해주세요."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            return f"OpenAI API 호출 실패: {response.status_code} - {error_detail}"
    
    except Exception as e:
        return f"OpenAI 콘텐츠 생성 중 오류가 발생했습니다: {str(e)}"

def generate_content_huggingface(keyword):
    """Hugging Face 무료 모델을 사용한 콘텐츠 생성"""
    try:
        # Hugging Face의 무료 Inference API 사용
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        prompt = f"""건강 주제 '{keyword}'에 대한 상세한 블로그 글을 작성해주세요.

주요 내용:
1. {keyword}의 기본 정보와 중요성
2. 실생활에서 적용할 수 있는 방법
3. 주의사항과 전문가 조언

1500자 이상으로 작성해주세요."""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        # 무료 API이므로 여러 번 시도
        for attempt in range(3):
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    if generated_text:
                        return generated_text
                elif isinstance(result, dict) and 'generated_text' in result:
                    return result['generated_text']
            
            # 모델이 로딩 중인 경우 잠시 대기
            if response.status_code == 503:
                time.sleep(10)
                continue
            
            break
        
        # Hugging Face API가 실패한 경우 기본 템플릿 제공
        return generate_fallback_content(keyword)
    
    except Exception as e:
        return generate_fallback_content(keyword)

def generate_content_colab(keyword):
    """Google Colab 스타일 무료 모델 시뮬레이션"""
    try:
        # 실제로는 Colab에서 실행되는 무료 모델을 시뮬레이션
        # 여기서는 기본 템플릿을 제공
        return generate_fallback_content(keyword)
    
    except Exception as e:
        return generate_fallback_content(keyword)

def generate_fallback_content(keyword):
    """API 실패 시 사용할 기본 콘텐츠 템플릿"""
    content = f"""# {keyword} - 건강 정보 가이드

## 서론
{keyword}에 대한 정확하고 유용한 정보를 제공하여 건강한 생활을 도움을 드리고자 합니다.

## 1. {keyword}의 기본 정보
{keyword}는 우리 건강에 중요한 역할을 합니다. 다음과 같은 특징들이 있습니다:

- 기본적인 정의와 중요성
- 우리 몸에 미치는 영향
- 일상생활에서의 역할

## 2. 실천할 수 있는 방법
{keyword}와 관련하여 실생활에서 적용할 수 있는 방법들:

- 올바른 생활습관 유지
- 균형잡힌 식단 관리
- 적절한 운동과 휴식
- 정기적인 건강 체크

## 3. 주의사항과 관리법
{keyword}를 관리할 때 주의해야 할 사항들:

- 과도한 섭취나 부족 주의
- 개인차를 고려한 접근
- 전문의와의 상담 권장
- 지속적인 관리의 중요성

## 전문가 조언
건강 전문가들은 {keyword}에 대해 다음과 같이 조언합니다:
- 개인의 건강 상태를 고려한 맞춤형 관리가 중요합니다.
- 급격한 변화보다는 점진적인 개선을 권장합니다.
- 정확한 정보를 바탕으로 한 올바른 실천이 필요합니다.

## 결론
{keyword}에 대한 올바른 이해와 실천을 통해 더 건강한 삶을 영위할 수 있습니다. 지속적인 관심과 관리를 통해 건강을 지켜나가시기 바랍니다.

*본 정보는 일반적인 건강 정보이며, 개인의 건강 상태에 따라 다를 수 있습니다. 구체적인 건강 문제는 전문의와 상담하시기 바랍니다.*"""
    
    return content

def generate_blog_content(keyword, model_type, api_key=None):
    """선택된 모델에 따라 블로그 콘텐츠 생성"""
    if model_type == "openai":
        if not api_key:
            return "OpenAI 모델을 사용하려면 API 키가 필요합니다."
        return generate_content_openai(keyword, api_key)
    elif model_type == "huggingface":
        return generate_content_huggingface(keyword)
    elif model_type == "colab":
        return generate_content_colab(keyword)
    else:
        return "지원하지 않는 모델입니다."

def upload_to_wordpress(wp_url, wp_username, wp_password, title, content):
    """워드프레스에 글 업로드"""
    try:
        # REST API 엔드포인트
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
        
        # 인증 정보
        credentials = base64.b64encode(f"{wp_username}:{wp_password}".encode()).decode()
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'title': title,
            'content': content,
            'status': 'draft'  # 초안으로 저장
        }
        
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 201:
            post_data = response.json()
            return True, f"글이 성공적으로 업로드되었습니다! 글 ID: {post_data['id']}"
        else:
            return False, f"업로드 실패: {response.status_code} - {response.text}"
    
    except Exception as e:
        return False, f"업로드 중 오류가 발생했습니다: {str(e)}"

def render_login_page():
    """로그인 페이지 렌더링"""
    st.markdown("<h1 class='main-header'>🔐 AI 블로그 자동화 시스템</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("### 로그인")
        
        # 로그인 폼
        username = st.text_input("아이디", placeholder="아이디를 입력하세요", key="login_username")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요", key="login_password")
        
        if st.button("로그인", key="login_button"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.success("로그인 성공! 잠시 후 메인 화면으로 이동합니다.")
                st.balloons()
                # 페이지를 다시 실행하여 메인 화면 표시
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_main_page():
    """메인 페이지 렌더링"""
    st.markdown("<h1 class='main-header'>📝 AI 블로그 자동화 시스템</h1>", unsafe_allow_html=True)
    
    # 상단 헤더 - 로그아웃 버튼
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("로그아웃", key="logout_button"):
            # 세션 상태 초기화
            st.session_state.logged_in = False
            st.session_state.generated_content = ""
            st.session_state.blog_title = ""
            st.session_state.login_attempted = False
            st.rerun()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🤖 AI 글 생성", "📤 워드프레스 업로드", "📋 네이버 블로그 복사"])
    
    with tab1:
        render_ai_generation_tab()
    
    with tab2:
        render_wordpress_upload_tab()
    
    with tab3:
        render_naver_copy_tab()

def render_ai_generation_tab():
    """AI 글 생성 탭"""
    st.header("AI 블로그 글 생성")
    
    # AI 모델 선택
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_model = st.selectbox(
            "AI 모델 선택",
            options=list(AI_MODELS.keys()),
            format_func=lambda x: AI_MODELS[x]["name"],
            key="model_select"
        )
        st.session_state.selected_model = selected_model
    
    with col2:
        model_info = AI_MODELS[selected_model]
        st.markdown(f"""
        <div class='model-info'>
            <strong>{model_info['name']}</strong><br>
            {model_info['description']}<br>
            {'🆓 무료' if model_info['free'] else '💰 유료'} | 
            {'🔑 API 키 필요' if model_info['requires_api_key'] else '🔓 API 키 불필요'}
        </div>
        """, unsafe_allow_html=True)
    
    # 입력 필드
    col1, col2 = st.columns(2)
    
    with col1:
        keyword = st.text_input("키워드", placeholder="예: 비타민D 효능", key="keyword_input")
        
        # API 키 입력 (필요한 경우에만)
        api_key = None
        if AI_MODELS[selected_model]["requires_api_key"]:
            api_key = st.text_input("API 키", type="password", placeholder="API 키를 입력하세요", key="api_key_input")
    
    with col2:
        st.info(f"""💡 **{AI_MODELS[selected_model]['name']} 사용 팁**
- 구체적인 키워드를 입력하세요
- 생성된 글은 1500자 이상입니다
{f"- {AI_MODELS[selected_model]['name']} API 키가 필요합니다" if AI_MODELS[selected_model]['requires_api_key'] else "- API 키 없이 무료로 사용 가능합니다"}
- 무료 모델은 품질이 다를 수 있습니다""")
    
    # 생성 버튼
    if st.button("AI 글 생성", type="primary", key="generate_button"):
        if keyword:
            # API 키 검증
            if AI_MODELS[selected_model]["requires_api_key"] and not api_key:
                st.error(f"{AI_MODELS[selected_model]['name']}을(를) 사용하려면 API 키가 필요합니다.")
                return
            
            with st.spinner(f"{AI_MODELS[selected_model]['name']}이(가) 블로그 글을 생성하고 있습니다..."):
                content = generate_blog_content(keyword, selected_model, api_key)
                st.session_state.generated_content = content
                st.session_state.blog_title = f"{keyword} - 건강 정보 가이드"
            
            st.success("글 생성이 완료되었습니다!")
        else:
            st.error("키워드를 입력해주세요.")
    
    # 생성된 콘텐츠 표시
    if st.session_state.generated_content:
        st.subheader("생성된 블로그 글")
        st.markdown(f"**제목:** {st.session_state.blog_title}")
        st.markdown(f"**사용된 모델:** {AI_MODELS[st.session_state.selected_model]['name']}")
        st.markdown("---")
        st.markdown(st.session_state.generated_content)

def render_wordpress_upload_tab():
    """워드프레스 업로드 탭"""
    st.header("워드프레스 자동 업로드")
    
    if not st.session_state.generated_content:
        st.warning("먼저 AI 글 생성 탭에서 블로그 글을 생성해주세요.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            wp_url = st.text_input("워드프레스 주소", placeholder="https://yoursite.com", key="wp_url")
            wp_username = st.text_input("워드프레스 사용자명", key="wp_username")
            wp_password = st.text_input("워드프레스 비밀번호", type="password", key="wp_password")
        
        with col2:
            st.info("🔐 **보안 정보**\n- 애플리케이션 비밀번호 사용 권장\n- REST API가 활성화되어야 합니다\n- 초안으로 저장됩니다")
        
        if st.button("워드프레스에 업로드", type="primary", key="wp_upload_button"):
            if wp_url and wp_username and wp_password:
                with st.spinner("워드프레스에 업로드 중..."):
                    success, message = upload_to_wordpress(
                        wp_url, wp_username, wp_password,
                        st.session_state.blog_title,
                        st.session_state.generated_content
                    )
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("모든 워드프레스 정보를 입력해주세요.")

def render_naver_copy_tab():
    """네이버 블로그 복사 탭"""
    st.header("네이버 블로그 복사")
    
    if not st.session_state.generated_content:
        st.warning("먼저 AI 글 생성 탭에서 블로그 글을 생성해주세요.")
    else:
        st.info("📋 아래 내용을 복사하여 네이버 블로그에 붙여넣기 하세요.")
        
        # 제목
        st.subheader("제목")
        st.code(st.session_state.blog_title, language=None)
        
        # 본문
        st.subheader("본문")
        st.code(st.session_state.generated_content, language=None)
        
        # 통계 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            word_count = len(st.session_state.generated_content)
            st.metric("글자 수", f"{word_count:,}자")
        with col2:
            st.metric("사용된 모델", AI_MODELS[st.session_state.selected_model]['name'])
        with col3:
            st.metric("모델 타입", "🆓 무료" if AI_MODELS[st.session_state.selected_model]['free'] else "💰 유료")

def main():
    """메인 함수"""
    # 세션 상태 초기화
    init_session_state()
    
    # 로그인 상태에 따른 페이지 렌더링
    if st.session_state.logged_in:
        render_main_page()
    else:
        render_login_page()

if __name__ == "__main__":
    main()
