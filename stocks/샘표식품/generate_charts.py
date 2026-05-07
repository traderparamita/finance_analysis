#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
샘표식품(248170) 투자 분석 차트 생성
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── 스타일 설정 ──
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BLUE = '#2563EB'
ORANGE = '#F97316'
GREEN = '#10B981'
RED = '#EF4444'
PURPLE = '#8B5CF6'
NAVY = '#1E3A5F'
LIGHT_BLUE = '#93C5FD'
LIGHT_ORANGE = '#FDBA74'
COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150
FIGSIZE = (10, 5.5)

# ── 데이터 ──
years = ['2021', '2022', '2023', '2024', '2025']

# 연결기준 (FnGuide 데이터)
revenue =       [3487, 3712, 3834, 4049, 4089]   # 억원
op_profit =     [235,  111,  98,   65,   245]     # 억원
net_income =    [237,  131,  104,  101,  199]     # 억원

op_margin =     [6.7,  3.0,  2.6,  1.6,  6.0]    # %
net_margin =    [6.8,  3.5,  2.7,  2.5,  4.9]    # %
roe =           [11.64, 5.92, 4.50, 4.17, 7.81]  # %
roa =           [7.95, 3.87, 2.91, 2.73, 5.32]   # %

debt_ratio =    [52.37, 54.07, 55.07, 50.39, 43.46]  # %
current_ratio = [203.9, 174.1, 131.3, 141.1, 165.1]  # %
equity_ratio =  [65.6,  64.9,  64.5,  66.5,  69.7]   # %
interest_cov =  [37.0,  19.3,  12.2,  3.5,   12.1]   # 배

# 성장률
rev_growth =    [None, 6.4,  3.3,  5.6,  1.0]   # %
op_growth =     [None, -52.8, -11.7, -33.7, 276.9]
ni_growth =     [None, -44.7, -20.6, -2.9,  97.0]

# 현금흐름 (백만원 → 억원)
ocf =           [320,  152,  205,  335,  583]   # 억원
icf =           [-633, -311, -316, -142, -374]
fcf_cf =        [317,  -8,   135,  -87,  -236]
capex =         [None, 416,  312,  198,  223]   # 억원 (2021 미확인)
# FCF = OCF - CAPEX
fcf =           [None, -264, -107, 137,  360]   # 억원

# 매출 구성 비중 (2023 기준, 가장 최근 상세)
seg_labels = ['장류\n(간장/된장/고추장)', '소스/양념류\n(연두/폰타나 등)', '기타 식품\n(면류/차류/통조림)']
seg_values = [49.9, 35.1, 15.0]

# 경쟁사 비교 (2024 연매출 기준, 억원)
comp_names = ['CJ제일제당\n(식품부문)', '대상', '오뚜기', '샘표식품']
comp_revenue = [113530, 40841, 31833, 4049]

x = np.arange(len(years))
width = 0.35


# ════════════════════════════════════════
# Chart 1: 매출액 & 영업이익 추이
# ════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=FIGSIZE)
bars1 = ax1.bar(x - width/2, revenue, width, label='매출액', color=BLUE, alpha=0.85)
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, op_profit, width, label='영업이익', color=ORANGE, alpha=0.85)

ax1.set_xlabel('연도', fontsize=11)
ax1.set_ylabel('매출액 (억원)', fontsize=11, color=BLUE)
ax2.set_ylabel('영업이익 (억원)', fontsize=11, color=ORANGE)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_title('샘표식품 매출액 & 영업이익 추이', fontsize=14, fontweight='bold', pad=15)

for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 30,
             f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, color=BLUE)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
             f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, color=ORANGE)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
