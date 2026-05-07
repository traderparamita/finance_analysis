#!/usr/bin/env python3
"""Alphabet Inc. (GOOGL) - 투자 분석 차트 생성"""

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
COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE]

OUT = os.path.dirname(os.path.abspath(__file__))
DPI = 150
FIGSIZE = (10, 5.5)

years = ['2020', '2021', '2022', '2023', '2024']

# ── 재무 데이터 ──
revenue =       [182.5, 257.6, 282.8, 307.4, 350.0]
op_income =     [41.2,  78.7,  74.8,  84.3,  112.4]
net_income =    [40.3,  76.0,  60.0,  73.8,  100.1]

op_margin =     [22.6, 30.6, 26.5, 27.4, 32.1]
net_margin =    [22.1, 29.5, 21.2, 24.0, 28.6]
roe =           [18.1, 32.1, 23.6, 27.4, 32.9]
roa =           [12.6, 14.5, 12.9, 13.7, 16.5]

rev_growth =    [12.8, 41.2,  9.8,  8.7, 13.9]
op_growth =     [20.4, 91.0, -5.0, 12.7, 33.3]
ni_growth =     [17.3, 88.8,-21.1, 23.0, 35.7]

debt_ratio =    [30.0, 30.0, 30.0, 30.0, 28.0]
equity_ratio =  [70.0, 70.0, 70.0, 70.0, 72.0]
current_ratio = [3.07, 2.93, 2.38, 2.10, 1.84]

ocf =           [65.1, 91.7, 91.5, 101.7, 125.3]
icf =           [-32.8,-35.5,-20.3,-27.1, -45.5]
fcf_val =       [-24.4,-61.4,-69.8,-72.1, -79.7]  # financing CF
capex =         [22.3, 24.6, 31.5, 32.3, 52.5]
free_cf =       [42.8, 67.0, 60.0, 69.5, 72.8]
cash =          [26.5, 20.9, 21.9, 24.0, 23.5]


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ {name}")


# ── Chart 1: 매출액 & 영업이익 ──
fig, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.35
ax.bar(x - w/2, revenue, w, label='매출액', color=BLUE)
ax.bar(x + w/2, op_income, w, label='영업이익', color=ORANGE)
for i, v in enumerate(revenue):
    ax.text(i - w/2, v + 3, f'{v:.0f}', ha='center', fontsize=9, fontweight='bold')
