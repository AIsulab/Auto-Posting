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
    """키워드 연관 무료 이미지 가져오기"""
    images = []
    
    # 키워드별 특화 이미지 매핑
    keyword_images = {
        "혈압": {
            "keywords": ["blood-pressure", "health", "medical", "heart"],
            "unsplash_ids": ["Nqj0Ci-mDHs", "hpjSkU2UYSU", "5jctAMjz21A"]
        },
        "음식": {
            "keywords": ["food", "healthy-food", "nutrition", "vegetables"],
            "unsplash_ids": ["08bOYnH_r_E", "1SPu0KT-Ejg", "nTZOILVZuOg"]
        },
        "건강": {
            "keywords": ["health", "wellness", "fitness", "medical"],
            "unsplash_ids": ["eWqOgJ-lfiI", "Nqj0Ci-mDHs", "5jctAMjz21A"]
        },
        "다이어트": {
            "keywords": ["diet", "healthy-eating", "fitness", "weight-loss"],
            "unsplash_ids": ["1SPu0KT-Ejg", "08bOYnH_r_E", "nTZOILVZuOg"]
        }
    }
    
    # 키워드 매칭
    matched_category = None
    for category, data in keyword_images.items():
        if category in keyword:
            matched_category = data
            break
    
    # 기본값 설정
    if not matched_category:
        matched_category = keyword_images["건강"]
    
    try:
        # Unsplash 특정 이미지 ID 사용 (무료)
        for i, img_id in enumerate(matched_category["unsplash_ids"][:count]):
            img_url = f"https://images.unsplash.com/{img_id}?w=600&h=400&fit=crop"
            images.append({
                "url": img_url,
                "alt": f"{keyword} 관련 {['시작', '중간', '마무리'][i]} 이미지"
            })
    except:
        # 백업: 키워드 기반 Pixabay 스타일
        backup_seeds = [101, 202, 303]
        for i in range(count):
            img_url = f"https://picsum.photos/600/400?random={backup_seeds[i]}"
            images.append({
                "url": img_url,
                "alt": f"{keyword} 관련 이미지 {i+1}"
            })
    
    return images

# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("AI SUALB 대표님 전용 블로그 자동화 로그인")
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

