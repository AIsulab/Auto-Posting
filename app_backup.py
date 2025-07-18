import streamlit as st
import requests
import json
import time
import random
import urllib.parse
import webbrowser

# Streamlit 페이지 설정
st.set_page_config(
    page_title="AI 블로그 자동화",
    page_icon="📝",
    layout="wide"
)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = "로컬 AI (무료)"
if 'openai_key' not in st.session_state:
    st.session_state['openai_key'] = ""

# 전문가별 인사말과 전문성 표현
greetings = {
    "건강_의사": "안녕하세요, 가정의학과 전문의입니다.",
    "운동_트레이너": "안녕하세요, 현직 퍼스널 트레이너입니다.",
    "요리_셰프": "안녕하세요, 건강식 전문 요리사입니다.",
    "공부_교사": "안녕하세요, 진로상담 전문 교사입니다.",
    "직장_멘토": "안녕하세요, 커리어 코치입니다."
}

expertise = {
    "건강_의사": "의학적 근거를 바탕으로",
    "운동_트레이너": "과학적인 운동 원리를 기반으로",
    "요리_셰프": "전문 요리사의 노하우로",
    "공부_교사": "교육 전문가의 관점에서",
    "직장_멘토": "풍부한 실무 경험을 바탕으로"
}

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

def generate_ai_blog(keyword, current_season):
    """AI/기술 전용 블로그 생성 - 훅킹과 체류시간 최적화"""
    
    # AI 전용 훅킹 제목들
    ai_titles = [
        f"{keyword} 완전 정복! 초보자도 3일만에 마스터하는 비법",
        f"🚀 {keyword} 실무 활용법 - 월급쟁이가 부업으로 월 300만원 벌기",
        f"⚡ {keyword} 무료 도구 10개 - 유료 못지않은 숨겨진 보석들",
        f"💡 {keyword} 트렌드 2025 - 놓치면 후회할 핵심 정보",
        f"🔥 {keyword} 자동화로 업무시간 70% 단축한 실제 후기"
    ]
    
    # AI 전용 훅킹 시작 문장들
    ai_hooks = [
        f"지난주에 {keyword}로 하루 만에 업무를 끝내고 일찍 퇴근했습니다.",
        f"{keyword} 때문에 제 인생이 바뀌었다고 해도 과언이 아니에요.",
        f"동료들이 야근할 때 저는 {keyword}로 10분 만에 끝내고 있었어요.",
        f"처음엔 {keyword}가 어려워 보였는데, 지금은 없으면 안 되는 필수템이 됐어요."
    ]
    
    # 랜덤 선택
    title = random.choice(ai_titles)
    hook = random.choice(ai_hooks)
    
       # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # AI 전용 블로그 내용
    blog_content = f"""# {title}

{hook}

오늘은 제가 실제로 사용해보고 효과를 본 {keyword} 활용법을 공유해드릴게요.

<img src="{images[0]['url']}" alt="{images[0]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px;">

## 🤔 왜 {keyword}를 시작하게 되었나요?

솔직히 처음엔 저도 반신반의했어요. "AI가 정말 내 일을 도와줄 수 있을까?" 하면서요.

그런데 직접 써보니 완전히 다른 세상이더라고요. 특히 요즘처럼 {keyword} 기술이 빠르게 발전하는 시대에는 이걸 모르면 정말 뒤처지게 돼요.

**이 글을 끝까지 읽으면:**
- ✅ {keyword} 핵심 기능 3가지 완벽 이해
- ✅ 실무에서 바로 써먹을 수 있는 템플릿 제공
- ✅ 초보자 실수 방지 체크리스트
- ✅ 무료 vs 유료 도구 비교분석

---

## 💡 {keyword} 핵심 활용법 3가지

<img src="{images[1]['url']}" alt="{images[1]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

### 1️⃣ 업무 자동화 (가장 중요!)

제가 가장 많이 사용하는 방법이에요. 

**실제 사례:** 매주 보고서 작성하는 데 3시간 걸렸는데, {keyword} 활용 후 30분으로 단축!

**구체적인 방법:**
- 📝 템플릿 미리 설정하기
- 🔄 반복 작업 자동화하기  
- 📊 데이터 분석 자동화하기

### 2️⃣ 창작 도우미 활용

이건 정말 게임체인저였어요.

**놀라운 결과:** 
- 블로그 글쓰기 시간 80% 단축
- 아이디어 고갈 문제 완전 해결
- 퀄리티는 오히려 더 좋아짐

### 3️⃣ 학습 가속화

{keyword}로 공부하면 이해도가 완전히 달라져요.

**실제 경험:**
- 어려운 개념도 쉽게 설명해줌
- 맞춤형 학습 계획 제공
- 실시간 질문 답변 가능

---

## 🚨 초보자가 자주 하는 실수 TOP 3

### ❌ 실수 1: 너무 복잡하게 시작하기

처음부터 고급 기능 쓰려다 포기하는 경우가 많아요.

**해결책:** 기본 기능부터 차근차근!

### ❌ 실수 2: 프롬프트 대충 작성하기

"대충 써도 알아서 해주겠지" → 이게 가장 큰 실수예요.

**해결책:** 구체적이고 명확한 지시사항 작성

### ❌ 실수 3: 결과를 그대로 사용하기

{keyword} 결과물은 반드시 검토하고 수정해야 해요.

**해결책:** 80% 활용 + 20% 인간의 터치

---

## 🔥 무료 도구 vs 유료 도구 솔직 비교

### 무료 도구의 장점:
- ✅ 부담 없이 시작 가능
- ✅ 기본 기능은 충분히 강력
- ✅ 학습용으로 최적

### 유료 도구의 장점:
- ✅ 무제한 사용량
- ✅ 고급 기능 제공
- ✅ 우선순위 처리

**제 추천:** 무료로 시작해서 필요에 따라 유료 전환!

---

## 🎯 실전 활용 템플릿 (복사해서 바로 사용!)

이 템플릿만 기억해도 80% 성공이에요!

---

## 🤝 마무리하며...

<img src="{images[2]['url']}" alt="{images[2]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

{keyword}는 이제 선택이 아닌 필수가 되었어요. 

특히 요즘처럼 업무 효율성이 중요한 시대에는 이런 도구 없이는 정말 경쟁력이 떨어지죠.

**마지막 팁:**
- 🔥 매일 조금씩이라도 써보세요
- 💡 실패를 두려워하지 마세요  
- 🚀 꾸준함이 가장 중요해요

**궁금한 점이나 성공 사례가 있으시면 댓글로 공유해주세요!** 

다른 분들에게도 큰 도움이 될 거예요. 😊

---

**🔗 관련 글 더 보기:**
- [{keyword} 고급 활용법]
- [업무 자동화 완전 가이드]
- [{current_season}철 생산성 향상 팁]

*이 글이 도움되셨다면 ❤️ 공감과 공유 부탁드려요!*
"""

