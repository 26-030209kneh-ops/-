import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="밸런스 게임", page_icon="⚖️", layout="centered")

# CSS 스타일링 (카드 디자인 및 커스텀 버튼)
st.markdown("""
    <style>
    .card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #f0f2f6;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #ff4b4b;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #888;
        margin-bottom: 10px;
    }
    .card-content {
        font-size: 1.4rem;
        font-weight: 800;
        color: #31333F;
        min-height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        word-break: keep-all;
    }
    .vs-badge {
        font-size: 2rem;
        font-weight: 900;
        color: #ff4b4b;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 밸런스 게임 대용량 데이터 풀 (풀에서 10개씩 무작위 추출)
RAW_GAMES_DATA = {
    "🍕 음식 밸런스 게임": [
        {"A": "평생 라면 안 먹기", "B": "평생 탄산음료 안 먹기"},
        {"A": "평생 찍먹으로 살기", "B": "평생 부먹으로 살기"},
        {"A": "매일 매운 음식만 먹기", "B": "매일 느끼한 음식만 먹기"},
        {"A": "여름에 미지근한 물 마시기", "B": "겨울에 얼음물 마시기"},
        {"A": "평생 고기 못 먹기", "B": "평생 밀가루 못 먹기"},
        {"A": "탄 음식 먹기", "B": "덜 익은 음식 먹기"},
        {"A": "평생 밥 없이 반찬만 먹기", "B": "평생 반찬 없이 밥만 먹기"},
        {"A": "짜장면 없는 짬뽕 세상", "B": "짬뽕 없는 짜장면 세상"},
        {"A": "치킨 양념만 먹기", "B": "치킨 후라이드만 먹기"},
        {"A": "평생 김치 없이 먹기", "B": "평생 단무지 없이 먹기"},
        {"A": "피자 테두리 크러스트만 먹기", "B": "토핑 부분만 먹기"},
        {"A": "평생 숟가락만 사용하기", "B": "평생 젓가락만 사용하기"},
        {"A": "모든 음식에 와사비 넣기", "B": "모든 음식에 캡사이신 넣기"},
        {"A": "아이스 아메리카노에 핫초코 파우더 섞기", "B": "따뜻한 라떼에 얼음 넣어 먹기"},
        {"A": "평생 민트초코만 먹기", "B": "평생 솔의눈만 마시기"}
    ],
    "🎮 게임 밸런스 게임": [
        {"A": "평생 핑 500ms로 게임하기", "B": "평생 프레임 15fps로 게임하기"},
        {"A": "팀원 전원 노마이크", "B": "팀원 전원 훈수 두는 잼민이"},
        {"A": "항상 딱 한 끗 차이로 패배하기", "B": "완벽하게 압도당하며 패배하기"},
        {"A": "버그는 없지만 재미없는 게임", "B": "갓겜이지만 버그가 10분마다 터지는 게임"},
        {"A": "모든 인게임 아이템 무제한 (골드/캐시)", "B": "세계 랭킹 1위 타이틀 획득"},
        {"A": "실수로 내 중요 아이템 삭제하기", "B": "팀원이 내 아이템 훔쳐가기"},
        {"A": "평생 싱글 플레이 게임만 하기", "B": "평생 멀티 플레이 게임만 하기"},
        {"A": "올스킵 불가 튜토리얼 3시간", "B": "엔딩 스킵 불가 엔딩크레딧 2시간"},
        {"A": "자동 전투만 있는 게임", "B": "컨트롤 너무 어려워서 손가락 아픈 게임"},
        {"A": "내가 빡겜할 때 렉 걸리기", "B": "막타 칠 때 화면 튕기기"},
        {"A": "친구들이랑 할 때 항상 짐", "B": "모르는 사람이랑 할 때 항상 이김"},
        {"A": "게임 중 엄마가 등짝 스매시", "B": "게임 중 정전되기"},
        {"A": "캐릭터가 내 얼굴로 고정", "B": "캐릭터 목소리가 내 목소리로 고정"},
        {"A": "패치할 때마다 사기 캐릭터 떡락", "B": "내가 접으면 그 캐릭터 떡상"},
        {"A": "평생 조이스틱으로만 FPS 하기", "B": "평생 마우스로만 철권 하기"}
    ]
}

MAX_ROUNDS = 10  # 라운드 수를 10판으로 지정

# 세션 상태 초기화 및 질문 랜덤 추출 함수
def start_new_game(category_name):
    questions_pool = RAW_GAMES_DATA[category_name]
    # 질문 수가 10개보다 작을 경우를 대비한 안전 조치
    sample_size = min(MAX_ROUNDS, len(questions_pool))
    st.session_state.current_questions = random.sample(questions_pool, sample_size)
    st.session_state.index = 0
    st.session_state.answers = []

if "category" not in st.session_state:
    st.session_state.category = list(RAW_GAMES_DATA.keys())[0]
    start_new_game(st.session_state.category)

# 카테고리 변경 이벤트
def on_category_change():
    st.session_state.category = st.session_state.category_select
    start_new_game(st.session_state.category)

# 메인 헤더
st.title("⚖️ 선택의 갈림길! 밸런스 게임")
st.write("10개의 무작위 질문으로 당신의 취향을 테스트해보세요.")

# 카테고리 선택
st.selectbox(
    "주제를 선택하세요", 
    options=list(RAW_GAMES_DATA.keys()),
    key="category_select",
    on_change=on_category_change
)

questions = st.session_state.current_questions
total_rounds = len(questions)

# 진행 상황 표시 (진행바)
progress = (st.session_state.index) / total_rounds
st.progress(progress)

# 게임 진행 여부 확인
if st.session_state.index < total_rounds:
    q = questions[st.session_state.index]
    
    st.write(f"**Round {st.session_state.index + 1} / {total_rounds}**")
    
    col1, col_vs, col2 = st.columns([4, 1, 4])
    
    # Option A 카드
    with col1:
        st.markdown(f"""
            <div class="card">
                <div class="card-title">OPTION A</div>
                <div class="card-content">{q['A']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("A 선택", key="btn_a", use_container_width=True):
            st.session_state.answers.append(q['A'])
            st.session_state.index += 1
            st.rerun()

    # VS 표시
    with col_vs:
        st.markdown("<div class='vs-badge'>VS</div>", unsafe_allow_html=True)

    # Option B 카드
    with col2:
        st.markdown(f"""
            <div class="card">
                <div class="card-title">OPTION B</div>
                <div class="card-content">{q['B']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("B 선택", key="btn_b", use_container_width=True):
            st.session_state.answers.append(q['B'])
            st.session_state.index += 1
            st.rerun()

else:
    # 최종 결과 화면
    st.balloons()
    st.success("🎉 10라운드 밸런스 게임 완주를 축하합니다!")
    st.subheader("📊 내가 선택한 최종 결과")
    
    for idx, ans in enumerate(st.session_state.answers, 1):
        st.write(f"**Round {idx}.** {ans}")
        
    if st.button("새로운 게임 시작하기 (랜덤 재구성)", use_container_width=True):
        start_new_game(st.session_state.category)
        st.rerun()
