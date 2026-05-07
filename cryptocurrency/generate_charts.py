"""
가상화폐(비트코인) 투자 분석 보고서 차트 생성
작성일: 2026-04-01
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib import font_manager
import os

# 한글 폰트 설정 (macOS)
font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'sans-serif'

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 색상 팔레트
COLORS = {
    'primary': '#F7931A',    # 비트코인 오렌지
    'secondary': '#4A90D9',  # 블루
    'danger': '#E74C3C',     # 레드
    'success': '#2ECC71',    # 그린
    'warning': '#F39C12',    # 옐로우
    'dark': '#2C3E50',       # 다크
    'light_bg': '#F8F9FA',   # 배경
    'grid': '#E0E0E0',
}


def style_ax(ax, title, xlabel='', ylabel=''):
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color=COLORS['dark'])
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=COLORS['dark'])
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=COLORS['dark'])
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.set_facecolor(COLORS['light_bg'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ── Chart 1: 비트코인 가격 역사 (2020~2026) ──
def chart1_price_history():
    fig, ax = plt.subplots(figsize=(14, 7))

    # 주요 가격 포인트 (월별 근사치)
    dates = [
        '2020.01', '2020.03', '2020.06', '2020.09', '2020.12',
        '2021.01', '2021.04', '2021.05', '2021.07', '2021.09', '2021.11', '2021.12',
        '2022.01', '2022.05', '2022.06', '2022.09', '2022.11', '2022.12',
        '2023.01', '2023.04', '2023.06', '2023.10', '2023.12',
        '2024.01', '2024.03', '2024.04', '2024.06', '2024.09', '2024.11', '2024.12',
        '2025.01', '2025.04', '2025.07', '2025.10', '2025.12',
        '2026.01', '2026.02', '2026.03', '2026.04'
    ]
    prices = [
        7200, 5000, 9500, 10500, 29000,
        33000, 58000, 37000, 30000, 43000, 69000, 46000,
        42000, 30000, 19000, 20000, 15500, 16500,
        21000, 28000, 30500, 34000, 42000,
        46000, 73000, 63762, 58000, 62000, 95000, 100000,
        100000, 83671, 92000, 126198, 82000,
        74000, 65000, 66000, 68680
    ]

    x = np.arange(len(dates))

    # 배경 구간 표시
    ax.axvspan(0, 4, alpha=0.1, color=COLORS['success'], label='코로나 회복기')
    ax.axvspan(5, 11, alpha=0.1, color=COLORS['primary'], label='2021 불마켓')
    ax.axvspan(12, 17, alpha=0.1, color=COLORS['danger'], label='2022 베어마켓')
    ax.axvspan(18, 22, alpha=0.1, color=COLORS['secondary'], label='2023 회복기')
    ax.axvspan(23, 29, alpha=0.1, color=COLORS['success'], label='ETF/반감기 랠리')
    ax.axvspan(30, 34, alpha=0.1, color=COLORS['warning'], label='2025 정점→조정')
    ax.axvspan(35, 38, alpha=0.1, color=COLORS['danger'], label='2026 전쟁 충격')

    ax.plot(x, prices, color=COLORS['primary'], linewidth=2.5, zorder=5)
    ax.fill_between(x, prices, alpha=0.15, color=COLORS['primary'])

    # 주요 이벤트 표시
    events = {
        2: ('코로나 폭락\n$5,000', -8000),
        10: ('ATH $69,000', 5000),
        16: ('FTX 파산\n$15,500', -5000),
        23: ('ETF 승인', 8000),
        25: ('반감기', -10000),
        33: ('ATH $126,198', 5000),
        38: ('현재 $68,680', 5000),
    }
    for idx, (text, offset) in events.items():
        ax.annotate(text, xy=(x[idx], prices[idx]),
                    xytext=(0, offset), textcoords='offset points',
                    fontsize=8, ha='center', fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=COLORS['dark'], lw=1),
                    color=COLORS['dark'],
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS['grid'], alpha=0.9))

    ax.set_xticks(x[::3])
    ax.set_xticklabels([dates[i] for i in range(0, len(dates), 3)], rotation=45, ha='right', fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))

    style_ax(ax, '비트코인 가격 역사 (2020~2026)', ylabel='가격 (USD)')
    ax.legend(loc='upper left', fontsize=8, framealpha=0.9, ncol=2)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart1_price_history.png'))
    plt.close(fig)
    print('  chart1_price_history.png 생성 완료')


# ── Chart 2: 반감기 사이클 비교 ──
def chart2_halving_cycles():
    fig, ax = plt.subplots(figsize=(12, 7))

    # 반감기 이후 일수 vs 가격 변동률 (근사치)
    days = np.arange(0, 731, 30)  # 0~730일 (2년)

    # 2012 반감기 (2012.11 → 2014.11)
    cycle1_peak = 9000  # %
    cycle1 = np.clip(cycle1_peak * np.sin(np.pi * days / 730) ** 0.6, 0, cycle1_peak)

    # 2016 반감기 (2016.07 → 2018.07)
    cycle2_peak = 2900
    cycle2 = np.clip(cycle2_peak * np.sin(np.pi * days / 730) ** 0.7, 0, cycle2_peak)

    # 2020 반감기 (2020.05 → 2022.05)
    cycle3_peak = 700
    cycle3 = np.clip(cycle3_peak * np.sin(np.pi * days / 700) ** 0.8, 0, cycle3_peak)

    # 2024 반감기 (2024.04 → 현재 ~710일)
    cycle4 = np.zeros_like(days, dtype=float)
    milestones = {0: 0, 90: 15, 180: 50, 270: 55, 365: 31, 450: 70, 540: 98, 600: 45, 660: 3, 710: 8, 730: 10}
    ms_days = sorted(milestones.keys())
    ms_vals = [milestones[d] for d in ms_days]
    cycle4 = np.interp(days, ms_days, ms_vals)

    ax.plot(days, cycle1, '--', color='#95A5A6', linewidth=1.5, label='2012 반감기 (+9,000%)', alpha=0.6)
    ax.plot(days, cycle2, '--', color=COLORS['secondary'], linewidth=1.5, label='2016 반감기 (+2,900%)', alpha=0.7)
    ax.plot(days, cycle3, '--', color=COLORS['success'], linewidth=1.5, label='2020 반감기 (+700%)', alpha=0.8)
    ax.plot(days[:24], cycle4[:24], '-', color=COLORS['primary'], linewidth=3, label='2024 반감기 (진행 중, +8%)')

    # 현재 위치 표시
    current_day = 710
    ax.axvline(x=current_day, color=COLORS['danger'], linestyle=':', alpha=0.7)
    ax.annotate('← 현재 (710일)', xy=(current_day, 150), fontsize=10, color=COLORS['danger'], fontweight='bold')

    # 과거 사이클 고점 구간 표시
    ax.axvspan(365, 550, alpha=0.08, color=COLORS['warning'])
    ax.text(457, max(cycle1) * 0.95, '과거 사이클 고점 구간\n(반감기 후 12~18개월)',
            ha='center', fontsize=9, color=COLORS['warning'], fontstyle='italic')

    ax.set_xlabel('반감기 이후 경과일', fontsize=11)
    ax.set_ylabel('가격 변동률 (%)', fontsize=11)
    style_ax(ax, '비트코인 반감기 사이클 비교')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart2_halving_cycles.png'))
    plt.close(fig)
    print('  chart2_halving_cycles.png 생성 완료')


# ── Chart 3: 공포·탐욕 지수 vs 가격 ──
def chart3_fear_greed():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])

    months = ['24.01', '24.03', '24.05', '24.07', '24.09', '24.11',
              '25.01', '25.03', '25.05', '25.07', '25.09', '25.11',
              '26.01', '26.03', '26.04']
    prices = [46000, 73000, 62000, 58000, 62000, 95000,
              100000, 85000, 90000, 92000, 120000, 82000,
              74000, 66000, 68680]
    fg_index = [72, 80, 55, 45, 60, 78,
                82, 65, 70, 68, 90, 40,
                25, 12, 8]

    x = np.arange(len(months))

    # 상단: 가격
    ax1.plot(x, prices, color=COLORS['primary'], linewidth=2, marker='o', markersize=4)
    ax1.fill_between(x, prices, alpha=0.15, color=COLORS['primary'])
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    style_ax(ax1, '비트코인 가격 vs 공포·탐욕 지수', ylabel='가격 (USD)')
    ax1.set_xticks(x)
    ax1.set_xticklabels([])

    # 하단: 공포·탐욕 지수
    colors = []
    for v in fg_index:
        if v <= 20:
            colors.append(COLORS['danger'])
        elif v <= 40:
            colors.append('#E67E22')
        elif v <= 60:
            colors.append(COLORS['warning'])
        elif v <= 80:
            colors.append(COLORS['success'])
        else:
            colors.append('#27AE60')

    ax2.bar(x, fg_index, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)

    # 구간 라벨
    ax2.axhline(y=20, color=COLORS['danger'], linestyle='--', alpha=0.5, linewidth=0.8)
    ax2.axhline(y=80, color=COLORS['success'], linestyle='--', alpha=0.5, linewidth=0.8)
    ax2.text(len(x) - 0.5, 10, '극단적 공포', fontsize=8, color=COLORS['danger'], ha='right')
    ax2.text(len(x) - 0.5, 85, '극단적 탐욕', fontsize=8, color=COLORS['success'], ha='right')

    # 현재 지수 강조
    ax2.annotate(f'현재: {fg_index[-1]}', xy=(x[-1], fg_index[-1]),
                 xytext=(0, 20), textcoords='offset points',
                 fontsize=10, fontweight='bold', color=COLORS['danger'],
                 arrowprops=dict(arrowstyle='->', color=COLORS['danger']))

    ax2.set_xticks(x)
    ax2.set_xticklabels(months, rotation=45, ha='right', fontsize=8)
    ax2.set_ylim(0, 100)
    style_ax(ax2, '', ylabel='공포·탐욕 지수')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart3_fear_greed.png'))
    plt.close(fig)
    print('  chart3_fear_greed.png 생성 완료')


# ── Chart 4: ETF 자금 흐름 ──
def chart4_etf_flows():
    fig, ax = plt.subplots(figsize=(12, 6))

    quarters = ['24Q1', '24Q2', '24Q3', '24Q4', '25Q1', '25Q2', '25Q3', '25Q4', '26Q1']
    inflows = [12.0, 4.5, 2.0, 5.5, 8.0, 6.5, 7.0, 1.5, -0.5]  # 십억 달러

    colors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in inflows]
    bars = ax.bar(quarters, inflows, color=colors, alpha=0.85, edgecolor='white', linewidth=1.5, width=0.6)

    for bar, val in zip(bars, inflows):
        y_pos = bar.get_height() + 0.2 if val >= 0 else bar.get_height() - 0.4
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                f'${val:.1f}B', ha='center', fontsize=9, fontweight='bold',
                color=COLORS['dark'])

    # 누적선
    cumulative = np.cumsum(inflows)
    ax2 = ax.twinx()
    ax2.plot(quarters, cumulative, color=COLORS['secondary'], linewidth=2, marker='D', markersize=6, label='누적 유입')
    ax2.set_ylabel('누적 유입 (십억 $)', fontsize=10, color=COLORS['secondary'])
    ax2.tick_params(axis='y', colors=COLORS['secondary'])

    style_ax(ax, '비트코인 ETF 분기별 순유입/유출', ylabel='분기 순유입 (십억 $)')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.spines['top'].set_visible(False)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart4_etf_flows.png'))
    plt.close(fig)
    print('  chart4_etf_flows.png 생성 완료')


# ── Chart 5: 리스크/리워드 시나리오 ──
def chart5_scenarios():
    fig, ax = plt.subplots(figsize=(10, 7))

    scenarios = ['극단적 약세\n(전쟁 확대)', '약세\n(매크로 역풍)', '기본\n(현상 유지)', '강세\n(전쟁 종료)', '극단적 강세\n(유동성 폭발)']
    prices = [50000, 60000, 75000, 100000, 150000]
    probabilities = [10, 20, 35, 25, 10]
    returns_pct = [round((p - 68680) / 68680 * 100, 1) for p in prices]

    colors = [COLORS['danger'], '#E67E22', COLORS['warning'], COLORS['success'], '#27AE60']

    bars = ax.barh(scenarios, prices, color=colors, alpha=0.85, edgecolor='white', linewidth=1.5, height=0.6)

    # 현재 가격 표시
    ax.axvline(x=68680, color=COLORS['dark'], linestyle='--', linewidth=2, alpha=0.7)
    ax.text(68680, 4.7, '현재 $68,680', fontsize=9, fontweight='bold', color=COLORS['dark'], ha='center')

    for bar, price, prob, ret in zip(bars, prices, probabilities, returns_pct):
        sign = '+' if ret > 0 else ''
        ax.text(bar.get_width() + 1500, bar.get_y() + bar.get_height() / 2,
                f'${price:,}  ({sign}{ret}%)  확률 {prob}%',
                va='center', fontsize=9, fontweight='bold', color=COLORS['dark'])

    ax.set_xlim(0, 180000)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    style_ax(ax, '2026년 말 비트코인 가격 시나리오', xlabel='가격 (USD)')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart5_scenarios.png'))
    plt.close(fig)
    print('  chart5_scenarios.png 생성 완료')


# ── Chart 6: 주요 리스크 매트릭스 ──
def chart6_risk_matrix():
    fig, ax = plt.subplots(figsize=(10, 8))

    risks = {
        '이란 전쟁 확대': (0.7, 0.9),
        '스태그플레이션': (0.5, 0.75),
        'ETF 순유출': (0.3, 0.7),
        '레버리지 위기': (0.45, 0.7),
        '규제 역풍': (0.2, 0.5),
        '양자컴퓨터 위협': (0.05, 0.3),
    }

    for name, (prob, impact) in risks.items():
        severity = prob * impact
        size = severity * 800 + 100
        color = COLORS['danger'] if severity > 0.4 else COLORS['warning'] if severity > 0.2 else COLORS['success']
        ax.scatter(prob, impact, s=size, color=color, alpha=0.7, edgecolors=COLORS['dark'], linewidth=1.5, zorder=5)
        ax.annotate(name, (prob, impact), textcoords='offset points', xytext=(10, 10),
                    fontsize=9, fontweight='bold', color=COLORS['dark'],
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    # 구간 구분
    ax.axhline(y=0.5, color=COLORS['grid'], linestyle='--', alpha=0.5)
    ax.axvline(x=0.5, color=COLORS['grid'], linestyle='--', alpha=0.5)
    ax.fill_between([0.5, 1], 0.5, 1, alpha=0.05, color=COLORS['danger'])
    ax.text(0.75, 0.95, '고위험 영역', fontsize=10, ha='center', color=COLORS['danger'], alpha=0.5, fontstyle='italic')
    ax.fill_between([0, 0.5], 0, 0.5, alpha=0.05, color=COLORS['success'])
    ax.text(0.25, 0.05, '저위험 영역', fontsize=10, ha='center', color=COLORS['success'], alpha=0.5, fontstyle='italic')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    style_ax(ax, '가상화폐 투자 리스크 매트릭스', xlabel='발생 확률', ylabel='영향도')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart6_risk_matrix.png'))
    plt.close(fig)
    print('  chart6_risk_matrix.png 생성 완료')


# ── Chart 7: 투자 전략 배분 ──
def chart7_allocation():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    strategies = [
        ('보수적 투자자', ['가상화폐 5%', '채권 45%', '주식 30%', '금/원자재 15%', '현금 5%'],
         [5, 45, 30, 15, 5]),
        ('균형형 투자자', ['가상화폐 10%', '채권 30%', '주식 40%', '금/원자재 10%', '현금 10%'],
         [10, 30, 40, 10, 10]),
        ('적극적 투자자', ['가상화폐 15%', '채권 15%', '주식 45%', '금/원자재 15%', '현금 10%'],
         [15, 15, 45, 15, 10]),
    ]

    pie_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning'], '#95A5A6']

    for ax_i, (title, labels, sizes) in zip(axes, strategies):
        wedges, texts, autotexts = ax_i.pie(sizes, labels=labels, colors=pie_colors, autopct='%1.0f%%',
                                             startangle=90, textprops={'fontsize': 8})
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
        ax_i.set_title(title, fontsize=12, fontweight='bold', color=COLORS['dark'], pad=10)

    fig.suptitle('투자 성향별 포트폴리오 배분 전략 (이란 전쟁 시기)', fontsize=14, fontweight='bold',
                 color=COLORS['dark'], y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart7_allocation.png'))
    plt.close(fig)
    print('  chart7_allocation.png 생성 완료')


# ── Chart 8: 분할매수(DCA) 시뮬레이션 ──
def chart8_dca_simulation():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])

    months = ['26.04', '26.05', '26.06', '26.07', '26.08', '26.09',
              '26.10', '26.11', '26.12']

    # 시나리오별 가격 경로
    base_prices = [68680, 64000, 60000, 63000, 68000, 72000, 78000, 85000, 90000]
    bear_prices = [68680, 62000, 56000, 52000, 55000, 58000, 62000, 60000, 65000]
    bull_prices = [68680, 70000, 72000, 80000, 88000, 95000, 100000, 110000, 120000]

    x = np.arange(len(months))

    ax1.plot(x, base_prices, '-o', color=COLORS['warning'], linewidth=2, label='기본 시나리오', markersize=5)
    ax1.plot(x, bear_prices, '-o', color=COLORS['danger'], linewidth=2, label='약세 시나리오', markersize=5)
    ax1.plot(x, bull_prices, '-o', color=COLORS['success'], linewidth=2, label='강세 시나리오', markersize=5)

    # DCA 평균 단가 (매월 동일 금액 투자 시)
    monthly_invest = 1000000  # 100만원
    dca_avg_base = []
    dca_avg_bear = []
    dca_avg_bull = []
    for i in range(len(months)):
        total_btc_b = sum(monthly_invest / p for p in base_prices[:i+1])
        total_btc_br = sum(monthly_invest / p for p in bear_prices[:i+1])
        total_btc_bl = sum(monthly_invest / p for p in bull_prices[:i+1])
        total_invested = monthly_invest * (i + 1)
        dca_avg_base.append(total_invested / total_btc_b)
        dca_avg_bear.append(total_invested / total_btc_br)
        dca_avg_bull.append(total_invested / total_btc_bl)

    ax1.plot(x, dca_avg_base, '--', color=COLORS['warning'], linewidth=1, alpha=0.6)

    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax1.set_xticks(x)
    ax1.set_xticklabels([])
    style_ax(ax1, 'DCA(분할매수) 시뮬레이션 — 시나리오별 가격 경로', ylabel='가격 (USD)')
    ax1.legend(fontsize=9)

    # 하단: DCA 수익률
    lump_returns_base = [(p - 68680) / 68680 * 100 for p in base_prices]
    dca_returns_base = [(base_prices[i] - dca_avg_base[i]) / dca_avg_base[i] * 100 for i in range(len(months))]

    width = 0.35
    ax2.bar(x - width/2, lump_returns_base, width, color=COLORS['secondary'], alpha=0.7, label='일시불 매수 수익률')
    ax2.bar(x + width/2, dca_returns_base, width, color=COLORS['primary'], alpha=0.7, label='DCA 수익률')

    ax2.axhline(y=0, color=COLORS['dark'], linewidth=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(months, fontsize=9)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    style_ax(ax2, '', xlabel='월', ylabel='수익률')
    ax2.legend(fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart8_dca_simulation.png'))
    plt.close(fig)
    print('  chart8_dca_simulation.png 생성 완료')


# ── Chart 9: 거래소 보유량 & 장기보유자 비율 ──
def chart9_onchain():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 거래소 보유량
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
    exchange_btc = [2.9, 2.85, 2.95, 2.7, 2.6, 2.45, 2.35, 2.28, 2.25]  # 백만 BTC

    ax1.fill_between(years, exchange_btc, alpha=0.3, color=COLORS['secondary'])
    ax1.plot(years, exchange_btc, '-o', color=COLORS['secondary'], linewidth=2.5, markersize=6)
    ax1.annotate(f'{exchange_btc[-1]}M BTC\n(2018년 이후 최저)',
                 xy=(len(years)-1, exchange_btc[-1]),
                 xytext=(-60, 30), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=COLORS['danger'],
                 arrowprops=dict(arrowstyle='->', color=COLORS['danger']),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEBD0', edgecolor=COLORS['warning']))
    ax1.set_ylabel('거래소 보유량 (백만 BTC)', fontsize=10)
    style_ax(ax1, '거래소 비트코인 보유량 추이')

    # 장기보유자 비율
    categories = ['장기보유자\n(>1년)', '중기보유자\n(3~12개월)', '단기보유자\n(<3개월)', 'ETF\n보유분']
    percentages = [72, 10, 12, 6]
    bar_colors = [COLORS['success'], COLORS['secondary'], COLORS['warning'], COLORS['primary']]

    bars = ax2.bar(categories, percentages, color=bar_colors, alpha=0.85, edgecolor='white', linewidth=1.5, width=0.6)
    for bar, pct in zip(bars, percentages):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f'{pct}%', ha='center', fontsize=11, fontweight='bold', color=COLORS['dark'])

    style_ax(ax2, '비트코인 보유 기간별 분포 (2026년 4월)', ylabel='비율 (%)')
    ax2.set_ylim(0, 85)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart9_onchain.png'))
    plt.close(fig)
    print('  chart9_onchain.png 생성 완료')


# ── Chart 10: 종합 평가 레이더 차트 ──
def chart10_radar():
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    categories = ['장기 펀더멘털', '단기 모멘텀', '밸류에이션\n(상대적)', '리스크/리워드', '시장 심리\n(역발상)', '제도화 수준']
    values = [8, 3, 7, 7, 8, 9]  # 시장 심리는 극단적 공포의 역발상 매수 관점

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values_plot = values + values[:1]
    angles += angles[:1]

    ax.plot(angles, values_plot, 'o-', linewidth=2.5, color=COLORS['primary'], markersize=8)
    ax.fill(angles, values_plot, alpha=0.25, color=COLORS['primary'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold', color=COLORS['dark'])
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='gray')
    ax.set_title('비트코인 투자 매력도 종합 평가\n(10점 만점)', fontsize=14, fontweight='bold',
                 color=COLORS['dark'], pad=20)

    # 평균 점수 표시
    avg = np.mean(values)
    ax.text(0, -2.5, f'종합 점수: {avg:.1f}/10', ha='center', fontsize=13,
            fontweight='bold', color=COLORS['primary'],
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0', edgecolor=COLORS['primary']))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart10_radar.png'))
    plt.close(fig)
    print('  chart10_radar.png 생성 완료')


if __name__ == '__main__':
    print('차트 생성 시작...\n')
    chart1_price_history()
    chart2_halving_cycles()
    chart3_fear_greed()
    chart4_etf_flows()
    chart5_scenarios()
    chart6_risk_matrix()
    chart7_allocation()
    chart8_dca_simulation()
    chart9_onchain()
    chart10_radar()
    print('\n모든 차트 생성 완료!')