def generate_health_blog(keyword, current_season):
    """건강 전용 블로그 생성 - 의료진 관점으로 신뢰도 높이기"""
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 건강 전용 훅킹 제목들
    health_titles = [
        f"{keyword} 의사가 알려주는 진짜 효과적인 방법 (임상 경험 15년)",
        f"🏥 {keyword} 오해와 진실 - 병원에서 말해주지 않는 이야기",
        f"⚕️ {keyword} 자가진단부터 관리까지 완벽 가이드",
        f"💊 {keyword} 약 없이도 가능한 자연치유법 (의학적 근거 포함)",
        f"🔬 {keyword} 최신 연구결과 - 2025년 업데이트된 정보"
    ]
    
    # 건강 전용 훅킹 시작 문장들
    health_hooks = [
        f"15년간 {keyword} 환자들을 진료하면서 가장 많이 받은 질문에 답해드릴게요.",
        f"병원에서 {keyword} 때문에 오신 분들께 항상 설명드리는 내용을 공유합니다.",
        f"제 가족도 {keyword}로 고생했기에, 더욱 신중하게 연구한 방법들입니다.",
        f"{keyword}에 대한 잘못된 정보가 너무 많아서, 의학적 근거를 바탕으로 정리했어요."
    ]
    
    # 랜덤 선택
    title = random.choice(health_titles)
    hook = random.choice(health_hooks)
    
    # 건강 전용 블로그 내용
    blog_content = f"""# {title}

{hook}

{current_season}철에는 특히 {keyword} 관련 문의가 많아지는데, 정확한 정보를 알려드리고 싶어서 이 글을 작성합니다.

<img src="{images[0]['url']}" alt="{images[0]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

## 🏥 {keyword}에 대한 오해부터 바로잡겠습니다

**가장 흔한 오해:** "{keyword}는 나이 들면 당연한 거야"

이건 완전히 잘못된 생각이에요. 나이와 상관없이 충분히 예방하고 관리할 수 있습니다.

**이 글에서 얻어가실 정보:**
- ✅ {keyword}의 진짜 원인 (의학적 근거)
- ✅ 집에서 할 수 있는 자가진단법
- ✅ 병원 가기 전 체크리스트
- ✅ 약물 없이도 가능한 자연 관리법
- ✅ 언제 전문의를 찾아야 하는지

---

## 🔬 {keyword}의 진짜 원인 (최신 연구 기반)

<img src="{images[1]['url']}" alt="{images[1]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

### 1️⃣ 주요 원인 3가지

**원인 1: 생활습관 요인 (70%)**
- 불규칙한 식사 패턴
- 수면 부족 (7시간 미만)
- 만성 스트레스

**원인 2: 환경적 요인 (20%)**
- {current_season}철 기후 변화
- 실내 공기질 문제
- 화학물질 노출

**원인 3: 유전적 요인 (10%)**
- 가족력이 있어도 관리 가능
- 조기 발견이 핵심

### 2️⃣ {current_season}철 특별 주의사항

**왜 {current_season}에 {keyword}가 악화될까요?**
- 기온 변화로 인한 혈관 수축
- 활동량 감소
- 면역력 저하

**{current_season}철 맞춤 관리법:**
- 🌡️ 실내 온도 22-24도 유지
- 💧 하루 물 8잔 이상 섭취
- 🏃‍♂️ 실내 운동 30분 이상

---

## 🏠 집에서 할 수 있는 자가진단법

### 체크리스트 (3개 이상이면 전문의 상담 권장)

- □ 아침에 일어날 때 {keyword} 증상이 심하다
- □ 계단 오를 때 평소보다 힘들다
- □ 식사 후 {keyword} 관련 불편함이 있다
- □ 스트레스받을 때 증상이 악화된다
- □ 가족 중에 {keyword} 병력이 있다

### 간단한 자가 테스트

**1분 테스트 방법:**
1. 편안한 자세로 앉기
2. 깊게 숨쉬기 3회
3. 증상 정도 1-10점으로 평가
4. 일주일간 기록하기

---

## 💊 약물 없이 가능한 자연 관리법

### 1️⃣ 식이요법 (가장 중요!)

**추천 음식:**
- 🥬 녹색 채소 (시금치, 브로콜리)
- 🐟 오메가3 풍부한 생선
- 🥜 견과류 (하루 한 줌)
- 🍓 항산화 과일 (베리류)

**피해야 할 음식:**
- ❌ 가공식품
- ❌ 과도한 염분
- ❌ 트랜스지방
- ❌ 과당 음료

### 2️⃣ 생활습관 개선

**수면 관리:**
- 밤 11시 이전 취침
- 7-8시간 숙면
- 카페인 오후 2시 이후 금지

**스트레스 관리:**
- 명상 또는 요가 (하루 10분)
- 취미 활동 시간 확보
- 충분한 휴식

### 3️⃣ 운동 처방

**{keyword}에 좋은 운동:**
- 🚶‍♂️ 걷기 (하루 30분)
- 🏊‍♂️ 수영 (주 2-3회)
- 🧘‍♀️ 요가 (주 2회)

**주의사항:**
- 무리한 운동 금지
- 점진적 강도 증가
- 운동 전후 스트레칭 필수

---

## 🚨 언제 병원에 가야 할까요?

### 즉시 병원 방문이 필요한 경우

- 🔴 갑작스러운 심한 증상
- 🔴 호흡곤란 동반
- 🔴 의식 저하
- 🔴 극심한 통증

### 정기 검진이 필요한 경우

- 🟡 가족력이 있는 경우
- 🟡 40세 이상
- 🟡 만성질환 보유자
- 🟡 생활습관 개선 후에도 증상 지속

---

## 🤝 마무리하며...

<img src="{images[2]['url']}" alt="{images[2]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

{keyword} 관리는 하루아침에 되는 것이 아닙니다. 

하지만 올바른 정보와 꾸준한 실천으로 충분히 개선할 수 있어요.

**핵심 포인트 정리:**
- 🎯 원인을 정확히 파악하기
- 💪 생활습관 개선이 가장 중요
- 🏥 정기 검진으로 조기 발견
- 😊 스트레스 관리도 필수

**여러분의 건강한 변화를 응원합니다!** 

궁금한 점이나 경험담이 있으시면 댓글로 공유해주세요. 다른 분들에게도 큰 도움이 될 거예요.

---

**🔗 관련 글 더 보기:**
- [{keyword} 예방법 완전 가이드]
- [{current_season}철 건강 관리법]
- [자연치유 vs 약물치료 비교]

*이 글이 도움되셨다면 ❤️ 공감과 공유 부탁드려요!*
"""

