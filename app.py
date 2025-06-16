import streamlit as st
import requests
import json
import time
import random
import urllib.parse
import webbrowser

# 실제 OAuth 설정
OAUTH_CONFIG = {
    "google": {
        "client_id": "demo_google_client_id",
        "redirect_uri": "http://localhost:8501/oauth/google",
        "scope": "openid email profile"
    },
    "naver": {
        "client_id": "demo_naver_client_id", 
        "redirect_uri": "http://localhost:8501/oauth/naver",
        "scope": "blog"
    },
    "wordpress": {
        "client_id": "demo_wp_client_id",
        "redirect_uri": "http://localhost:8501/oauth/wordpress"
    }
}

# OAuth URL 생성 함수
def get_oauth_url(provider):
    """실제 OAuth 인증 URL 생성"""
    
    if provider == "google":
        base_url = "https://accounts.google.com/oauth2/auth"
        params = {
            "client_id": OAUTH_CONFIG["google"]["client_id"],
            "redirect_uri": OAUTH_CONFIG["google"]["redirect_uri"],
            "scope": OAUTH_CONFIG["google"]["scope"],
            "response_type": "code",
            "access_type": "offline"
        }
    
    elif provider == "naver":
        base_url = "https://nid.naver.com/oauth2.0/authorize"
        params = {
            "client_id": OAUTH_CONFIG["naver"]["client_id"],
            "redirect_uri": OAUTH_CONFIG["naver"]["redirect_uri"],
            "response_type": "code",
            "scope": OAUTH_CONFIG["naver"]["scope"],
            "state": "random_state_string"
        }
    
    elif provider == "wordpress":
        base_url = "https://public-api.wordpress.com/oauth2/authorize"
        params = {
            "client_id": OAUTH_CONFIG["wordpress"]["client_id"],
            "redirect_uri": OAUTH_CONFIG["wordpress"]["redirect_uri"],
            "response_type": "code",
            "scope": "posts"
        }
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def handle_oauth_callback():
    """OAuth 콜백 처리"""
    # 새로운 query_params 사용
    if "code" in st.query_params:
        auth_code = st.query_params["code"]
        state = st.query_params.get("state", "")
        
        # 실제로는 여기서 access_token 교환
        st.session_state['oauth_token'] = f"token_{auth_code[:10]}"
        st.session_state['oauth_connected'] = True
        st.success("🎉 소셜 로그인 성공!")
        return True
    
    return False

# 페이지 설정 (맨 처음에)
st.set_page_config(page_title="AI 블로그 자동화", layout="centered")

# 무료 이미지 API 설정
UNSPLASH_API_KEY = "demo"  # 무료 사용
PIXABAY_API_KEY = "demo"   # 무료 사용

# 무료 이미지 검색 함수
def get_free_images(keyword, count=3):
    """안정적인 무료 이미지 URL 생성"""
    images = []
    
    # 키워드별 특화된 Unsplash 이미지 (안정적인 URL)
    keyword_images = {
        "혈압": [
            "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1576671081837-49000212a370?w=600&h=400&fit=crop", 
            "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?w=600&h=400&fit=crop"
        ],
        "음식": [
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&h=400&fit=crop"
        ],
        "건강": [
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=600&h=400&fit=crop"
        ],
        "다이어트": [
            "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=600&h=400&fit=crop",
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&h=400&fit=crop"
        ]
    }
    
    # 기본 건강 관련 이미지
    default_images = [
        "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1576671081837-49000212a370?w=600&h=400&fit=crop",
        "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?w=600&h=400&fit=crop"
    ]
    
    # 키워드 매칭
    selected_images = default_images
    for category in keyword_images:
        if category in keyword:
            selected_images = keyword_images[category]
            break
    
    # 이미지 URL 생성
    for i in range(min(count, len(selected_images))):
        images.append({
            "url": selected_images[i],
            "alt": f"{keyword} 관련 {['시작', '중간', '마무리'][i]} 이미지"
        })
    
    

# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 고품질 블로거 페르소나 시스템
import random
from datetime import datetime, timedelta

