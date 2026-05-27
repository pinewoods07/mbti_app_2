import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import numpy as np

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🍕 MBTI 피자 토핑 분석기",
    page_icon="🍕",
    layout="centered",
)

# ─────────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.title-box {
    background: linear-gradient(135deg, #ff6b35, #f7c59f, #ff6b35);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(255,107,53,0.3);
}

.title-box h1 {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2.8rem;
    color: white;
    text-shadow: 3px 3px 0px #c0392b;
    margin: 0;
}

.title-box p {
    color: white;
    font-size: 1rem;
    margin: 10px 0 0 0;
    opacity: 0.9;
}

.result-card {
    background: white;
    border: 4px solid #ff6b35;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 8px 8px 0px #ff6b35;
    margin: 20px 0;
}

.topping-emoji {
    font-size: 5rem;
    display: block;
    margin-bottom: 10px;
}

.topping-name {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2rem;
    color: #c0392b;
    margin: 0;
}

.analysis-box {
    background: #fff9f5;
    border-left: 6px solid #ff6b35;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #333;
}

.analysis-box .label {
    font-weight: 700;
    color: #ff6b35;
    font-size: 1.1rem;
}

.verdict-box {
    background: linear-gradient(135deg, #c0392b, #e74c3c);
    color: white;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin: 15px 0;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 4px 4px 0px #922b21;
}

.selectbox-label {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.2rem;
    color: #c0392b;
    margin-bottom: 5px;
}

.footer {
    text-align: center;
    color: #aaa;
    font-size: 0.8rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 2px dashed #ffcba4;
}

div[data-testid="stSelectbox"] > div {
    border: 3px solid #ff6b35 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 피자 그리기 함수
# ─────────────────────────────────────────────
def draw_pizza(mbti):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#fff9f5')

    # ── 공통: 도우 (크러스트) ──
    crust = Circle((0, 0), 1.1, color='#c8832a', zorder=1)
    ax.add_patch(crust)

    # ── 공통: 소스 ──
    sauce = Circle((0, 0), 0.95, color='#c0392b', zorder=2)
    ax.add_patch(sauce)

    # ── 공통: 치즈 베이스 ──
    cheese = Circle((0, 0), 0.88, color='#f5c842', zorder=3)
    ax.add_patch(cheese)

    # ── MBTI별 토핑 그리기 ──
    rng = np.random.default_rng(seed=sum(ord(c) for c in mbti))

    if mbti == "INTJ":
        # 트러플 오일: 우아한 나선형 갈색 점들
        for i in range(12):
            angle = i * (2 * np.pi / 12)
            r = 0.55
            x, y = r * np.cos(angle), r * np.sin(angle)
            dot = Circle((x, y), 0.07, color='#4a2c0a', zorder=5, alpha=0.85)
            ax.add_patch(dot)
        center_dot = Circle((0, 0), 0.09, color='#4a2c0a', zorder=5)
        ax.add_patch(center_dot)
        ax.text(0, 0, '✦', fontsize=14, ha='center', va='center',
                color='#f5c842', zorder=6, fontweight='bold')

    elif mbti == "INTP":
        # 파인애플: 노란 삼각형 조각들
        for i in range(8):
            angle = i * (2 * np.pi / 8) + 0.2
            r = rng.uniform(0.25, 0.65)
            x, y = r * np.cos(angle), r * np.sin(angle)
            triangle = plt.Polygon(
                [[x, y+0.1], [x-0.09, y-0.07], [x+0.09, y-0.07]],
                color='#FFD700', zorder=5, ec='#FFA500', linewidth=1.5
            )
            ax.add_patch(triangle)

    elif mbti == "ENTJ":
        # 살라미: 붉은 원형 슬라이스, 균일 배치
        positions = []
        for ring, count, radius in [(1, 1, 0.0), (2, 6, 0.45), (3, 10, 0.72)]:
            for i in range(count):
                angle = i * (2 * np.pi / count)
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions.append((x, y))
        for (x, y) in positions:
            salami = Circle((x, y), 0.11, color='#8B0000', zorder=5, alpha=0.9)
            ax.add_patch(salami)
            inner = Circle((x, y), 0.05, color='#c0392b', zorder=6)
            ax.add_patch(inner)

    elif mbti == "ENTP":
        # 할라피뇨: 초록 타원형 슬라이스
        for i in range(10):
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0.15, 0.72)
            x, y = r * np.cos(angle), r * np.sin(angle)
            ellipse = patches.Ellipse(
                (x, y), 0.18, 0.08,
                angle=np.degrees(angle),
                color='#228B22', zorder=5, alpha=0.9
            )
            ax.add_patch(ellipse)
            seed_ellipse = patches.Ellipse(
                (x, y), 0.06, 0.03,
                angle=np.degrees(angle),
                color='#90EE90', zorder=6
            )
            ax.add_patch(seed_ellipse)

    elif mbti == "INFJ":
        # 루꼴라: 잎사귀 모양 (작은 녹색 타원 여러 개)
        for i in range(14):
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0.1, 0.75)
            x, y = r * np.cos(angle), r * np.sin(angle)
            leaf = patches.Ellipse(
                (x, y), 0.22, 0.1,
                angle=rng.uniform(0, 180),
                color=rng.choice(['#2d5a1b', '#4a7c2f', '#6aab3f']),
                zorder=5, alpha=0.85
            )
            ax.add_patch(leaf)

    elif mbti == "INFP":
        # 바질: 큰 초록 잎 3~4장
        leaf_positions = [(0.3, 0.35), (-0.4, 0.25), (0.1, -0.45), (-0.25, -0.3)]
        for (lx, ly) in leaf_positions:
            leaf = patches.Ellipse(
                (lx, ly), 0.35, 0.18,
                angle=rng.uniform(20, 160),
                color='#27ae60', zorder=5, alpha=0.9
            )
            ax.add_patch(leaf)
            vein = patches.FancyArrowPatch(
                (lx - 0.12, ly), (lx + 0.12, ly),
                color='#1a7a40', linewidth=1, zorder=6
            )
            ax.add_patch(vein)

    elif mbti == "ENFJ":
        # 모짜렐라: 흰색 불규칙 얼룩들
        for i in range(9):
            angle = i * (2 * np.pi / 9)
            r = rng.uniform(0.2, 0.65)
            x, y = r * np.cos(angle), r * np.sin(angle)
            moz = patches.Ellipse(
                (x, y),
                rng.uniform(0.18, 0.32),
                rng.uniform(0.12, 0.22),
                angle=rng.uniform(0, 180),
                color='#FFFDE7', zorder=5, alpha=0.95,
                ec='#F0E68C', linewidth=1
            )
            ax.add_patch(moz)

    elif mbti == "ENFP":
        # 콘: 노란 작은 알갱이들 (랜덤하게 산포)
        for i in range(30):
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0.05, 0.78)
            x, y = r * np.cos(angle), r * np.sin(angle)
            corn = patches.Ellipse(
                (x, y), 0.1, 0.07,
                angle=rng.uniform(0, 180),
                color='#FFD700', zorder=5,
                ec='#FFA500', linewidth=0.8
            )
            ax.add_patch(corn)

    elif mbti == "ISTJ":
        # 양파: 보라색 링 조각들
        for i in range(8):
            angle = i * (2 * np.pi / 8)
            r = rng.uniform(0.2, 0.65)
            x, y = r * np.cos(angle), r * np.sin(angle)
            onion = patches.Arc(
                (x, y), 0.22, 0.14,
                angle=np.degrees(angle),
                theta1=0, theta2=270,
                color='#9b59b6', linewidth=3, zorder=5
            )
            ax.add_patch(onion)

    elif mbti == "ISFJ":
        # 버섯: 갈색 우산 모양
        mushroom_pos = [
            (0.0, 0.5), (-0.45, 0.2), (0.45, 0.2),
            (0.0, -0.45), (-0.3, -0.55), (0.35, -0.45)
        ]
        for (mx, my) in mushroom_pos:
            cap = patches.Ellipse(
                (mx, my + 0.05), 0.22, 0.13,
                color='#8B4513', zorder=5
            )
            ax.add_patch(cap)
            stem = plt.Polygon(
                [[mx - 0.04, my], [mx + 0.04, my],
                 [mx + 0.03, my - 0.1], [mx - 0.03, my - 0.1]],
                color='#D2B48C', zorder=5
            )
            ax.add_patch(stem)

    elif mbti == "ESTJ":
        # 페퍼로니: 균일하게 배치된 빨간 원
        positions_e = []
        for ring, count, radius in [(1, 1, 0.0), (2, 5, 0.42), (3, 9, 0.70)]:
            for i in range(count):
                angle = i * (2 * np.pi / count) + (0.3 if ring == 3 else 0)
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions_e.append((x, y))
        for (x, y) in positions_e:
            pep = Circle((x, y), 0.12, color='#cc2200', zorder=5)
            ax.add_patch(pep)
            pep_inner = Circle((x, y), 0.06, color='#ff4422', zorder=6)
            ax.add_patch(pep_inner)
            pep_shine = Circle((x + 0.03, y + 0.03), 0.025,
                               color='white', zorder=7, alpha=0.4)
            ax.add_patch(pep_shine)

    elif mbti == "ESFJ":
        # 고구마 무스: 주황 물결 소용돌이
        theta = np.linspace(0, 4 * np.pi, 300)
        r_spiral = theta / (4 * np.pi) * 0.78
        x_s = r_spiral * np.cos(theta)
        y_s = r_spiral * np.sin(theta)
        ax.plot(x_s, y_s, color='#FF8C00', linewidth=6, zorder=5, alpha=0.8)
        ax.plot(x_s, y_s, color='#FFD580', linewidth=2, zorder=6, alpha=0.6)

    elif mbti == "ISTP":
        # 올리브: 검정/초록 링 모양
        olive_pos = [
            (0.1, 0.5), (-0.5, 0.1), (0.45, -0.2),
            (-0.15, -0.5), (0.55, 0.35), (-0.4, -0.45)
        ]
        colors = ['#2C2C2C', '#3B7A3B', '#2C2C2C', '#3B7A3B', '#2C2C2C', '#3B7A3B']
        for (ox, oy), col in zip(olive_pos, colors):
            outer = Circle((ox, oy), 0.11, color=col, zorder=5)
            ax.add_patch(outer)
            inner = Circle((ox, oy), 0.05, color='#cc2200', zorder=6)
            ax.add_patch(inner)

    elif mbti == "ISFP":
        # 선드라이 토마토: 진한 빨간 타원
        for i in range(8):
            angle = i * (2 * np.pi / 8) + 0.4
            r = rng.uniform(0.2, 0.65)
            x, y = r * np.cos(angle), r * np.sin(angle)
            tmt = patches.Ellipse(
                (x, y), 0.2, 0.13,
                angle=rng.uniform(0, 180),
                color='#8B0000', zorder=5, alpha=0.9
            )
            ax.add_patch(tmt)
            tmt2 = patches.Ellipse(
                (x, y), 0.1, 0.06,
                angle=rng.uniform(0, 180),
                color='#cc3300', zorder=6, alpha=0.7
            )
            ax.add_patch(tmt2)

    elif mbti == "ESTP":
        # 베이컨: 구불구불한 줄무늬
        for i in range(5):
            y_base = -0.6 + i * 0.28
            x_wave = np.linspace(-0.75, 0.75, 100)
            y_wave = y_base + 0.07 * np.sin(x_wave * 8 + i)
            # 갈색 굵은 선
            ax.plot(x_wave, y_wave, color='#8B3A3A',
                    linewidth=7, zorder=5, alpha=0.85,
                    solid_capstyle='round')
            # 연한 줄
            ax.plot(x_wave, y_wave + 0.015, color='#CD853F',
                    linewidth=3, zorder=6, alpha=0.6,
                    solid_capstyle='round')

    elif mbti == "ESFP":
        # 케첩: 지그재그 드리즐 패턴
        x_drizzle = np.linspace(-0.75, 0.75, 200)
        for offset in [-0.3, 0.0, 0.3]:
            y_drizzle = offset + 0.18 * np.sin(x_drizzle * 10)
            ax.plot(x_drizzle, y_drizzle, color='#cc0000',
                    linewidth=3, zorder=5, alpha=0.85,
                    solid_capstyle='round')
        # 작은 케첩 방울들
        for i in range(6):
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0.1, 0.6)
            x, y = r * np.cos(angle), r * np.sin(angle)
            drop = Circle((x, y), 0.05, color='#ee0000', zorder=6, alpha=0.8)
            ax.add_patch(drop)

    # ── 공통: 크러스트 테두리 강조 ──
    crust_ring = Circle((0, 0), 1.1, fill=False,
                         ec='#a0611a', linewidth=4, zorder=7)
    ax.add_patch(crust_ring)

    # ── MBTI 텍스트 ──
    ax.text(0, -1.22, mbti, fontsize=15, ha='center', va='center',
            color='#c0392b', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9f5',
                      edgecolor='#ff6b35', linewidth=2))

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# 데이터: MBTI → 피자 토핑 정보
# ─────────────────────────────────────────────
PIZZA_DATA = {
    "INTJ": {
        "topping": "트러플 오일",
        "emoji": "🫙",
        "oneliner": "나 없으면 이 피자 그냥 치킨이야",
        "analysis": (
            "트러플 오일은 고급스럽고 독특한 향을 지니고 있으며, "
            "혼자 있어야 진정한 가치를 발휘합니다. "
            "처음엔 '이게 뭐야' 싶지만, 한 번 맛을 알면 헤어날 수 없죠. "
            "대중적이지 않아도 본인은 전혀 신경 쓰지 않습니다. "
            "오히려 '몰라도 돼'라고 생각하고 있어요."
        ),
        "verdict": "🔬 결론: 당신은 피자계의 석학입니다. 하지만 친구가 없어요.",
        "good_mbti": "ENFJ",
        "good_topping": "모짜렐라",
        "good_reason": "모짜렐라가 받쳐줘야 트러플이 빛남",
        "bad_mbti": "ESFP",
        "bad_topping": "케첩",
        "bad_reason": "당신의 깊이를 케첩이 이해할 수 없음",
    },
    "INTP": {
        "topping": "파인애플",
        "emoji": "🍍",
        "oneliner": "나는 맞아, 그게 틀린 거야",
        "analysis": (
            "파인애플 피자는 전 세계에서 가장 논쟁적인 존재입니다. "
            "본인은 논리적으로 '과일과 고기의 조합은 타당하다'고 생각하지만 "
            "주변 모두가 이해 못 합니다. "
            "억울하죠? 맞아요. 근데 본인도 왜 억울한지 설명하다가 지쳐요."
        ),
        "verdict": "🤔 결론: 당신은 옳습니다. 그래서 외롭습니다.",
        "good_mbti": "ENFP",
        "good_topping": "할라피뇨",
        "good_reason": "둘 다 '왜 저걸 넣어?' 소리 들음. 동병상련",
        "bad_mbti": "ESTJ",
        "bad_topping": "살라미",
        "bad_reason": "살라미는 전통을 중시함. 파인애플을 절대 용납 안 함",
    },
    "ENTJ": {
        "topping": "살라미",
        "emoji": "🍖",
        "oneliner": "내가 없으면 이 피자 무너져",
        "analysis": (
            "살라미는 피자의 실질적 지배자입니다. "
            "빠짐없이 균일하게 배치되고, 강하고 자신감 넘치는 맛. "
            "누가 토핑 구성 설명해달라고 하면 살라미가 제일 먼저 튀어나옵니다. "
            "리더십? 타고났죠. 부담스럽다고요? 그게 매력입니다."
        ),
        "verdict": "💼 결론: 당신은 피자 CEO입니다. 직원들은 좀 힘듭니다.",
        "good_mbti": "INTJ",
        "good_topping": "트러플 오일",
        "good_reason": "서로 고급진 거 알아봄. 최강 콤비",
        "bad_mbti": "INFP",
        "bad_topping": "바질",
        "bad_reason": "바질은 감성을 원함. 살라미는 성과를 원함",
    },
    "ENTP": {
        "topping": "할라피뇨",
        "emoji": "🌶️",
        "oneliner": "어? 왜 매워? 원래 이래",
        "analysis": (
            "할라피뇨는 예측 불가능합니다. "
            "어디서 터질지 모르고, 자꾸 자극하고, 처음엔 괜찮다가 나중에 후회하게 만들죠. "
            "하지만 없으면 심심하고, 있으면 대화가 생깁니다. "
            "피자에서 제일 재밌는 토핑? 단연 할라피뇨."
        ),
        "verdict": "💥 결론: 당신은 피자계의 어그로입니다. 근데 사랑받아요.",
        "good_mbti": "INTP",
        "good_topping": "파인애플",
        "good_reason": "둘 다 논란 제조기. 같이 있으면 피자가 레전드됨",
        "bad_mbti": "ISTJ",
        "bad_topping": "양파",
        "bad_reason": "양파는 규칙적이고 성실함. 할라피뇨의 카오스를 감당 못 함",
    },
    "INFJ": {
        "topping": "루꼴라",
        "emoji": "🌿",
        "oneliner": "나를 이해하는 사람이 없어",
        "analysis": (
            "루꼴라는 피자 위에서 혼자 고고히 존재합니다. "
            "쌉싸름한 맛은 깊이 있는 내면을 상징하고, "
            "아무도 처음엔 루꼴라를 주문하지 않지만 "
            "먹어본 사람은 '이게 없으면 허전해'라고 합니다. "
            "당신도 그런 사람입니다. 희귀하고 소중해요."
        ),
        "verdict": "🌙 결론: 당신은 피자계의 예언자입니다. 아무도 안 믿어줘요.",
        "good_mbti": "ENFP",
        "good_topping": "할라피뇨",
        "good_reason": "ENFP가 루꼴라를 세상에 알려줌",
        "bad_mbti": "ESTP",
        "bad_topping": "페퍼로니",
        "bad_reason": "페퍼로니는 깊이 따위 관심 없음",
    },
    "INFP": {
        "topping": "바질",
        "emoji": "🌱",
        "oneliner": "이 피자에 담긴 감성을 느껴봐",
        "analysis": (
            "바질은 피자의 감성 담당입니다. "
            "비주얼은 최고고, 향은 시적이며, 존재 자체로 피자를 예술로 만듭니다. "
            "하지만 열에 약하고, 너무 일찍 올리면 시들어버립니다. "
            "섬세하게 다뤄야 해요. 당신도 마찬가지입니다."
        ),
        "verdict": "🎨 결론: 당신은 피자계의 시인입니다. 배는 안 불러요.",
        "good_mbti": "ENFJ",
        "good_topping": "모짜렐라",
        "good_reason": "모짜렐라가 바질을 포근하게 감싸줌",
        "bad_mbti": "ENTJ",
        "bad_topping": "살라미",
        "bad_reason": "살라미는 감성을 KPI로 환산하려 함",
    },
    "ENFJ": {
        "topping": "모짜렐라",
        "emoji": "🧀",
        "oneliner": "나 없으면 이거 그냥 토마토 토스트야",
        "analysis": (
            "모짜렐라는 피자의 어머니입니다. "
            "모든 토핑을 감싸 안고, 없으면 피자가 아닙니다. "
            "누구와도 잘 어울리고, 존재 자체가 하나로 묶는 힘. "
            "당신이 없는 모임은 어딘가 허전합니다. "
            "모두가 당신을 기본값으로 여기는 게 조금 억울하지만, "
            "그래도 사랑받잖아요."
        ),
        "verdict": "🤝 결론: 당신은 피자계의 총무입니다. 수고 많으세요.",
        "good_mbti": "INTJ",
        "good_topping": "트러플 오일",
        "good_reason": "트러플의 빛을 모짜렐라가 받쳐줌",
        "bad_mbti": "INTP",
        "bad_topping": "파인애플",
        "bad_reason": "파인애플이 모짜렐라를 질척하게 만듦",
    },
    "ENFP": {
        "topping": "콘 (옥수수)",
        "emoji": "🌽",
        "oneliner": "어? 나 여기 있어요!! 안 보여요??",
        "analysis": (
            "콘은 피자에서 가장 밝고 에너지 넘치는 토핑입니다. "
            "달콤하고, 통통 튀고, 어디서든 눈에 띕니다. "
            "진지한 피자에 갑자기 나타나서 분위기를 환기시키죠. "
            "싫어하는 사람도 있지만 좋아하는 사람은 정말 좋아합니다. "
            "중간이 없어요."
        ),
        "verdict": "⚡ 결론: 당신은 피자계의 에너지 드링크입니다.",
        "good_mbti": "INFJ",
        "good_topping": "루꼴라",
        "good_reason": "콘이 루꼴라를 세상 밖으로 꺼내줌",
        "bad_mbti": "INTJ",
        "bad_topping": "트러플 오일",
        "bad_reason": "트러플은 콘의 에너지를 '유치하다'고 판단함",
    },
    "ISTJ": {
        "topping": "양파",
        "emoji": "🧅",
        "oneliner": "나는 항상 여기 있었어. 원래부터.",
        "analysis": (
            "양파는 피자의 전통 그 자체입니다. "
            "화려하지 않고, 튀지 않으며, 묵묵히 제 역할을 합니다. "
            "빠지면 '어 뭔가 허전한데?'라는 말이 나오지만 "
            "있을 때는 아무도 언급하지 않습니다. "
            "하지만 양파 없는 피자는... 그냥 좀 심심해요."
        ),
        "verdict": "📋 결론: 당신은 피자계의 공무원입니다. 연금 나옵니다.",
        "good_mbti": "ISFJ",
        "good_topping": "버섯",
        "good_reason": "둘 다 묵묵히 자기 자리 지킴. 환상의 팀워크",
        "bad_mbti": "ENTP",
        "bad_topping": "할라피뇨",
        "bad_reason": "할라피뇨의 카오스를 양파는 절대 이해 못 함",
    },
    "ISFJ": {
        "topping": "버섯",
        "emoji": "🍄",
        "oneliner": "나 괜찮아... 정말로.",
        "analysis": (
            "버섯은 눈에 띄지 않지만 피자의 깊은 맛을 담당합니다. "
            "혼자선 뭔가 부족한 것 같지만, "
            "없으면 맛이 확 떨어지는 그런 존재. "
            "자기 희생적이고 다른 토핑들과 조화를 이루기 위해 "
            "자신의 맛을 죽이기도 합니다. "
            "제발 좀 자기 자신을 위해 살아요."
        ),
        "verdict": "🍄 결론: 당신은 피자계의 서브 캐릭터입니다. 사실 주인공이에요.",
        "good_mbti": "ISTJ",
        "good_topping": "양파",
        "good_reason": "서로 묵묵히 서포트. 말 안 해도 통함",
        "bad_mbti": "ENTJ",
        "bad_topping": "살라미",
        "bad_reason": "살라미가 버섯의 자리를 계속 빼앗음",
    },
    "ESTJ": {
        "topping": "페퍼로니",
        "emoji": "🍕",
        "oneliner": "나는 규칙대로 배치된다. 항상.",
        "analysis": (
            "페퍼로니는 피자의 상징입니다. "
            "완벽하게 균일한 간격, 빠짐없는 배치, 강렬한 존재감. "
            "피자 하면 페퍼로니, 페퍼로니 하면 피자. "
            "전통을 중시하고 효율을 사랑하며, "
            "왜 파인애플이 피자 위에 있는지 이해하지 못합니다."
        ),
        "verdict": "📐 결론: 당신은 피자계의 팀장입니다. 칼퇴는 없어요.",
        "good_mbti": "ISTJ",
        "good_topping": "양파",
        "good_reason": "둘 다 규칙과 전통 존중. 완벽한 조합",
        "bad_mbti": "INTP",
        "bad_topping": "파인애플",
        "bad_reason": "파인애플은 페퍼로니의 세계관을 파괴함",
    },
    "ESFJ": {
        "topping": "고구마 무스",
        "emoji": "🍠",
        "oneliner": "다들 좋아하지? 맞지? 맞지???",
        "analysis": (
            "고구마 무스는 대한민국 피자의 국민 토핑입니다. "
            "달달하고, 부드럽고, 거부감이 없으며, 모두가 좋아합니다. "
            "인정받기 위해 태어난 존재. "
            "단 한 명이라도 '별로'라고 하면 하루 종일 마음에 걸립니다. "
            "그러지 않아도 돼요, 당신은 충분히 사랑받고 있어요."
        ),
        "verdict": "💛 결론: 당신은 피자계의 인싸입니다. 좋아요 1000개.",
        "good_mbti": "ENFJ",
        "good_topping": "모짜렐라",
        "good_reason": "둘 다 분위기 메이커. 완벽한 파티 피자",
        "bad_mbti": "INTJ",
        "bad_topping": "트러플 오일",
        "bad_reason": "트러플은 대중성을 경멸함",
    },
    "ISTP": {
        "topping": "올리브",
        "emoji": "🫒",
        "oneliner": "나 여기 있는데 왜 아무도 몰라",
        "analysis": (
            "올리브는 과소평가된 토핑입니다. "
            "싫어하는 사람은 골라내고, 좋아하는 사람은 진심으로 좋아하는 양극단. "
            "말이 없고, 차갑고, 독립적이며, 자기 페이스를 절대 잃지 않습니다. "
            "손재주가 좋아서 피자 칼 다루는 솜씨가 남다릅니다. "
            "아마도."
        ),
        "verdict": "🔧 결론: 당신은 피자계의 장인입니다. 과묵한 천재.",
        "good_mbti": "ISTP",
        "good_topping": "올리브",
        "good_reason": "둘이 말 없이 앉아서 피자 먹음. 완벽한 저녁",
        "bad_mbti": "ESFJ",
        "bad_topping": "고구마 무스",
        "bad_reason": "고구마 무스가 계속 '재밌지?' 물어봄",
    },
    "ISFP": {
        "topping": "선드라이 토마토",
        "emoji": "🍅",
        "oneliner": "나는 그냥 예쁘고 싶어",
        "analysis": (
            "선드라이 토마토는 피자에서 가장 감각적인 토핑입니다. "
            "색깔도 예쁘고, 맛도 독특하고, 비주얼에 진심. "
            "화려한 걸 좋아하지만 조용히 즐깁니다. "
            "자기 표현이 강하지만 강요하지 않아요. "
            "당신이 만든 피자 인스타 사진이 제일 맛있어 보입니다."
        ),
        "verdict": "🎭 결론: 당신은 피자계의 인스타그래머입니다. 팔로워 많음.",
        "good_mbti": "INFP",
        "good_topping": "바질",
        "good_reason": "감성 토핑 동맹. 피자가 예술이 됨",
        "bad_mbti": "ESTJ",
        "bad_topping": "페퍼로니",
        "bad_reason": "페퍼로니는 예쁜 것보다 효율을 원함",
    },
    "ESTP": {
        "topping": "베이컨",
        "emoji": "🥓",
        "oneliner": "일단 올리고 생각은 나중에",
        "analysis": (
            "베이컨은 피자의 행동파입니다. "
            "생각보다 먼저 움직이고, 일단 올리면 무조건 맛있습니다. "
            "계획? 없어요. 그냥 하면 되거든요. "
            "자신감이 넘치고 어디서나 존재감을 뿜으며, "
            "파티에서 제일 먼저 없어지는 토핑."
        ),
        "verdict": "🏎️결론: 당신은 피자계의 스턴트맨입니다. 짜릿해요.",
        "good_mbti": "ENFP",
        "good_topping": "콘",
        "good_reason": "둘 다 에너지 폭발. 피자가 축제가 됨",
        "bad_mbti": "INFJ",
        "bad_topping": "루꼴라",
        "bad_reason": "루꼴라의 감성을 베이컨이 이해할 수 없음",
    },
    "ESFP": {
        "topping": "케첩 드리즐",
        "emoji": "🥫",
        "oneliner": "나 왔어~~ 파티 시작이야!!",
        "analysis": (
            "케첩 드리즐은 피자의 파티 메이커입니다. "
            "없어도 되는데 있으면 기분이 달라지고, "
            "뿌리면 일단 기분은 좋아집니다. "
            "진지함은 1도 없고, 현재를 즐기며, "
            "내일 걱정은 내일의 내가 합니다. "
            "오늘 이 피자가 최고의 피자예요. 늘 그렇듯이."
        ),
        "verdict": "🎉 결론: 당신은 피자계의 DJ입니다. 항상 신나요.",
        "good_mbti": "ESTP",
        "good_topping": "베이컨",
        "good_reason": "둘 다 현재 충실. 최고의 파티 피자",
        "bad_mbti": "INTJ",
        "bad_topping": "트러플 오일",
        "bad_reason": "트러플은 케첩을 '격이 다르다'며 무시함",
    },
}