ax1.set_ylim(0, max(revenue)*1.15)
ax2.set_ylim(0, max(op_profit)*1.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart1_revenue_profit.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 2: 수익성 지표 추이
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(years, op_margin, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='영업이익률(%)')
ax.plot(years, net_margin, 's-', color=ORANGE, linewidth=2.5, markersize=8, label='순이익률(%)')

for i, (om, nm) in enumerate(zip(op_margin, net_margin)):
    ax.annotate(f'{om}%', (years[i], om), textcoords="offset points", xytext=(0, 12),
                ha='center', fontsize=9, color=BLUE)
    ax.annotate(f'{nm}%', (years[i], nm), textcoords="offset points", xytext=(0, -18),
                ha='center', fontsize=9, color=ORANGE)

ax.set_title('샘표식품 수익성 지표 추이', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('비율 (%)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, max(max(op_margin), max(net_margin)) * 1.4)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart2_profitability.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 3: ROE & ROA 추이
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(years, roe, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='ROE(%)')
ax.fill_between(years, roe, alpha=0.15, color=BLUE)
ax.plot(years, roa, 's-', color=GREEN, linewidth=2.5, markersize=8, label='ROA(%)')
ax.fill_between(years, roa, alpha=0.15, color=GREEN)

for i in range(len(years)):
    ax.annotate(f'{roe[i]}%', (years[i], roe[i]), textcoords="offset points",
                xytext=(0, 12), ha='center', fontsize=9, color=BLUE)
    ax.annotate(f'{roa[i]}%', (years[i], roa[i]), textcoords="offset points",
                xytext=(0, -16), ha='center', fontsize=9, color=GREEN)

ax.set_title('샘표식품 ROE & ROA 추이', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('비율 (%)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart3_roe_roa.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 4: 재무 안정성 지표
# ════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=FIGSIZE)
w = 0.2
ax1.bar(x - w, debt_ratio, w, label='부채비율(%)', color=RED, alpha=0.8)
ax1.bar(x,     equity_ratio, w, label='자기자본비율(%)', color=GREEN, alpha=0.8)
ax1.bar(x + w, current_ratio, w, label='유동비율(%)', color=BLUE, alpha=0.8)

for i in range(len(years)):
    ax1.text(x[i]-w, debt_ratio[i]+2, f'{debt_ratio[i]:.1f}', ha='center', fontsize=8, color=RED)
    ax1.text(x[i], equity_ratio[i]+2, f'{equity_ratio[i]:.1f}', ha='center', fontsize=8, color=GREEN)
    ax1.text(x[i]+w, current_ratio[i]+2, f'{current_ratio[i]:.1f}', ha='center', fontsize=8, color=BLUE)

ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_title('샘표식품 재무 안정성 지표', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('비율 (%)', fontsize=11)
ax1.legend(fontsize=9)
ax1.set_ylim(0, max(current_ratio)*1.2)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart4_stability.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 5: 성장률 지표
# ════════════════════════════════════════
years_g = ['2022', '2023', '2024', '2025']
xg = np.arange(len(years_g))
w = 0.25

fig, ax = plt.subplots(figsize=FIGSIZE)
ax.bar(xg - w, rev_growth[1:], w, label='매출 성장률(%)', color=BLUE, alpha=0.85)
ax.bar(xg,     op_growth[1:], w, label='영업이익 성장률(%)', color=ORANGE, alpha=0.85)
ax.bar(xg + w, ni_growth[1:], w, label='순이익 성장률(%)', color=GREEN, alpha=0.85)

ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
ax.set_xticks(xg)
ax.set_xticklabels(years_g)
ax.set_title('샘표식품 성장률 지표', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('성장률 (%)', fontsize=11)
ax.legend(fontsize=9, loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart5_growth.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 6: 매출 구성 비중 (파이)
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
colors_pie = [BLUE, ORANGE, GREEN]
explode = (0.03, 0.03, 0.03)
wedges, texts, autotexts = ax.pie(seg_values, labels=seg_labels, colors=colors_pie,
                                   autopct='%1.1f%%', startangle=90, explode=explode,
                                   textprops={'fontsize': 11})
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight('bold')
ax.set_title('샘표식품 매출 구성 비중 (2023년 기준)', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart6_segment.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 7: 경쟁사 비교 (가로막대)
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=FIGSIZE)
y_pos = np.arange(len(comp_names))
bars = ax.barh(y_pos, comp_revenue, color=[PURPLE, GREEN, ORANGE, BLUE], alpha=0.85, height=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(comp_names, fontsize=11)
ax.set_xlabel('매출액 (억원)', fontsize=11)
ax.set_title('경쟁사 매출 비교 (2024년 기준)', fontsize=14, fontweight='bold', pad=15)

for bar in bars:
    width_val = bar.get_width()
    ax.text(width_val + 500, bar.get_y() + bar.get_height()/2.,
            f'{width_val:,.0f}억', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_xlim(0, max(comp_revenue)*1.15)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart7_competitors.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 8: 순이익 & 순이익률 콤보
# ════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=FIGSIZE)
bars = ax1.bar(x, net_income, width=0.5, label='당기순이익', color=BLUE, alpha=0.8)
ax2 = ax1.twinx()
ax2.plot(years, net_margin, 'o-', color=RED, linewidth=2.5, markersize=8, label='순이익률(%)')

for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 3,
             f'{int(bar.get_height())}', ha='center', fontsize=9, color=BLUE, fontweight='bold')
for i, v in enumerate(net_margin):
    ax2.text(i, v + 0.3, f'{v}%', ha='center', fontsize=9, color=RED, fontweight='bold')

ax1.set_xlabel('연도', fontsize=11)
ax1.set_ylabel('당기순이익 (억원)', fontsize=11, color=BLUE)
ax2.set_ylabel('순이익률 (%)', fontsize=11, color=RED)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_title('샘표식품 당기순이익 & 순이익률', fontsize=14, fontweight='bold', pad=15)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart8_net_income.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 9: SWOT 다이어그램
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# 4 quadrants
quadrants = [
    (0.1, 5.1, 4.8, 4.8, '#DBEAFE', 'Strengths (강점)', BLUE,
     ['- 80년 전통 간장 시장 1위',
      '- 독보적 발효기술 (3,000+ 미생물)',
      '- 연두: 글로벌 히트 상품',
      '- R&D 매출 4~5% 투자',
      '- 안정적 재무구조 (부채비율 43%)']),
    (5.1, 5.1, 4.8, 4.8, '#FEF3C7', 'Weaknesses (약점)', ORANGE,
     ['- 소규모 시가총액 (1,293억)',
      '- 영업이익률 급락 (12.4%->1.6%)',
      '- 판관비 급증 (36% 상승)',
      '- 낮은 배당수익률 (0.7%)',
      '- 거래량 부족 (유동성 리스크)']),
    (0.1, 0.1, 4.8, 4.8, '#D1FAE5', 'Opportunities (기회)', GREEN,
     ['- K-푸드 글로벌 확산 수혜',
      '- 발효식품 시장 연 7% 성장',
      '- 바이오소재 신사업 진출',
      '- 제천 신공장 (2028년 완공)',
      '- 건강식품/비건 트렌드']),
    (5.1, 0.1, 4.8, 4.8, '#FEE2E2', 'Threats (위협)', RED,
     ['- 대기업(CJ/대상) 지배적 점유율',
      '- 내수 장류시장 정체/축소',
      '- 원재료 가격 상승 지속',
      '- 인구 감소로 내수시장 한계',
      '- 승계 관련 불확실성']),
]

for (qx, qy, qw, qh, color, title, tcolor, items) in quadrants:
    rect = mpatches.FancyBboxPatch((qx, qy), qw, qh, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor=tcolor, linewidth=2)
    ax.add_patch(rect)
    ax.text(qx + qw/2, qy + qh - 0.4, title, ha='center', va='top',
            fontsize=13, fontweight='bold', color=tcolor)
    for j, item in enumerate(items):
        ax.text(qx + 0.3, qy + qh - 1.0 - j*0.75, item,
                fontsize=9.5, va='top', color='#1F2937')

ax.set_title('샘표식품 SWOT 분석', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart9_swot.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 10: 현금흐름 추이 (3종 막대)
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=FIGSIZE)
w = 0.25
ax.bar(x - w, ocf, w, label='영업활동CF', color=BLUE, alpha=0.85)
ax.bar(x,     icf, w, label='투자활동CF', color=ORANGE, alpha=0.85)
ax.bar(x + w, fcf_cf, w, label='재무활동CF', color=GREEN, alpha=0.85)

ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_title('샘표식품 현금흐름 추이', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('금액 (억원)', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart10_cashflow.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 11: CAPEX, FCF & 현금보유
# ════════════════════════════════════════
years_cf = ['2022', '2023', '2024', '2025']
xc = np.arange(len(years_cf))

fig, ax1 = plt.subplots(figsize=FIGSIZE)
ax1.bar(xc - 0.2, capex[1:], 0.35, label='CAPEX', color=ORANGE, alpha=0.8)
ax1.bar(xc + 0.2, fcf[1:], 0.35, label='FCF', color=GREEN, alpha=0.8)
ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)

for i in range(len(years_cf)):
    ax1.text(xc[i]-0.2, capex[i+1]+5, f'{capex[i+1]}', ha='center', fontsize=9, color=ORANGE)
    ax1.text(xc[i]+0.2, fcf[i+1]+ (5 if fcf[i+1]>=0 else -20), f'{fcf[i+1]}', ha='center', fontsize=9, color=GREEN)

ax1.set_xticks(xc)
ax1.set_xticklabels(years_cf)
ax1.set_title('샘표식품 CAPEX & FCF 추이', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('금액 (억원)', fontsize=11)
ax1.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart11_fcf_cash.png'), dpi=DPI, bbox_inches='tight')
plt.close()


# ════════════════════════════════════════
# Chart 12: 영업이익 vs 영업CF (이익의 질)
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.bar(x - 0.2, op_profit, 0.35, label='영업이익', color=BLUE, alpha=0.8)
ax.bar(x + 0.2, ocf, 0.35, label='영업활동CF', color=GREEN, alpha=0.8)

for i in range(len(years)):
    ax.text(x[i]-0.2, op_profit[i]+5, f'{op_profit[i]}', ha='center', fontsize=9, color=BLUE)
    ax.text(x[i]+0.2, ocf[i]+5, f'{ocf[i]}', ha='center', fontsize=9, color=GREEN)

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_title('샘표식품 영업이익 vs 영업활동CF (이익의 질)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('금액 (억원)', fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'chart12_earnings_quality.png'), dpi=DPI, bbox_inches='tight')
plt.close()

print("모든 차트가 성공적으로 생성되었습니다!")