def generate_finance_blog(keyword, current_season):
    """재테크 전용 블로그 생성 - 실전 경험과 수익 인증으로 신뢰도 확보"""
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 재테크 전용 훅킹 제목들
    finance_titles = [
        f"{keyword} 초보자도 월 50만원 수익! 3개월 실전 후기",
        f"💰 {keyword} 실패담 공개 - 300만원 날린 후 찾은 진짜 방법",
        f"📈 {keyword} 고수가 알려주는 숨겨진 수익 포인트 7가지",
        f"🔥 {keyword} 2025년 전망 - 지금 시작해야 하는 이유",
        f"⚡ {keyword} 자동 수익 시스템 구축법 (직장인 부업 추천)"
    ]
    
    # 재테크 전용 훅킹 시작 문장들
    finance_hooks = [
        f"작년 이맘때 {keyword}를 시작해서 지금까지 누적 수익이 1,200만원을 넘었습니다.",
        f"{keyword}로 실패만 3번 하고 나서야 깨달은 진짜 핵심을 공유해드릴게요.",
        f"직장 다니면서 {keyword}로 부업 수익 월 평균 80만원을 만들고 있어요.",
        f"처음엔 {keyword}가 어려워 보였는데, 지금은 없어서는 안 될 수익원이 됐어요."
    ]
    
    # 랜덤 선택
    title = random.choice(finance_titles)
    hook = random.choice(finance_hooks)
    
    # 수익 관련 랜덤 수치
    monthly_profit = random.randint(30, 150)
    success_rate = random.randint(75, 92)
    period_months = random.randint(3, 12)
    
    # 재테크 전용 블로그 내용
    blog_content = f"""# {title}

{hook}

솔직하게 수익 인증과 함께 제가 실제로 해본 {keyword} 경험을 공유해드릴게요.

<img src="{images[0]['url']}" alt="{images[0]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

## 💰 실제 수익 현황 공개 (스크린샷 첨부)

**지난 {period_months}개월 누적 수익:**
- 📊 총 수익: {monthly_profit * period_months:,}만원
- 📈 월 평균: {monthly_profit}만원
- 🎯 성공률: {success_rate}%
- 💪 재투자 비율: 60%

**이 글에서 얻어가실 것들:**
- ✅ {keyword} 시작하는 구체적인 방법
- ✅ 초보자 실수 방지 체크리스트  
- ✅ 월 50만원 수익 달성 로드맵
- ✅ 리스크 관리 핵심 전략
- ✅ 세금 절약 꿀팁까지!

---

## 🚀 {keyword} 시작하기 전 필수 준비사항

<img src="{images[1]['url']}" alt="{images[1]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

### 1️⃣ 자금 관리 원칙 (가장 중요!)

**절대 지켜야 할 3가지:**
- 💡 생활비 6개월치는 별도 보관
- 💡 투자 자금은 잃어도 되는 돈으로만
- 💡 한 곳에 몰빵 절대 금지

**추천 자금 배분:**
- 🔵 안전 자산 (60%): 예금, 적금
- 🟡 중위험 자산 (30%): {keyword}
- 🔴 고위험 자산 (10%): 고수익 상품

### 2️⃣ {current_season}철 {keyword} 시장 분석

**현재 시장 상황:**
- 📈 전년 동기 대비 상승세
- 🌍 글로벌 경제 회복 신호
- 💼 기관 투자자 유입 증가

**{current_season}철 특징:**
- 🎯 {keyword} 수요 증가 시기
- 💰 보너스 시즌으로 자금 유입
- 📊 연말 정산 효과 기대

### 3️⃣ 플랫폼 선택 가이드

**초보자 추천 순위:**
1. **A플랫폼** ⭐⭐⭐⭐⭐
   - 수수료: 0.1%
   - 장점: 사용 편의성 최고
   - 단점: 상품 다양성 부족

2. **B플랫폼** ⭐⭐⭐⭐
   - 수수료: 0.15%
   - 장점: 분석 도구 풍부
   - 단점: 초보자에게 복잡

3. **C플랫폼** ⭐⭐⭐
   - 수수료: 0.2%
   - 장점: 교육 자료 많음
   - 단점: 속도 느림

---

## 📈 실전 투자 전략 (월 50만원 수익 달성법)

### 전략 1: 분산 투자 포트폴리오

**제가 실제 사용하는 비율:**
- 🏢 대형주 (40%): 안정성 확보
- 🚀 성장주 (35%): 수익성 추구  
- 🌍 해외 (15%): 환율 헤지
- 💎 테마주 (10%): 고수익 기회

### 전략 2: 타이밍 분석법

**매수 타이밍:**
- 📉 시장 조정 시 (20% 이상 하락)
- 📊 거래량 급증 후 안정화
- 🗞️ 악재 출현 후 1-2주

**매도 타이밍:**
- 📈 목표 수익률 달성 (20-30%)
- 📰 호재 소식 정점
- 🔴 기술적 지표 과열

### 전략 3: 리스크 관리

**손절 원칙:**
- 🚨 -10% 도달 시 무조건 손절
- 📱 알림 설정으로 감정 배제
- 📝 손절 이유 반드시 기록

**수익 관리:**
- 🎯 +20% 달성 시 50% 매도
- 💰 +30% 달성 시 추가 30% 매도
- 🔄 남은 20%로 추가 상승 기대

---

## 🚨 초보자가 반드시 피해야 할 실수 TOP 5

### ❌ 실수 1: 감정적 투자

**실패 사례:** 
FOMO(Fear of Missing Out)에 빠져서 고점에 매수 → 30% 손실

**해결책:**
- 📋 투자 계획서 미리 작성
- ⏰ 쿨타임 24시간 원칙
- 🤝 투자 스터디 그룹 참여

### ❌ 실수 2: 과도한 레버리지

**실패 사례:**
3배 레버리지로 큰 수익 노림 → 마진콜로 전 재산 날림

**해결책:**
- 💡 레버리지 최대 1.5배까지만
- 📊 증거금 여유분 항상 확보
- 🛡️ 스탑로스 주문 필수

### ❌ 실수 3: 정보 과의존

**실패 사례:**
유튜버 추천 종목만 따라하기 → 연속 손실

**해결책:**
- 🔍 자체 분석 능력 기르기
- 📚 기본기 공부 우선
- 💭 다양한 의견 종합 판단

---

## 💡 세금 절약 꿀팁 (연간 100만원 절약 가능)

### ISA 계좌 활용법

**장점:**
- 🎁 연간 200만원 비과세 혜택
- 💰 손익통산으로 세금 최적화
- 🔄 자유로운 상품 변경

**활용 전략:**
- 고수익 상품을 ISA에 우선 배치
- 손실 종목과 수익 종목 균형 조절
- 만기 시 연금계좌로 이월

### 연금저축 세액공제

**절세 효과:**
- 📋 연간 최대 66만원 세액공제
- 💼 소득 구간별 공제율 차등
- 🎯 은퇴 준비와 절세 동시 효과

---

## 🎯 2025년 {keyword} 전망과 추천 전략

### 상반기 전망
- 📈 경기 회복으로 상승 기조 유지
- 🏦 금리 인하 가능성으로 유동성 증가
- 🌍 해외 자금 유입 기대

### 하반기 전망  
- 🗳️ 정치적 이벤트 영향 주의
- 📊 실적 시즌 변동성 확대
- 💱 환율 변동 리스크 관리 필요

### 추천 투자 테마
1. **AI 관련주** - 기술 혁신 수혜
2. **2차전지** - 전기차 보급 확산  
3. **바이오** - 고령화 사회 대비
4. **리츠** - 부동산 간접 투자

---

## 🤝 마무리하며...

<img src="{images[2]['url']}" alt="{images[2]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

{keyword}는 단순한 돈벌이가 아닌 미래를 위한 준비입니다.

**성공하는 투자자의 공통점:**
- 🎯 명확한 목표 설정
- 📚 꾸준한 학습
- 😌 감정 통제
- ⏰ 장기적 관점

**마지막 조언:**
- 💪 작은 금액부터 시작하세요
- 📖 실패도 소중한 경험입니다
- 🤝 혼자가 아닌 함께 성장하세요

**여러분의 재정 자유를 응원합니다!** 

성공 사례나 궁금한 점이 있으시면 댓글로 공유해주세요. 서로 도움이 되는 정보를 나눠요!

---

**🔗 관련 글 더 보기:**
- [{keyword} 세금 완벽 가이드]
- [초보자를 위한 포트폴리오 구성법]
- [{current_season}철 투자 전략]

*이 글이 도움되셨다면 ❤️ 공감과 공유 부탁드려요!*
"""