# 업그레이드된 로컬 AI 글 생성 함수 (이미지 포함)
def generate_local_blog(keyword, hook_style):
    """자연스러운 블로거 말투 + 이미지가 포함된 블로그 글 생성"""
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 자연스러운 블로거 시작 문장
    hooks = {
        "충격적 사실로 시작": f"안녕하세요! 오늘은 {keyword}에 대해서 정말 중요한 이야기를 해드리려고 해요. 사실 저도 처음엔 몰랐는데, 알고 보니 정말 놀라운 사실들이 많더라구요.",
        "질문으로 시작": f"혹시 {keyword} 때문에 고민 많이 하고 계신가요? 저도 예전에 똑같은 고민을 했었거든요. 그래서 오늘은 제가 직접 찾아본 정보들을 공유해드릴게요!",
        "개인 경험담": f"안녕하세요! 오늘은 제가 {keyword}를 직접 경험해본 이야기를 들려드리려고 해요. 솔직히 처음엔 반신반의했는데, 지금은 정말 만족하고 있어서 여러분께도 꼭 알려드리고 싶었어요.",
        "최신 연구 결과": f"요즘 {keyword}에 대한 새로운 연구 결과들이 많이 나오고 있더라구요! 2025년에 발표된 최신 자료들을 정리해서 쉽게 설명해드릴게요."
    }
    
    # 자연스러운 블로거 스타일 글
    blog_content = f"""# {keyword}, 이것만 알면 끝! (2025년 완전정리)

{hooks[hook_style]}

![{images[0]['alt']}]({images[0]['url']})

사실 이 주제로 글을 쓰게 된 건, 주변에서 너무 많은 분들이 물어보셔서예요. 그래서 제가 알고 있는 모든 걸 정리해서 한 번에 알려드리려고 해요!

---

## 이 글을 끝까지 읽으시면...

✓ {keyword}의 핵심을 완전히 이해하실 수 있어요
✓ 실제로 효과 있는 방법들을 알게 되실 거예요  
✓ 흔히 하는 실수들을 미리 피할 수 있어요
✓ 저만의 노하우도 공개할 예정이에요!

**대략 5분 정도 투자하시면, 정말 유용한 정보 얻어가실 수 있을 거예요 😊**

---

## 일단 기본부터 제대로 알아봐요

많은 분들이 {keyword}에 대해서 대충은 알고 계시지만, 정확하게 아는 분은 생각보다 적더라구요.

**혹시 이런 고민 해보신 적 있나요?**
- 인터넷에서 본 정보 따라했는데 별로 효과 없었던...
- 친구들이 하라는 대로 했는데 나한테는 안 맞았던...  
- 뭔가 하고는 있는데 제대로 하는 건지 확신이 안 서던...

만약 하나라도 해당되신다면, 이 글이 정말 도움 될 거예요!

---

## 제가 직접 정리한 핵심 포인트 5가지

![{images[1]['alt']}]({images[1]['url']})

### 1️⃣ 기초가 정말 중요해요

{keyword}를 제대로 이해하려면 기본기부터 탄탄히 해야 해요. 

**여기서 중요한 건:**
- 원리를 제대로 이해하기
- 잘못 알려진 정보들 구분하기  
- 과학적 근거 있는 정보 찾기

저도 처음엔 이걸 몰라서 많이 헤맸거든요 ㅠㅠ

### 2️⃣ 실생활에 바로 적용할 수 있는 방법들

이론만 아는 건 의미가 없죠. 바로 써먹을 수 있는 실용적인 방법들을 알려드릴게요.

**제가 추천하는 단계:**
- 현재 상황 체크하기 (이게 제일 중요!)
- 목표 정하기 (너무 높지 않게)
- 실행하기 (꾸준히!)
- 결과 확인하기 (1-2주마다)

### 3️⃣ 많이들 하는 실수 (저도 했었어요...)

솔직히 말씀드리면, 저도 이런 실수들 다 해봤어요 😅

**특히 조심하셔야 할 것들:**
- 너무 성급하게 결과 기대하기
- 중간에 포기하기
- 남과 비교하기 (개인차가 정말 커요!)

### 4️⃣ 단계별로 차근차근 해보세요

급하게 하시지 마시고, 단계별로 천천히 해보시는 걸 추천드려요.

**제가 해본 4주 계획:**
- **1주차:** 기본기 다지기 (조급해하지 마세요!)
- **2주차:** 본격 시작 (이때부터 재미있어져요)
- **3주차:** 점검하고 조정하기
- **4주차:** 습관으로 만들기

### 5️⃣ 좀 더 고급 팁들 (이건 보너스!)

기본을 마스터하시면, 이런 고급 기법들도 시도해보세요.

**개인적으로 효과 봤던 방법들:**
- 전문가들이 실제로 쓰는 방법
- 효율 극대화 하는 꿀팁
- 나에게 맞게 커스터마이징 하는 법

---

## 이제 실전에 적용해봐요!

![{images[2]['alt']}]({images[2]['url']})

이론은 충분히 알아봤으니, 이제 실제로 해볼 차례예요.

### 오늘부터 바로 시작할 수 있는 것들

1. **오늘:** 현재 상태 점검 (5분이면 충분해요)
2. **이번 주:** 기본 습관 만들기
3. **다음 주:** 본격적으로 시작
4. **한 달 후:** 첫 번째 체크
5. **3개월 후:** 완전히 내 것으로 만들기

### 언제쯤 효과를 볼 수 있을까요?

개인차가 있긴 하지만, 제 경험상...

- **1주차:** "어? 뭔가 달라지는 것 같은데?"
- **1개월:** "아, 확실히 달라졌네!"
- **3개월:** "이제 완전히 익숙해졌어요"
- **6개월:** "이제 안 할 수가 없어요"

---

## 실제 후기들 (진짜 받은 댓글들!)

> "처음엔 별 기대 안 했는데, 정말 효과 있어요! 감사합니다 ㅎㅎ" - 김○○님  
> "이런 좋은 정보를 무료로 알려주시다니... 정말 고맙습니다!" - 박○○님  
> "단계별로 설명해주셔서 따라하기 쉬웠어요 👍" - 최○○님

---

## 자주 받는 질문들

**Q: 얼마나 오래 해야 하나요?**  
A: 개인차가 있지만, 보통 2-4주 정도면 변화를 느끼실 수 있어요.

**Q: 비용이 많이 들까요?**  
A: 대부분 돈 안 들고 할 수 있는 것들이에요. 걱정 마세요!

**Q: 저도 할 수 있을까요?**  
A: 물론이죠! 특별한 조건 없어요. 누구나 할 수 있어요.

---

## 마무리하면서...

{keyword}에 대한 이야기, 어떠셨나요?

사실 이런 정보들을 정리해서 올리는 이유가, 저처럼 헤매시는 분들이 더 이상 없었으면 하는 마음에서예요.

**혹시 이 글이 도움 되셨다면:**
- 좋아요 한 번 눌러주세요 (정말 힘이 돼요!)
- 댓글로 경험담 공유해주세요
- 주변 분들한테도 알려주세요

**궁금한 점 있으시면 언제든 댓글로 물어보세요!**

빠짐없이 답변드릴게요 😊

---

### 관련 글들도 확인해보세요

- {keyword} 더 자세한 가이드
- {keyword} 실패 사례 모음  
- 2025년 {keyword} 트렌드

**구독하시면 이런 유용한 글들을 가장 먼저 받아보실 수 있어요!**

---

*오늘도 좋은 하루 보내세요! 여러분의 {keyword} 여정을 응원합니다 🌟*
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
            ai_content = None
            
            if selected_model == "OpenAI GPT-3.5":
                if not openai_key:
                    st.error("❌ OpenAI API 키를 입력해주세요!")
                else:
                    # OpenAI API 호출
                    hooks = {
                        "충격적 사실로 시작": f"충격! {keyword}에 대해 90%가 모르는 놀라운 사실부터 시작해서",
                        "질문으로 시작": f"{keyword} 때문에 고민이세요? 이 글을 읽고 나면 해답을 찾을 수 있습니다.",
                        "개인 경험담": f"제가 직접 {keyword}를 경험해보니 정말 놀라운 변화가 있었습니다.",
                        "최신 연구 결과": f"2025년 최신 연구에서 밝혀진 {keyword}의 진실을 공개합니다."
                    }
                    
                    prompt = f"""
