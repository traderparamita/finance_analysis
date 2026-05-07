#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""샘표(007540) 투자 분석 차트 생성"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
BLUE = '#2563EB'
ORANGE = '#F97316'
GREEN = '#10B981'
RED = '#EF4444'
PURPLE = '#8B5CF6'
COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE]

# 출력 디렉토리
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 데이터 정의 (연결 기준, 단위: 억원)
# ============================================================
years = ['2020', '2021', '2022', '2023', '2024', '2025']

# 손익
revenue =       [3191, 3490, 3718, 3839, 4050, 4090]
op_profit =     [411,  219,  103,   81,   59,  241]
net_income =    [353,  230,  162,  106,  107,  188]

# 수익성
op_margin =     [12.88, 6.28, 2.78, 2.12, 1.45, 5.90]
net_margin =    [11.1,  3.40, 2.81, 1.58, 1.62, 2.38]
roe =           [10.50, 6.42, 5.35, 3.06, 3.26, 4.63]
roa =           [8.50,  5.58, 3.57, 2.26, 2.25, 3.88]

# 성장률 (YoY, 2021~2025)
years_g = ['2021', '2022', '2023', '2024', '2025']
rev_growth =    [9.4,   6.6,  3.3,  5.5,  1.0]
op_growth =     [-46.7, -52.8, -21.3, -27.7, 310.9]
ni_growth =     [-34.8, -29.6, -34.6, 0.9, 75.7]

# 안정성
debt_ratio =    [30.98, 41.27, 42.37, 43.89, 40.80, 35.85]
equity_ratio =  [76.3,  70.8,  70.2,  69.5,  71.0,  73.6]
current_ratio = [250.0, 248.3, 211.4, 150.1, 168.8, 199.3]  # 2020 추정

# 현금흐름 (2020~2025, 2020/2021 추정)
cf_op =    [400,  300,  183,  229,  351,  618]
cf_inv =   [-350, -320, -313, -265, -149, -389]
cf_fin =   [-50,  -30,  -38,   60,  -75, -249]
capex =    [300,  350,  418,  312,  206,  227]
fcf =      [100,  -50, -235,  -83,  145,  391]
cash_end = [200,  180,  148,  172,  299,  279]

# 밸류에이션
per =  [7.88, 10.33, 13.06, 23.41, 16.50, 14.43]
pbr =  [0.61,  0.59,  0.62,  0.63,  0.47,  0.58]
eps =  [6217,  4130,  3629,  2114,  2284,  3388]
bps =  [80786, 72054, 75948, 77969, 80416, 84351]

# 매출 구성
segment_labels = ['장류\n(간장/된장/고추장)', '소스/양념\n(연두/폰타나)', '면류/차류', '통조림', '기타/B2B']
segment_values = [42, 28, 12, 10, 8]

# 경쟁사 비교 (시총 억원 기준)
comp_names = ['CJ(지주)', '오뚜기', '대상홀딩스', '샘표']
comp_mktcap = [55145, 14669, 3248, 1579]
comp_pbr = [1.34, 0.61, 0.55, 0.58]

# SWOT
swot = {
    'Strengths (강점)': [
        '80년 전통 간장 시장 1위 (57%)',
        '발효 기술 R&D (3,000+ 미생물)',
        '연두: 글로벌 비건 트렌드 적합',
        '자기자본비율 73.6%, 무차입 경영',
        '자사주 29.9% → 소각 시 가치 상승',
    ],
    'Weaknesses (약점)': [
        '소형주 유동성 (시총 1,579억)',
        '극도로 낮은 배당 (DPS 200원)',
        '해외사업 적자 (미국/중국)',
        '지주회사 디스카운트',
        '증권사 커버리지 부재',
    ],
    'Opportunities (기회)': [
        'K-Food 글로벌 확산 수혜',
        '자사주 소각 의무화 → 주당가치↑',
        '바이오소재 신사업 진출',
        '제천 신공장 (2028) 생산능력 확대',
        '식물성/비건 식품 시장 성장',
    ],
    'Threats (위협)': [
        '내수 장류시장 축소 (인구 감소)',
        '원재료 가격 변동 리스크',
        '대기업(CJ/대상) 경쟁 심화',
        '승계 이슈 (290억 증여세)',
        '국세청 조사 리스크',
    ],
}


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ {name}")