def generate_travel_blog(keyword, current_season):
    """여행 전용 블로그 생성 - 실제 경험담과 꿀팁으로 몰입도 극대화"""
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 여행 전용 훅킹 제목들
    travel_titles = [
        f"{keyword} 3박4일 완벽 가이드 - 현지인이 알려준 숨은 명소",
        f"🌟 {keyword} 혼자 여행 후기 - 20만원으로 떠난 힐링 여행",
        f"📸 {keyword} 인스타 핫플 총정리 - 사진 맛집 베스트 10",
        f"💰 {keyword} 가성비 여행 꿀팁 - 50% 절약하는 비법 공개",
        f"🎒 {keyword} 여행 준비물부터 코스까지 올인원 가이드"
    ]
    
    # 여행 전용 훅킹 시작 문장들
    travel_hooks = [
        f"지난달 {keyword} 다녀온 후 아직도 그 여운에 빠져있어요.",
        f"{keyword} 여행을 계획하시는 분들을 위해 진짜 유용한 정보만 골라서 정리했습니다.",
        f"처음 {keyword} 갔을 때는 아무것도 몰라서 후회했는데, 이번엔 완전 달랐어요.",
        f"{keyword} 여행 다녀온 지 일주일 됐는데, 벌써 다시 가고 싶어서 미치겠어요."
    ]
    
    # 랜덤 선택
    title = random.choice(travel_titles)
    hook = random.choice(travel_hooks)
    
    # 여행 관련 랜덤 수치
    budget = random.randint(15, 80)
    days = random.randint(2, 7)
    spots = random.randint(5, 12)
    
    # 여행 전용 블로그 내용
    blog_content = f"""# {title}

{hook}

총 {days}일 동안 {budget}만원의 예산으로 다녀온 {keyword} 여행 경험을 솔직하게 공유해드릴게요!

<img src="{images[0]['url']}" alt="{images[0]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

## 🎯 {keyword} 여행 기본 정보

**여행 개요:**
- 📅 여행 기간: {days}일
- 💰 총 예산: {budget}만원 (1인 기준)
- 🎒 여행 스타일: 자유여행
- 📍 주요 방문지: {spots}곳

**{current_season}철 {keyword} 여행의 장점:**
- 🌤️ 날씨가 여행하기 딱 좋음
- 👥 성수기 대비 상대적으로 한적함
- 💸 숙박비, 항공료 할인 혜택
- 📸 {current_season} 풍경 사진 찍기 좋음

**이 글에서 얻어가실 정보:**
- ✅ {keyword} 필수 코스 {spots}곳 상세 리뷰
- ✅ 현지인 추천 맛집 & 카페
- ✅ 숙소 예약부터 교통편까지 꿀팁
- ✅ 예산 절약 노하우 대공개
- ✅ 인스타 감성 사진 스팟 정보

---

## 🗺️ {keyword} 완벽 여행 코스 ({days}일 일정)

<img src="{images[1]['url']}" alt="{images[1]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

### 1일차: 도착 & 시내 탐방

**오전 (10:00-12:00)**
- ✈️ 도착 후 숙소 체크인
- ☕ 현지 카페에서 여행 계획 점검
- 📱 현지 심카드/와이파이 구매

**오후 (13:00-18:00)**
- 🏛️ {keyword} 대표 관광지 방문
- 📸 인증샷 필수 스팟 3곳
- 🛍️ 기념품 거리 둘러보기

**저녁 (19:00-21:00)**
- 🍽️ 현지 대표 음식 체험
- 🌃 야경 명소에서 힐링 타임
- 📝 여행 일기 작성

### 2일차: 자연 & 액티비티

**오전 (09:00-12:00)**
- 🌄 일출 명소 (일찍 출발 추천)
- 🥾 트레킹 코스 (초급자 코스)
- 🌿 자연 속에서 휴식

**오후 (13:00-17:00)**
- 🏊‍♂️ 해변/호수 액티비티
- 🚴‍♂️ 자전거 투어 참여
- 📷 자연 풍경 사진 촬영

**저녁 (18:00-20:00)**
- 🍻 현지 맥주/전통주 체험
- 🎵 현지 문화 공연 관람
- 💤 일찍 휴식

### 3일차 이후: 심화 탐방

**추천 활동:**
- 🏛️ 박물관/미술관 투어
- 🛍️ 현지 시장 쇼핑
- 🧘‍♀️ 스파/마사지 힐링
- 🍳 쿠킹 클래스 참여

---

## 🍽️ 현지인 추천 맛집 베스트 5

### 1위: [맛집 이름] ⭐⭐⭐⭐⭐

**추천 메뉴:** 대표 요리 (가격: 15,000원)
- 👍 장점: 현지인들도 줄서서 먹는 곳
- 📍 위치: 중심가에서 도보 5분
- ⏰ 운영시간: 11:00-21:00
- 💡 팁: 오픈 시간에 가야 웨이팅 없음

### 2위: [카페 이름] ⭐⭐⭐⭐

**추천 메뉴:** 시그니처 음료 (가격: 8,000원)
- 👍 장점: 인스타 감성 뿜뿜
- 📍 위치: 관광지 근처
- ⏰ 운영시간: 09:00-22:00
- 💡 팁: 루프탑 자리 예약 필수

### 3-5위: 간단 소개

**3위:** 길거리 음식 (가격대: 3,000-5,000원)
**4위:** 전통 음식점 (가격대: 20,000-30,000원)  
**5위:** 디저트 카페 (가격대: 8,000-12,000원)

---

## 🏨 숙소 & 교통 꿀팁

### 숙소 선택 가이드

**호텔급 (1박 8-15만원)**
- ✅ 편의시설 완벽
- ✅ 서비스 최고급
- ❌ 비싼 가격

**게스트하우스 (1박 3-6만원)**
- ✅ 가성비 최고
- ✅ 현지인/여행자 교류
- ❌ 프라이버시 부족

**에어비앤비 (1박 5-10만원)**
- ✅ 현지 생활 체험
- ✅ 취사 가능
- ❌ 호스트 의존적

### 교통편 완전 정복

**대중교통 (가장 추천)**
- 🚌 버스: 저렴하고 경치 좋음
- 🚇 지하철: 빠르고 정확함
- 🚕 택시: 편하지만 비쌈

**렌터카 (자유도 최고)**
- 💰 비용: 하루 5-8만원
- 📋 필요서류: 국제면허증
- ⚠️ 주의사항: 현지 교통법규 숙지

---

## 💰 예산 절약 꿀팁 (50% 절약 가능!)

### 항공료 절약법

**예약 타이밍:**
- 🎯 출발 2-3개월 전 예약
- 📅 화요일/수요일 출발
- 🌙 새벽/늦은 시간 항공편

**할인 혜택 활용:**
- 💳 항공사 제휴 카드 사용
- 🎁 마일리지 적립/사용
- 📱 항공사 앱 전용 할인

### 숙박비 절약법

**예약 사이트 비교:**
- 🔍 최소 3-4곳 비교 필수
- 📱 앱 전용 할인 체크
- 💌 직접 예약 시 할인 문의

**시기별 전략:**
- 🌸 성수기 피하기
- 📅 평일 숙박 선택
- 🏨 장기 숙박 할인 활용

### 식비 절약법

**현명한 식사 전략:**
- 🥪 아침: 편의점/마트 활용
- 🍜 점심: 현지 로컬 식당
- 🍽️ 저녁: 맛집 1-2곳만 사치

---

## 📸 인스타 감성 사진 스팟 TOP 5

### 📍 스팟 1: [명소 이름]
- 📷 베스트 앵글: 계단에서 아래로
- ⏰ 골든타임: 오후 4-5시
- 💡 촬영 팁: 역광 활용하기

### 📍 스팟 2: [카페/건물]
- 📷 베스트 앵글: 창가 자리
- ⏰ 골든타임: 오전 10-11시
- 💡 촬영 팁: 소품 활용하기

### 📍 스팟 3-5: 간단 소개
- 자연 풍경 (일출/일몰)
- 거리 예술/벽화
- 현지 시장 풍경

---

## 🎒 여행 준비물 체크리스트

### 필수 준비물
- ✅ 여권/신분증
- ✅ 항공권/숙소 예약 확인서
- ✅ 여행자 보험
- ✅ 현금/카드
- ✅ 충전기/보조배터리

### 계절별 추가 준비물
**{current_season}철 필수:**
- 🧥 겉옷 (일교차 대비)
- 🕶️ 선글라스/모자
- 🧴 선크림/로션
- 💊 상비약

---

## 🤝 마무리하며...

<img src="{images[2]['url']}" alt="{images[2]['alt']}" style="width:100%; max-width:600px; height:auto; margin:20px 0; border-radius:8px; display:block;">

{keyword} 여행은 정말 강력 추천합니다!

**이번 여행에서 얻은 것들:**
- 🌟 새로운 경험과 추억
- 📸 인생 사진들
- 🤝 현지인들과의 소중한 만남
- 💪 혼자서도 할 수 있다는 자신감

**여행 준비하시는 분들께:**
- 🎯 계획은 70%, 여유는 30%
- 💰 예산은 여유롭게 준비하세요
- 📱 현지 정보 미리 조사 필수
- 😊 열린 마음으로 즐기세요

**여러분의 행복한 여행을 응원합니다!** 

궁금한 점이나 추가 정보가 필요하시면 댓글로 남겨주세요. 최대한 도움드리겠습니다!

---

**🔗 관련 글 더 보기:**
- [{keyword} 숨은 명소 베스트 10]
- [{current_season}철 국내여행 추천]
- [혼자 여행 완벽 가이드]

*이 글이 도움되셨다면 ❤️ 공감과 공유 부탁드려요!*
"""
    

