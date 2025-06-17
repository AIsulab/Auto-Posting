import streamlit as st
import requests
import json
import time
import random
import urllib.parse

# 페이지 설정 (맨 처음에)
st.set_page_config(
    page_title="AI 블로그 자동화 Pro", 
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS로 UI/UX 최적화
st.markdown("""
<style>
    /* 전체 앱 스타일링 */
    .main > div {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .main > div {
            padding: 1rem 0.5rem;
        }
    }
    
    /* 제목 스타일링 */
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    /* 로그인 폼 스타일링 */
    .login-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
        margin: 2rem auto;
        max-width: 400px;
    }
    
    /* 버튼 스타일링 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* 입력 필드 스타일링 */
    .stTextInput > div > div > input {
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 성공/에러 메시지 스타일링 */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* 카드 스타일 */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f5;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* 헤더 고정 */
    .main-header {
        position: sticky;
        top: 0;
        background: white;
        z-index: 999;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e1e5e9;
    }
    
    /* 모바일 최적화 */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        .login-container {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.8rem 1.5rem;
            font-size: 16px;
        }
    }
    
    /* 로딩 애니메이션 */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 그라데이션 배경 */
    .gradient-bg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* 통계 카드 */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    /* 호버 효과 */
    .hover-effect {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hover-effect:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# 로그인 정보
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

# 로그인 체크
if not st.session_state.get('login_ok', False):
    
    # 헤더 (박스 없이)
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀 AI 블로그 자동화 Pro</h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0;">진수 대표님 전용 시스템</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 로그인 폼 (박스 없이, 깔끔하게)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("#### 🔑 로그인")
        
        user_id = st.text_input("아이디", value="aisulab", label_visibility="collapsed", placeholder="아이디를 입력하세요")
        user_pw = st.text_input("비밀번호", value="!js44358574", type="password", label_visibility="collapsed", placeholder="비밀번호를 입력하세요")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔑 로그인", use_container_width=True, key="login_btn"):
            if user_id == VALID_ID and user_pw == VALID_PW:
                st.session_state['login_ok'] = True
                st.success("✅ 로그인 성공!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    
    st.stop()

# 메인 화면 헤더 (고정)
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 2rem;">🚀 AI 블로그 자동화 Pro</h1>
            <p style="margin: 0; color: #666;">💰 수익화 최적화 + 📈 SEO 자동화 + 🔄 자동 게시</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 로그아웃 버튼 (우상단)
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("🚪 로그아웃", key="logout_btn"):
        st.session_state['login_ok'] = False
        st.rerun()

# 상태 표시 (카드 형태) - 기존 코드 아래에 추가

# 주요 기능 소개 섹션
st.markdown("<br>", unsafe_allow_html=True)

# 기능 소개 헤더
st.markdown("""
<div style="text-align: center; margin: 3rem 0 2rem 0;">
    <h2 style="color: #333;">🚀 주요 기능</h2>
    <p style="color: #666; font-size: 1.1rem;">AI 블로그 자동화 Pro의 강력한 기능들을 확인해보세요</p>
</div>
""", unsafe_allow_html=True)

# 기능 카드들 (3열)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card hover-effect">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h4 style="color: #667eea; margin-bottom: 1rem;">AI 글 생성</h4>
            <p style="color: #666; line-height: 1.6;">
                • 7개 카테고리 전문 글<br>
                • 키워드별 맞춤 내용<br>
                • SEO 최적화 자동 적용<br>
                • 이미지 자동 삽입
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card hover-effect">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
            <h4 style="color: #28a745; margin-bottom: 1rem;">수익화 최적화</h4>
            <p style="color: #666; line-height: 1.6;">
                • Google Ads 자동 삽입<br>
                • 구독 CTA 버튼 생성<br>
                • 체류시간 증가 최적화<br>
                • 상품 추천 섹션
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card hover-effect">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📤</div>
            <h4 style="color: #dc3545; margin-bottom: 1rem;">자동 게시</h4>
            <p style="color: #666; line-height: 1.6;">
                • 워드프레스 자동 업로드<br>
                • 네이버 블로그 연동<br>
                • 예약 게시 기능<br>
                • 다중 플랫폼 지원
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 통계 섹션
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h3 style="color: #333;">📊 실시간 통계</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h2 style="margin: 0; font-size: 2.5rem;">8,000+</h2>
        <p style="margin: 0.5rem 0 0 0;">가능한 글 조합</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h2 style="margin: 0; font-size: 2.5rem;">7</h2>
        <p style="margin: 0.5rem 0 0 0;">전문 카테고리</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h2 style="margin: 0; font-size: 2.5rem;">100%</h2>
        <p style="margin: 0.5rem 0 0 0;">자동화 시스템</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h2 style="margin: 0; font-size: 2.5rem;">24/7</h2>
        <p style="margin: 0.5rem 0 0 0;">무제한 이용</p>
    </div>
    """, unsafe_allow_html=True)

# 시작하기 버튼
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 블로그 생성 시작하기", use_container_width=True, key="start_btn"):
        st.balloons()
        st.success("🎉 곧 블로그 생성 기능이 추가됩니다!")

# 푸터
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; background-color: #f8f9fa; border-radius: 15px;">
    <p style="color: #666; margin: 0;">
        🏆 by AI SULAB | 진수 대표님 전용 시스템 | 새로고침해도 로그인 유지 ⭐
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 핵심 함수들 정의
# =============================================================================

def get_current_season():
    """현재 계절 반환"""
    month = time.localtime().tm_mon
    if 3 <= month <= 5:
        return "봄"
    elif 6 <= month <= 8:
        return "여름"
    elif 9 <= month <= 11:
        return "가을"
    else:
        return "겨울"

def get_free_images(keyword, count=3):
    """키워드별 랜덤 이미지 생성"""
    
    # 키워드별 이미지 풀
    image_pools = {
        "AI": ["tech", "computer", "robot", "future", "digital"],
        "건강": ["health", "fitness", "medical", "wellness", "nature"],
        "투자": ["money", "business", "finance", "chart", "success"],
        "여행": ["travel", "landscape", "city", "beach", "mountain"],
        "요리": ["food", "cooking", "kitchen", "restaurant", "meal"]
    }
    
    # 키워드 매칭
    image_category = "tech"  # 기본값
    for key in image_pools:
        if key in keyword:
            image_category = random.choice(image_pools[key])
            break
    
    # 이미지 URL 생성
    images = []
    for i in range(count):
        width = random.randint(600, 800)
        height = random.randint(400, 500)
        
        images.append({
            "url": f"https://picsum.photos/{width}/{height}?random={random.randint(1, 10000)}",
            "alt": f"{keyword} 관련 {['시작', '중간', '마무리'][i]} 이미지"
        })
    
    return images

def detect_keyword_category(keyword):
    """키워드 카테고리 자동 감지"""
    
    categories = {
        "AI/기술": ["AI", "인공지능", "챗GPT", "로봇", "자동화", "프로그래밍", "코딩"],
        "건강": ["건강", "다이어트", "운동", "의료", "병원", "약", "치료", "영양"],
        "재테크": ["투자", "주식", "부동산", "재테크", "돈", "수익", "펀드", "적금"],
        "여행": ["여행", "관광", "휴가", "해외", "국내", "맛집", "호텔", "항공"],
        "라이프스타일": ["요리", "패션", "뷰티", "인테리어", "취미", "문화", "예술"]
    }
    
    for category, keywords in categories.items():
        if any(k in keyword for k in keywords):
            return category
    
    return "라이프스타일"  # 기본 카테고리

def generate_seo_metadata(keyword, title):
    """SEO 메타데이터 자동 생성"""
    
    description = f"{keyword}에 대한 완벽한 가이드입니다. 실제 경험과 전문가 조언을 바탕으로 한 실용적인 정보를 제공합니다."
    
    keywords_list = [
        keyword,
        f"{keyword} 방법",
        f"{keyword} 가이드", 
        f"{keyword} 팁",
        f"{keyword} 후기",
        "실제 경험",
        "전문가 조언"
    ]
    
    return {
        "title": title,
        "description": description,
        "keywords": ", ".join(keywords_list),
        "author": "AI SULAB",
        "og_title": title,
        "og_description": description
    }

def insert_ads_and_cta(content, keyword):
    """광고 및 CTA 자동 삽입"""
    
    # Google Ads 코드 (예시)
    google_ads = """
<!-- Google Ads -->
<div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
    <p style="font-size: 12px; color: #666;">광고</p>
    <div id="google-ads-placeholder" style="min-height: 280px; background: #e9ecef; display: flex; align-items: center; justify-content: center;">
        <span style="color: #666;">Google Ads 영역</span>
    </div>
</div>
"""
    
    # 구독 CTA
    subscribe_cta = f"""
<!-- 구독 CTA -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; margin: 40px 0; color: white;">
    <h3 style="color: white; margin-bottom: 15px;">🎯 {keyword} 최신 정보를 놓치지 마세요!</h3>
    <p style="margin-bottom: 20px; opacity: 0.9;">매주 업데이트되는 전문가 팁과 실전 노하우를 이메일로 받아보세요</p>
    <button style="background: #ff6b6b; border: none; padding: 15px 30px; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; font-size: 16px;">
        📧 무료 뉴스레터 구독하기
    </button>
    <p style="font-size: 12px; margin-top: 10px; opacity: 0.7;">언제든 구독 해지 가능 | 스팸 메일 없음</p>
</div>
"""
    
    # 관련 상품 추천
    product_cta = f"""
<!-- 상품 추천 CTA -->
<div style="border: 2px solid #28a745; padding: 25px; border-radius: 10px; margin: 30px 0;">
    <h4 style="color: #28a745; margin-bottom: 15px;">💡 {keyword} 관련 추천 상품</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <strong>🔥 베스트셀러</strong><br>
            <span style="color: #666;">전문가가 추천하는 필수 아이템</span>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <strong>⭐ 신제품</strong><br>
            <span style="color: #666;">최신 트렌드 반영 상품</span>
        </div>
    </div>
    <div style="text-align: center; margin-top: 15px;">
        <button style="background: #28a745; border: none; padding: 12px 25px; border-radius: 20px; color: white; font-weight: bold;">
            🛒 추천 상품 보기
        </button>
    </div>
</div>
"""
    
    # 컨텐츠 중간중간에 삽입
    sections = content.split('\n\n')
    
    # 전체 섹션 수에 따라 삽입 위치 결정
    total_sections = len(sections)
    
    if total_sections > 6:
        # 첫 번째 광고: 30% 지점
        insert_pos1 = int(total_sections * 0.3)
        sections.insert(insert_pos1, google_ads)
        
        # 구독 CTA: 60% 지점  
        insert_pos2 = int(total_sections * 0.6) + 1
        sections.insert(insert_pos2, subscribe_cta)
        
        # 상품 추천: 마지막에서 두 번째
        sections.insert(-1, product_cta)
    
    return '\n\n'.join(sections)

# =============================================================================

st.success("✅ 기본 시스템 로딩 완료!")
st.info("💡 다음 단계: 블로그 생성 엔진 추가 예정")