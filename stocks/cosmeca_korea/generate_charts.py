"""
코스메카코리아 투자 보고서 - 차트 생성 스크립트
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── 데이터 ──
years = ['2021', '2022', '2023', '2024', '2025']
revenue    = [3965, 3994, 4707, 5243, 6409]  # 억원
op_profit  = [201, 104, 492, 604, 835]
net_income = [89, 27, 223, 428, 454]

op_margin  = [5.07, 2.60, 10.44, 11.51, 13.03]
net_margin = [4.28, 1.50, 7.20, 10.24, 9.02]

roe = [9.20, 2.98, 15.09, 19.53, 17.97]
roa = [4.52, 1.53, 8.21, 11.30, 10.06]

debt_ratio   = [99.44, 89.72, 78.65, 68.36, 87.91]
equity_ratio = [50.14, 52.71, 55.98, 59.40, 53.22]

rev_growth = [16.93, 0.74, 17.86, 11.39, 22.24]
op_growth  = [102.99, -48.43, 374.12, 22.80, 38.39]

# 색상 팔레트
C_BLUE = '#2563EB'
C_ORANGE = '#F97316'
C_GREEN = '#10B981'
C_RED = '#EF4444'
C_PURPLE = '#8B5CF6'
C_GRAY = '#6B7280'

def save(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, name), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ {name}")


# ── 1. 매출액 & 영업이익 추이 ──
fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.35

bars1 = ax1.bar(x - w/2, revenue, w, label='매출액', color=C_BLUE, alpha=0.85, zorder=3)
bars2 = ax1.bar(x + w/2, op_profit, w, label='영업이익', color=C_ORANGE, alpha=0.85, zorder=3)

for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=C_ORANGE)

ax1.set_xlabel('연도', fontsize=11)
ax1.set_ylabel('억원', fontsize=11)
ax1.set_title('코스메카코리아 매출액 & 영업이익 추이 (2021~2025)', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(axis='y', alpha=0.3, zorder=0)
ax1.set_ylim(0, max(revenue) * 1.25)
save(fig, 'chart1_revenue_profit.png')


# ── 2. 수익성 지표 (영업이익률 & 순이익률) ──
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, op_margin, 'o-', color=C_BLUE, linewidth=2.5, markersize=8, label='영업이익률 (%)', zorder=3)
ax.plot(years, net_margin, 's-', color=C_GREEN, linewidth=2.5, markersize=8, label='순이익률 (%)', zorder=3)

for i, (om, nm) in enumerate(zip(op_margin, net_margin)):
    ax.annotate(f'{om:.1f}%', (years[i], om), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9, fontweight='bold', color=C_BLUE)
    ax.annotate(f'{nm:.1f}%', (years[i], nm), textcoords="offset points", xytext=(0, -18), ha='center', fontsize=9, fontweight='bold', color=C_GREEN)

ax.set_title('수익성 지표 추이 (2021~2025)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('%', fontsize=11)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, zorder=0)
ax.set_ylim(0, max(op_margin) * 1.5)
save(fig, 'chart2_profitability.png')


# ── 3. ROE & ROA 추이 ──
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.fill_between(years, roe, alpha=0.15, color=C_PURPLE)
ax.plot(years, roe, 'o-', color=C_PURPLE, linewidth=2.5, markersize=8, label='ROE (%)', zorder=3)
ax.plot(years, roa, 's-', color=C_ORANGE, linewidth=2.5, markersize=8, label='ROA (%)', zorder=3)

for i, (r1, r2) in enumerate(zip(roe, roa)):
    ax.annotate(f'{r1:.1f}%', (years[i], r1), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9, fontweight='bold', color=C_PURPLE)
    ax.annotate(f'{r2:.1f}%', (years[i], r2), textcoords="offset points", xytext=(0, -18), ha='center', fontsize=9, fontweight='bold', color=C_ORANGE)

ax.set_title('자본효율성 지표 (ROE & ROA) 추이', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('%', fontsize=11)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, zorder=0)
ax.set_ylim(0, max(roe) * 1.4)
save(fig, 'chart3_roe_roa.png')


# ── 4. 부채비율 & 자기자본비율 ──
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(x - w/2, debt_ratio, w, label='부채비율 (%)', color=C_RED, alpha=0.75, zorder=3)
ax.bar(x + w/2, equity_ratio, w, label='자기자본비율 (%)', color=C_GREEN, alpha=0.75, zorder=3)

for i in range(len(years)):
    ax.text(x[i] - w/2, debt_ratio[i] + 1.5, f'{debt_ratio[i]:.1f}%', ha='center', fontsize=9, fontweight='bold', color=C_RED)
    ax.text(x[i] + w/2, equity_ratio[i] + 1.5, f'{equity_ratio[i]:.1f}%', ha='center', fontsize=9, fontweight='bold', color=C_GREEN)

ax.set_title('재무 안정성 지표 (2021~2025)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('%', fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
ax.set_ylim(0, 130)
save(fig, 'chart4_stability.png')


# ── 5. 매출 성장률 & 영업이익 성장률 ──
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(x - w/2, rev_growth, w, label='매출 성장률 (%)', color=C_BLUE, alpha=0.8, zorder=3)
ax.bar(x + w/2, op_growth, w, label='영업이익 성장률 (%)', color=C_ORANGE, alpha=0.8, zorder=3)

for i in range(len(years)):
    offset_r = 5 if rev_growth[i] >= 0 else -12
    offset_o = 5 if op_growth[i] >= 0 else -12
    ax.text(x[i] - w/2, rev_growth[i] + offset_r, f'{rev_growth[i]:.1f}%', ha='center', fontsize=8, fontweight='bold', color=C_BLUE)
    ax.text(x[i] + w/2, op_growth[i] + offset_o, f'{op_growth[i]:.1f}%', ha='center', fontsize=8, fontweight='bold', color=C_ORANGE)

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_title('성장성 지표 (전년 대비 증가율)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('%', fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, zorder=0)
save(fig, 'chart5_growth.png')


# ── 6. 지역별 매출 비중 (파이차트) ──
fig, ax = plt.subplots(figsize=(8, 8))
regions = ['한국\n51%', '미국\n31%', '중국\n8%', '유럽\n7%', '기타\n3%']
sizes = [51, 31, 8, 7, 3]
colors = [C_BLUE, C_ORANGE, C_RED, C_GREEN, C_GRAY]
explode = (0.03, 0.06, 0, 0, 0)

wedges, texts = ax.pie(sizes, labels=regions, colors=colors, explode=explode,
                       startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title('지역별 매출 비중 (2024년 상반기 기준)', fontsize=14, fontweight='bold', pad=15)
save(fig, 'chart6_region.png')


# ── 7. 경쟁사 비교 (매출 규모) ──
fig, ax = plt.subplots(figsize=(10, 5.5))
companies = ['한국콜마', '코스맥스', '코스메카코리아']
comp_revenue = [24521, 21661, 5243]
comp_colors = [C_GRAY, C_GRAY, C_BLUE]

bars = ax.barh(companies, comp_revenue, color=comp_colors, height=0.5, zorder=3)
for bar, val in zip(bars, comp_revenue):
    ax.text(val + 200, bar.get_y() + bar.get_height()/2,
            f'{val:,}억원', va='center', fontsize=11, fontweight='bold')

ax.set_title('국내 화장품 ODM/OEM Top 3 매출 비교 (2024년)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('억원', fontsize=11)
ax.grid(axis='x', alpha=0.3, zorder=0)
ax.set_xlim(0, max(comp_revenue) * 1.3)
save(fig, 'chart7_competitors.png')


# ── 8. 순이익 추이 & 당기순이익률 콤보 ──
fig, ax1 = plt.subplots(figsize=(10, 5.5))
bars = ax1.bar(years, net_income, color=C_GREEN, alpha=0.8, width=0.5, label='당기순이익 (억원)', zorder=3)
ax2 = ax1.twinx()
ax2.plot(years, net_margin, 'D-', color=C_PURPLE, linewidth=2.5, markersize=8, label='순이익률 (%)', zorder=4)

for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
             f'{int(bar.get_height())}', ha='center', fontsize=10, fontweight='bold', color=C_GREEN)
for i, nm in enumerate(net_margin):
    ax2.annotate(f'{nm:.1f}%', (years[i], nm), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9, fontweight='bold', color=C_PURPLE)

ax1.set_title('당기순이익 & 순이익률 추이 (2021~2025)', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('억원', fontsize=11)
ax2.set_ylabel('순이익률 (%)', fontsize=11, color=C_PURPLE)
ax1.grid(axis='y', alpha=0.3, zorder=0)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
save(fig, 'chart8_net_income.png')


# ── 9. SWOT 다이어그램 ──
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('코스메카코리아 SWOT 분석', fontsize=16, fontweight='bold', y=0.98)

swot_data = {
    'S 강점': [
        '• K-뷰티 ODM 선도기업',
        '• OGM 원스톱 서비스',
        '• 한/미/중 3국 생산거점',
        '• 높은 수익성 (OPM 13%)',
        '• 판교 R&D센터 신설',
    ],
    'W 약점': [
        '• 상위 2사 대비 규모 격차',
        '• 지배구조 이슈',
        '• 중국 법인 실적 변동성',
        '• 특정 고객사 의존도',
        '• 글로벌 인지도 열위',
    ],
    'O 기회': [
        '• K-뷰티 글로벌 확산 지속',
        '• 미국 인디뷰티 시장 확대',
        '• AI/바이오 신제형 개발',
        '• ESG 경영 가치 제고',
        '• 2026 역대 최대 실적 전망',
    ],
    'T 위협': [
        '• 글로벌 경기 침체 우려',
        '• 환율 변동 리스크',
        '• 대형 경쟁사 공격적 확장',
        '• 중국 시장 불확실성',
        '• 원재료 가격 상승',
    ],
}

colors_swot = [C_BLUE, C_ORANGE, C_GREEN, C_RED]
for ax, (title, items), color in zip(axes.flat, swot_data.items(), colors_swot):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(color + '10')
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=color, linewidth=3))
    ax.text(0.5, 0.92, title, ha='center', va='top', fontsize=14, fontweight='bold', color=color)
    for j, item in enumerate(items):
        ax.text(0.08, 0.78 - j * 0.15, item, ha='left', va='top', fontsize=11, color='#1F2937')
    ax.axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, 'chart9_swot.png')


# ── 10. 현금흐름 추이 ──
op_cf   = [79, 167, 420, 695, 550]   # 영업활동현금흐름 (억원)
inv_cf  = [-85, -104, -221, -526, -638]  # 투자활동현금흐름
fin_cf  = [-18, -103, -132, 20, 238]     # 재무활동현금흐름

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(years))
w = 0.25
bars1 = ax.bar(x - w, op_cf, w, label='영업활동', color=C_BLUE, alpha=0.85, zorder=3)
bars2 = ax.bar(x, inv_cf, w, label='투자활동', color=C_RED, alpha=0.85, zorder=3)
bars3 = ax.bar(x + w, fin_cf, w, label='재무활동', color=C_GREEN, alpha=0.85, zorder=3)

for bar in bars1:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + (15 if y >= 0 else -30),
            f'{int(y)}', ha='center', fontsize=8, fontweight='bold', color=C_BLUE)
for bar in bars2:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + (-30 if y < 0 else 15),
            f'{int(y)}', ha='center', fontsize=8, fontweight='bold', color=C_RED)
for bar in bars3:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + (15 if y >= 0 else -30),
            f'{int(y)}', ha='center', fontsize=8, fontweight='bold', color=C_GREEN)

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_title('현금흐름 추이 (2021~2025, 억원)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('억원', fontsize=11)
ax.legend(fontsize=10, loc='upper left')
ax.grid(axis='y', alpha=0.3, zorder=0)
save(fig, 'chart10_cashflow.png')


# ── 11. FCF & 현금보유 추이 ──
fcf      = [-11, 51, 234, 208, -64]     # 잉여현금흐름 (억원)
cash_end = [301, 260, 329, 538, 689]    # 기말 현금보유
capex    = [90, 116, 186, 487, 614]     # CAPEX

fig, ax1 = plt.subplots(figsize=(10, 6))
# CAPEX & FCF 바
w = 0.35
bars_capex = ax1.bar(x - w/2, capex, w, label='CAPEX (억원)', color=C_ORANGE, alpha=0.8, zorder=3)
bars_fcf = ax1.bar(x + w/2, fcf, w, label='FCF (억원)', color=C_PURPLE, alpha=0.8, zorder=3)

for bar in bars_capex:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 12,
             f'{int(bar.get_height())}', ha='center', fontsize=9, fontweight='bold', color=C_ORANGE)
for bar in bars_fcf:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, y + (12 if y >= 0 else -25),
             f'{int(y)}', ha='center', fontsize=9, fontweight='bold', color=C_PURPLE)

# 현금보유 라인 (우축)
ax2 = ax1.twinx()
ax2.plot(years, cash_end, 'D-', color=C_BLUE, linewidth=2.5, markersize=8, label='기말 현금보유 (억원)', zorder=4)
for i, c in enumerate(cash_end):
    ax2.annotate(f'{c}', (years[i], c), textcoords="offset points", xytext=(0, 12),
                 ha='center', fontsize=9, fontweight='bold', color=C_BLUE)

ax1.axhline(y=0, color='black', linewidth=0.8)
ax1.set_title('CAPEX, FCF & 현금보유 추이 (2021~2025)', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('억원', fontsize=11)
ax2.set_ylabel('현금보유 (억원)', fontsize=11, color=C_BLUE)
ax1.grid(axis='y', alpha=0.3, zorder=0)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
save(fig, 'chart11_fcf_cash.png')


# ── 12. 영업이익 vs 영업CF 비교 (이익의 질) ──
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, op_profit, 'o-', color=C_ORANGE, linewidth=2.5, markersize=8, label='영업이익 (억원)', zorder=3)
ax.plot(years, op_cf, 's-', color=C_BLUE, linewidth=2.5, markersize=8, label='영업활동현금흐름 (억원)', zorder=3)
ax.fill_between(years, op_profit, op_cf, alpha=0.1, color=C_BLUE)

for i in range(len(years)):
    ax.annotate(f'{op_profit[i]}', (years[i], op_profit[i]), textcoords="offset points",
                xytext=(0, 12), ha='center', fontsize=9, fontweight='bold', color=C_ORANGE)
    ax.annotate(f'{op_cf[i]}', (years[i], op_cf[i]), textcoords="offset points",
                xytext=(0, -18), ha='center', fontsize=9, fontweight='bold', color=C_BLUE)

ax.set_title('영업이익 vs 영업활동현금흐름 (이익의 질)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('억원', fontsize=11)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, zorder=0)
ax.set_ylim(0, max(max(op_profit), max(op_cf)) * 1.3)
save(fig, 'chart12_earnings_quality.png')


print("\n모든 차트가 성공적으로 생성되었습니다!")