def generate_education_blog(keyword, current_season):
    """교육 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "교육_전문가")

def generate_lifestyle_blog(keyword, current_season):
    """라이프스타일 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "라이프스타일_전문가")

def generate_trend_blog(keyword, current_season):
    """트렌드 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "트렌드_분석가")

def generate_health_blog(keyword, current_season):
    """건강 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "건강_전문가")

def generate_finance_blog(keyword, current_season):
    """재테크 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "재테크_전문가")

def generate_travel_blog(keyword, current_season):
    """여행 관련 블로그 글 생성"""
    return generate_local_blog(keyword, "여행_전문가")

def generate_local_blog(keyword, hook_style):
    """키워드별 맞춤 고품질 블로그 생성"""
    
    current_season = get_current_season()
    
    def detect_keyword_category(keyword):
        """키워드에서 카테고리 자동 감지"""
        ai_keywords = ["AI", "인공지능", "챗GPT", "로봇", "자동화", "머신러닝", "딥러닝"]
        health_keywords = ["건강", "다이어트", "운동", "혈압", "당뇨", "면역력", "영양", "의료"]
        finance_keywords = ["투자", "재테크", "주식", "부동산", "비트코인", "펀드", "적금", "대출"]
        travel_keywords = ["여행", "국내여행", "해외여행", "캠핑", "맛집", "카페", "제주도", "부산여행"]
        education_keywords = ["육아", "교육", "학습법", "입시", "영어공부", "자격증", "취업", "이직"]
        lifestyle_keywords = ["정리정돈", "인테리어", "패션", "뷰티", "반려동물", "가전제품"]
        trend_keywords = ["MZ세대", "ESG", "지속가능", "친환경", "제로웨이스트", "비건"]
        
        if any(ai_word in keyword for ai_word in ai_keywords):
            return "AI/기술"
        elif any(health_word in keyword for health_word in health_keywords):
            return "건강"  
        elif any(finance_word in keyword for finance_word in finance_keywords):
            return "재테크"
        elif any(travel_word in keyword for travel_word in travel_keywords):
            return "여행"
        elif any(edu_word in keyword for edu_word in education_keywords):
            return "육아교육"
        elif any(life_word in keyword for life_word in lifestyle_keywords):
            return "라이프스타일"
        else:
            return "트렌드"
    
    keyword_category = detect_keyword_category(keyword)
    
    if keyword_category == "AI/기술":
        return generate_ai_blog(keyword, current_season)
    elif keyword_category == "건강":
        return generate_health_blog(keyword, current_season)
    elif keyword_category == "재테크":
        return generate_finance_blog(keyword, current_season)
    elif keyword_category == "여행":
        return generate_travel_blog(keyword, current_season)
    elif keyword_category == "육아교육":
        return generate_education_blog(keyword, current_season)
    elif keyword_category == "라이프스타일":
        return generate_lifestyle_blog(keyword, current_season)
    else:
        return generate_trend_blog(keyword, current_season)
    
    # 키워드별 자연스러운 도입부 패턴
    KEYWORD_INTROS = {
        "AI/기술": [
            f"요즘 {keyword}에 대한 관심이 폭발적으로 늘어나고 있죠.",
            f"제가 {keyword} 분야에서 일하면서 가장 많이 받는 질문들을 정리해봤어요.",
            f"{keyword} 트렌드가 빠르게 변하면서 헷갈리는 분들이 많더라고요.",
            f"{current_season}이 되면서 {keyword} 관련 질문들이 정말 많아졌어요."
        ],
        
        "건강": [
            f"{current_season}이 되니까 {keyword} 관련 문의가 정말 많아졌어요.",
            f"병원에서 {keyword} 때문에 오시는 분들이 늘어나고 있어요.",
            f"제 주변에서도 {keyword} 고민하시는 분들이 정말 많아요."
        ],
        
        "재테크": [
            f"요즘 {keyword}에 대한 관심이 뜨거워지고 있죠.",
            f"{current_season} 들어서 {keyword} 상담 요청이 부쩍 늘었어요.",
            f"경제 상황이 변하면서 {keyword}에 대한 문의가 많아졌어요."
        ],
        
        "라이프스타일": [
            f"{current_season}이 되니까 {keyword}에 대한 관심이 많아졌어요.",
            f"요즘 {keyword} 관련해서 문의가 정말 많이 들어와요.",
            f"제 주변에서도 {keyword}에 대해 궁금해하시는 분들이 많더라고요."
        ]
    }
    # ===== 여기까지 추가 =====
    
    # 랜덤 페르소나 선택 (기존 코드 그대로)
    persona_name, persona = get_smart_persona(keyword)
    
    # 기본 변수 설정
    current_season = get_current_season()
    structure = random.choice(BLOG_STRUCTURES)
    success_rate = random.randint(78, 94)
    period_weeks = random.randint(2, 8)
    people_count = random.randint(100, 500)
    
    # 무료 이미지 가져오기
    images = get_free_images(keyword, 3)
    
    # 개인적 경험담 생성
    personal_exp = generate_personal_experience(keyword, persona, persona_name)
    
    # 키워드 카테고리 감지하고 맞춤 도입부 선택
    keyword_category = detect_keyword_category(keyword)
    category_intros = KEYWORD_INTROS[keyword_category]
    selected_intro = random.choice(category_intros)

    # 시작 스타일 선택 (수정됨)
    if structure == "개인_경험담_중심":
        start_style = f"{personal_exp}\n\n그때 정말 깨달았어요. {keyword}이(가) 얼마나 중요한지를..."
    elif structure == "실패담_중심":
        start_style = f"처음에는 저도 {keyword}에 대해 잘못 알고 있었어요."
    elif structure == "Q&A_형식":
        start_style = f"많은 분들이 {keyword}에 대해 자주 물어보시는 질문들이 있어요."
    else:
        start_style = selected_intro  # 여기가 핵심 변경점!
    
    # AI SULAB 고정 블로그 글 생성
    blog_content = f"""# {keyword} 완벽 가이드 - AI SULAB이 전해드리는 검증된 정보

안녕하세요! AI SULAB입니다. 오늘은 {keyword}에 대한 정보를 공유해드릴게요.

{start_style}

![{images[0]['alt']}]({images[0]['url']})

## 🤔 왜 이 글을 쓰게 되었나요?

{current_season}이 되니까 {keyword} 관련 문의가 정말 많아졌어요. 전국 각지 분들이 자주 물어보시는데, 인터넷에 떠도는 정보들이 너무 일반적이고 실제랑 다른 경우가 많더라고요.

그래서 제가 직접 연구하고 분석한 **진짜 효과 있었던 것들만** 정리해서 공유하려고 해요.

**이 글에서 얻어가실 수 있는 것들:**
- ✅ 실제로 {success_rate}% 효과를 본 구체적인 방법
- ✅ {period_weeks}주 만에 변화를 느낄 수 있는 실행 계획  
- ✅ 제가 직접 분석한 시행착오와 해결 방법
- ✅ 전국 각지 정보까지!

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

예를 들어, 제가 조사한 {people_count}명 중에서 같은 방법으로 해도:
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

### ❌ 별로였던 것들 (솔직하게)

**1. 너무 복잡한 방법들**
처음에 의욕적으로 복잡한 프로그램을 시작했는데, 3일 만에 포기했어요 😅

**2. 비싼 건 무조건 좋을 거라는 착각**
가격과 효과는 비례하지 않더라고요. 오히려 기본에 충실한 게 최고였어요.

---

## 🤝 마무리하며... (진심으로)

{current_season} 철이라 더욱 신경 쓰이는 {keyword}, 정말 많은 분들이 고민하고 계시죠.

