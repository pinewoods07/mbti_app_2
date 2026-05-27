import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np

st.set_page_config(
    page_title="🍕 MBTI 피자 토핑 분석기",
    page_icon="🍕",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.title-box {
    background: linear-gradient(135deg, #ff6b35, #f7c59f, #ff6b35);
    border-radius: 20px; padding: 30px; text-align: center;
    margin-bottom: 30px; box-shadow: 0 8px 32px rgba(255,107,53,0.3);
}
.title-box h1 {
    font-family: 'Black Han Sans', sans-serif; font-size: 2.8rem;
    color: white; text-shadow: 3px 3px 0px #c0392b; margin: 0;
}
.title-box p { color: white; font-size: 1rem; margin: 10px 0 0 0; opacity: 0.9; }
.result-card {
    background: white; border: 4px solid #ff6b35; border-radius: 20px;
    padding: 30px; text-align: center; box-shadow: 8px 8px 0px #ff6b35; margin: 20px 0;
}
.topping-emoji { font-size: 5rem; display: block; margin-bottom: 10px; }
.topping-name { font-family: 'Black Han Sans', sans-serif; font-size: 2rem; color: #c0392b; margin: 0; }
.analysis-box {
    background: #fff9f5; border-left: 6px solid #ff6b35; border-radius: 10px;
    padding: 20px; margin: 20px 0; font-size: 0.95rem; line-height: 1.8; color: #333;
}
.analysis-box .label { font-weight: 700; color: #ff6b35; font-size: 1.1rem; }
.verdict-box {
    background: linear-gradient(135deg, #c0392b, #e74c3c); color: white;
    border-radius: 15px; padding: 20px; text-align: center; margin: 15px 0;
    font-size: 1.1rem; font-weight: 700; box-shadow: 4px 4px 0px #922b21;
}
.selectbox-label { font-family: 'Black Han Sans', sans-serif; font-size: 1.2rem; color: #c0392b; margin-bottom: 5px; }
.footer {
    text-align: center; color: #aaa; font-size: 0.8rem;
    margin-top: 40px; padding: 20px; border-top: 2px dashed #ffcba4;
}
div[data-testid="stSelectbox"] > div { border: 3px solid #ff6b35 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 피자 그리기 함수 (대폭 업그레이드)
# ─────────────────────────────────────────────
def draw_pizza(mbti):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFF8F0')

    rng = np.random.default_rng(seed=sum(ord(c) for c in mbti))

    # ══ 크러스트 그라데이션 효과 (여러 겹) ══
    for r, c in [(1.18,'#7B3F00'),(1.13,'#A0522D'),(1.08,'#C68642'),(1.02,'#D4A055')]:
        ax.add_patch(Circle((0,0), r, color=c, zorder=1))

    # 크러스트 위 점점이 (구운 느낌)
    for i in range(18):
        angle = i * (2*np.pi/18) + rng.uniform(-0.1, 0.1)
        bx = 1.1 * np.cos(angle)
        by = 1.1 * np.sin(angle)
        ax.add_patch(Circle((bx, by), rng.uniform(0.03,0.055),
                             color='#8B4513', zorder=2, alpha=0.6))

    # ══ 토마토 소스 (여러 겹으로 자연스럽게) ══
    ax.add_patch(Circle((0,0), 0.97, color='#B22222', zorder=3))
    ax.add_patch(Circle((0,0), 0.93, color='#CC2222', zorder=3))
    # 소스 얼룩
    for _ in range(8):
        angle = rng.uniform(0, 2*np.pi)
        r = rng.uniform(0.1, 0.7)
        ax.add_patch(patches.Ellipse(
            (r*np.cos(angle), r*np.sin(angle)),
            rng.uniform(0.1,0.25), rng.uniform(0.08,0.18),
            angle=rng.uniform(0,180),
            color='#AA1111', zorder=3, alpha=0.4))

    # ══ 치즈 베이스 (불규칙한 얼룩 느낌) ══
    ax.add_patch(Circle((0,0), 0.88, color='#F4C430', zorder=4))
    # 치즈 기포/얼룩
    for _ in range(12):
        angle = rng.uniform(0, 2*np.pi)
        r = rng.uniform(0.05, 0.72)
        ax.add_patch(patches.Ellipse(
            (r*np.cos(angle), r*np.sin(angle)),
            rng.uniform(0.06,0.18), rng.uniform(0.05,0.13),
            angle=rng.uniform(0,180),
            color=rng.choice(['#E8B800','#FFD700','#F5D020','#EEC900']),
            zorder=4, alpha=0.6))

    # ══ 피자 슬라이스 구분선 ══
    for i in range(8):
        angle = i * (np.pi / 4)
        ax.plot([0, 0.97*np.cos(angle)], [0, 0.97*np.sin(angle)],
                color='#C8A000', linewidth=0.8, zorder=5, alpha=0.5)

    # ══ MBTI별 토핑 ══

    if mbti == "INTJ":
        # 트러플 오일: 황금빛 오일 방울 + 나선형 배치
        theta = np.linspace(0, 3*np.pi, 200)
        r_sp = theta / (3*np.pi) * 0.75
        ax.plot(r_sp*np.cos(theta), r_sp*np.sin(theta),
                color='#8B6914', linewidth=1.5, zorder=6, alpha=0.4, linestyle='--')
        for i in range(14):
            angle = i * (2*np.pi/14)
            r = 0.52
            x, y = r*np.cos(angle), r*np.sin(angle)
            # 오일 방울 (광택 효과)
            ax.add_patch(Circle((x,y), 0.075, color='#3D1C00', zorder=7, alpha=0.9))
            ax.add_patch(Circle((x,y), 0.045, color='#6B3A2A', zorder=8))
            ax.add_patch(Circle((x+0.02,y+0.02), 0.02, color='white', zorder=9, alpha=0.5))
        ax.add_patch(Circle((0,0), 0.09, color='#3D1C00', zorder=7))
        ax.add_patch(Circle((0.03,0.03), 0.03, color='white', zorder=8, alpha=0.5))

    elif mbti == "INTP":
        # 파인애플: 노란 삼각형 + 갈색 테두리, 풍성하게
        for i in range(14):
            angle = rng.uniform(0, 2*np.pi)
            r = rng.uniform(0.1, 0.72)
            x, y = r*np.cos(angle), r*np.sin(angle)
            size = rng.uniform(0.07, 0.13)
            tri = plt.Polygon(
                [[x, y+size*1.3],
                 [x-size, y-size*0.7],
                 [x+size, y-size*0.7]],
                color='#FFD700', zorder=7,
                ec='#B8860B', linewidth=1.5)
            ax.add_patch(tri)
            # 파인애플 격자 무늬
            ax.plot([x, x], [y-size*0.3, y+size*0.8],
                    color='#B8860B', linewidth=0.8, zorder=8, alpha=0.7)

    elif mbti == "ENTJ":
        # 살라미: 균일 배치, 테두리+광택+기름기
        positions = [(0,0,0.0)]
        for count, radius in [(6,0.44),(10,0.73)]:
            for i in range(count):
                angle = i*(2*np.pi/count)
                positions.append((radius*np.cos(angle), radius*np.sin(angle), angle))
        for (x,y,a) in positions:
            ax.add_patch(Circle((x,y), 0.115, color='#5C0A0A', zorder=7))
            ax.add_patch(Circle((x,y), 0.095, color='#8B0000', zorder=8))
            ax.add_patch(Circle((x,y), 0.055, color='#A52020', zorder=9))
            # 기름기 방울
            for j in range(4):
                a2 = j*(np.pi/2)+0.3
                ax.add_patch(Circle((x+0.06*np.cos(a2),y+0.06*np.sin(a2)),
                                    0.015, color='#FF6B35', zorder=10, alpha=0.6))
            ax.add_patch(Circle((x+0.04,y+0.04), 0.025, color='white', zorder=10, alpha=0.35))

    elif mbti == "ENTP":
        # 할라피뇨: 진짜 고추 슬라이스처럼 (링 모양 + 씨앗)
        for i in range(13):
            angle_pos = rng.uniform(0, 2*np.pi)
            r = rng.uniform(0.1, 0.75)
            x, y = r*np.cos(angle_pos), r*np.sin(angle_pos)
            rot = rng.uniform(0, 180)
            w, h = rng.uniform(0.16,0.22), rng.uniform(0.10,0.14)
            # 고추 링 (외곽)
            ax.add_patch(patches.Ellipse((x,y), w, h, angle=rot,
                                         color='#1A6B1A', zorder=7))
            # 고추 링 (내부 구멍)
            ax.add_patch(patches.Ellipse((x,y), w*0.55, h*0.55, angle=rot,
                                         color='#F4C430', zorder=8))
            # 씨앗
            for _ in range(3):
                sx = x + rng.uniform(-0.04,0.04)
                sy = y + rng.uniform(-0.02,0.02)
                ax.add_patch(patches.Ellipse((sx,sy), 0.025, 0.015,
                                             color='#FFFFF0', zorder=9))

    elif mbti == "INFJ":
        # 루꼴라: 잎맥까지 표현한 정교한 잎사귀
        for i in range(12):
            angle = rng.uniform(0, 2*np.pi)
            r = rng.uniform(0.08, 0.73)
            x, y = r*np.cos(angle), r*np.sin(angle)
            rot = rng.uniform(0, 360)
            color = rng.choice(['#1B4D1B','#2D6B2D','#3A8A3A','#4CAF4C'])
            ax.add_patch(patches.Ellipse((x,y), 0.26, 0.12, angle=rot,
                                         color=color, zorder=7, alpha=0.9))
            # 잎맥
            rad = np.radians(rot)
            ax.plot([x-0.11*np.cos(rad), x+0.11*np.cos(rad)],
                    [y-0.11*np.sin(rad), y+0.11*np.sin(rad)],
                    color='#0D3D0D', linewidth=0.8, zorder=8)
            # 곁가지
            for side in [-1, 1]:
                mx = x + side*0.05*np.cos(rad+np.pi/2)
                my = y + side*0.05*np.sin(rad+np.pi/2)
                ax.plot([x, mx],[y, my],
                        color='#0D3D0D', linewidth=0.5, zorder=8, alpha=0.7)

    elif mbti == "INFP":
        # 바질: 큼직하고 윤기나는 잎 + 잎맥 풍성하게
        leaf_data = [
            (0.35, 0.38, 40), (-0.42, 0.28, 130),
            (0.08, -0.48, 70), (-0.28, -0.35, 160),
            (0.5, -0.15, 20), (-0.1, 0.52, 110),
        ]
        for (lx, ly, rot) in leaf_data:
            rad = np.radians(rot)
            # 잎 그림자
            ax.add_patch(patches.Ellipse((lx+0.02, ly-0.02), 0.38, 0.2,
                                         angle=rot, color='#1A5C1A', zorder=6, alpha=0.4))
            # 잎 본체
            ax.add_patch(patches.Ellipse((lx, ly), 0.36, 0.19,
                                         angle=rot, color='#27AE60', zorder=7))
            ax.add_patch(patches.Ellipse((lx, ly), 0.36, 0.19,
                                         angle=rot, color='#2ECC71', zorder=7, alpha=0.4))
            # 중심 잎맥
            ax.plot([lx-0.16*np.cos(rad), lx+0.16*np.cos(rad)],
                    [ly-0.16*np.sin(rad), ly+0.16*np.sin(rad)],
                    color='#1A6B3A', linewidth=1.2, zorder=8)
            # 곁가지 잎맥
            for t in [-0.08, 0, 0.08]:
                px = lx + t*np.cos(rad)
                py = ly + t*np.sin(rad)
                for side in [-1,1]:
                    ex = px + side*0.07*np.cos(rad+np.pi/2)
                    ey = py + side*0.07*np.sin(rad+np.pi/2)
                    ax.plot([px,ex],[py,ey],
                            color='#1A6B3A', linewidth=0.6, zorder=8, alpha=0.8)

    elif mbti == "ENFJ":
        # 모짜렐라: 녹아내린 치즈 느낌 (불규칙 흰 얼룩 + 그을린 점)
        for i in range(10):
            angle = i*(2*np.pi/10) + rng.uniform(-0.2,0.2)
            r = rng.uniform(0.18, 0.68)
            x, y = r*np.cos(angle), r*np.sin(angle)
            w = rng.uniform(0.22, 0.38)
            h = rng.uniform(0.14, 0.26)
            rot = rng.uniform(0,180)
            ax.add_patch(patches.Ellipse((x,y), w, h, angle=rot,
                                         color='#FFFDE7', zorder=7, alpha=0.95,
                                         ec='#F0DC82', linewidth=1.2))
            # 그을린 점
            for _ in range(rng.integers(2,5)):
                bx = x + rng.uniform(-w/3, w/3)
                by = y + rng.uniform(-h/3, h/3)
                ax.add_patch(Circle((bx,by), rng.uniform(0.01,0.03),
                                    color='#C8A000', zorder=8, alpha=0.5))

    elif mbti == "ENFP":
        # 콘: 통통한 낱알 + 광택
        for i in range(35):
            angle = rng.uniform(0, 2*np.pi)
            r = rng.uniform(0.05, 0.78)
            x, y = r*np.cos(angle), r*np.sin(angle)
            rot = rng.uniform(0,180)
            col = rng.choice(['#FFD700','#FFC200','#FFE44D','#F5C800'])
            ax.add_patch(patches.Ellipse((x,y), 0.11, 0.075, angle=rot,
                                         color=col, zorder=7,
                                         ec='#CC9900', linewidth=1))
            ax.add_patch(patches.Ellipse((x+0.015,y+0.015), 0.04, 0.025,
                                         angle=rot, color='white', zorder=8, alpha=0.4))

    elif mbti == "ISTJ":
        # 양파: 반투명 링, 여러 겹으로 쌓인 느낌
        for i in range(10):
            angle = i*(2*np.pi/10)
            r = rng.uniform(0.18, 0.68)
            x, y = r*np.cos(angle), r*np.sin(angle)
            rot = rng.uniform(0,180)
            # 겹겹이
            for scale, alpha, col in [
                (1.0, 0.8, '#9B59B6'),
                (0.75, 0.6, '#C39BD3'),
                (0.45, 0.9, '#E8DAEF')]:
                ax.add_patch(patches.Ellipse((x,y), 0.24*scale, 0.13*scale,
                                             angle=rot, color=col,
                                             zorder=7, alpha=alpha,
                                             ec='#7D3C98', linewidth=0.8))

    elif mbti == "ISFJ":
        # 버섯: 갓+줄기 입체감 있게
        mushroom_pos = [
            (0.0,0.55),(−0.48,0.22),(0.48,0.22),
            (0.0,−0.48),(−0.32,−0.58),(0.38,−0.48),(−0.55,−0.2)
        ]
        for (mx,my) in mushroom_pos:
            # 갓 그림자
            ax.add_patch(patches.Ellipse((mx+0.02,my+0.02), 0.28, 0.16,
                                         color='#5C2E00', zorder=6, alpha=0.35))
            # 갓
            ax.add_patch(patches.Ellipse((mx,my+0.06), 0.27, 0.15,
                                         color='#8B4513', zorder=7))
            ax.add_patch(patches.Ellipse((mx,my+0.06), 0.27, 0.15,
                                         color='#A0522D', zorder=7, alpha=0.5))
            # 갓 하이라이트
            ax.add_patch(patches.Ellipse((mx-0.05,my+0.09), 0.1, 0.05,
                                         color='white', zorder=8, alpha=0.25))
            # 줄기
            stem = plt.Polygon(
                [[mx-0.045,my+0.02],[mx+0.045,my+0.02],
                 [mx+0.035,my-0.1],[mx-0.035,my-0.1]],
                color='#D2B48C', zorder=7)
            ax.add_patch(stem)
            # 주름선
            for j in range(3):
                lx = mx - 0.06 + j*0.06
                ax.plot([lx,lx],[my-0.09,my+0.02],
                        color='#C4A882', linewidth=0.5, zorder=8, alpha=0.6)

    elif mbti == "ESTJ":
        # 페퍼로니: 완벽 균일 배치 + 입체감
        positions_e = [(0,0)]
        for count, radius in [(6,0.43),(11,0.72)]:
            for i in range(count):
                angle = i*(2*np.pi/count)
                positions_e.append((radius*np.cos(angle), radius*np.sin(angle)))
        for (x,y) in positions_e:
            ax.add_patch(Circle((x,y), 0.125, color='#6B0000', zorder=7))
            ax.add_patch(Circle((x,y), 0.105, color='#990000', zorder=8))
            ax.add_patch(Circle((x,y), 0.075, color='#CC2200', zorder=9))
            ax.add_patch(Circle((x,y), 0.04, color='#FF4422', zorder=10))
            ax.add_patch(Circle((x+0.04,y+0.04), 0.025,
                                 color='white', zorder=11, alpha=0.3))
            # 기름기 방울
            for j in range(3):
                a2 = j*(2*np.pi/3)
                ax.add_patch(Circle((x+0.085*np.cos(a2),y+0.085*np.sin(a2)),
                                    0.012, color='#FF8C00', zorder=10, alpha=0.5))

    elif mbti == "ESFJ":
        # 고구마 무스: 소용돌이 + 풍성한 크림 덩어리
        theta = np.linspace(0, 5*np.pi, 500)
        r_sp = theta/(5*np.pi)*0.78
        xs, ys = r_sp*np.cos(theta), r_sp*np.sin(theta)
        for lw, col, alpha in [(10,'#CC6600',0.6),(7,'#FF8C00',0.7),(4,'#FFB347',0.8),(2,'#FFD580',0.9)]:
            ax.plot(xs, ys, color=col, linewidth=lw, zorder=6+lw//3, alpha=alpha,
                    solid_capstyle='round')
        # 크림 방울
        for i in range(8):
            angle = i*(2*np.pi/8)
            r = 0.45
            x, y = r*np.cos(angle), r*np.sin(angle)
            ax.add_patch(patches.Ellipse((x,y), 0.18, 0.13,
                                         color='#FFE4B5', zorder=10, alpha=0.85,
                                         ec='#DDA050', linewidth=1))

    elif mbti == "ISTP":
        # 올리브: 단면 + 속 빨간 피망
        olive_pos = [
            (0.1,0.52),(−0.52,0.12),(0.47,−0.22),
            (−0.18,−0.52),(0.57,0.35),(−0.42,−0.47),(0.0,−0.2)
        ]
        colors = ['#2C2C2C','#3B7A3B','#2C2C2C','#3B7A3B','#2C2C2C','#3B7A3B','#2C2C2C']
        for (ox,oy),col in zip(olive_pos,colors):
            ax.add_patch(Circle((ox,oy), 0.115, color=col, zorder=7))
            ax.add_patch(Circle((ox,oy), 0.085, color='#4A4A4A' if col=='#2C2C2C' else '#4A9A4A', zorder=8))
            # 피망 속
            ax.add_patch(Circle((ox,oy), 0.048, color='#CC2200', zorder=9))
            ax.add_patch(Circle((ox,oy), 0.025, color='#FF4422', zorder=10))
            ax.add_patch(Circle((ox+0.015,oy+0.015), 0.012, color='white', zorder=11, alpha=0.4))

    elif mbti == "ISFP":
        # 선드라이 토마토: 쭈글쭈글한 질감 표현
        for i in range(9):
            angle = i*(2*np.pi/9)+0.4
            r = rng.uniform(0.18, 0.68)
            x, y = r*np.cos(angle), r*np.sin(angle)
            rot = rng.uniform(0,180)
            ax.add_patch(patches.Ellipse((x,y), 0.24, 0.15, angle=rot,
                                         color='#7B0000', zorder=7))
            ax.add_patch(patches.Ellipse((x,y), 0.2, 0.12, angle=rot,
                                         color='#A00000', zorder=8))
            # 주름
            for j in range(4):
                rad = np.radians(rot + j*40)
                ax.plot([x+0.03*np.cos(rad), x+0.09*np.cos(rad)],
                        [y+0.03*np.sin(rad), y+0.09*np.sin(rad)],
                        color='#600000', linewidth=0.8, zorder=9, alpha=0.7)
            ax.add_patch(Circle((x-0.05,y+0.03), 0.018,
                                 color='#FF6644', zorder=9, alpha=0.5))

    elif mbti == "ESTP":
        # 베이컨: 구불구불 + 지방층
        for i in range(6):
            y_base = -0.72 + i*0.27
            x_wave = np.linspace(-0.78, 0.78, 200)
            wave = y_base + 0.06*np.sin(x_wave*9 + i*1.1)
            # 가장자리 클리핑 (원 안에만)
            mask = x_wave**2 + wave**2 < 0.82**2
            xm, ym = x_wave[mask], wave[mask]
            if len(xm) == 0: continue
            # 지방 (흰색)
            ax.plot(xm, ym+0.025, color='#F5E6D3', linewidth=9,
                    zorder=6, alpha=0.9, solid_capstyle='round')
            # 살코기 (갈색)
            ax.plot(xm, ym, color='#8B1A1A', linewidth=7,
                    zorder=7, alpha=0.9, solid_capstyle='round')
            # 구운 느낌
            ax.plot(xm, ym, color='#A0522D', linewidth=4,
                    zorder=8, alpha=0.7, solid_capstyle='round')
            ax.plot(xm, ym+0.01, color='#CD853F', linewidth=2,
                    zorder=9, alpha=0.5, solid_capstyle='round')

    elif mbti == "ESFP":
        # 케첩: 지그재그 드리즐 + 방울 + 광택
        for k, (offset, phase) in enumerate([(-0.38,0),(-0.13,1.2),(0.13,0.4),(0.38,2.1)]):
            x_d = np.linspace(-0.76, 0.76, 300)
            y_d = offset + 0.16*np.sin(x_d*11 + phase)
            mask = x_d**2 + y_d**2 < 0.82**2
            xm, ym = x_d[mask], y_d[mask]
            if len(xm)==0: continue
            ax.plot(xm, ym, color='#AA0000', linewidth=5, zorder=6,
                    alpha=0.85, solid_capstyle='round')
            ax.plot(xm, ym, color='#EE0000', linewidth=2.5, zorder=7,
                    alpha=0.7, solid_capstyle='round')
            ax.plot(xm, ym+0.008, color='#FF6666', linewidth=1, zorder=8,
                    alpha=0.4, solid_capstyle='round')
        for i in range(8):
            angle = rng.uniform(0, 2*np.pi)
            r = rng.uniform(0.08, 0.65)
            x, y = r*np.cos(angle), r*np.sin(angle)
            ax.add_patch(Circle((x,y), rng.uniform(0.03,0.065),
                                 color='#CC0000', zorder=9, alpha=0.8))
            ax.add_patch(Circle((x+0.01,y+0.01), rng.uniform(0.01,0.02),
                                 color='white', zorder=10, alpha=0.4))

    # ══ 크러스트 테두리 마무리 ══
    ax.add_patch(Circle((0,0), 1.18, fill=False,
                         ec='#5C2E00', linewidth=3, zorder=11))
    ax.add_patch(Circle((0,0), 0.97, fill=False,
                         ec='#8B6914', linewidth=1, zorder=11, alpha=0.4))

    # ══ MBTI 라벨 ══
    ax.text(0, -1.33, mbti, fontsize=16, ha='center', va='center',
            color='#c0392b', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff9f5',
                      edgecolor='#ff6b35', linewidth=2.5))

    plt.tight_layout(pad=0.3)
    return fig


# ─────────────────────────────────────────────
# 데이터 (궁합 토핑명 수정 완료)
# ─────────────────────────────────────────────
PIZZA_DATA = {
    "INTJ": {
        "topping": "트러플 오일", "emoji": "🫙",
        "oneliner": "나 없으면 이 피자 그냥 치킨이야",
        "analysis": "트러플 오일은 고급스럽고 독특한 향을 지니고 있으며, 혼자 있어야 진정한 가치를 발휘합니다. 처음엔 '이게 뭐야' 싶지만, 한 번 맛을 알면 헤어날 수 없죠. 대중적이지 않아도 본인은 전혀 신경 쓰지 않습니다. 오히려 '몰라도 돼'라고 생각하고 있어요.",
        "verdict": "🔬 결론: 당신은 피자계의 석학입니다. 하지만 친구가 없어요.",
        "good_mbti": "ENFJ", "good_topping": "모짜렐라", "good_reason": "모짜렐라가 받쳐줘야 트러플이 빛남",
        "bad_mbti": "ESFP", "bad_topping": "케첩 드리즐", "bad_reason": "당신의 깊이를 케첩이 이해할 수 없음",
    },
    "INTP": {
        "topping": "파인애플", "emoji": "🍍",
        "oneliner": "나는 맞아, 그게 틀린 거야",
        "analysis": "파인애플 피자는 전 세계에서 가장 논쟁적인 존재입니다. 본인은 논리적으로 '과일과 고기의 조합은 타당하다'고 생각하지만 주변 모두가 이해 못 합니다. 억울하죠? 맞아요. 근데 본인도 왜 억울한지 설명하다가 지쳐요.",
        "verdict": "🤔 결론: 당신은 옳습니다. 그래서 외롭습니다.",
        "good_mbti": "ENFP", "good_topping": "콘 (옥수수)", "good_reason": "둘 다 '왜 저걸 넣어?' 소리 들음. 동병상련",
        "bad_mbti": "ESTJ", "bad_topping": "페퍼로니", "bad_reason": "페퍼로니는 전통을 중시함. 파인애플을 절대 용납 안 함",
    },
    "ENTJ": {
        "topping": "살라미", "emoji": "🍖",
        "oneliner": "내가 없으면 이 피자 무너져",
        "analysis": "살라미는 피자의 실질적 지배자입니다. 빠짐없이 균일하게 배치되고, 강하고 자신감 넘치는 맛. 누가 토핑 구성 설명해달라고 하면 살라미가 제일 먼저 튀어나옵니다. 리더십? 타고났죠. 부담스럽다고요? 그게 매력입니다.",
        "verdict": "💼 결론: 당신은 피자 CEO입니다. 직원들은 좀 힘듭니다.",
        "good_mbti": "INTJ", "good_topping": "트러플 오일", "good_reason": "서로 고급진 거 알아봄. 최강 콤비",
        "bad_mbti": "INFP", "bad_topping": "바질", "bad_reason": "바질은 감성을 원함. 살라미는 성과를 원함",
    },
    "ENTP": {
        "topping": "할라피뇨", "emoji": "🌶️",
        "oneliner": "어? 왜 매워? 원래 이래",
        "analysis": "할라피뇨는 예측 불가능합니다. 어디서 터질지 모르고, 자꾸 자극하고, 처음엔 괜찮다가 나중에 후회하게 만들죠. 하지만 없으면 심심하고, 있으면 대화가 생깁니다. 피자에서 제일 재밌는 토핑? 단연 할라피뇨.",
        "verdict": "💥 결론: 당신은 피자계의 어그로입니다. 근데 사랑받아요.",
        "good_mbti": "INTP", "good_topping": "파인애플", "good_reason": "둘 다 논란 제조기. 같이 있으면 피자가 레전드됨",
        "bad_mbti": "ISTJ", "bad_topping": "양파", "bad_reason": "양파는 규칙적이고 성실함. 할라피뇨의 카오스를 감당 못 함",
    },
    "INFJ": {
        "topping": "루꼴라", "emoji": "🌿",
        "oneliner": "나를 이해하는 사람이 없어",
        "analysis": "루꼴라는 피자 위에서 혼자 고고히 존재합니다. 쌉싸름한 맛은 깊이 있는 내면을 상징하고, 아무도 처음엔 루꼴라를 주문하지 않지만 먹어본 사람은 '이게 없으면 허전해'라고 합니다. 당신도 그런 사람입니다. 희귀하고 소중해요.",
        "verdict": "🌙 결론: 당신은 피자계의 예언자입니다. 아무도 안 믿어줘요.",
        "good_mbti": "ENFP", "good_topping": "콘 (옥수수)", "good_reason": "ENFP가 루꼴라를 세상에 알려줌",
        "bad_mbti": "ESTP", "bad_topping": "베이컨", "bad_reason": "베이컨은 깊이 따위 관심 없음",
    },
    "INFP": {
        "topping": "바질", "emoji": "🌱",
        "oneliner": "이 피자에 담긴 감성을 느껴봐",
        "analysis": "바질은 피자의 감성 담당입니다. 비주얼은 최고고, 향은 시적이며, 존재 자체로 피자를 예술로 만듭니다. 하지만 열에 약하고, 너무 일찍 올리면 시들어버립니다. 섬세하게 다뤄야 해요. 당신도 마찬가지입니다.",
        "verdict": "🎨 결론: 당신은 피자계의 시인입니다. 배는 안 불러요.",
        "good_mbti": "ENFJ", "good_topping": "모짜렐라", "good_reason": "모짜렐라가 바질을 포근하게 감싸줌",
        "bad_mbti": "ENTJ", "bad_topping": "살라미", "bad_reason": "살라미는 감성을 KPI로 환산하려 함",
    },
    "ENFJ": {
        "topping": "모짜렐라", "emoji": "🧀",
        "oneliner": "나 없으면 이거 그냥 토마토 토스트야",
        "analysis": "모짜렐라는 피자의 어머니입니다. 모든 토핑을 감싸 안고, 없으면 피자가 아닙니다. 누구와도 잘 어울리고, 존재 자체가 하나로 묶는 힘. 당신이 없는 모임은 어딘가 허전합니다.",
        "verdict": "🤝 결론: 당신은 피자계의 총무입니다. 수고 많으세요.",
        "good_mbti": "INTJ", "good_topping": "트러플 오일", "good_reason": "트러플의 빛을 모짜렐라가 받쳐줌",
        "bad_mbti": "INTP", "bad_topping": "파인애플", "bad_reason": "파인애플이 모짜렐라를 질척하게 만듦",
    },
    "ENFP": {
        "topping": "콘 (옥수수)", "emoji": "🌽",
        "oneliner": "어? 나 여기 있어요!! 안 보여요??",
        "analysis": "콘은 피자에서 가장 밝고 에너지 넘치는 토핑입니다. 달콤하고, 통통 튀고, 어디서든 눈에 띕니다. 진지한 피자에 갑자기 나타나서 분위기를 환기시키죠. 싫어하는 사람도 있지만 좋아하는 사람은 정말 좋아합니다.",
        "verdict": "⚡ 결론: 당신은 피자계의 에너지 드링크입니다.",
        "good_mbti": "INFJ", "good_topping": "루꼴라", "good_reason": "콘이 루꼴라를 세상 밖으로 꺼내줌",
        "bad_mbti": "INTJ", "bad_topping": "트러플 오일", "bad_reason": "트러플은 콘의 에너지를 '유치하다'고 판단함",
    },
    "ISTJ": {
        "topping": "양파", "emoji": "🧅",
        "oneliner": "나는 항상 여기 있었어. 원래부터.",
        "analysis": "양파는 피자의 전통 그 자체입니다. 화려하지 않고, 튀지 않으며, 묵묵히 제 역할을 합니다. 빠지면 '어 뭔가 허전한데?'라는 말이 나오지만 있을 때는 아무도 언급하지 않습니다.",
        "verdict": "📋 결론: 당신은 피자계의 공무원입니다. 연금 나옵니다.",
        "good_mbti": "ISFJ", "good_topping": "버섯", "good_reason": "둘 다 묵묵히 자기 자리 지킴. 환상의 팀워크",
        "bad_mbti": "ENTP", "bad_topping": "할라피뇨", "bad_reason": "할라피뇨의 카오스를 양파는 절대 이해 못 함",
    },
    "ISFJ": {
        "topping": "버섯", "emoji": "🍄",
        "oneliner": "나 괜찮아... 정말로.",
        "analysis": "버섯은 눈에 띄지 않지만 피자의 깊은 맛을 담당합니다. 혼자선 뭔가 부족한 것 같지만, 없으면 맛이 확 떨어지는 그런 존재. 제발 좀 자기 자신을 위해 살아요.",
        "verdict": "🍄 결론: 당신은 피자계의 서브 캐릭터입니다. 사실 주인공이에요.",
        "good_mbti": "ISTJ", "good_topping": "양파", "good_reason": "서로 묵묵히 서포트. 말 안 해도 통함",
        "bad_mbti": "ENTJ", "bad_topping": "살라미", "bad_reason": "살라미가 버섯의 자리를 계속 빼앗음",
    },
    "ESTJ": {
        "topping": "페퍼로니", "emoji": "🍕",
        "oneliner": "나는 규칙대로 배치된다. 항상.",
        "analysis": "페퍼로니는 피자의 상징입니다. 완벽하게 균일한 간격, 빠짐없는 배치, 강렬한 존재감. 전통을 중시하고 효율을 사랑하며, 왜 파인애플이 피자 위에 있는지 이해하지 못합니다.",
        "verdict": "📐 결론: 당신은 피자계의 팀장입니다. 칼퇴는 없어요.",
        "good_mbti": "ISTJ", "good_topping": "양파", "good_reason": "둘 다 규칙과 전통 존중. 완벽한 조합",
        "bad_mbti": "INTP", "bad_topping": "파인애플", "bad_reason": "파인애플은 페퍼로니의 세계관을 파괴함",
    },
    "ESFJ": {
        "topping": "고구마 무스", "emoji": "🍠",
        "oneliner": "다들 좋아하지? 맞지? 맞지???",
        "analysis": "고구마 무스는 대한민국 피자의 국민 토핑입니다. 달달하고, 부드럽고, 거부감이 없으며, 모두가 좋아합니다. 단 한 명이라도 '별로'라고 하면 하루 종일 마음에 걸립니다.",
        "verdict": "💛 결론: 당신은 피자계의 인싸입니다. 좋아요 1000개.",
        "good_mbti": "ENFJ", "good_topping": "모짜렐라", "good_reason": "둘 다 분위기 메이커. 완벽한 파티 피자",
        "bad_mbti": "INTJ", "bad_topping": "트러플 오일", "bad_reason": "트러플은 대중성을 경멸함",
    },
    "ISTP": {
        "topping": "올리브", "emoji": "🫒",
        "oneliner": "나 여기 있는데 왜 아무도 몰라",
        "analysis": "올리브는 과소평가된 토핑입니다. 싫어하는 사람은 골라내고, 좋아하는 사람은 진심으로 좋아하는 양극단. 말이 없고, 차갑고, 독립적이며, 자기 페이스를 절대 잃지 않습니다.",
        "verdict": "🔧 결론: 당신은 피자계의 장인입니다. 과묵한 천재.",
        "good_mbti": "ISTP", "good_topping": "올리브", "good_reason": "둘이 말 없이 앉아서 피자 먹음. 완벽한 저녁",
        "bad_mbti": "ESFJ", "bad_topping": "고구마 무스", "bad_reason": "고구마 무스가 계속 '재밌지?' 물어봄",
    },
    "ISFP": {
        "topping": "선드라이 토마토", "emoji": "🍅",
        "oneliner": "나는 그냥 예쁘고 싶어",
        "analysis": "선드라이 토마토는 피자에서 가장 감각적인 토핑입니다. 색깔도 예쁘고, 맛도 독특하고, 비주얼에 진심. 자기 표현이 강하지만 강요하지 않아요.",
        "verdict": "🎭 결론: 당신은 피자계의 인스타그래머입니다. 팔로워 많음.",
        "good_mbti": "INFP", "good_topping": "바질", "good_reason": "감성 토핑 동맹. 피자가 예술이 됨",
        "bad_mbti": "ESTJ", "bad_topping": "페퍼로니", "bad_reason": "페퍼로니는 예쁜 것보다 효율을 원함",
    },
    "ESTP": {
        "topping": "베이컨", "emoji": "🥓",
        "oneliner": "일단 올리고 생각은 나중에",
        "analysis": "베이컨은 피자의 행동파입니다. 생각보다 먼저 움직이고, 일단 올리면 무조건 맛있습니다. 계획? 없어요. 그냥 하면 되거든요.",
        "verdict": "🏎️ 결론: 당신은 피자계의 스턴트맨입니다. 짜릿해요.",
        "good_mbti": "ENFP", "good_topping": "콘 (옥수수)", "good_reason": "둘 다 에너지 폭발. 피자가 축제가 됨",
        "bad_mbti": "INFJ", "bad_topping": "루꼴라", "bad_reason": "루꼴라의 감성을 베이컨이 이해할 수 없음",
    },
    "ESFP": {
        "topping": "케첩 드리즐", "emoji": "🥫",
        "oneliner": "나 왔어~~ 파티 시작이야!!",
        "analysis": "케첩 드리즐은 피자의 파티 메이커입니다. 없어도 되는데 있으면 기분이 달라지고, 뿌리면 일단 기분은 좋아집니다. 오늘 이 피자가 최고의 피자예요. 늘 그렇듯이.",
        "verdict": "🎉 결론: 당신은 피자계의 DJ입니다. 항상 신나요.",
        "good_mbti": "ESTP", "good_topping": "베이컨", "good_reason": "둘 다 현재 충실. 최고의 파티 피자",
        "bad_mbti": "INTJ", "bad_topping": "트러플 오일", "bad_reason": "트러플은 케첩을 '격이 다르다'며 무시함",
    },
}

MBTI_LIST = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
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

    st.markdown(f"""
    <div class="result-card">
        <span class="topping-emoji">{data['emoji']}</span>
        <p style="color:#888; font-size:0.9rem; margin:0;">당신({selected})은...</p>
        <p class="topping-name">"{data['topping']}"</p>
        <p style="color:#555; font-style:italic; margin-top:10px;">"{data['oneliner']}"</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-family:'Black Han Sans',sans-serif; font-size:1.1rem;
              color:#c0392b; margin:20px 0 5px 0;">🎨 당신의 피자</p>
    """, unsafe_allow_html=True)

    fig = draw_pizza(selected)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(f"""
    <div class="analysis-box">
        <p class="label">🔍 심층 분석 (매우 과학적)</p>
        <p>{data['analysis']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="verdict-box">{data['verdict']}</div>
    """, unsafe_allow_html=True)

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

    with st.expander("🍕 전체 토핑 지도 보기"):
        cols = st.columns(4)
        for i, (mbti, info) in enumerate(PIZZA_DATA.items()):
            with cols[i % 4]:
                is_me = "⭐ " if mbti == selected else ""
                st.markdown(f"""
                <div style="background:{'#fff3e0' if mbti==selected else '#f9f9f9'};
                            border:2px solid {'#ff6b35' if mbti==selected else '#eee'};
                            border-radius:10px; padding:10px; text-align:center;
                            margin-bottom:10px;">
                    <div style="font-size:1.8rem;">{info['emoji']}</div>
                    <div style="font-weight:700; color:#c0392b;">{is_me}{mbti}</div>
                    <div style="font-size:0.75rem; color:#666;">{info['topping']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    🍕 이 분석은 100% 비과학적입니다. 그래도 맞는 것 같죠? | Made with Streamlit
</div>
""", unsafe_allow_html=True)
