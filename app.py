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
    layout="wide"
)

# 로그인 정보
VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 세션 상태 초기화
if 'login_ok' not in st.session_state:
    st.session_state['login_ok'] = False

# 로그인 체크
if not st.session_state.get('login_ok', False):
    st.title("🚀 AI 블로그 자동화 Pro")
    st.markdown("### 진수 대표님 전용 시스템")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_id = st.text_input("아이디", value="aisulab")
        user_pw = st.text_input("비밀번호", value="!js44358574", type="password")
        
        if st.button("🔑 로그인", use_container_width=True):
            if user_id == VALID_ID and user_pw == VALID_PW:
                st.session_state['login_ok'] = True
                st.success("✅ 로그인 성공!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 아이디/비밀번호가 틀렸습니다.")
    st.stop()

# 메인 화면
st.title("🚀 AI 블로그 자동화 Pro")
st.markdown("### 💰 수익화 최적화 + 📈 SEO 자동화 + 🔄 자동 게시")

# 로그아웃 버튼
if st.button("🚪 로그아웃"):
    st.session_state['login_ok'] = False
    st.rerun()

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