**가장 중요한 건:**
- 자신에게 맞는 방법 찾기
- 꾸준함이 완벽함보다 중요
- 작은 성취도 인정하고 격려하기

**여러분께 부탁드리고 싶은 것:**
- 댓글로 경험담 공유해주세요 (정말 도움 돼요!)
- 궁금한 점 있으면 언제든 물어보세요
- 주변 분들께도 공유해주시면 감사하겠어요

여러분의 건강한 변화를 진심으로 응원하는 AI SULAB이었습니다! 💪

---

**📝 관련 글도 확인해보세요:**
- [{keyword} 초보자를 위한 가이드]
- [자주 하는 실수 TOP 5]  
- [{current_season} 철 {keyword} 관리법]

*이 글이 도움되셨다면 하트❤️와 공유 부탁드려요!*
"""
    
    return blog_content

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
    
# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 고품질 블로거 페르소나 시스템
import random
from datetime import datetime, timedelta

# 다양한 블로거 페르소나 정의 (20가지)
BLOGGER_PERSONAS = {
    "건강관리사_김민지": {"age": 32, "job": "병원 영양사", "location": "서울 강남구", "experience": "7년차"},
    "헬스트레이너_박준호": {"age": 28, "job": "개인 PT 트레이너", "location": "부산 해운대구", "experience": "5년차"},
    "약사_이수현": {"age": 35, "job": "동네 약국 약사", "location": "대구 수성구", "experience": "10년차"},
    "주부_최은영": {"age": 41, "job": "전업주부 (前 간호사)", "location": "인천 연수구", "experience": "15년"},
    "운동강사_이민수": {"age": 26, "job": "필라테스 강사", "location": "광주 서구", "experience": "3년차"},
    "한의사_박소영": {"age": 38, "job": "한방병원 원장", "location": "전주 완산구", "experience": "12년차"},
    "간호사_김태현": {"age": 29, "job": "대학병원 간호사", "location": "울산 남구", "experience": "6년차"},
    "요가강사_정미래": {"age": 31, "job": "요가스튜디오 대표", "location": "수원 영통구", "experience": "8년차"},
    "물리치료사_조현우": {"age": 34, "job": "재활병원 물리치료사", "location": "청주 흥덕구", "experience": "9년차"},
    "피트니스코치_안서연": {"age": 27, "job": "크로스핏 코치", "location": "포항 북구", "experience": "4년차"},
    "영양상담사_송지훈": {"age": 30, "job": "보건소 영양사", "location": "천안 동남구", "experience": "7년차"},
    "재활트레이너_홍예진": {"age": 33, "job": "스포츠 재활 전문가", "location": "창원 의창구", "experience": "8년차"}
}

# 키워드별 전문 페르소나 매칭
KEYWORD_PERSONA_MAPPING = {
    "건강": ["건강관리사_김민지", "약사_이수현", "간호사_김태현", "주부_최은영"],
    "운동": ["헬스트레이너_박준호", "운동강사_이민수", "피트니스코치_안서연"],
    "다이어트": ["헬스트레이너_박준호", "영양상담사_송지훈", "다이어트코치_윤하늘"],
    "재테크": ["주부블로거_문지영", "웰니스코치_서예린"],
    "여행": ["주부블로거_문지영", "웰니스코치_서예린"],
    "육아": ["주부_최은영", "주부블로거_문지영"],
    "라이프스타일": ["요가강사_정미래", "웰니스코치_서예린"]
}

def get_smart_persona(keyword):
    """키워드에 맞는 스마트한 페르소나 생성"""
    personas = {
        "건강_의사": {
            "job": "가정의학과 전문의",
            "experience": "15년",
            "specialty": "만성질환 관리",
            "tone": "전문적이면서도 친근한"
        },
        "운동_트레이너": {
            "job": "퍼스널 트레이너",
            "experience": "10년",
            "specialty": "체중 관리, 근력 운동",
            "tone": "열정적이고 동기부여하는"
        },
        "요리_셰프": {
            "job": "전문 요리사",
            "experience": "12년",
            "specialty": "건강식, 한식 퓨전",
            "tone": "실용적이고 창의적인"
        },
        "공부_교사": {
            "job": "진로상담 교사",
            "experience": "8년",
            "specialty": "학습법, 시간관리",
            "tone": "조언자적이고 체계적인"
        },
        "직장_멘토": {
            "job": "커리어 코치",
            "experience": "20년",
            "specialty": "직무 역량 개발",
            "tone": "통찰력 있고 실천적인"
        }
    }
    
    # 키워드에 따른 페르소나 선택
    if "건강" in keyword or "질병" in keyword or "다이어트" in keyword:
        persona_name = "건강_의사"
    elif "운동" in keyword or "체중" in keyword or "근육" in keyword:
        persona_name = "운동_트레이너"
    elif "요리" in keyword or "음식" in keyword or "레시피" in keyword:
        persona_name = "요리_셰프"
    elif "공부" in keyword or "학습" in keyword or "시험" in keyword:
        persona_name = "공부_교사"
    else:
        persona_name = "직장_멘토"
    
    return persona_name, personas[persona_name]

def generate_personal_experience(keyword, persona, persona_name):
    """페르소나의 특성을 반영한 개인적 경험담 생성"""
    experiences = {
        "건강_의사": [
            f"제가 {persona['experience']}동안 {persona['specialty']} 분야에서 수많은 환자들을 진료하면서 발견한 {keyword}에 대한 놀라운 사실이 있습니다.",
            f"진료실에서 만난 환자들 중 {keyword} 때문에 고민하시는 분들이 정말 많았어요. 그래서 제가 특별히 연구하고 정리한 내용을 공유하려고 합니다.",
            f"{persona['specialty']} 전문의로서, {keyword}에 대한 오해와 진실을 명확하게 알려드리고 싶습니다."
        ],
        "운동_트레이너": [
            f"{persona['experience']}간의 트레이닝 경험에서 찾아낸 {keyword}의 핵심 포인트를 알려드립니다.",
            f"제 회원님들 중 {keyword}로 고민하시는 분들을 위해 특별히 개발한 프로그램이 있습니다.",
            f"저도 처음에는 {keyword}에 대해 잘못 알고 있었어요. 그런데 수많은 시행착오 끝에 발견한 진짜 해결책이 있습니다."
        ],
        "요리_셰프": [
            f"주방에서 {persona['experience']}동안 연구한 {keyword} 비법을 처음으로 공개합니다.",
            f"{persona['specialty']} 전문가로서 {keyword}에 대한 특별한 노하우를 알려드리려고 해요.",
            f"많은 분들이 {keyword}를 어려워하시는데, 제가 쉽게 알려드리겠습니다."
        ],
        "공부_교사": [
            f"{persona['experience']}동안 수많은 학생들의 {keyword} 고민을 해결해주면서 깨달은 점이 있습니다.",
            f"진로상담 교사로서 {keyword}에 대한 학생들의 고민을 해결해주면서 발견한 핵심 원리가 있어요.",
            f"{keyword}! 선생님인 저도 처음에는 막막했답니다. 그래서 준비했어요."
        ],
        "직장_멘토": [
            f"20년 넘게 수많은 직장인들의 {keyword} 고민을 상담하면서 발견한 공통점이 있습니다.",
            f"저도 처음 직장생활 할 때는 {keyword} 때문에 정말 힘들었어요. 그때의 경험을 바탕으로 해결책을 찾았습니다.",
            f"수많은 기업에서 강의하면서 모은 {keyword}에 대한 노하우를 공유합니다."
        ]
    }
    
    return random.choice(experiences[persona_name])

# 전문가별 인사말과 전문성 표현
greetings = {
    "건강_의사": "안녕하세요, 가정의학과 전문의입니다.",
    "운동_트레이너": "안녕하세요, 현직 퍼스널 트레이너입니다.",
    "요리_셰프": "안녕하세요, 건강식 전문 요리사입니다.",
    "공부_교사": "안녕하세요, 진로상담 전문 교사입니다.",
    "직장_멘토": "안녕하세요, 커리어 코치입니다."
}

expertise = {
    "건강_의사": "의학적 근거를 바탕으로",
    "운동_트레이너": "과학적인 운동 원리를 기반으로",
    "요리_셰프": "전문 요리사의 노하우로",
    "공부_교사": "교육 전문가의 관점에서",
    "직장_멘토": "풍부한 실무 경험을 바탕으로"
}

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

# 무료 이미지 검색 함수
def get_free_images(keyword, count=3):
    """무료 이미지 URL 가져오기"""
    images = []
    
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
    except Exception as e:
        # 기본 이미지
        images = [{
            "url": "https://picsum.photos/600/300?random=1",
            "alt": f"{keyword} 관련 이미지"
        } for _ in range(count)]
    
    return images

# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 고품질 블로거 페르소나 시스템
import random
from datetime import datetime, timedelta

# 다양한 블로거 페르소나 정의 (20가지)
BLOGGER_PERSONAS = {
    "건강관리사_김민지": {"age": 32, "job": "병원 영양사", "location": "서울 강남구", "experience": "7년차"},
    "헬스트레이너_박준호": {"age": 28, "job": "개인 PT 트레이너", "location": "부산 해운대구", "experience": "5년차"},
    "약사_이수현": {"age": 35, "job": "동네 약국 약사", "location": "대구 수성구", "experience": "10년차"},
    "주부_최은영": {"age": 41, "job": "전업주부 (前 간호사)", "location": "인천 연수구", "experience": "15년"},
    "운동강사_이민수": {"age": 26, "job": "필라테스 강사", "location": "광주 서구", "experience": "3년차"},
    "한의사_박소영": {"age": 38, "job": "한방병원 원장", "location": "전주 완산구", "experience": "12년차"},
    "간호사_김태현": {"age": 29, "job": "대학병원 간호사", "location": "울산 남구", "experience": "6년차"},
    "요가강사_정미래": {"age": 31, "job": "요가스튜디오 대표", "location": "수원 영통구", "experience": "8년차"},
    "물리치료사_조현우": {"age": 34, "job": "재활병원 물리치료사", "location": "청주 흥덕구", "experience": "9년차"},
    "피트니스코치_안서연": {"age": 27, "job": "크로스핏 코치", "location": "포항 북구", "experience": "4년차"},
    "영양상담사_송지훈": {"age": 30, "job": "보건소 영양사", "location": "천안 동남구", "experience": "7년차"},
    "재활트레이너_홍예진": {"age": 33, "job": "스포츠 재활 전문가", "location": "창원 의창구", "experience": "8년차"}
}

# 키워드별 전문 페르소나 매칭
KEYWORD_PERSONA_MAPPING = {
    "건강": ["건강관리사_김민지", "약사_이수현", "간호사_김태현", "주부_최은영"],
    "운동": ["헬스트레이너_박준호", "운동강사_이민수", "피트니스코치_안서연"],
    "다이어트": ["헬스트레이너_박준호", "영양상담사_송지훈", "다이어트코치_윤하늘"],
    "재테크": ["주부블로거_문지영", "웰니스코치_서예린"],
    "여행": ["주부블로거_문지영", "웰니스코치_서예린"],
    "육아": ["주부_최은영", "주부블로거_문지영"],
    "라이프스타일": ["요가강사_정미래", "웰니스코치_서예린"]
}

def get_smart_persona(keyword):
    """키워드에 맞는 스마트한 페르소나 생성"""
    personas = {
        "건강_의사": {
            "job": "가정의학과 전문의",
            "experience": "15년",
            "specialty": "만성질환 관리",
            "tone": "전문적이면서도 친근한"
        },
        "운동_트레이너": {
            "job": "퍼스널 트레이너",
            "experience": "10년",
            "specialty": "체중 관리, 근력 운동",
            "tone": "열정적이고 동기부여하는"
        },
        "요리_셰프": {
            "job": "전문 요리사",
            "experience": "12년",
            "specialty": "건강식, 한식 퓨전",
            "tone": "실용적이고 창의적인"
        },
        "공부_교사": {
            "job": "진로상담 교사",
            "experience": "8년",
            "specialty": "학습법, 시간관리",
            "tone": "조언자적이고 체계적인"
        },
        "직장_멘토": {
            "job": "커리어 코치",
            "experience": "20년",
            "specialty": "직무 역량 개발",
            "tone": "통찰력 있고 실천적인"
        }
    }
    
    # 키워드에 따른 페르소나 선택
    if "건강" in keyword or "질병" in keyword or "다이어트" in keyword:
        persona_name = "건강_의사"
    elif "운동" in keyword or "체중" in keyword or "근육" in keyword:
        persona_name = "운동_트레이너"
    elif "요리" in keyword or "음식" in keyword or "레시피" in keyword:
        persona_name = "요리_셰프"
    elif "공부" in keyword or "학습" in keyword or "시험" in keyword:
        persona_name = "공부_교사"
    else:
        persona_name = "직장_멘토"
    
    return persona_name, personas[persona_name]

def generate_personal_experience(keyword, persona, persona_name):
    """페르소나의 특성을 반영한 개인적 경험담 생성"""
    experiences = {
        "건강_의사": [
            f"제가 {persona['experience']}동안 {persona['specialty']} 분야에서 수많은 환자들을 진료하면서 발견한 {keyword}에 대한 놀라운 사실이 있습니다.",
            f"진료실에서 만난 환자들 중 {keyword} 때문에 고민하시는 분들이 정말 많았어요. 그래서 제가 특별히 연구하고 정리한 내용을 공유하려고 합니다.",
            f"{persona['specialty']} 전문의로서, {keyword}에 대한 오해와 진실을 명확하게 알려드리고 싶습니다."
        ],
        "운동_트레이너": [
            f"{persona['experience']}간의 트레이닝 경험에서 찾아낸 {keyword}의 핵심 포인트를 알려드립니다.",
            f"제 회원님들 중 {keyword}로 고민하시는 분들을 위해 특별히 개발한 프로그램이 있습니다.",
            f"저도 처음에는 {keyword}에 대해 잘못 알고 있었어요. 그런데 수많은 시행착오 끝에 발견한 진짜 해결책이 있습니다."
        ],
        "요리_셰프": [
            f"주방에서 {persona['experience']}동안 연구한 {keyword} 비법을 처음으로 공개합니다.",
            f"{persona['specialty']} 전문가로서 {keyword}에 대한 특별한 노하우를 알려드리려고 해요.",
            f"많은 분들이 {keyword}를 어려워하시는데, 제가 쉽게 알려드리겠습니다."
        ],
        "공부_교사": [
            f"{persona['experience']}동안 수많은 학생들의 {keyword} 고민을 해결해주면서 깨달은 점이 있습니다.",
            f"진로상담 교사로서 {keyword}에 대한 학생들의 고민을 해결해주면서 발견한 핵심 원리가 있어요.",
            f"{keyword}! 선생님인 저도 처음에는 막막했답니다. 그래서 준비했어요."
        ],
        "직장_멘토": [
            f"20년 넘게 수많은 직장인들의 {keyword} 고민을 상담하면서 발견한 공통점이 있습니다.",
            f"저도 처음 직장생활 할 때는 {keyword} 때문에 정말 힘들었어요. 그때의 경험을 바탕으로 해결책을 찾았습니다.",
            f"수많은 기업에서 강의하면서 모은 {keyword}에 대한 노하우를 공유합니다."
        ]
    }
    
    return random.choice(experiences[persona_name])

# 전문가별 인사말과 전문성 표현
greetings = {
    "건강_의사": "안녕하세요, 가정의학과 전문의입니다.",
    "운동_트레이너": "안녕하세요, 현직 퍼스널 트레이너입니다.",
    "요리_셰프": "안녕하세요, 건강식 전문 요리사입니다.",
    "공부_교사": "안녕하세요, 진로상담 전문 교사입니다.",
    "직장_멘토": "안녕하세요, 커리어 코치입니다."
}

expertise = {
    "건강_의사": "의학적 근거를 바탕으로",
    "운동_트레이너": "과학적인 운동 원리를 기반으로",
    "요리_셰프": "전문 요리사의 노하우로",
    "공부_교사": "교육 전문가의 관점에서",
    "직장_멘토": "풍부한 실무 경험을 바탕으로"
}

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

# 무료 이미지 검색 함수
def get_free_images(keyword, count=3):
    """무료 이미지 URL 가져오기"""
    images = []
    
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
    except Exception as e:
        # 기본 이미지
        images = [{
            "url": "https://picsum.photos/600/300?random=1",
            "alt": f"{keyword} 관련 이미지"
        } for _ in range(count)]
    
    return images

# 로그인 정보를 URL 파라미터로 유지
if 'logged_in' not in st.query_params:
    if 'login_ok' not in st.session_state:
        st.session_state['login_ok'] = False

VALID_ID = "aisulab"
VALID_PW = "!js44358574"

# 고품질 블로거 페르소나 시스템
import random
from datetime import datetime, timedelta

# 다양한 블로거 페르소나 정의 (20가지)
BLOGGER_PERSONAS = {
    "건강관리사_김민지": {"age": 32, "job": "병원 영양사", "location": "서울 강남구", "experience": "7년차"},
    "헬스트레이너_박준호": {"age": 28, "job": "개인 PT 트레이너", "location": "부산 해운대구", "experience": "5년차"},
    "약사_이수현": {"age": 35, "job": "동네 약국 약사", "location": "대구 수성구", "experience": "10년차"},
    "주부_최은영": {"age": 41, "job": "전업주부 (前 간호사)", "location": "인천 연수구", "experience": "15년"},
    "운동강사_이민수": {"age": 26, "job": "필라테스 강사", "location": "광주 서구", "experience": "3년차"},
    "한의사_박소영": {"age": 38, "job": "한방병원 원장", "location": "전주 완산구", "experience": "12년차"},
    "간호사_김태현": {"age": 29, "job": "대학병원 간호사", "location": "울산 남구", "experience": "6년차"},
    "요가강사_정미래": {"age": 31, "job": "요가스튜디오 대표", "location": "수원 영통구", "experience": "8년차"},
    "물리치료사_조현우": {"age": 34, "job": "재활병원 물리치료사", "location": "청주 흥덕구", "experience": "9년차"},
    "피트니스코치_안서연": {"age": 27, "job": "크로스핏 코치", "location": "포항 북구", "experience": "4년차"},
    "영양상담사_송지훈": {"age": 30, "job": "보건소 영양사", "location": "천안 동남구", "experience": "7년차"},
    "재활트레이너_홍예진": {"age": 33, "job": "스포츠 재활 전문가", "location": "창원 의창구", "experience": "8년차"}
}

# 키워드별 전문 페르소나 매칭
KEYWORD_PERSONA_MAPPING = {
    "건강": ["건강관리사_김민지", "약사_이수현", "간호사_김태현", "주부_최은영"],
    "운동": ["헬스트레이너_박준호", "운동강사_이민수", "피트니스코치_안서연"],
    "다이어트": ["헬스트레이너_박준호", "영양상담사_송지훈", "다이어트코치_윤하늘"],
    "재테크": ["주부블로거_문지영", "웰니스코치_서예린"],
    "여행": ["주부블로거_문지영", "웰니스코치_서예린"],
    "육아": ["주부_최은영", "주부블로거_문지영"],
    "라이프스타일": ["요가강사_정미래", "웰니스코치_서예린"]
}

def get_smart_persona(keyword):
    """키워드에 맞는 스마트한 페르소나 생성"""
    personas = {
        "건강_의사": {
            "job": "가정의학과 전문의",
            "experience": "15년",
            "specialty": "만성질환 관리",
            "tone": "전문적이면서도 친근한"
        },
        "운동_트레이너": {
            "job": "퍼스널 트레이너",
            "experience": "10년",
            "specialty": "체중 관리, 근력 운동",
            "tone": "열정적이고 동기부여하는"
        },
        "요리_셰프": {
            "job": "전문 요리사",
            "experience": "12년",
            "specialty": "건강식, 한식 퓨전",
            "tone": "실용적이고 창의적인"
        },
        "공부_교사": {
            "job": "진로상담 교사",
            "experience": "8년",
            "specialty": "학습법, 시간관리",
            "tone": "조언자적이고 체계적인"
        },
        "직장_멘토": {
            "job": "커리어 코치",
            "experience": "20년",
            "specialty": "직무 역량 개발",
            "tone": "통찰력 있고 실천적인"
        }
    }
    
    # 키워드에 따른 페르소나 선택
    if "건강" in keyword or "질병" in keyword or "다이어트" in keyword:
        persona_name = "건강_의사"
    elif "운동" in keyword or "체중" in keyword or "근육" in keyword:
        persona_name = "운동_트레이너"
    elif "요리" in keyword or "음식" in keyword or "레시피" in keyword:
        persona_name = "요리_셰프"
    elif "공부" in keyword or "학습" in keyword or "시험" in keyword:
        persona_name = "공부_교사"
    else:
        persona_name = "직장_멘토"
    
    return persona_name, personas[persona_name]

def generate_personal_experience(keyword, persona, persona_name):
    """페르소나의 특성을 반영한 개인적 경험담 생성"""
    experiences = {
        "건강_의사": [
            f"제가 {persona['experience']}동안 {persona['specialty']} 분야에서 수많은 환자들을 진료하면서 발견한 {keyword}에 대한 놀라운 사실이 있습니다.",
            f"진료실에서 만난 환자들 중 {keyword} 때문에 고민하시는 분들이 정말 많았어요. 그래서 제가 특별히 연구하고 정리한 내용을 공유하려고 합니다.",
            f"{persona['specialty']} 전문의로서, {keyword}에 대한 오해와 진실을 명확하게 알려드리고 싶습니다."
        ],
        "운동_트레이너": [
            f"{persona['experience']}간의 트레이닝 경험에서 찾아낸 {keyword}의 핵심 포인트를 알려드립니다.",
            f"제 회원님들 중 {keyword}로 고민하시는 분들을 위해 특별히 개발한 프로그램이 있습니다.",
            f"저도 처음에는 {keyword}에 대해 잘못 알고 있었어요. 그런데 수많은 시행착오 끝에 발견한 진짜 해결책이 있습니다."
        ],
        "요리_셰프": [
            f"주방에서 {persona['experience']}동안 연구한 {keyword} 비법을 처음으로 공개합니다.",
            f"{persona['specialty']} 전문가로서 {keyword}에 대한 특별한 노하우를 알려드리려고 해요.",
            f"많은 분들이 {keyword}를 어려워하시는데, 제가 쉽게 알려드리겠습니다."
        ],
        "공부_교사": [
            f"{persona['experience']}동안 수많은 학생들의 {keyword} 고민을 해결해주면서 깨달은 점이 있습니다.",
            f"진로상담 교사로서 {keyword}에 대한 학생들의 고민을 해결해주면서 발견한 핵심 원리가 있어요.",
            f"{keyword}! 선생님인 저도 처음에는 막막했답니다. 그래서 준비했어요."
        ],
        "직장_멘토": [
            f"20년 넘게 수많은 직장인들의 {keyword} 고민을 상담하면서 발견한 공통점이 있습니다.",
            f"저도 처음 직장생활 할 때는 {keyword} 때문에 정말 힘들었어요. 그때의 경험을 바탕으로 해결책을 찾았습니다.",
            f"수많은 기업에서 강의하면서 모은 {keyword}에 대한 노하우를 공유합니다."
        ]
    }
    
    return random.choice(experiences[persona_name])