MBTI_LIST = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>🍕 MBTI 피자 토핑 분석기</h1>
    <p>당신의 MBTI는 어떤 피자 토핑일까요? 진지하게 분석해드립니다. (거짓말)</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="selectbox-label">👇 당신의 MBTI를 선택하세요</p>',
            unsafe_allow_html=True)
selected = st.selectbox("", ["-- 선택 --"] + MBTI_LIST, label_visibility="collapsed")

if selected != "-- 선택 --":
    data = PIZZA_DATA[selected]

    # ── 결과 카드 ──
    st.markdown(f"""
    <div class="result-card">
        <span class="topping-emoji">{data['emoji']}</span>
        <p style="color:#888; font-size:0.9rem; margin:0;">당신({selected})은...</p>
        <p class="topping-name">"{data['topping']}"</p>
        <p style="color:#555; font-style:italic; margin-top:10px;">"{data['oneliner']}"</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 🍕 피자 그림 ──
    st.markdown("""
    <p style="font-family:'Black Han Sans',sans-serif; font-size:1.1rem;
              color:#c0392b; margin:20px 0 5px 0;">🎨 당신의 피자</p>
    """, unsafe_allow_html=True)

    fig = draw_pizza(selected)
    st.pyplot(fig)
    plt.close(fig)

    # ── 분석 박스 ──
    st.markdown(f"""
    <div class="analysis-box">
        <p class="label">🔍 심층 분석 (매우 과학적)</p>
        <p>{data['analysis']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 판결문 ──
    st.markdown(f"""
    <div class="verdict-box">
        {data['verdict']}
    </div>
    """, unsafe_allow_html=True)

    # ── 궁합 ──
    st.markdown("""
    <p style="font-family:'Black Han Sans',sans-serif; font-size:1.1rem;
              color:#c0392b; margin:20px 0 10px 0;">🍕 토핑 궁합</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"""
**✅ 최고의 조합**

**{data['good_mbti']}** ({data['good_topping']})

{data['good_reason']}
        """)
    with col2:
        st.error(f"""
**❌ 최악의 조합**

**{data['bad_mbti']}** ({data['bad_topping']})

{data['bad_reason']}
        """)

    st.divider()

    # ── 전체 토핑 지도 ──
    with st.expander("🍕 전체 토핑 지도 보기"):
        cols = st.columns(4)
        for i, (mbti, info) in enumerate(PIZZA_DATA.items()):
            with cols[i % 4]:
                is_me = "⭐ " if mbti == selected else ""
                st.markdown(f"""
                <div style="background:{'#fff3e0' if mbti == selected else '#f9f9f9'};
                            border:2px solid {'#ff6b35' if mbti == selected else '#eee'};
                            border-radius:10px; padding:10px; text-align:center;
                            margin-bottom:10px;">
                    <div style="font-size:1.8rem;">{info['emoji']}</div>
                    <div style="font-weight:700; color:#c0392b;">{is_me}{mbti}</div>
                    <div style="font-size:0.75rem; color:#666;">{info['topping']}</div>
                </div>
                """, unsafe_allow_html=True)

# ── 푸터 ──
st.markdown("""
<div class="footer">
    🍕 이 분석은 100% 비과학적입니다. 그래도 맞는 것 같죠? | Made with Streamlit
</div>
""", unsafe_allow_html=True)
