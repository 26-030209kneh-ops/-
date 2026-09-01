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
        font-size: 1.5rem;
        font-weight: 800;
        color: #31333F;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
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

# 밸런스 게임 데이터셋
GAMES_DATA = {
    "🍕 음식 밸런스 게임": [
        {"A": "평생 라면 안 먹기", "B": "평생 탄산음료 안 먹기"},
        {"A": "평생 찍먹으로 살기", "B": "평생 부먹으로 살기"},
        {"A": "매일 매운 음식만 먹기", "B": "매일 느끼한 음식만 먹기"},
        {"A": "여름에 미지근한 물 마시기", "B": "겨울에 얼음물 마시기"}
    ],
    "🎮 게임 밸런스 게임": [
        {"A": "평생 핑 500ms로 게임하기", "B": "평생 프레임 15fps로 게임하기"},
        {"A": "팀원 전원 노마이크", "B": "팀원 전원 훈수 두는 잼민이"},
        {"A": "항상 딱 한 끗 차이로 패배하기", "B": "완벽하게 압도당하며 패배하기"},
        {"A": "버그는 없지만 재미없는 게임", "B": "갓겜이지만 버그가 10분마다 터지는 게임"}
    ]
}

# 세션 상태 초기화
if "category" not in st.session_state:
    st.session_state.category = list(GAMES_DATA.keys())[0]
if "index" not in st.session_state:
    st.session_state.index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# 카테고리 변경 시 상태 리셋 함수
def reset_game():
    st.session_state.index = 0
    st.session_state.answers = []

# 메인 헤더
st.title("⚖️ 선택의 갈림길! 밸런스 게임")
st.write("당신의 취향을 선택해보세요.")

# 카테고리 선택
selected_category = st.selectbox(
    "주제를 선택하세요", 
    options=list(GAMES_DATA.keys()),
    on_change=reset_game,
    key="category_select"
)

# 카테고리 업데이트
if selected_category != st.session_state.category:
    st.session_state.category = selected_category
    reset_game()

current_questions = GAMES_DATA[st.session_state.category]

# 진행 상황 표시
progress = (st.session_state.index) / len(current_questions)
st.progress(progress)

# 게임 진행 여부 확인
if st.session_state.index < len(current_questions):
    q = current_questions[st.session_state.index]
    
    st.write(f"**Question {st.session_state.index + 1} / {len(current_questions)}**")
    
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
    st.success("🎉 모든 질문을 완료했습니다!")
    st.subheader("📊 내가 선택한 목록")
    
    for idx, ans in enumerate(st.session_state.answers, 1):
        st.write(f"**Q{idx}.** {ans}")
        
    if st.button("다시 하기", use_container_width=True):
        reset_game()
        st.rerun()