for i, v in enumerate(op_income):
    ax.text(i + w/2, v + 3, f'{v:.1f}', ha='center', fontsize=9, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('십억 달러 (B$)')
ax.set_title('Alphabet 매출액 & 영업이익 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
save(fig, 'chart1_revenue_profit.png')


# ── Chart 2: 수익성 지표 ──
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(years, op_margin, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='영업이익률 (%)')
ax.plot(years, net_margin, 's-', color=ORANGE, linewidth=2.5, markersize=8, label='순이익률 (%)')
for i in range(len(years)):
    ax.annotate(f'{op_margin[i]:.1f}%', (years[i], op_margin[i]), textcoords="offset points", xytext=(0,12), ha='center', fontsize=9)
    ax.annotate(f'{net_margin[i]:.1f}%', (years[i], net_margin[i]), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=9)
ax.set_ylabel('%')
ax.set_title('Alphabet 수익성 지표 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax.legend()
ax.grid(alpha=0.3)
ax.set_ylim(15, 40)
save(fig, 'chart2_profitability.png')


# ── Chart 3: ROE & ROA ──
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(years, roe, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='ROE (%)')
ax.fill_between(years, roe, alpha=0.15, color=BLUE)
ax.plot(years, roa, 's-', color=GREEN, linewidth=2.5, markersize=8, label='ROA (%)')
ax.fill_between(years, roa, alpha=0.15, color=GREEN)
for i in range(len(years)):
    ax.annotate(f'{roe[i]:.1f}%', (years[i], roe[i]), textcoords="offset points", xytext=(0,12), ha='center', fontsize=9)
    ax.annotate(f'{roa[i]:.1f}%', (years[i], roa[i]), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=9)
ax.set_ylabel('%')
ax.set_title('Alphabet ROE & ROA 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax.legend()
ax.grid(alpha=0.3)
save(fig, 'chart3_roe_roa.png')


# ── Chart 4: 재무 안정성 ──
fig, ax1 = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.25
ax1.bar(x - w, debt_ratio, w, label='부채비율 (%)', color=RED)
ax1.bar(x, equity_ratio, w, label='자기자본비율 (%)', color=BLUE)
ax2 = ax1.twinx()
ax2.plot(years, current_ratio, 'D-', color=GREEN, linewidth=2.5, markersize=8, label='유동비율 (배)')
for i, v in enumerate(current_ratio):
    ax2.annotate(f'{v:.2f}', (years[i], v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color=GREEN)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel('%')
ax2.set_ylabel('유동비율 (배)')
ax1.set_title('Alphabet 재무 안정성 지표 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper right')
ax1.grid(axis='y', alpha=0.3)
ax1.set_axisbelow(True)
save(fig, 'chart4_stability.png')


# ── Chart 5: 성장률 ──
fig, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.25
ax.bar(x - w, rev_growth, w, label='매출 성장률', color=BLUE)
ax.bar(x, op_growth, w, label='영업이익 성장률', color=ORANGE)
ax.bar(x + w, ni_growth, w, label='순이익 성장률', color=GREEN)
ax.axhline(y=0, color='gray', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('%')
ax.set_title('Alphabet 성장률 지표 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
save(fig, 'chart5_growth.png')


# ── Chart 6: 매출 구성 (FY2024) ──
fig, ax = plt.subplots(figsize=(9, 6))
segments = ['Google Search\n(56.6%)', 'Google Cloud\n(12.4%)', '구독/플랫폼/\n디바이스 (11.5%)', 'YouTube 광고\n(10.3%)', 'Google\nNetwork (8.7%)', 'Other Bets\n(0.5%)']
sizes = [56.6, 12.4, 11.5, 10.3, 8.7, 0.5]
colors_pie = [BLUE, GREEN, PURPLE, RED, ORANGE, '#94A3B8']
explode = (0.05, 0.05, 0, 0, 0, 0)
wedges, texts, autotexts = ax.pie(sizes, explode=explode, colors=colors_pie,
    autopct='%1.1f%%', startangle=140, pctdistance=0.75,
    textprops={'fontsize': 10})
for t in autotexts:
    t.set_fontweight('bold')
ax.legend(segments, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
ax.set_title('Alphabet 매출 구성 (FY2024)', fontsize=14, fontweight='bold', pad=15)
save(fig, 'chart6_segment.png')


# ── Chart 7: 경쟁사 비교 (FY2024 매출) ──
fig, ax = plt.subplots(figsize=FIGSIZE)
companies = ['Amazon', 'Apple', 'Alphabet', 'Microsoft', 'Meta']
revenues_comp = [620, 400, 350, 265, 165]
colors_comp = ['#FF9900', '#555555', BLUE, '#00A4EF', '#1877F2']
bars = ax.barh(companies, revenues_comp, color=colors_comp, height=0.6)
for bar, val in zip(bars, revenues_comp):
    ax.text(val + 5, bar.get_y() + bar.get_height()/2, f'${val}B', va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('매출액 (십억 달러)')
ax.set_title('빅테크 기업 매출 비교 (FY2024)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 700)
ax.grid(axis='x', alpha=0.3)
ax.set_axisbelow(True)
save(fig, 'chart7_competitors.png')


# ── Chart 8: 순이익 & 순이익률 콤보 ──
fig, ax1 = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
ax1.bar(x, net_income, 0.5, color=BLUE, alpha=0.85, label='순이익 (B$)')
for i, v in enumerate(net_income):
    ax1.text(i, v + 1.5, f'{v:.1f}', ha='center', fontsize=9, fontweight='bold')
ax2 = ax1.twinx()
ax2.plot(years, net_margin, 'D-', color=ORANGE, linewidth=2.5, markersize=8, label='순이익률 (%)')
for i, v in enumerate(net_margin):
    ax2.annotate(f'{v:.1f}%', (years[i], v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color=ORANGE)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel('십억 달러 (B$)')
ax2.set_ylabel('순이익률 (%)')
ax1.set_title('Alphabet 순이익 & 순이익률 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')
ax1.grid(axis='y', alpha=0.3)
ax1.set_axisbelow(True)
save(fig, 'chart8_net_income.png')


# ── Chart 9: SWOT ──
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Alphabet SWOT 분석', fontsize=16, fontweight='bold', y=0.98)

swot = {
    'Strengths (강점)': [
        '• 검색 시장 점유율 90%+',
        '• 연간 FCF $72.8B의 현금 창출력',
        '• AI/Gemini 기술 선도',
        '• 구글 클라우드 고성장 (30%+)',
        '• Android 30억+ 기기 생태계',
    ],
    'Weaknesses (약점)': [
        '• 광고 매출 의존도 75%+',
        '• Other Bets 수익성 부족',
        '• 유동비율 하락 추세',
        '• 반독점 규제 리스크',
        '• 하드웨어 사업 경쟁력 미흡',
    ],
    'Opportunities (기회)': [
        '• AI 시장 연 26%+ 성장',
        '• 클라우드 시장 점유율 확대',
        '• Waymo 자율주행 상용화',
        '• YouTube 쇼핑/구독 수익',
        '• 헬스케어 AI 진출',
    ],
    'Threats (위협)': [
        '• 반독점 소송 (크롬/광고)',
        '• OpenAI/MS의 AI 검색 경쟁',
        '• 개인정보 규제 강화',
        '• 애플 디폴트 검색 계약 불확실',
        '• AI CAPEX 과잉투자 리스크',
    ],
}

bg_colors = ['#DBEAFE', '#FEE2E2', '#D1FAE5', '#FEF3C7']
title_colors = [BLUE, RED, GREEN, ORANGE]

for idx, (title, items) in enumerate(swot.items()):
    ax = axes[idx//2][idx%2]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(bg_colors[idx])
    ax.set_title(title, fontsize=13, fontweight='bold', color=title_colors[idx], pad=10)
    text = '\n'.join(items)
    ax.text(0.05, 0.85, text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', linespacing=1.8)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, 'chart9_swot.png')


# ── Chart 10: 현금흐름 3종 ──
fig, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.25
ax.bar(x - w, ocf, w, label='영업CF', color=BLUE)
ax.bar(x, icf, w, label='투자CF', color=RED)
ax.bar(x + w, fcf_val, w, label='재무CF', color=PURPLE)
ax.axhline(y=0, color='gray', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('십억 달러 (B$)')
ax.set_title('Alphabet 현금흐름 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
save(fig, 'chart10_cashflow.png')


# ── Chart 11: CAPEX, FCF & 현금보유 ──
fig, ax1 = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.3
ax1.bar(x - w/2, capex, w, label='CAPEX', color=RED, alpha=0.85)
ax1.bar(x + w/2, free_cf, w, label='FCF', color=BLUE, alpha=0.85)
for i in range(len(years)):
    ax1.text(i - w/2, capex[i]+1, f'{capex[i]:.1f}', ha='center', fontsize=8, fontweight='bold')
    ax1.text(i + w/2, free_cf[i]+1, f'{free_cf[i]:.1f}', ha='center', fontsize=8, fontweight='bold')
ax2 = ax1.twinx()
ax2.plot(years, cash, 'D-', color=GREEN, linewidth=2.5, markersize=8, label='기말 현금 (B$)')
for i, v in enumerate(cash):
    ax2.annotate(f'{v:.1f}', (years[i], v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color=GREEN)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel('십억 달러 (B$)')
ax2.set_ylabel('기말 현금 (B$)')
ax1.set_title('Alphabet CAPEX, FCF & 현금보유 추이 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')
ax1.grid(axis='y', alpha=0.3)
ax1.set_axisbelow(True)
save(fig, 'chart11_fcf_cash.png')


# ── Chart 12: 영업이익 vs 영업CF (이익의 질) ──
fig, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(years))
w = 0.3
ax.bar(x - w/2, op_income, w, label='영업이익', color=ORANGE, alpha=0.85)
ax.bar(x + w/2, ocf, w, label='영업현금흐름', color=BLUE, alpha=0.85)
ratio = [o/p*100 for o, p in zip(ocf, op_income)]
ax2 = ax.twinx()
ax2.plot(years, ratio, 'D-', color=GREEN, linewidth=2.5, markersize=8, label='영업CF/영업이익 (%)')
for i, v in enumerate(ratio):
    ax2.annotate(f'{v:.0f}%', (years[i], v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color=GREEN)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('십억 달러 (B$)')
ax2.set_ylabel('%')
ax.set_title('Alphabet 영업이익 vs 영업CF — 이익의 질 (2020-2024)', fontsize=14, fontweight='bold', pad=15)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc='upper left')
ax.grid(axis='y', alpha=0.3)
ax.set_axisbelow(True)
save(fig, 'chart12_earnings_quality.png')

print("\n✅ 모든 차트 생성 완료!")
