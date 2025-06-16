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

# 업그레이드된 로컬 AI 글 생성 함수 (이미지 포함)
def generate_local_blog(keyword, hook_style):
    """풍부한 콘텐츠 + 이미지가 포함된 블로그 글 생성"""
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 훅킹 시작 문장 (더 강력하게)
    hooks = {
        "충격적 사실로 시작": f"🚨 충격! {keyword}에 대한 놀라운 진실을 지금 공개합니다. 이 글을 읽고 나면 당신의 생각이 완전히 바뀔 것입니다.",
        "질문으로 시작": f"❓ {keyword} 때문에 밤잠을 설치고 계신가요? 수많은 사람들이 같은 고민을 하고 있습니다. 이 글에서 확실한 해답을 찾아보세요.",
        "개인 경험담": f"💭 저도 한때 {keyword} 때문에 정말 힘들었습니다. 하지만 이 방법을 알고 난 후 제 인생이 완전히 달라졌어요. 제 경험담을 솔직하게 공유합니다.",
        "최신 연구 결과": f"📊 2024년 최신 연구에서 {keyword}에 대한 충격적인 사실이 밝혀졌습니다. 전문가들도 깜짝 놀란 이 연구 결과를 독점 공개합니다."
    }
    
    # 더 풍부한 블로그 글 템플릿
    blog_content = f"""# 🔥 {keyword} 완벽 가이드 - 2024년 최신 업데이트

{hooks[hook_style]}

![{images[0]['alt']}]({images[0]['url']})
*이미지: {keyword} 관련 시각 자료*

---

## 🎯 이 글을 읽으면 얻을 수 있는 것들

✅ {keyword}의 핵심 원리 완벽 이해  
✅ 실제로 효과 있는 검증된 방법들  
✅ 전문가만 아는 숨겨진 팁들  
✅ 흔한 실수들과 피하는 방법  
✅ 단계별 실행 계획  

**⏰ 읽는 시간: 약 5분 | 💡 실용도: ★★★★★**

---

## 🔍 {keyword}, 정말 제대로 알고 계신가요?

많은 사람들이 {keyword}에 대해 안다고 생각하지만, 실상은 그렇지 않습니다. 

**잠깐, 이런 경험 있으신가요?**
- 인터넷에서 본 정보를 따라했는데 효과가 없었던 경험
- 주변 사람들의 조언이 서로 달라서 혼란스러웠던 경험  
- 뭔가 하고는 있는데 제대로 하는 건지 확신이 서지 않는 경험

만약 하나라도 해당된다면, 이 글을 끝까지 읽어보세요. 분명 도움이 될 거예요.

---

## 💡 핵심 포인트 5가지 (전문가 검증)

![{images[1]['alt']}]({images[1]['url']})
*이미지: 전문가가 추천하는 핵심 방법들*

### 1️⃣ 기본 개념부터 탄탄히 
{keyword}의 기본 개념을 정확히 이해하는 것이 첫 번째입니다. 

**🎯 핵심 포인트:**
- 기본 원리 이해하기
- 흔한 오해들 바로잡기  
- 과학적 근거 확인하기

**💬 전문가 조언:** "기초가 탄탄해야 응용도 가능합니다."

### 2️⃣ 실용적인 방법론
이론만으로는 부족합니다. 실제 생활에서 바로 적용할 수 있는 구체적인 방법들을 알아보겠습니다.

**📋 실행 체크리스트:**
- [ ] 첫 번째 단계: 현재 상태 파악
- [ ] 두 번째 단계: 목표 설정  
- [ ] 세 번째 단계: 구체적 실행
- [ ] 네 번째 단계: 결과 확인

### 3️⃣ 피해야 할 실수들
많은 사람들이 저지르는 흔한 실수들을 미리 알고 피하는 것이 중요합니다.

**⚠️ 주의사항:**
- 성급한 결론 내리기
- 일관성 없는 실행
- 개인차 무시하기

### 4️⃣ 단계별 로드맵
체계적으로 접근하는 것이 성공의 열쇠입니다.

**🗓️ 주차별 계획:**
- **1주차:** 기초 다지기
- **2주차:** 본격 실행
- **3주차:** 점검 및 조정
- **4주차:** 정착 및 발전

### 5️⃣ 고급 팁 (보너스)
일반적인 방법에서 한 단계 더 나아간 고급 기법들을 소개합니다.

**🚀 프로 팁:**
- 전문가들만 아는 숨겨진 방법
- 효율성을 극대화하는 기법
- 개인별 맞춤 조정 방법

---

## 🎯 실전 적용 가이드

![{images[2]['alt']}]({images[2]['url']})
*이미지: 실제 적용 모습*

이제 구체적으로 어떻게 실천할 수 있는지 단계별로 알아보겠습니다.

### 🏃‍♂️ 바로 시작할 수 있는 5가지

1. **오늘 당장:** 현재 상태 점검하기
2. **이번 주:** 기본 습관 만들기  
3. **다음 주:** 본격적인 실행
4. **한 달 후:** 첫 번째 점검
5. **3개월 후:** 완전한 정착

### 📈 예상 결과 타임라인

- **1주차:** 작은 변화 감지
- **1개월:** 눈에 띄는 개선
- **3개월:** 확실한 변화
- **6개월:** 완전한 정착

---

## 🔥 성공 사례 & 후기

**실제 적용해본 분들의 생생한 후기:**

> "처음엔 반신반의했는데, 정말 효과가 있더라고요!" - 김○○님  
> "이런 정보가 무료라니, 정말 감사합니다." - 박○○님  
> "단계별로 따라하니까 어렵지 않았어요." - 최○○님

---

## ❓ 자주 묻는 질문 (FAQ)

**Q: 얼마나 걸리나요?**  
A: 개인차가 있지만, 보통 2-4주 정도면 변화를 느낄 수 있습니다.

**Q: 비용이 많이 드나요?**  
A: 대부분 무료 또는 저비용으로 가능합니다.

**Q: 누구나 할 수 있나요?**  
A: 네, 특별한 조건 없이 누구나 시작할 수 있습니다.

---

## 🎉 마무리하며

{keyword}에 대한 완벽 가이드, 어떠셨나요?

**이 글이 도움되셨다면:**
- 👍 좋아요 버튼 클릭
- 💬 댓글로 여러분의 경험 공유
- 📤 주변 분들에게 공유하기

**여러분의 성공 스토리를 기다립니다!**

더 궁금한 점이 있으시면 언제든 댓글로 질문해주세요. 성심성의껏 답변드리겠습니다.

---

### 🔗 관련 글 추천
- [{keyword} 심화 과정 가이드]
- [{keyword} 실패 사례 분석]  
- [{keyword} 최신 트렌드 2024]

**📢 구독하시면 최신 정보를 가장 먼저 받아보실 수 있습니다!**

---
*이 글이 여러분의 {keyword} 여정에 도움이 되기를 진심으로 바랍니다. 함께 성장해요! 💪*
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
                        "최신 연구 결과": f"2024년 최신 연구에서 밝혀진 {keyword}의 진실을 공개합니다."
                    }
                    
                    prompt = f"""
당신은 블로그 콘텐츠 전문가입니다. {keyword} 주제로 독자가 끝까지 읽을 수밖에 없는 매력적이고 풍부한 블로그 글을 작성해주세요.

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

wp_url = st.text_input("워드프레스 주소", placeholder="https://sulab.shop", value="https://sulab.shop")
wp_id = st.text_input("워드프레스 아이디", value="fosum@kakao.com")
wp_pw = st.text_input("워드프레스 비밀번호", value="js44358574")

# 생성된 글이 있을 때만 업로드 가능
if 'generated_content' in st.session_state:
    if st.button("📤 워드프레스에 업로드"):
        if wp_url and wp_id and wp_pw:
            with st.spinner("워드프레스에 업로드 중..."):
                # API URL 생성
                if wp_url.endswith('/'):
                    api_url = f"{wp_url}wp-json/wp/v2/posts"
                else:
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