# ============================================================
# Chart 1: 매출액 & 영업이익 추이 (막대)
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.35
bars1 = ax1.bar(x - w/2, revenue, w, label='매출액', color=BLUE, alpha=0.85)
ax2 = ax1.twinx()
bars2 = ax2.bar(x + w/2, op_profit, w, label='영업이익', color=ORANGE, alpha=0.85)
ax1.set_xlabel('연도')
ax1.set_ylabel('매출액 (억원)', color=BLUE)
ax2.set_ylabel('영업이익 (억원)', color=ORANGE)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylim(0, max(revenue) * 1.2)
ax2.set_ylim(0, max(op_profit) * 1.3)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
             f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, color=BLUE)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9, color=ORANGE)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title('샘표 매출액 & 영업이익 추이', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
save(fig, 'chart1_revenue_profit.png')

# ============================================================
# Chart 2: 수익성 지표 추이 (라인)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, op_margin, 'o-', color=BLUE, linewidth=2, markersize=7, label='영업이익률 (%)')
ax.plot(years, net_margin, 's-', color=ORANGE, linewidth=2, markersize=7, label='순이익률 (%)')
ax.plot(years, roe, '^-', color=GREEN, linewidth=2, markersize=7, label='ROE (%)')
ax.plot(years, roa, 'D-', color=RED, linewidth=2, markersize=7, label='ROA (%)')
for i, (om, nm, r, ra) in enumerate(zip(op_margin, net_margin, roe, roa)):
    ax.annotate(f'{om}', (years[i], om), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color=BLUE)
ax.set_title('샘표 수익성 지표 추이', fontsize=14, fontweight='bold')
ax.set_xlabel('연도')
ax.set_ylabel('비율 (%)')
ax.legend(loc='upper right')
ax.grid(alpha=0.3)
ax.set_ylim(0, max(op_margin) * 1.3)
save(fig, 'chart2_profitability.png')

# ============================================================
# Chart 3: ROE & ROA 추이 (라인+영역)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, roe, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='ROE (%)', zorder=3)
ax.fill_between(years, roe, alpha=0.15, color=BLUE)
ax.plot(years, roa, 's-', color=GREEN, linewidth=2.5, markersize=8, label='ROA (%)', zorder=3)
ax.fill_between(years, roa, alpha=0.15, color=GREEN)
for i in range(len(years)):
    ax.annotate(f'{roe[i]}%', (years[i], roe[i]), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9, color=BLUE, fontweight='bold')
    ax.annotate(f'{roa[i]}%', (years[i], roa[i]), textcoords="offset points", xytext=(0, -18), ha='center', fontsize=9, color=GREEN, fontweight='bold')
ax.set_title('샘표 ROE & ROA 추이', fontsize=14, fontweight='bold')
ax.set_xlabel('연도')
ax.set_ylabel('비율 (%)')
ax.legend(loc='upper right')
ax.grid(alpha=0.3)
ax.set_ylim(0, max(roe) * 1.4)
save(fig, 'chart3_roe_roa.png')

# ============================================================
# Chart 4: 재무 안정성 지표 (막대)
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.25
ax1.bar(x - w, debt_ratio, w, label='부채비율 (%)', color=RED, alpha=0.8)
ax1.bar(x, equity_ratio, w, label='자기자본비율 (%)', color=BLUE, alpha=0.8)
ax1.bar(x + w, [c/10 for c in current_ratio], w, label='유동비율 (% ÷10)', color=GREEN, alpha=0.8)
for i in range(len(years)):
    ax1.text(x[i] - w, debt_ratio[i] + 1, f'{debt_ratio[i]:.1f}', ha='center', fontsize=8, color=RED)
    ax1.text(x[i], equity_ratio[i] + 1, f'{equity_ratio[i]:.1f}', ha='center', fontsize=8, color=BLUE)
    ax1.text(x[i] + w, current_ratio[i]/10 + 1, f'{current_ratio[i]:.0f}', ha='center', fontsize=8, color=GREEN)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_title('샘표 재무 안정성 지표', fontsize=14, fontweight='bold')
ax1.set_ylabel('비율 (%)')
ax1.legend(loc='upper right')
ax1.grid(axis='y', alpha=0.3)
save(fig, 'chart4_stability.png')

# ============================================================
# Chart 5: 성장률 지표 (막대)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years_g))
w = 0.25
ax.bar(x - w, rev_growth, w, label='매출 성장률', color=BLUE, alpha=0.8)
# 영업이익 성장률은 2025년 310.9%로 너무 크므로 클리핑
op_growth_clipped = [min(g, 80) for g in op_growth]
ax.bar(x, op_growth_clipped, w, label='영업이익 성장률', color=ORANGE, alpha=0.8)
ax.bar(x + w, ni_growth, w, label='순이익 성장률', color=GREEN, alpha=0.8)
# 2025 영업이익 성장률 주석
ax.annotate('+310.9%', (x[-1], op_growth_clipped[-1]), textcoords="offset points",
            xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color=ORANGE,
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))
for i in range(len(years_g)):
    ax.text(x[i] - w, rev_growth[i] + (2 if rev_growth[i] >= 0 else -6),
            f'{rev_growth[i]:.1f}', ha='center', fontsize=8, color=BLUE)