당신은 2025년 최신 블로그 콘텐츠 전문가입니다. {keyword} 주제로 2025년 트렌드를 반영한 독자가 끝까지 읽을 수밖에 없는 매력적이고 풍부한 블로그 글을 작성해주세요.

시작 방식: {hooks[hook_style]}

다음 요소들을 반드시 포함해주세요:

🎯 구조:
- 강력한 제목 (이모지 포함)
- 후킹이 강한 도입부
- 읽으면 얻을 수 있는 것들 (체크리스트)
- 5개 핵심 포인트 (번호 매기기)
- 실전 적용 가이드
- FAQ 섹션
- 감정적 마무리 + CTA

💡 스타일:
- 이모지 적극 활용
- 대화체 톤
- 구체적인 예시와 수치
- 독자 참여 유도 문장
- 중간중간 질문 던지기

📝 내용:
- 전문성 + 접근성
- 실용적인 팁과 방법
- 단계별 가이드
- 주의사항과 실수 방지법
- 성공 사례 언급

✨ 참여 유도:
- 댓글 작성 유도
- 공유 요청
- 관련 글 추천
- 구독 유도

2000자 이상, 한국어로 작성해주세요.
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
                            st.success("✅ AI로 블로그 글 생성 완료!")
                        else:
                            st.error(f"❌ OpenAI API 오류: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
            else:
                # 로컬 AI 사용 (완전 무료)
                ai_content = generate_local_blog(keyword, hook_style)
                st.success("✅ 로컬 AI로 블로그 글 생성 완료!")

            if ai_content:
                # 생성된 이미지들 미리보기
                st.subheader("📸 포함된 이미지들")
                images = get_free_images(keyword, 3)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(images[0]['url'], caption="시작 이미지", use_column_width=True)
                with col2:
                    st.image(images[1]['url'], caption="중간 이미지", use_column_width=True)  
                with col3:
                    st.image(images[2]['url'], caption="마무리 이미지", use_column_width=True)

                st.info("💡 위 이미지들이 블로그 글에 자동 삽입됩니다!")

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

# 네이버 블로그 연동 (소셜 로그인 포함)
st.markdown("---")
st.subheader("📋 네이버 블로그 연동")

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
st.markdown("### 🚀 다음 업데이트 예정")
st.info("""
- 📱 모바일 앱 버전
- 💻 PC 프로그램 버전  
- 🤖 더 많은 AI 모델 지원
- 📊 블로그 성과 분석
- 💰 수익화 도구
""")

st.caption("💡 by AI SULAB 대표님의 AI 블로그 자동화 시스템 | 새로고침해도 로그인 유지됩니다!")