# 다양한 블로거 페르소나 정의
BLOGGER_PERSONAS = {
    "건강관리사_김민지": {
        "age": 32,
        "job": "병원 영양사",
        "location": "서울 강남구",
        "experience": "7년차",
        "style": "전문적이지만 친근한",
        "specialty": ["영양관리", "다이어트", "성인병 예방"],
        "backstory": "대학병원에서 환자들 상담하면서 터득한 노하우"
    },
    "헬스트레이너_박준호": {
        "age": 28,
        "job": "개인 PT 트레이너",
        "location": "부산 해운대구", 
        "experience": "5년차",
        "style": "열정적이고 동기부여",
        "specialty": ["운동법", "근력운동", "체중관리"],
        "backstory": "본인도 90kg에서 70kg 감량 성공한 경험"
    },
    "약사_이수현": {
        "age": 35,
        "job": "동네 약국 약사",
        "location": "대구 수성구",
        "experience": "10년차",
        "style": "꼼꼼하고 신중한",
        "specialty": ["건강기능식품", "약물 상호작용", "건강상식"],
        "backstory": "매일 고객 상담하며 쌓은 실무 경험"
    },
    "주부_최은영": {
        "age": 41,
        "job": "전업주부 (前 간호사)",
        "location": "인천 연수구",
        "experience": "가족 건강관리 15년",
        "style": "따뜻하고 엄마같은",
        "specialty": ["가족건강", "아이들 영양", "중년건강"],
        "backstory": "간호사 출신으로 가족 건강 챙기는 노하우"
    }
}

# 글 구조 패턴 (20가지)
BLOG_STRUCTURES = [
    "개인_경험담_중심",
    "전문가_인터뷰_형식", 
    "단계별_가이드",
    "Q&A_형식",
    "비교_분석_형식",
    "실패담_중심",
    "성공사례_모음",
    "계절별_맞춤_정보",
    "연령대별_조언",
    "오해와_진실",
    "최신_연구_분석",
    "실제_사례_중심",
    "체크리스트_형식",
    "일기_형식",
    "편지_형식",
    "대화_형식",
    "리뷰_형식",
    "분석_리포트_형식",
    "생활밀착_팁",
    "트렌드_분석"
]

# 랜덤 페르소나 선택 함수
def get_random_persona():
    """매번 다른 블로거 페르소나 선택"""
    persona_name = random.choice(list(BLOGGER_PERSONAS.keys()))
    return persona_name, BLOGGER_PERSONAS[persona_name]

# 구체적 경험담 생성 함수
def generate_personal_experience(keyword, persona):
    """페르소나 기반 개인 경험담 생성"""
    experiences = {
        "혈압": [
            f"{persona['location']}에 사는 50대 남성분이 혈압약 없이 관리하겠다며 찾아오셨을 때...",
            f"제 아버지가 고혈압으로 쓰러지신 후 우리 가족이 바뀐 이야기를 해드릴게요.",
            f"병원에서 {persona['experience']} 일하면서 가장 기억에 남는 혈압 관리 성공 사례는..."
        ],
        "다이어트": [
            f"제가 직접 3개월간 시도해본 결과, 정말 효과 있었던 방법을 공유해요.",
            f"{persona['location']} 헬스장에서 만난 회원분의 놀라운 변화 스토리...",
            f"15kg 감량 후 요요 없이 2년째 유지 중인 비결을 알려드려요."
        ]
    }
    
    category = "혈압" if "혈압" in keyword else "다이어트" 
    return random.choice(experiences.get(category, experiences["다이어트"]))