ax.set_xticks(x)
ax.set_xticklabels(years_g)
ax.set_title('샘표 성장률 추이 (YoY)', fontsize=14, fontweight='bold')
ax.set_ylabel('성장률 (%)')
ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)
save(fig, 'chart5_growth.png')

# ============================================================
# Chart 6: 매출 구성 비중 (파이)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
explode = [0.05] * len(segment_labels)
wedges, texts, autotexts = ax.pie(segment_values, labels=segment_labels, autopct='%1.1f%%',
                                    colors=COLORS, explode=explode, startangle=90,
                                    textprops={'fontsize': 10})
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight('bold')
ax.set_title('샘표 매출 구성 비중 (연결 기준, 2025년)', fontsize=14, fontweight='bold')
save(fig, 'chart6_segment.png')

# ============================================================
# Chart 7: 경쟁사 비교 (가로막대 - PBR)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.5))
# 시총 비교
colors_comp = [BLUE, ORANGE, GREEN, RED]
y_pos = np.arange(len(comp_names))
bars = ax1.barh(y_pos, comp_mktcap, color=colors_comp, alpha=0.8)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(comp_names)
ax1.set_xlabel('시가총액 (억원)')
ax1.set_title('시가총액 비교', fontsize=12, fontweight='bold')
for i, bar in enumerate(bars):
    ax1.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
             f'{comp_mktcap[i]:,}억', va='center', fontsize=9)
# PBR 비교
bars2 = ax2.barh(y_pos, comp_pbr, color=colors_comp, alpha=0.8)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(comp_names)
ax2.set_xlabel('PBR (배)')
ax2.set_title('PBR 비교', fontsize=12, fontweight='bold')
ax2.axvline(x=1.0, color='gray', linewidth=1, linestyle='--', alpha=0.5)
for i, bar in enumerate(bars2):
    ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
             f'{comp_pbr[i]:.2f}배', va='center', fontsize=9)
fig.suptitle('샘표 vs 동종업계 비교', fontsize=14, fontweight='bold')
fig.tight_layout()
save(fig, 'chart7_competitors.png')

# ============================================================
# Chart 8: 순이익 & 순이익률 콤보 (막대+라인)
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
bars = ax1.bar(x, net_income, 0.5, label='당기순이익 (억원)', color=BLUE, alpha=0.8)
ax2 = ax1.twinx()
ax2.plot(years, net_margin, 'o-', color=ORANGE, linewidth=2.5, markersize=8, label='순이익률 (%)')
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(bar.get_height())}', ha='center', fontsize=9, color=BLUE, fontweight='bold')
for i, v in enumerate(net_margin):
    ax2.text(i, v + 0.3, f'{v}%', ha='center', fontsize=9, color=ORANGE, fontweight='bold')
