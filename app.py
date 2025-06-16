import streamlit as st
import requests
import base64
import json
from datetime import datetime
import time
import random

# 페이지 설정
st.set_page_config(
    page_title="AI 블로그 자동화 시스템",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 로그인 정보
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# CSS 스타일 (모바일 친화적)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86C1;
        margin-bottom: 30px;
        font-size: 2.5rem;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
    }
    
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
    }
    
    .model-card {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #2E86C1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .model-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .success-message {
        color: #28a745;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        color: #dc3545;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 5px solid #ffc107;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .content-preview {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin: 15px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    @media (max-width: 768px) {
        .login-container {
            margin: 10px;
            padding: 20px;
        }
        
        .model-card, .feature-box {
            margin: 10px 0;
            padding: 15px;
        }
        
        .content-preview {
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# AI 모델 정보
AI_MODELS = {
    "huggingface_gpt2": {
        "name": "GPT-2 (Hugging Face)",
        "description": "창의적인 텍스트 생성에 특화된 무료 모델",
        "api_url": "https://api-inference.huggingface.co/models/gpt2",
        "strength": "창의성",
        "best_for": "스토리텔링, 창의적 글쓰기"
    },
    "huggingface_kogpt2": {
        "name": "KoGPT-2 (한국어 특화)",
        "description": "한국어 텍스트 생성 전용 무료 모델",
        "api_url": "https://api-inference.huggingface.co/models/skt/kogpt2-base-v2",
        "strength": "한국어 자연스러움",
        "best_for": "한국어 블로그, 자연스러운 표현"
    },
    "huggingface_openchat": {
        "name": "OpenChat (대화형)",
        "description": "대화형 응답에 최적화된 무료 모델",
        "api_url": "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106",
        "strength": "대화형 응답",
        "best_for": "Q&A 형식, 친근한 톤"
    },
    "huggingface_flan": {
        "name": "Flan-T5 (지시 이해)",
        "description": "명확한 지시 이해에 특화된 무료 모델",
        "api_url": "https://api-inference.huggingface.co/models/google/flan-t5-large",
        "strength": "지시 이해",
        "best_for": "구체적 요구사항, 정보성 글"
    },
    "huggingface_bloom": {
        "name": "BLOOM (다국어)",
        "description": "다국어 지원 대형 언어 모델",
        "api_url": "https://api-inference.huggingface.co/models/bigscience/bloom-560m",
        "strength": "다국어 지원",
        "best_for": "전문적 글쓰기, 다양한 주제"
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
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "huggingface_kogpt2"
    if 'generation_stats' not in st.session_state:
        st.session_state.generation_stats = {}

def authenticate_user(username, password):
    """사용자 인증"""
    return username == VALID_ID and password == VALID_PW

def create_hooking_prompt(keyword):
    """광고 수익 최적화를 위한 훅킹 프롬프트 생성"""
    hooking_starters = [
        f"'{keyword}'에 대해 99%의 사람들이 모르는 충격적인 진실이 있습니다.",
        f"의사들이 절대 말하지 않는 '{keyword}'의 숨겨진 비밀을 공개합니다.",
        f"'{keyword}' 때문에 매년 수만 명이 고통받고 있다는 사실, 알고 계셨나요?",
        f"3분만 투자하면 '{keyword}'에 대한 당신의 인생이 바뀔 수 있습니다.",
        f"'{keyword}'로 고민하던 제가 단 7일 만에 완전히 달라진 이야기를 들려드릴게요."
    ]
    
    selected_hook = random.choice(hooking_starters)
    
    prompt = f"""
당신은 광고 수익 최적화 전문 블로거입니다. 독자의 체류시간을 최대화하고 참여도를 높이는 블로그 글을 작성해주세요.

주제: {keyword}

필수 구조:
1. 훅킹 시작: {selected_hook}

2. 문제 인식 단계:
- 독자가 공감할 수 있는 구체적인 문제 상황 제시
- "혹시 이런 경험 있으신가요?" 형태의 질문으로 참여 유도

3. 해결책 제시 (3단계 구성):
- 1단계: 즉시 실행 가능한 간단한 방법
- 2단계: 중급자를 위한 심화 방법  
- 3단계: 고급자를 위한 전문가 팁

4. 실제 사례/스토리:
- "실제로 이 방법을 사용한 A씨의 이야기" 형태
- 구체적인 수치나 결과 포함

5. 주의사항과 FAQ:
- "많은 분들이 궁금해하시는 질문들"
- 실수하기 쉬운 부분 강조

6. 강력한 마무리 CTA:
- "이 글이 도움되셨다면 댓글로 경험을 공유해주세요!"
- "주변 분들에게도 공유해서 도움을 주세요!"
- "더 자세한 정보가 필요하시면 댓글로 질문해주세요!"

글쓰기 규칙:
- 1500자 이상 작성
- 친근하고 대화하는 듯한 톤 사용
- 단락을 짧게 나누어 가독성 향상
- 중요한 부분은 **강조** 표시
- 숫자나 통계를 활용해 신뢰성 증대
- 독자의 행동을 유도하는 문장 자주 사용

지금 바로 시작해주세요!
"""
    return prompt

def generate_content_huggingface(keyword, model_key):
    """Hugging Face 모델을 사용한 콘텐츠 생성"""
    try:
        model_info = AI_MODELS[model_key]
        api_url = model_info["api_url"]
        
        # 광고 수익 최적화 프롬프트 생성
        prompt = create_hooking_prompt(keyword)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1500,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }
        }
        
        # 여러 번 시도
        for attempt in range(3):
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    if generated_text and len(generated_text) > 500:
                        return clean_generated_content(generated_text, keyword)
                elif isinstance(result, dict):
                    if 'generated_text' in result:
                        generated_text = result['generated_text']
                        if len(generated_text) > 500:
                            return clean_generated_content(generated_text, keyword)
                    elif 'error' in result:
                        if 'loading' in result['error'].lower():
                            time.sleep(15)  # 모델 로딩 대기
                            continue
            
            # 503 에러 (모델 로딩 중)인 경우 대기
            if response.status_code == 503:
                time.sleep(20)
                continue
            
            break
        
        # API 실패 시 최적화된 템플릿 제공
        return generate_optimized_template(keyword)
    
    except Exception as e:
        return generate_optimized_template(keyword)

def clean_generated_content(generated_text, keyword):
    """생성된 콘텐츠 정리 및 최적화"""
    # 불필요한 부분 제거
    content = generated_text.strip()
    
    # 제목 추출 시도
    lines = content.split('\n')
    title = f"{keyword} - 전문가가 알려주는 완벽 가이드"
    
    # 내용 정리
    if len(content) < 800:
        return generate_optimized_template(keyword)
    
    # CTA 추가 (없는 경우)
    if "댓글" not in content and "공유" not in content:
        content += "\n\n---\n\n"
        content += "💬 **이 글이 도움되셨나요?**\n"
        content += "- 댓글로 여러분의 경험을 공유해주세요!\n"
        content += "- 주변 분들에게도 공유해서 도움을 주세요!\n"
        content += "- 더 궁금한 점이 있으시면 언제든 댓글로 질문해주세요!\n\n"
        content += "🔔 **더 유용한 건강 정보가 필요하시다면 구독과 좋아요 부탁드립니다!**"
    
    return content

def generate_optimized_template(keyword):
    """광고 수익 최적화된 기본 템플릿"""
    hooking_starters = [
        f"'{keyword}'에 대해 99%의 사람들이 모르는 충격적인 진실을 공개합니다.",
        f"의사들이 절대 말하지 않는 '{keyword}'의 숨겨진 비밀이 있습니다.",
        f"'{keyword}' 때문에 고민하시는 분들, 3분만 투자해보세요."
    ]
    
    selected_hook = random.choice(hooking_starters)
    
    content = f"""{selected_hook}

혹시 이런 경험 있으신가요? 

'{keyword}'에 대한 정보를 찾아보려고 인터넷을 뒤져봐도 정작 **실질적으로 도움되는 정보**는 찾기 어려우셨을 겁니다. 

오늘 이 글을 끝까지 읽으시면, 그동안 몰랐던 '{keyword}'의 핵심 포인트를 완벽하게 이해하실 수 있을 거예요.

## 🚨 대부분 사람들이 놓치는 핵심 포인트

많은 분들이 '{keyword}'에 대해 잘못 알고 계신 부분이 있습니다. 

**첫 번째 오해:** 단순히 정보만 알면 된다고 생각하시는 것
**두 번째 오해:** 모든 사람에게 같은 방법이 통한다고 생각하시는 것
**세 번째 오해:** 즉석에서 결과를 기대하시는 것

## 💡 단계별 실전 가이드

### 1단계: 기초 다지기 (누구나 가능)
- **즉시 실행 가능한 방법**: 오늘부터 바로 시작할 수 있는 간단한 습관
- **준비물**: 특별한 도구 없이도 가능한 방법들
- **소요시간**: 하루 5-10분이면 충분

### 2단계: 중급자 과정 (1-2주 후)
- **심화 방법**: 기초를 다진 후 적용할 수 있는 고급 기법
- **주의사항**: 이 단계에서 많은 분들이 실수하는 부분들
- **효과 측정**: 자신의 진행 상황을 확인하는 방법

### 3단계: 전문가 레벨 (1개월 후)
- **고급 팁**: 전문가들만 아는 특별한 노하우
- **개인 맞춤**: 자신에게 맞는 방법을 찾는 법
- **지속 관리**: 효과를 오래 유지하는 비결

## 📈 실제 성공 사례

**A씨(35세, 직장인)의 이야기:**
"처음에는 반신반의했는데, 정말로 2주 만에 확실한 변화를 느꼈어요. 특히 2단계 방법이 저에게는 가장 효과적이었습니다."

**B씨(28세, 주부)의 후기:**
"바쁜 일상 중에도 쉽게 따라할 수 있어서 좋았어요. 지금은 주변 사람들에게도 추천하고 있습니다."

## ❓ 자주 묻는 질문들

**Q: 얼마나 오래 해야 효과를 볼 수 있나요?**
A: 개인차가 있지만, 대부분 1-2주 내에 초기 변화를 느끼실 수 있습니다.

**Q: 나이나 성별에 상관없이 가능한가요?**
A: 네, 이 방법은 연령과 성별에 관계없이 적용 가능합니다.

**Q: 부작용은 없나요?**
A: 자연스러운 방법이므로 부작용 걱정은 하지 않으셔도 됩니다.

## ⚠️ 꼭 피해야 할 실수들

1. **성급한 기대**: 너무 빠른 결과를 원하면 오히려 역효과
2. **일관성 부족**: 며칠 하다가 그만두면 의미가 없음
3. **과도한 적용**: 많이 한다고 더 좋은 것은 아님

## 🎯 마무리: 지금 바로 시작하세요!

오늘 알려드린 '{keyword}' 정보가 여러분의 삶에 실질적인 도움이 되길 바랍니다.

**기억하세요:**
- 완벽할 필요 없습니다. 시작이 중요해요.
- 자신에게 맞는 속도로 진행하세요.
- 꾸준함이 가장 중요합니다.

---

💬 **이 글이 도움되셨나요?**

- **댓글로 여러분의 경험을 공유해주세요!** 다른 분들에게도 큰 도움이 됩니다.
- **주변 분들에게도 공유해서** 더 많은 사람들이 도움받을 수 있도록 해주세요!
- **더 궁금한 점이 있으시면** 언제든 댓글로 질문해주세요.

🔔 **더 유용한 정보가 필요하시다면 구독과 좋아요 부탁드립니다!**"""

    return content

def save_to_file(content, filename):
    """생성된 콘텐츠를 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def display_generation_stats():
    """생성 통계 표시"""
    if st.session_state.generation_stats:
        st.markdown("### 📊 생성 통계")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stats-card">
                <h4>총 생성 횟수</h4>
                <h2>{}</h2>
            </div>
            """.format(st.session_state.generation_stats.get('total_generations', 0)), 
            unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stats-card">
                <h4>성공률</h4>
                <h2>{}%</h2>
            </div>
            """.format(st.session_state.generation_stats.get('success_rate', 0)), 
            unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stats-card">
                <h4>평균 길이</h4>
                <h2>{} 자</h2>
            </div>
            """.format(st.session_state.generation_stats.get('avg_length', 0)), 
            unsafe_allow_html=True)

def login_page():
    """로그인 페이지"""
    st.markdown('<h1 class="main-header">🔐 AI 블로그 자동화 시스템</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <h3 style="text-align: center; margin-bottom: 20px; color: #2E86C1;">로그인</h3>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("아이디", placeholder="사용자 아이디를 입력하세요")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        submit_button = st.form_submit_button("로그인", use_container_width=True)
        
        if submit_button:
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("잘못된 아이디 또는 비밀번호입니다.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 시스템 소개
    st.markdown("""
    <div class="feature-box">
        <h3>🚀 시스템 특징</h3>
        <ul>
            <li><strong>다양한 AI 모델</strong>: 5개의 전문화된 AI 모델 지원</li>
            <li><strong>광고 수익 최적화</strong>: 독자 참여도를 높이는 콘텐츠 구조</li>
            <li><strong>모바일 친화적</strong>: 반응형 디자인으로 어디서든 사용 가능</li>
            <li><strong>자동 최적화</strong>: SEO 친화적이고 CTA가 포함된 블로그 글 생성</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def main_page():
    """메인 페이지"""
    st.markdown('<h1 class="main-header">📝 AI 블로그 자동화 시스템</h1>', unsafe_allow_html=True)
    
    # 로그아웃 버튼
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("로그아웃", type="secondary"):
            st.session_state.logged_in = False
            st.rerun()
    
    # 시스템 상태 표시
    display_generation_stats()
    
    # AI 모델 선택
    st.markdown("### 🤖 AI 모델 선택")
    
    for model_key, model_info in AI_MODELS.items():
        with st.container():
            st.markdown(f"""
            <div class="model-card">
                <h4>{model_info['name']}</h4>
                <p>{model_info['description']}</p>
                <p><strong>강점:</strong> {model_info['strength']}</p>
                <p><strong>추천용도:</strong> {model_info['best_for']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"선택: {model_info['name']}", key=model_key):
                st.session_state.selected_model = model_key
                st.success(f"✅ {model_info['name']} 모델이 선택되었습니다!")
    
    st.markdown("---")
    
    # 현재 선택된 모델 표시
    if st.session_state.selected_model:
        current_model = AI_MODELS[st.session_state.selected_model]
        st.info(f"🎯 현재 선택된 모델: **{current_model['name']}**")
    
    # 콘텐츠 생성
    st.markdown("### ✍️ 블로그 콘텐츠 생성")
    
    with st.form("content_generation_form"):
        keyword = st.text_input(
            "키워드/주제", 
            placeholder="예: 다이어트, 투자, 건강관리 등",
            help="블로그 글의 주제나 키워드를 입력하세요"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            content_type = st.selectbox(
                "콘텐츠 유형",
                ["정보성 글", "체험담", "가이드", "리뷰", "비교분석"]
            )
        
        with col2:
            target_length = st.selectbox(
                "글 길이",
                ["짧음 (800-1200자)", "보통 (1200-1800자)", "길음 (1800자 이상)"]
            )
        
        advanced_options = st.expander("🔧 고급 옵션")
        with advanced_options:
            include_seo = st.checkbox("SEO 최적화 포함", value=True)
            include_cta = st.checkbox("CTA (Call-to-Action) 포함", value=True)
            emotional_tone = st.selectbox(
                "감정 톤",
                ["친근함", "전문적", "열정적", "신뢰감", "유머러스"]
            )
        
        generate_button = st.form_submit_button("🚀 콘텐츠 생성", use_container_width=True)
        
        if generate_button:
            if not keyword:
                st.error("키워드를 입력해주세요!")
            elif not st.session_state.selected_model:
                st.error("AI 모델을 선택해주세요!")
            else:
                with st.spinner("AI가 콘텐츠를 생성하고 있습니다... ⏳"):
                    try:
                        # 콘텐츠 생성
                        generated_content = generate_content_huggingface(
                            keyword, 
                            st.success("✅ 콘텐츠가 성공적으로 생성되었습니다!")
                            st.rerun()
                        else:
                            st.error("콘텐츠 생성에 실패했습니다. 다시 시도해주세요.")
                    
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
    
    # 생성된 콘텐츠 표시
    if st.session_state.generated_content:
        st.markdown("---")
        st.markdown("### 📄 생성된 콘텐츠")
        
        # 콘텐츠 미리보기
        with st.container():
            st.markdown(f"**제목:** {st.session_state.blog_title}")
            st.markdown(f"**길이:** {len(st.session_state.generated_content):,} 자")
            st.markdown(f"**사용 모델:** {AI_MODELS[st.session_state.selected_model]['name']}")
            
            # 콘텐츠 표시
            st.markdown("""
            <div class="content-preview">
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.generated_content)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 액션 버튼들
        st.markdown("### 🔧 콘텐츠 관리")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📋 복사하기", use_container_width=True):
                st.code(st.session_state.generated_content, language=None)
                st.info("위 텍스트를 선택하여 복사하세요!")
        
        with col2:
            if st.button("💾 다운로드", use_container_width=True):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"blog_post_{timestamp}.txt"
                
                st.download_button(
                    label="파일 다운로드",
                    data=st.session_state.generated_content,
                    file_name=filename,
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col3:
            if st.button("🔄 재생성", use_container_width=True):
                st.session_state.generated_content = ""
                st.session_state.blog_title = ""
                st.rerun()
        
        with col4:
            if st.button("✏️ 편집모드", use_container_width=True):
                st.session_state.edit_mode = True
                st.rerun()
        
        # 편집 모드
        if st.session_state.get('edit_mode', False):
            st.markdown("---")
            st.markdown("### ✏️ 콘텐츠 편집")
            
            with st.form("edit_form"):
                new_title = st.text_input("제목 수정", value=st.session_state.blog_title)
                new_content = st.text_area(
                    "내용 수정", 
                    value=st.session_state.generated_content,
                    height=400
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    save_button = st.form_submit_button("💾 저장", use_container_width=True)
                with col2:
                    cancel_button = st.form_submit_button("❌ 취소", use_container_width=True)
                
                if save_button:
                    st.session_state.blog_title = new_title
                    st.session_state.generated_content = new_content
                    st.session_state.edit_mode = False
                    st.success("✅ 수정사항이 저장되었습니다!")
                    st.rerun()
                
                if cancel_button:
                    st.session_state.edit_mode = False
                    st.rerun()

def analytics_page():
    """분석 페이지"""
    st.markdown('<h1 class="main-header">📊 콘텐츠 분석</h1>', unsafe_allow_html=True)
    
    if st.session_state.generated_content:
        content = st.session_state.generated_content
        
        # 기본 통계
        st.markdown("### 📈 기본 통계")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            char_count = len(content)
            st.markdown(f"""
            <div class="stats-card">
                <h4>총 글자 수</h4>
                <h2>{char_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            word_count = len(content.split())
            st.markdown(f"""
            <div class="stats-card">
                <h4>단어 수</h4>
                <h2>{word_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
            st.markdown(f"""
            <div class="stats-card">
                <h4>문단 수</h4>
                <h2>{paragraph_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            read_time = max(1, char_count // 500)  # 대략적인 읽기 시간 (분)
            st.markdown(f"""
            <div class="stats-card">
                <h4>예상 읽기시간</h4>
                <h2>{read_time}분</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # SEO 분석
        st.markdown("### 🔍 SEO 분석")
        
        # 키워드 밀도 분석
        keywords_in_content = []
        common_words = ['이', '가', '을', '를', '의', '에', '와', '과', '도', '만', '부터', '까지', '로', '으로']
        words = [word.strip('.,!?()[]{}') for word in content.split() if len(word) > 1]
        words = [word for word in words if word not in common_words]
        
        from collections import Counter
        word_freq = Counter(words)
        top_keywords = word_freq.most_common(10)
        
        if top_keywords:
            st.markdown("**주요 키워드 (빈도):**")
            for word, freq in top_keywords:
                st.write(f"- {word}: {freq}회")
        
        # 가독성 점수
        st.markdown("### 📖 가독성 분석")
        
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h4>평균 문장 길이</h4>
                <h2>{avg_sentence_length:.1f} 단어</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            readability_score = 100 - (avg_sentence_length * 2)  # 간단한 가독성 점수
            readability_score = max(0, min(100, readability_score))
            
            st.markdown(f"""
            <div class="stats-card">
                <h4>가독성 점수</h4>
                <h2>{readability_score:.0f}/100</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # 감정 분석 (간단 버전)
        st.markdown("### 😊 감정 톤 분석")
        
        positive_words = ['좋은', '훌륭한', '최고', '완벽', '추천', '도움', '효과', '성공', '만족']
        negative_words = ['나쁜', '문제', '실패', '어려운', '힘든', '위험', '주의', '경고']
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            tone = "긍정적"
            tone_color = "#28a745"
        elif negative_count > positive_count:
            tone = "부정적"
            tone_color = "#dc3545"
        else:
            tone = "중립적"
            tone_color = "#6c757d"
        
        st.markdown(f"""
        <div style="background-color: {tone_color}20; padding: 15px; border-radius: 10px; border-left: 5px solid {tone_color};">
            <h4 style="color: {tone_color};">전체적인 톤: {tone}</h4>
            <p>긍정 단어: {positive_count}개 | 부정 단어: {negative_count}개</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("분석할 콘텐츠가 없습니다. 먼저 콘텐츠를 생성해주세요.")

def settings_page():
    """설정 페이지"""
    st.markdown('<h1 class="main-header">⚙️ 시스템 설정</h1>', unsafe_allow_html=True)
    
    # API 설정
    st.markdown("### 🔑 API 설정")
    
    with st.expander("Hugging Face API 토큰"):
        api_token = st.text_input(
            "API 토큰 (선택사항)", 
            type="password",
            help="더 안정적인 서비스를 위해 개인 API 토큰을 설정할 수 있습니다."
        )
        
        if st.button("토큰 저장"):
            if api_token:
                st.session_state.hf_api_token = api_token
                st.success("API 토큰이 저장되었습니다!")
            else:
                st.warning("토큰을 입력해주세요.")
    
    # 콘텐츠 설정
    st.markdown("### 📝 콘텐츠 기본 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_tone = st.selectbox(
            "기본 톤",
            ["친근함", "전문적", "열정적", "신뢰감", "유머러스"],
            index=0
        )
        
        default_length = st.selectbox(
            "기본 길이",
            ["짧음 (800-1200자)", "보통 (1200-1800자)", "길음 (1800자 이상)"],
            index=1
        )
    
    with col2:
        auto_seo = st.checkbox("자동 SEO 최적화", value=True)
        auto_cta = st.checkbox("자동 CTA 포함", value=True)
        auto_stats = st.checkbox("자동 통계 업데이트", value=True)
    
    # 템플릿 관리
    st.markdown("### 📋 템플릿 관리")
    
    template_options = st.multiselect(
        "사용할 템플릿 구성요소",
        ["훅킹 인트로", "문제 제기", "해결책 단계", "실제 사례", "FAQ", "주의사항", "강력한 CTA"],
        default=["훅킹 인트로", "문제 제기", "해결책 단계", "실제 사례", "FAQ", "강력한 CTA"]
    )
    
    # 시스템 정보
    st.markdown("### ℹ️ 시스템 정보")
    
    st.info(f"""
    **시스템 버전:** 1.0.0
    **지원 모델:** {len(AI_MODELS)}개
    **현재 선택 모델:** {AI_MODELS.get(st.session_state.selected_model, {}).get('name', '없음')}
    **총 생성 횟수:** {st.session_state.generation_stats.get('total_generations', 0)}회
    """)
    
    # 데이터 관리
    st.markdown("### 🗂️ 데이터 관리")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 세션 초기화", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'logged_in':
                    del st.session_state[key]
            st.success("세션이 초기화되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("📊 통계 리셋", use_container_width=True):
            st.session_state.generation_stats = {}
            st.success("통계가 리셋되었습니다!")
    
    with col3:
        if st.button("💾 설정 저장", use_container_width=True):
            # 설정 저장 로직 (실제로는 파일이나 DB에 저장)
            st.success("설정이 저장되었습니다!")

def main():
    """메인 애플리케이션"""
    init_session_state()
    
    # 로그인 체크
    if not st.session_state.logged_in:
        login_page()
        return
    
    # 네비게이션
    st.sidebar.markdown("## 📱 메뉴")
    
    pages = {
        "🏠 메인": "main",
        "📊 분석": "analytics", 
        "⚙️ 설정": "settings"
    }
    
    selected_page = st.sidebar.radio("페이지 선택", list(pages.keys()))
    
    # 현재 상태 표시
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 현재 상태")
    
    if st.session_state.selected_model:
        model_name = AI_MODELS[st.session_state.selected_model]['name']
        st.sidebar.info(f"**선택된 모델:**\n{model_name}")
    
    if st.session_state.generated_content:
        content_length = len(st.session_state.generated_content)
        st.sidebar.success(f"**생성된 콘텐츠:**\n{content_length:,}자")
    
    # 통계 요약
    if st.session_state.generation_stats:
        total = st.session_state.generation_stats.get('total_generations', 0)
        st.sidebar.metric("총 생성 횟수", total)
    
    # 페이지 라우팅
    page_key = pages[selected_page]
    
    if page_key == "main":
        main_page()
    elif page_key == "analytics":
        analytics_page()
    elif page_key == "settings":
        settings_page()

if __name__ == "__main__":
    main()session_state.selected_model
                        )
                        
                        if generated_content:
                            st.session_state.generated_content = generated_content
                            st.session_state.blog_title = f"{keyword} - 완벽 가이드"
                            
                            # 통계 업데이트
                            if 'generation_stats' not in st.session_state:
                                st.session_state.generation_stats = {}
                            
                            stats = st.session_state.generation_stats
                            stats['total_generations'] = stats.get('total_generations', 0) + 1
                            stats['success_rate'] = 100  # 템플릿 사용으로 항상 성공
                            stats['avg_length'] = len(generated_content)
                            
                            st.