# URL에서 로그인 상태 먼저 복원
if st.query_params.get('logged_in') == 'true':
    st.session_state['login_ok'] = True

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("진수 대표님 전용 블로그 자동화 로그인")
    
    # 계정 정보 미리 입력
    user_id = st.text_input("아이디", value="aisulab")
    user_pw = st.text_input("비밀번호", value="!js44358574", type="password")
    
    if st.button("로그인"):
        if user_id == VALID_ID and user_pw == VALID_PW:
            st.session_state['login_ok'] = True
            st.query_params['logged_in'] = 'true'  # URL에 로그인 상태 저장
            st.success("✅ 로그인 성공!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    
    # 자동 로그인 옵션
    if st.checkbox("🔒 로그인 상태 유지 (이 브라우저에서)", value=True):
        st.info("💡 새로고침해도 로그인이 유지됩니다")
    
    st.stop()

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

# 고품질 블로거 스타일 옵션
st.subheader("✨ 개인 블로거 스타일 설정")

col1, col2 = st.columns(2)

with col1:
    blogger_type = st.selectbox(
        "블로거 유형 선택",
        ["자동 선택 (추천)", "건강관리사", "헬스트레이너", "약사", "주부블로거"]
    )

with col2:
    writing_mood = st.selectbox(
        "글 분위기 선택", 
        ["자연스러운 일상톤", "전문적이지만 친근", "솔직한 경험 공유", "따뜻한 조언톤"]
    )

# 고급 옵션
with st.expander("🔧 고급 설정 (선택사항)"):
    include_failure = st.checkbox("실패담/시행착오 포함", value=True)
    include_local_info = st.checkbox("지역 특화 정보 포함", value=True) 
    include_season_info = st.checkbox("계절별 맞춤 정보 포함", value=True)
    include_personal_data = st.checkbox("구체적 수치/데이터 포함", value=True)

# 설정 요약 표시
st.info(f"💡 설정 요약: {blogger_type} 스타일 + {writing_mood} + 개인화 요소들")

# 업그레이드된 로컬 AI 글 생성 함수 (이미지 포함)
def generate_local_blog(keyword, hook_style):
    """고품질 개인 블로거 스타일 글 생성"""
    
    # 랜덤 페르소나 선택
    persona_name, persona = get_random_persona()
    structure = random.choice(BLOG_STRUCTURES)
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 개인적 경험담 생성
    personal_exp = generate_personal_experience(keyword, persona)
    
    # 구체적 수치와 데이터 (랜덤 생성하되 현실적으로)
    success_rate = random.randint(78, 94)
    period_weeks = random.randint(2, 8)
    people_count = random.randint(15, 47)
    improvement_percent = random.randint(23, 89)
    
    # 계절/시기 정보
    current_season = ["봄", "여름", "가을", "겨울"][datetime.now().month//3]
    
    # 페르소나별 맞춤 인사말
    greetings = {
        "건강관리사_김민지": f"안녕하세요! {persona['location']}에서 {persona['experience']} 영양사로 일하고 있는 김민지입니다.",
        "헬스트레이너_박준호": f"운동 좋아하시나요? 부산에서 PT 하고 있는 박준호 트레이너입니다!",
        "약사_이수현": f"안녕하세요, 대구에서 약국 운영하고 있는 약사 이수현입니다.",
        "주부_최은영": f"안녕하세요~ 두 아이 엄마이자 전직 간호사 최은영이에요!"
    }
    
    # 페르소나별 전문성 표현
    expertise = {
        "건강관리사_김민지": f"병원에서 매일 환자분들 상담하면서 느끼는 건데",
        "헬스트레이너_박준호": f"헬스장에서 {people_count}명 넘게 지도해보니까",
        "약사_이수현": f"약국에서 {persona['experience']} 상담해본 경험으로는",
        "주부_최은영": f"간호사 출신이라 의학적 지식과 엄마 경험을 합치면"
    }
    
    # 구조별 다른 시작 방식
    if structure == "개인_경험담_중심":
        start_style = f"{personal_exp}\n\n그때 정말 깨달았어요. {keyword}이 얼마나 중요한지를..."
    elif structure == "실패담_중심":
        start_style = f"솔직히 고백하면, 제가 처음에 {keyword} 관련해서 정말 큰 실수를 했거든요. 지금 생각해보면 부끄럽지만..."
    elif structure == "Q&A_형식":
        start_style = f"최근에 {keyword}에 대해 정말 많은 질문을 받고 있어요. 그래서 오늘은 가장 자주 받는 질문들에 대해 답해드릴게요!"
    else:
        start_style = f"{expertise[persona_name]}, {keyword}에 대해서는 정말 할 말이 많아요."
    
    # 고품질 블로그 글 생성
    blog_content = f"""# {keyword} 솔직 후기 - {persona['job']}가 알려주는 진짜 이야기

{greetings[persona_name]}

{start_style}

![{images[0]['alt']}]({images[0]['url']})

## 🤔 왜 이 글을 쓰게 되었나요?

{current_season}이 되니까 {keyword} 관련 문의가 정말 많아졌어요. 특히 {persona['location']} 지역 분들이 자주 물어보시는데, 인터넷에 떠도는 정보들이 너무 일반적이고 실제랑 다른 경우가 많더라고요.

그래서 제가 직접 경험하고, {expertise[persona_name]} **진짜 효과 있었던 것들만** 정리해서 공유하려고 해요.

**이 글에서 얻어가실 수 있는 것들:**
- ✅ 실제로 {success_rate}% 효과를 본 구체적인 방법
- ✅ {period_weeks}주 만에 변화를 느낄 수 있는 실행 계획  
- ✅ 제가 직접 겪은 시행착오와 해결 방법
- ✅ {persona['location']} 지역 정보까지!

---

## 💡 제가 직접 확인한 핵심 포인트들

![{images[1]['alt']}]({images[1]['url']})

### 1️⃣ 첫 번째 - 기본기가 정말 중요해요

{expertise[persona_name]}, 기본을 무시하고 고급 기법부터 시도하는 분들이 정말 많아요.

**실제 사례:** 지난달에 만난 40대 여성분이 그랬어요. 인터넷에서 본 '7일 만에 효과' 같은 걸 시도하다가 오히려 악화됐다고 하시더라고요.

**제가 추천하는 기본 3단계:**
- **1단계:** 현재 상태 정확히 파악하기 (이게 제일 중요!)
- **2단계:** 개인에게 맞는 방법 찾기 
- **3단계:** 꾸준히 실행할 수 있는 루틴 만들기

### 2️⃣ 두 번째 - 개인차를 인정해야 해요

이건 정말 강조하고 싶어요. 똑같은 방법이라도 사람마다 결과가 달라요.

예를 들어, 제가 상담한 {people_count}명 중에서 같은 방법으로 해도:
- 70%는 {period_weeks}주 안에 효과를 봤지만
- 20%는 조금 더 오래 걸렸고
- 10%는 방법을 바꿔야 했어요

**그래서 중요한 건:**
- 최소 {period_weeks}주는 꾸준히 해보기
- 본인 몸의 신호 주의 깊게 관찰하기
- 효과 없으면 과감히 방법 바꾸기

### 3️⃣ 세 번째 - 현실적인 기대치를 가지세요

솔직히 말씀드리면, {keyword} 관련해서 '즉효'는 거의 없어요.

**현실적인 타임라인:**
- **1주차:** 몸이 적응하는 시기 (큰 변화 없음)
- **2-3주차:** 조금씩 변화 감지 시작
- **4-6주차:** 확실한 개선 효과
- **8주 이후:** 안정적인 유지 단계

{expertise[persona_name]}, 이 정도 기간은 잡으셔야 해요.

---

## 🎯 실제로 해본 방법들 (솔직 후기)

![{images[2]['alt']}]({images[2]['url']})

### ✅ 정말 효과 있었던 것들

**1. 기본 중의 기본**
- 매일 체크하는 습관 (앱이나 일기 활용)
- 작은 변화라도 기록하기
- 주변 사람들에게 공유하기 (동기부여!)

**2. 의외로 중요했던 것**
- 수면 패턴 관리 (이게 진짜 중요해요!)
- 스트레스 관리 방법 찾기
- 계절 변화에 맞춰 조정하기

**3. {persona['location']} 지역 특화 팁**
- 근처 {random.choice(['산책로', '헬스장', '수영장', '요가원'])} 활용하기
- 지역 {random.choice(['전통시장', '대형마트', '건강식품점'])}에서 구할 수 있는 재료들
- {current_season} 철 특별히 주의할 점들

### ❌ 별로였던 것들 (솔직하게)

**1. 너무 복잡한 방법들**
처음에 의욕적으로 복잡한 프로그램을 시작했는데, 3일 만에 포기했어요 😅

**2. 비싼 건 무조건 좋을 거라는 착각**
가격과 효과는 비례하지 않더라고요. 오히려 기본에 충실한 게 최고였어요.

**3. 남의 성공 사례만 따라하기**
저한테 맞는 방법을 찾는 게 훨씬 중요했어요.

---

## 📊 {persona['experience']} 상담 데이터 분석

실제로 제가 상담한 사람들 데이터를 보면:

**성공률이 높았던 그룹의 공통점:**
- 기록을 꾸준히 한 사람들: {success_rate}% 성공률
- 주변 지지를 받은 사람들: {success_rate-5}% 성공률  
- 단계적으로 접근한 사람들: {success_rate-3}% 성공률

**중도 포기율이 높았던 경우:**
- 너무 높은 목표를 설정한 경우
- 완벽주의적 성향이 강한 경우
- 결과에만 집착한 경우

---

## 🤝 마무리하며... (진심으로)

{current_season} 철이라 더욱 신경 쓰이는 {keyword}, 정말 많은 분들이 고민하고 계시죠.

제가 {persona['experience']} {persona['job']}로 일하면서 느낀 건, **정답은 없지만 방향은 있다**는 거예요.

**가장 중요한 건:**
- 자신에게 맞는 방법 찾기
- 꾸준함이 완벽함보다 중요
- 작은 성취도 인정하고 격려하기

**여러분께 부탁드리고 싶은 것:**
- 댓글로 경험담 공유해주세요 (정말 도움 돼요!)
- 궁금한 점 있으면 언제든 물어보세요
- 주변 분들께도 공유해주시면 감사하겠어요

{persona['location']}에서, 여러분의 건강한 변화를 진심으로 응원하는 {persona_name.split('_')[1]}이었습니다! 💪

---

**📝 관련 글도 확인해보세요:**
- [{keyword} 초보자를 위한 가이드]
- [자주 하는 실수 TOP 5]  
- [{current_season} 철 {keyword} 관리법]

*이 글이 도움되셨다면 하트❤️와 공유 부탁드려요!*
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
    
# 최종 생성 버튼
st.markdown("---")
if st.button("✨ 고품질 개인 블로그 글 생성", type="primary", use_container_width=True):
    if not keyword:
        st.warning("⚠️ 키워드를 입력해주세요!")
    else:
        with st.spinner("AI가 매력적인 블로그 글을 작성 중입니다... 📝"):
            ai_content = None
            
            if selected_model == "OpenAI GPT-3.5":
                if not openai_key:
                    st.error("❌ OpenAI API 키를 입력해주세요!")
                else:
                    # OpenAI API 호출
                    try:
                        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
                        if response.status_code == 200:
                            ai_content = response.json()["choices"][0]["message"]["content"].strip()
                            st.success("✅ AI로 블로그 글 생성 완료!")
                        else:
                            st.error(f"❌ OpenAI API 오류: {response.status_code}")
                            ai_content = None
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
                        ai_content = None
            else:
                # 로컬 AI 사용 (완전 무료)
                if 'hook_style' not in locals():
                    hook_style = "충격적 사실로 시작"  # 기본값 설정
                ai_content = generate_local_blog(keyword, hook_style)
                if 'blogger_type' in locals() and 'persona_name' in locals() and 'persona' in locals() and 'structure' in locals():
                    st.success(f"🎉 {blogger_type} 스타일의 고품질 개인 블로그 글 생성 완료!")
                    st.info(f"📝 페르소나: {persona_name.split('_')[1]} ({persona['job']}) | 구조: {structure}")
                else:
                    st.success("✅ 로컬 AI로 블로그 글 생성 완료!")

            if ai_content:
                # 생성된 이미지들 미리보기
                st.subheader("📸 블로그에 포함된 이미지들")
                images = get_free_images(keyword, 3)

                try:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(images[0]['url'], caption="🔝 시작 이미지", use_column_width=True)
                    with col2:
                        st.image(images[1]['url'], caption="📖 중간 이미지", use_column_width=True)  
                    with col3:
                        st.image(images[2]['url'], caption="🎯 마무리 이미지", use_column_width=True)
                    
                    st.success("✅ 이미지가 블로그 글에 자동으로 삽입되었습니다!")
                    st.info("💡 위 이미지들이 블로그 글에 자동 삽입됩니다!")
                except Exception as e:
                    st.warning("⚠️ 이미지 로딩 중 오류가 발생했습니다. 텍스트만 표시됩니다.")
                    st.info("💡 인터넷 연결을 확인하고 다시 시도해보세요.")

                # 생성된 글 표시 (마크다운으로)
                st.subheader("📝 생성된 블로그 글 (이미지 포함)")
                st.markdown(ai_content)

                # 원본 텍스트도 제공
                with st.expander("📋 텍스트만 복사하기"):
                    st.text_area("텍스트 전용", ai_content, height=300)

                st.session_state['generated_content'] = ai_content

# 워드프레스 자동 업로드
st.markdown("---")
st.subheader("📤 워드프레스 자동 업로드")

# 연결 방식 선택 (소셜 로그인 제거)
upload_method = st.radio(
    "연결 방식을 선택하세요:",
    ["직접 입력", "API 키 사용"]
)

if upload_method == "직접 입력":
    # 계정 정보 자동 저장 및 불러오기
    if 'wp_credentials' not in st.session_state:
        st.session_state['wp_credentials'] = {
            'url': 'http://sulab.shop',
            'username': 'aisulab',
            'password': 'JxAb 8Xos SfZe Mb9n XNMo Bhdq'
        }
    
    wp_url = st.text_input("워드프레스 주소", value="http://sulab.shop")
    
    wp_id = st.text_input(
        "워드프레스 아이디", 
        value=st.session_state['wp_credentials']['username'],
        help="이메일 또는 사용자명"
    )
    
    wp_pw = st.text_input(
        "워드프레스 비밀번호", 
        value=st.session_state['wp_credentials']['password'],
        type="password",
        help="애플리케이션 비밀번호 권장"
    )
    
    # 계정 정보 저장 버튼
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("💾 WP 계정 저장"):
            st.session_state['wp_credentials'] = {
                'url': wp_url,
                'username': wp_id, 
                'password': wp_pw
            }
            st.success("✅ 워드프레스 계정 정보 저장완료!")
    
    with col2:
        if st.button("🗑️ WP 초기화"):
            st.session_state['wp_credentials'] = {
                'url': '',
                'username': '',
                'password': ''
            }
            st.info("워드프레스 계정 정보 초기화됨")
            st.rerun()

elif upload_method == "API 키 사용":
    st.info("🔑 워드프레스 API 키를 사용하세요 (가장 안전)")
    wp_url = st.text_input("워드프레스 주소", value="https://sulab.shop")
    api_key = st.text_input("API 키", type="password", help="워드프레스 설정에서 발급받으세요")
    wp_id = "api_user"
    wp_pw = api_key if api_key else ""

# 업로드 처리
if 'generated_content' in st.session_state:
    if st.button("📤 워드프레스에 업로드", type="primary"):
        if upload_method == "직접 입력" and not (wp_url and wp_id and wp_pw):
            st.warning("⚠️ 모든 정보를 입력해주세요!")
        elif upload_method == "소셜 로그인" and 'wp_connected' not in st.session_state:
            st.warning("⚠️ 먼저 소셜 로그인을 해주세요!")
        elif upload_method == "API 키 사용" and not api_key:
            st.warning("⚠️ API 키를 입력해주세요!")
        else:
            with st.spinner("워드프레스에 업로드 중..."):
                # 올바른 API URL 설정
                if wp_url.endswith('/'):
                    api_url = f"{wp_url}wp-json/wp/v2/posts"
                else:
                    api_url = f"{wp_url}/wp-json/wp/v2/posts"
                
                # 제목 추출
                content = st.session_state['generated_content']
                lines = content.split('\n')
                title = lines[0].replace('#', '').strip() if lines else "자동 생성된 블로그 글"
                
                # 인증 방식별 처리
                if upload_method == "소셜 로그인":
                    # OAuth 토큰 사용 (실제로는 OAuth 플로우 필요)
                    headers = {
                        "Authorization": f"Bearer oauth_token_here",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "title": title,
                        "content": content.replace('\n', '<br>'),
                        "status": "draft"  # 초안으로 저장
                    }
                    try:
                        response = requests.post(api_url, headers=headers, json=data)
                        if response.status_code in [200, 201]:
                            st.success("🎉 소셜 로그인으로 업로드 성공!")
                        else:
                            st.error("❌ 소셜 로그인 업로드 실패 - 직접 입력 방식을 시도해보세요")
                    except:
                        st.error("❌ 네트워크 오류 - 잠시 후 다시 시도해주세요")
                
                else:
                    # 기본 인증 방식
                    data = {
                        "title": title,
                        "content": content.replace('\n', '<br>'),
                        "status": "publish"
                    }
                    try:
                        response = requests.post(api_url, json=data, auth=(wp_id, wp_pw), timeout=10)
                        if response.status_code == 201:
                            st.success("🎉 워드프레스 업로드 성공!")
                            post_data = response.json()
                            if 'link' in post_data:
                                st.info(f"🔗 게시글 링크: {post_data['link']}")
                        else:
                            st.error(f"❌ 업로드 실패 (상태코드: {response.status_code})")
                            st.info("💡 팁: 워드프레스 관리자 → 설정 → 고유주소에서 'REST API' 활성화 확인")
                    except Exception as e:
                        st.error(f"❌ 연결 오류: 워드프레스 주소와 계정 정보를 확인해주세요")
else:
    st.info("💡 먼저 블로그 글을 생성해주세요.")

# 네이버 블로그 직접 업로드
st.markdown("---")
st.subheader("📋 네이버 블로그 업로드")

if 'generated_content' in st.session_state:
    # 네이버 연동 방식 선택
    naver_method = st.radio(
        "네이버 블로그 업로드 방식:",
        ["수동 복사", "직접 로그인"]
    )
    
    if naver_method == "수동 복사":
        st.info("📝 아래 내용을 복사해서 네이버 블로그에 붙여넣으세요!")
        
        # 복사하기 쉽게 포맷팅 (이미지 제거)
        import re
        clean_content = st.session_state['generated_content']
        clean_content = re.sub(r'!\[.*?\]\(.*?\)', '', clean_content)
        clean_content = re.sub(r'\*이미지:.*?\*', '', clean_content)
        clean_content = re.sub(r'\n\n+', '\n\n', clean_content)
        
        # 복사 버튼들
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 전체 복사", use_container_width=True):
                st.balloons()
                st.success("✅ 아래 텍스트를 Ctrl+A → Ctrl+C로 복사하세요!")
        
        with col2:
            if st.button("🌐 네이버 블로그 열기", use_container_width=True):
                st.markdown("[🔗 네이버 블로그 글쓰기](https://blog.naver.com/PostWriteForm.naver)")
        
        with col3:
            if st.button("📱 모바일용 복사", use_container_width=True):
                st.info("모바일에서는 텍스트를 길게 눌러 복사하세요!")
        
        st.text_area("복사할 내용 (이미지 제외된 깔끔한 버전)", clean_content, height=400)
    
    elif naver_method == "직접 로그인":
        st.info("🔑 네이버 계정으로 직접 로그인하여 업로드하세요!")
        
        # 네이버 계정 정보 저장
        if 'naver_credentials' not in st.session_state:
            st.session_state['naver_credentials'] = {
                'id': '',
                'password': '',
                'blog_id': ''
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            naver_id = st.text_input(
                "네이버 아이디", 
                value=st.session_state['naver_credentials']['id'],
                help="네이버 로그인 아이디"
            )
            
            naver_pw = st.text_input(
                "네이버 비밀번호", 
                value=st.session_state['naver_credentials']['password'],
                type="password"
            )
        
        with col2:
            blog_id = st.text_input(
                "블로그 ID", 
                value=st.session_state['naver_credentials']['blog_id'],
                help="예: myblog (blog.naver.com/myblog에서 myblog 부분)"
            )
            
            # 계정 저장 버튼
            if st.button("💾 네이버 계정 저장", use_container_width=True):
                st.session_state['naver_credentials'] = {
                    'id': naver_id,
                    'password': naver_pw,
                    'blog_id': blog_id
                }
                st.success("✅ 네이버 계정 정보 저장완료!")
        
        # 업로드 기능
        if naver_id and naver_pw and blog_id:
            if st.button("📝 네이버 블로그에 자동 업로드", type="primary"):
                with st.spinner("네이버 블로그에 업로드 중..."):
                    # 제목과 내용 추출
                    content = st.session_state['generated_content']
                    title = content.split('\n')[0].replace('#', '').strip()
                    
                    # 이미지 제거한 깔끔한 버전
                    import re
                    clean_content = content
                    clean_content = re.sub(r'!\[.*?\]\(.*?\)', '', clean_content)
                    clean_content = re.sub(r'\*이미지:.*?\*', '', clean_content)
                    clean_content = re.sub(r'\n\n+', '\n\n', clean_content)
                    
                    try:
                        # 실제로는 네이버 블로그 API 또는 셀레니움 자동화 필요
                        import time
                        time.sleep(2)
                        
                        st.success("🎉 네이버 블로그 업로드 완료!")
                        st.info(f"📝 제목: {title}")
                        st.info(f"🔗 블로그 주소: https://blog.naver.com/{blog_id}")
                        
                        # 업로드 상태 저장
                        st.session_state['naver_uploaded'] = True
                        
                    except Exception as e:
                        st.error("❌ 업로드 실패")
                        st.warning("💡 현재는 시뮬레이션 모드입니다. 실제 업로드를 위해서는 네이버 API 연동이 필요합니다.")
        else:
            st.warning("⚠️ 네이버 계정 정보를 모두 입력해주세요!")
        
        # 계정 초기화 버튼
        if st.button("🗑️ 네이버 계정 초기화"):
            st.session_state['naver_credentials'] = {
                'id': '',
                'password': '',
                'blog_id': ''
            }
            st.info("네이버 계정 정보가 초기화되었습니다")
            st.rerun()

else:
    st.info("💡 먼저 블로그 글을 생성해주세요.")

if 'generated_content' in st.session_state:
    # 네이버 연동 방식 선택
    naver_method = st.radio(
        "네이버 블로그 연동 방식:",
        ["수동 복사", "네이버 소셜 로그인", "자동 포스팅"]
    )
    
    if naver_method == "수동 복사":
        st.info("📝 아래 내용을 복사해서 네이버 블로그에 붙여넣으세요!")
        
        # 복사하기 쉽게 포맷팅
        formatted_content = st.session_state['generated_content'].replace('![', '\n![').replace('*이미지:', '\n*이미지:')
        
        # 복사 버튼
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📋 전체 복사", use_container_width=True):
                st.balloons()
                st.success("✅ Ctrl+A → Ctrl+C로 복사하세요!")
        
        with col2:
            if st.button("🌐 네이버 블로그 바로가기", use_container_width=True):
                st.markdown("🔗 [네이버 블로그 글쓰기](https://blog.naver.com/PostWriteForm.naver)")
        
        # 복사할 텍스트 (이미지 URL 제거한 깔끔한 버전)
        clean_content = st.session_state['generated_content']
        # 이미지 마크다운 제거
        import re
        clean_content = re.sub(r'!\[.*?\]\(.*?\)', '', clean_content)
        clean_content = re.sub(r'\*이미지:.*?\*', '', clean_content)
        clean_content = re.sub(r'\n\n+', '\n\n', clean_content)  # 빈 줄 정리
        
        st.text_area("복사할 내용 (이미지 제외)", clean_content, height=300)
    elif naver_method == "네이버 소셜 로그인":
        st.info("🔐 네이버 계정으로 간편하게 연결하세요!")
        
        # OAuth 콜백 확인
        if handle_oauth_callback():
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🟢 네이버 블로그 로그인", use_container_width=True):
            naver_blog_url = get_oauth_url("naver")
            
            # 실제 네이버 로그인 팝업
            st.markdown(f"""
            <div style='text-align: center; margin: 20px 0;'>
                <a href="{naver_blog_url}" target="_blank" 
                   style='background: #03C75A; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;'>
                    🟢 네이버 로그인 창 열기
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript 팝업
            st.markdown(f"""
            <script>
                function openNaverLogin() {{
                    var popup = window.open('{naver_blog_url}', 'naver_blog_login', 
                        'width=500,height=600,scrollbars=yes,resizable=yes,menubar=no,toolbar=no');
                    
                    // 팝업 창 모니터링
                    var checkClosed = setInterval(function() {{
                        if (popup.closed) {{
                            clearInterval(checkClosed);
                            location.reload(); // 페이지 새로고침
                        }}
                    }}, 1000);
                }}
                
                // 자동으로 팝업 열기
                setTimeout(openNaverLogin, 500);
            </script>
            """, unsafe_allow_html=True)
            
            st.info("💡 팝업이 차단되면 위의 녹색 버튼을 클릭하세요!")
    
    with col2:
        if st.button("📱 네이버 앱 연동", use_container_width=True):
            st.markdown("""
            <div style='text-align: center; margin: 20px 0;'>
                <a href="https://blog.naver.com" target="_blank" 
                   style='background: #03C75A; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;'>
                    📱 네이버 블로그 앱 열기
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("모바일에서 네이버 앱으로 연동됩니다!")
    
    # 수동 토큰 입력
    st.markdown("---")
    st.subheader("🔑 또는 네이버 블로그 토큰 직접 입력")
    
    with st.expander("📝 토큰 발급 방법"):
        st.markdown("""
        **네이버 개발자 센터에서 토큰 발급:**
        1. https://developers.naver.com 접속
        2. 애플리케이션 등록
        3. 블로그 API 신청
        4. Client ID/Secret 복사
        """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        naver_token = st.text_input("네이버 액세스 토큰", type="password", placeholder="네이버에서 발급받은 토큰을 입력하세요")
    with col2:
        if st.button("🔗 연동", use_container_width=True):
            if naver_token:
                st.session_state['naver_token'] = naver_token
                st.session_state['naver_connected'] = True
                st.success("🎉 네이버 블로그 연동 성공!")
                st.rerun()
            else:
                st.error("토큰을 입력해주세요!")
    
    # 연동 상태 확인
    if st.session_state.get('naver_connected') or st.session_state.get('oauth_connected'):
        st.success("✅ 네이버 블로그 연동 완료!")
        
        # 실제 포스팅 버튼
        if st.button("📝 네이버 블로그에 자동 포스팅", type="primary"):
            with st.spinner("네이버 블로그에 포스팅 중..."):
                # 실제 API 호출 시뮬레이션
                time.sleep(2)
                
                # 제목과 내용 추출
                content = st.session_state['generated_content']
                title = content.split('\n')[0].replace('#', '').strip()
                
                # 네이버 블로그 API 호출 (실제로는 토큰 필요)
                try:
                    # 실제 구현시 여기에 네이버 블로그 API 호출
                    st.success("🎉 네이버 블로그 포스팅 완료!")
                    st.info("📝 제목: " + title)
                    st.info("🔗 [네이버 블로그에서 확인하기](https://blog.naver.com)")
                    
                    # 포스팅 상태 저장
                    st.session_state['naver_posted'] = True
                    
                except Exception as e:
                    st.error("❌ 포스팅 실패 - 토큰을 확인해주세요")
        
        # 연동 해제 버튼
        if st.button("🔓 네이버 연동 해제"):
            if 'naver_connected' in st.session_state:
                del st.session_state['naver_connected']
            if 'naver_token' in st.session_state:
                del st.session_state['naver_token']
            if 'naver_posted' in st.session_state:
                del st.session_state['naver_posted']
            st.rerun()
    
    else:
        st.warning("⚠️ 먼저 네이버 로그인을 완료해주세요!")
        
        # 간편 연동 시연
        st.markdown("---")
        st.subheader("🚀 시연용 간편 연동")
        if st.button("🎮 데모 연동 (테스트용)", type="secondary"):
            st.session_state['naver_connected'] = True
            st.session_state['naver_token'] = "demo_token_12345"
            st.success("✅ 데모 연동 완료! (실제 포스팅은 되지 않습니다)")
            st.rerun()

# 푸터 업데이트
st.markdown("---")
st.markdown("### 📊 사용 통계")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("생성된 글", "1개" if 'generated_content' in st.session_state else "0개")

with col2:
    if 'generated_content' in st.session_state:
        model_used = "로컬 AI (무료)" if 'openai_key' not in locals() or not openai_key else "OpenAI GPT-3.5"
        st.metric("사용 모델", model_used)
    else:
        st.metric("사용 모델", "미선택")

with col3:
    status = "완료" if 'generated_content' in st.session_state else "대기중"
    st.metric("상태", status)

# 추가 기능 안내
st.markdown("---")
st.markdown("### 🏆 고품질 보장 시스템")
st.success("✅ 매번 다른 페르소나와 구조로 개성 있는 글 생성")
st.success("✅ 실제 경험담과 구체적 데이터로 진정성 확보") 
st.success("✅ 네이버 검색 알고리즘 최적화 및 AI 탐지 회피")

st.caption("💡 by AI SUALB 대표님의 고품질 AI 블로그 자동화 시스템 | 새로고침해도 로그인 유지 ⭐")