ax1.set_xlabel('연도')
ax1.set_ylabel('당기순이익 (억원)', color=BLUE)
ax2.set_ylabel('순이익률 (%)', color=ORANGE)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
ax1.set_title('샘표 당기순이익 & 순이익률', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
save(fig, 'chart8_net_income.png')

# ============================================================
# Chart 9: SWOT 다이어그램
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
bg_colors = ['#DBEAFE', '#FEE2E2', '#D1FAE5', '#FEF3C7']
titles = list(swot.keys())
for idx, (ax, title, bg) in enumerate(zip(axes.flat, titles, bg_colors)):
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    items = swot[title]
    for i, item in enumerate(items):
        y = 0.85 - i * 0.17
        ax.text(0.05, y, f'• {item}', fontsize=8.5, va='top', wrap=True,
                transform=ax.transAxes)
fig.suptitle('샘표 SWOT 분석', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()
save(fig, 'chart9_swot.png')

# ============================================================
# Chart 10: 현금흐름 추이 (3종 막대)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.25
ax.bar(x - w, cf_op, w, label='영업활동CF', color=BLUE, alpha=0.8)
ax.bar(x, cf_inv, w, label='투자활동CF', color=RED, alpha=0.8)
ax.bar(x + w, cf_fin, w, label='재무활동CF', color=GREEN, alpha=0.8)
for i in range(len(years)):
    ax.text(x[i] - w, cf_op[i] + (10 if cf_op[i] >= 0 else -25),
            f'{cf_op[i]}', ha='center', fontsize=8, color=BLUE)
    ax.text(x[i], cf_inv[i] - 25,
            f'{cf_inv[i]}', ha='center', fontsize=8, color=RED)
    ax.text(x[i] + w, cf_fin[i] + (10 if cf_fin[i] >= 0 else -25),
            f'{cf_fin[i]}', ha='center', fontsize=8, color=GREEN)
ax.axhline(y=0, color='gray', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_title('샘표 현금흐름 추이', fontsize=14, fontweight='bold')
ax.set_ylabel('억원')
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)
save(fig, 'chart10_cashflow.png')

# ============================================================
# Chart 11: CAPEX, FCF & 현금보유 (막대+라인)
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.3
ax1.bar(x - w/2, capex, w, label='CAPEX', color=RED, alpha=0.7)
ax1.bar(x + w/2, fcf, w, label='FCF', color=GREEN, alpha=0.7)
ax2 = ax1.twinx()
ax2.plot(years, cash_end, 'o-', color=PURPLE, linewidth=2.5, markersize=8, label='기말현금')
for i in range(len(years)):
    ax1.text(x[i] - w/2, capex[i] + 8, f'{capex[i]}', ha='center', fontsize=8, color=RED)
    y_pos_fcf = fcf[i] + 8 if fcf[i] >= 0 else fcf[i] - 20
    ax1.text(x[i] + w/2, y_pos_fcf, f'{fcf[i]}', ha='center', fontsize=8, color=GREEN)
for i, v in enumerate(cash_end):
    ax2.text(i, v + 8, f'{v}', ha='center', fontsize=9, color=PURPLE, fontweight='bold')
ax1.set_xlabel('연도')
ax1.set_ylabel('억원')
ax2.set_ylabel('기말현금 (억원)', color=PURPLE)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.axhline(y=0, color='gray', linewidth=0.8)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title('샘표 CAPEX, FCF & 현금보유', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
save(fig, 'chart11_fcf_cash.png')

# ============================================================
# Chart 12: 영업이익 vs 영업CF (이익의 질)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.3
ax.bar(x - w/2, op_profit, w, label='영업이익', color=BLUE, alpha=0.8)
ax.bar(x + w/2, cf_op, w, label='영업활동CF', color=GREEN, alpha=0.8)
for i in range(len(years)):
    ax.text(x[i] - w/2, op_profit[i] + 8, f'{op_profit[i]}', ha='center', fontsize=9, color=BLUE)
    ax.text(x[i] + w/2, cf_op[i] + 8, f'{cf_op[i]}', ha='center', fontsize=9, color=GREEN)
# 비율 표시
for i in range(len(years)):
    if op_profit[i] > 0:
        ratio = cf_op[i] / op_profit[i]
        ax.text(x[i], max(op_profit[i], cf_op[i]) + 40,
                f'×{ratio:.1f}', ha='center', fontsize=9, fontweight='bold', color=PURPLE)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_title('샘표 영업이익 vs 영업활동CF (이익의 질)', fontsize=14, fontweight='bold')
ax.set_ylabel('억원')
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)
save(fig, 'chart12_earnings_quality.png')

print("\n✅ 모든 차트 생성 완료!")
