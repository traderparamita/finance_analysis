#!/usr/bin/env python3
"""
shared/chart_engine.py
차트 생성 공통 엔진 — 회사별 config 딕셔너리를 받아 차트 12개를 생성한다.

사용법:
    from shared.chart_engine import generate_all_charts
    from 미래에셋생명.config import CONFIG
    generate_all_charts(CONFIG)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import os
import textwrap

# ── 한글 폰트 자동 감지 (cross-platform) ──────────────
# pdf_utils.py와 동일한 후보 리스트를 사용해 일관성 유지.
_CHART_FONT_CANDIDATES = [
    # macOS
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
    '/System/Library/Fonts/AppleGothic.ttf',
    '/Library/Fonts/AppleSDGothicNeo.ttc',
    # Linux
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/nanum/NanumGothic.ttf',
    # Windows
    'C:/Windows/Fonts/malgun.ttf',
    'C:/Windows/Fonts/NanumGothic.ttf',
    # 사용자 설치
    os.path.expanduser('~/.fonts/NotoSansKR-Regular.otf'),
    os.path.expanduser('~/.fonts/NanumGothic.ttf'),
    os.path.expanduser('~/Library/Fonts/NotoSansKR-Regular.otf'),
]

# 환경변수 오버라이드 (최우선)
_env_font = os.environ.get('FINANCE_KOREAN_FONT')
if _env_font:
    _CHART_FONT_CANDIDATES.insert(0, os.path.expanduser(_env_font))

_CHART_FONT_FAMILY = None
for _fp in _CHART_FONT_CANDIDATES:
    if os.path.exists(_fp):
        try:
            font_manager.fontManager.addfont(_fp)
            _CHART_FONT_FAMILY = font_manager.FontProperties(fname=_fp).get_name()
            break
        except Exception:
            continue

if _CHART_FONT_FAMILY:
    plt.rcParams['font.family'] = _CHART_FONT_FAMILY
else:
    # 한글 폰트 없으면 sans-serif (한글 깨짐) — pdf_utils에서 이미 경고 발생
    plt.rcParams['font.family'] = 'sans-serif'

plt.rcParams['axes.unicode_minus'] = False

FIGSIZE = (10, 5.5)
DPI = 150


def _save(fig, out_dir, name):
    fig.savefig(os.path.join(out_dir, name), dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ {name}')


# ══════════════════════════════════════════════════════════
# Chart 1: 매출(보험료수익) & 영업이익 묶음 막대
# ══════════════════════════════════════════════════════════
def chart1_revenue_profit(cfg, out_dir):
    c = cfg['colors']
    years = cfg['years']
    revenue = cfg['revenue']
    op_income = cfg['op_income']
    company = cfg['name']

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years))
    w = 0.35
    ax.bar(x - w/2, revenue,   w, label=cfg.get('revenue_label', '매출액'), color=c['primary'], alpha=0.85)
    ax.bar(x + w/2, op_income, w, label='영업이익', color=c['accent'], alpha=0.85)

    label_gap_rev = max(revenue) * 0.01
    label_gap_op  = max(op_income) * 0.02
    for i, v in enumerate(revenue):
        ax.text(i - w/2, v + label_gap_rev, f'{v:,}', ha='center', fontsize=8, fontweight='bold', color=c['primary'])
    for i, v in enumerate(op_income):
        ax.text(i + w/2, v + label_gap_op, f'{v:,}', ha='center', fontsize=8, fontweight='bold', color=c['accent'])

    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel(cfg.get('unit', '억원'))
    ax.set_title(f'{company} {cfg.get("revenue_label","매출액")} & 영업이익 추이 ({years[0]}-{years[-1]})',
                 fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    _save(fig, out_dir, 'chart1_revenue_profit.png')


# ══════════════════════════════════════════════════════════
# Chart 2: 영업이익률 + 순이익률 꺾은선
# ══════════════════════════════════════════════════════════
def chart2_margins(cfg, out_dir):
    c = cfg['colors']
    years = cfg['years']
    op_margin  = cfg['op_margin']
    net_margin = cfg['net_margin']
    company    = cfg['name']

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(years, op_margin,  'o-', color=c['accent'],  linewidth=2.5, markersize=8, label='영업이익률 (%)')
    ax.plot(years, net_margin, 's-', color=c['primary'], linewidth=2.5, markersize=8, label='순이익률 (%)')

    for i in range(len(years)):
        ax.annotate(f'{op_margin[i]:.1f}%',  (years[i], op_margin[i]),
                    textcoords='offset points', xytext=(0, 12),  ha='center', fontsize=9, color=c['accent'])
        ax.annotate(f'{net_margin[i]:.1f}%', (years[i], net_margin[i]),
                    textcoords='offset points', xytext=(0, -16), ha='center', fontsize=9, color=c['primary'])

    ax.set_ylabel('%')
    ax.set_title(f'{company} 수익성 지표 추이 ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    ax.legend(); ax.grid(alpha=0.3)
    ymax = max(max(op_margin), max(net_margin)) * 1.4
    ax.set_ylim(0, ymax)
    _save(fig, out_dir, 'chart2_margins.png')


# ══════════════════════════════════════════════════════════
# Chart 3: ROE & ROA 면적+꺾은선
# ══════════════════════════════════════════════════════════
def chart3_roe_roa(cfg, out_dir):
    c = cfg['colors']
    years = cfg['years']
    roe = cfg['roe']
    roa = cfg['roa']
    company = cfg['name']

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(years, roe, 'o-', color=c['accent'],  linewidth=2.5, markersize=8, label='ROE (%)')
    ax.fill_between(years, roe, alpha=0.18, color=c['accent'])
    ax.plot(years, roa, 's-', color=c['primary'], linewidth=2.5, markersize=8, label='ROA (%)')
    ax.fill_between(years, roa, alpha=0.18, color=c['primary'])

    for i in range(len(years)):
        ax.annotate(f'{roe[i]:.1f}%', (years[i], roe[i]),
                    textcoords='offset points', xytext=(0, 12),  ha='center', fontsize=9, color=c['accent'])
        ax.annotate(f'{roa[i]:.1f}%', (years[i], roa[i]),
                    textcoords='offset points', xytext=(0, -16), ha='center', fontsize=9, color=c['primary'])

    ax.set_ylabel('%')
    ax.set_title(f'{company} ROE & ROA 추이 ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    ax.legend(); ax.grid(alpha=0.3)
    ax.set_ylim(0, max(max(roe), max(roa)) * 1.4)
    _save(fig, out_dir, 'chart3_roe_roa.png')


# ══════════════════════════════════════════════════════════
# Chart 4: 재무 안정성 (부채비율 + 보조지표 혼합)
# ══════════════════════════════════════════════════════════
def chart4_financial_stability(cfg, out_dir):
    c = cfg['colors']
    years = cfg['years']
    debt_ratio    = cfg['debt_ratio']
    company       = cfg['name']
    # 보험사: equity(자기자본) / 일반기업: current_ratio(유동비율)
    secondary     = cfg.get('equity') or cfg.get('current_ratio', [])
    secondary_label = cfg.get('stability_secondary_label', '유동비율 (%)')
    debt_label      = cfg.get('debt_label', '부채비율 (%)')

    fig, ax1 = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years))
    w = 0.4
    ax1.bar(x, debt_ratio, w, label=debt_label, color=c.get('red', '#E74C3C'), alpha=0.72)
    for i, v in enumerate(debt_ratio):
        ax1.text(i, v + max(debt_ratio)*0.01, f'{v:,}%' if v > 100 else f'{v:.1f}%',
                 ha='center', fontsize=8, fontweight='bold', color=c.get('red', '#E74C3C'))
    ax1.set_ylabel(debt_label, color=c.get('red', '#E74C3C'))
    ax1.tick_params(axis='y', labelcolor=c.get('red', '#E74C3C'))
    ax1.set_ylim(0, max(debt_ratio) * 1.3)
    ax1.set_xticks(x); ax1.set_xticklabels(years)
    ax1.grid(axis='y', alpha=0.3); ax1.set_axisbelow(True)

    if secondary:
        ax2 = ax1.twinx()
        ax2.plot(years, secondary, 'D-', color=c['primary'], linewidth=2.5, markersize=8, label=secondary_label)
        for i, v in enumerate(secondary):
            ax2.annotate(f'{v:,}', (years[i], v),
                         textcoords='offset points', xytext=(0, 10), ha='center', fontsize=8,
                         color=c['primary'], fontweight='bold')
        ax2.set_ylabel(secondary_label, color=c['primary'])
        ax2.tick_params(axis='y', labelcolor=c['primary'])
        ax2.set_ylim(0, max(secondary) * 1.3)
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, loc='upper right')
    else:
        ax1.legend()

    ax1.set_title(f'{company} 재무 안정성 ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    _save(fig, out_dir, 'chart4_financial_stability.png')


# ══════════════════════════════════════════════════════════
# Chart 5: 성장률 묶음 막대
# ══════════════════════════════════════════════════════════
def chart5_growth_rates(cfg, out_dir):
    c = cfg['colors']
    years = cfg['years']
    rev_growth = cfg['rev_growth']
    op_growth  = cfg['op_growth']
    ni_growth  = cfg['ni_growth']
    company    = cfg['name']
    green      = c.get('green', '#2ECC71')

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years))
    w = 0.25
    ax.bar(x - w, rev_growth, w, label='매출 성장률',    color=c['primary'], alpha=0.85)
    ax.bar(x,     op_growth,  w, label='영업이익 성장률', color=c['accent'],  alpha=0.85)
    ax.bar(x + w, ni_growth,  w, label='순이익 성장률',  color=green,        alpha=0.85)
    ax.axhline(y=0, color='gray', linewidth=0.8)

    for i, v in enumerate(rev_growth):
        if v != 0:
            ax.text(i - w, v + (1.5 if v >= 0 else -5), f'{v:.1f}%',
                    ha='center', fontsize=7.5, color=c['primary'], fontweight='bold')
    for i, v in enumerate(op_growth):
        if v != 0:
            ax.text(i, v + (1.5 if v >= 0 else -5), f'{v:.1f}%',
                    ha='center', fontsize=7.5, color=c['accent'], fontweight='bold')
    for i, v in enumerate(ni_growth):
        if v != 0:
            ax.text(i + w, v + (1.5 if v >= 0 else -5), f'{v:.1f}%',
                    ha='center', fontsize=7.5, color=green, fontweight='bold')

    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel('%')
    ax.set_title(f'{company} 성장률 추이 ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    ax.legend(); ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    _save(fig, out_dir, 'chart5_growth_rates.png')


# ══════════════════════════════════════════════════════════
# Chart 6: 사업부문 파이차트 (+ 선택적 보조 막대)
# ══════════════════════════════════════════════════════════
def chart6_segments(cfg, out_dir):
    c = cfg['colors']
    company      = cfg['name']
    seg_labels   = cfg['seg_labels']
    seg_sizes    = cfg['seg_sizes']
    seg_colors   = cfg.get('seg_colors') or [c['primary'], c['accent'],
                                              c.get('green', '#2ECC71'), c.get('gray', '#95A5A6')]
    # 보조 막대 데이터 (선택)
    sub_labels   = cfg.get('sub_labels')
    sub_sizes    = cfg.get('sub_sizes')
    sub_title    = cfg.get('sub_title', '보조 비중')

    if sub_labels and sub_sizes:
        fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(f'{company} 사업부문 및 {sub_title} (최근 기준)', fontsize=13, fontweight='bold')
    else:
        fig, ax_pie = plt.subplots(figsize=(9, 6))
        fig.suptitle(f'{company} 사업부문 구성 (최근 기준)', fontsize=13, fontweight='bold')

    explode = tuple([0.05] + [0.0] * (len(seg_sizes) - 1))
    wedges, texts, autotexts = ax_pie.pie(
        seg_sizes, explode=explode, colors=seg_colors,
        autopct='%1.1f%%', startangle=140, pctdistance=0.78,
        textprops={'fontsize': 10}
    )
    for t in autotexts:
        t.set_fontweight('bold'); t.set_fontsize(11)
    ax_pie.legend(seg_labels, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
    ax_pie.set_title('사업부문별 매출 비중', fontsize=12, fontweight='bold', pad=10)

    if sub_labels and sub_sizes:
        sub_colors = seg_colors[:len(sub_labels)]
        y_pos = np.arange(len(sub_labels))
        bars = ax_bar.barh(y_pos, sub_sizes, color=sub_colors, height=0.55)
        for bar, val in zip(bars, sub_sizes):
            ax_bar.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{val}%', va='center', fontsize=10, fontweight='bold')
        ax_bar.set_yticks(y_pos); ax_bar.set_yticklabels(sub_labels, fontsize=10)
        ax_bar.set_xlabel('%'); ax_bar.set_xlim(0, max(sub_sizes) * 1.3)
        ax_bar.set_title(sub_title, fontsize=12, fontweight='bold', pad=10)
        ax_bar.grid(axis='x', alpha=0.3); ax_bar.invert_yaxis()

    plt.tight_layout()
    _save(fig, out_dir, 'chart6_segments.png')


# ══════════════════════════════════════════════════════════
# Chart 7: 당기순이익 막대 + 순이익률 꺾은선
# ══════════════════════════════════════════════════════════
def chart7_net_income(cfg, out_dir):
    c = cfg['colors']
    years      = cfg['years']
    net_income = cfg['net_income']
    net_margin = cfg['net_margin']
    company    = cfg['name']

    fig, ax1 = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years))
    ax1.bar(x, net_income, 0.5, color=c['accent'], alpha=0.85, label='당기순이익')
    for i, v in enumerate(net_income):
        ax1.text(i, v + max(net_income)*0.01, f'{v:,}', ha='center', fontsize=9,
                 fontweight='bold', color=c['accent'])
    ax2 = ax1.twinx()
    ax2.plot(years, net_margin, 'D-', color=c['primary'], linewidth=2.5, markersize=8, label='순이익률 (%)')
    for i, v in enumerate(net_margin):
        ax2.annotate(f'{v:.1f}%', (years[i], v),
                     textcoords='offset points', xytext=(0, 10), ha='center', fontsize=9, color=c['primary'])
    ax1.set_xticks(x); ax1.set_xticklabels(years)
    ax1.set_ylabel(cfg.get('unit', '억원'))
    ax2.set_ylabel('순이익률 (%)')
    ax1.set_title(f'{company} 당기순이익 & 순이익률 ({years[0]}-{years[-1]})',
                  fontsize=13, fontweight='bold', pad=15)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper left')
    ax1.grid(axis='y', alpha=0.3); ax1.set_axisbelow(True)
    _save(fig, out_dir, 'chart7_net_income.png')


# ══════════════════════════════════════════════════════════
# Chart 8: SWOT 4분면
# ══════════════════════════════════════════════════════════
def chart8_swot(cfg, out_dir):
    """SWOT 4분면 — v4.1 가독성 개선판.

    - 큰 figsize(14×10) + DPI 150 = 2100×1500
    - 각 사분면: 색상 헤더 띠 + 진한 테두리 + 항목 사이 여유 간격
    - 긴 한국어 항목 자동 줄바꿈(textwrap)
    - 4분면 명확한 거터(여백)
    """
    c = cfg['colors']
    company = cfg['name']
    swot    = cfg['swot']  # {'강점': [...], '약점': [...], '기회': [...], '위협': [...]}

    red     = c.get('red',   '#E74C3C')
    green   = c.get('green', '#2ECC71')
    primary = c['primary']
    accent  = c['accent']

    # 사분면 설정: (제목, 사분면 라벨, 배경, 헤더띠, 텍스트색)
    quadrants = [
        ('Strengths',     '강점', '#FFF8E1', accent,  '#1A202C'),
        ('Weaknesses',    '약점', '#FFEBEE', red,     '#1A202C'),
        ('Opportunities', '기회', '#E8F5E9', green,   '#1A202C'),
        ('Threats',       '위협', '#EDE7F6', primary, '#1A202C'),
    ]
    keys = list(swot.keys())

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle(f'{company} SWOT 분석',
                 fontsize=18, fontweight='bold', y=0.98, color=primary)

    for idx in range(4):
        title_en, title_kor, bg, header_color, text_color = quadrants[idx]
        items = swot.get(keys[idx], [])
        row, col = idx // 2, idx % 2
        ax = axes[row][col]
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(bg)
        ax.set_xticks([]); ax.set_yticks([])

        # 4분면 진한 테두리
        for spine in ax.spines.values():
            spine.set_edgecolor(header_color)
            spine.set_linewidth(2.0)

        # 헤더 색상 띠 (상단 13%)
        ax.add_patch(plt.Rectangle(
            (0, 0.87), 1, 0.13, transform=ax.transAxes,
            facecolor=header_color, alpha=0.92, zorder=1, edgecolor='none'))
        ax.text(0.5, 0.935, f'{title_en}  ({title_kor})',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, fontweight='bold', color='white', zorder=2)

        # 항목 텍스트: 긴 줄 자동 wrap + 항목 사이 빈 줄
        wrapped = []
        for item in items:
            txt = item.lstrip('•').strip()
            txt = '•  ' + txt
            wrapped.append(textwrap.fill(txt, width=30, subsequent_indent='    '))
        body = '\n\n'.join(wrapped)
        ax.text(0.05, 0.80, body, transform=ax.transAxes,
                fontsize=10.5, verticalalignment='top',
                linespacing=1.5, color=text_color, zorder=2)

    plt.subplots_adjust(left=0.03, right=0.97, top=0.92, bottom=0.03,
                        wspace=0.08, hspace=0.12)
    _save(fig, out_dir, 'chart8_swot.png')


# ══════════════════════════════════════════════════════════
# Chart 9: 현금흐름 3종 묶음 막대
# ══════════════════════════════════════════════════════════
def chart9_cashflow(cfg, out_dir):
    c      = cfg['colors']
    years  = cfg['years']
    ocf    = cfg['ocf']
    icf    = cfg['icf']
    fcf_f  = cfg['fin_cf']
    company = cfg['name']
    red    = c.get('red',    '#E74C3C')
    purple = c.get('purple', '#8E44AD')

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years)); w = 0.25
    ax.bar(x - w, ocf,   w, label='영업CF', color=c['primary'], alpha=0.85)
    ax.bar(x,     icf,   w, label='투자CF', color=red,           alpha=0.85)
    ax.bar(x + w, fcf_f, w, label='재무CF', color=purple,        alpha=0.85)
    ax.axhline(y=0, color='gray', linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel(cfg.get('unit', '억원'))
    ax.set_title(f'{company} 현금흐름 추이 ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    ax.legend(); ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    _save(fig, out_dir, 'chart9_cashflow.png')


# ══════════════════════════════════════════════════════════
# Chart 10: CAPEX & FCF 혼합
# ══════════════════════════════════════════════════════════
def chart10_capex_fcf(cfg, out_dir):
    c       = cfg['colors']
    years   = cfg['years']
    capex   = cfg['capex']
    fcf     = cfg['fcf']
    company = cfg['name']
    red     = c.get('red', '#E74C3C')

    fig, ax1 = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years)); w = 0.3
    ax1.bar(x - w/2, capex, w, label='CAPEX', color=red,        alpha=0.80)
    ax1.bar(x + w/2, fcf,   w, label='FCF',   color=c['accent'], alpha=0.80)
    for i in range(len(years)):
        ax1.text(i - w/2, capex[i] + max(capex)*0.02, f'{capex[i]:,}',
                 ha='center', fontsize=8, fontweight='bold', color=red)
        ax1.text(i + w/2, fcf[i]   + max(fcf)*0.01,   f'{fcf[i]:,}',
                 ha='center', fontsize=8, fontweight='bold', color=c['accent'])
    ax1.set_xticks(x); ax1.set_xticklabels(years)
    ax1.set_ylabel(cfg.get('unit', '억원'))
    ax1.set_title(f'{company} CAPEX & FCF ({years[0]}-{years[-1]})', fontsize=13, fontweight='bold', pad=15)
    ax1.legend(loc='upper left'); ax1.grid(axis='y', alpha=0.3); ax1.set_axisbelow(True)
    _save(fig, out_dir, 'chart10_capex_fcf.png')


# ══════════════════════════════════════════════════════════
# Chart 11: 이익의 질 — 영업이익 vs 영업CF
# ══════════════════════════════════════════════════════════
def chart11_earnings_quality(cfg, out_dir):
    c       = cfg['colors']
    years   = cfg['years']
    op_income = cfg['op_income']
    ocf     = cfg['ocf']
    company = cfg['name']
    green   = c.get('green', '#2ECC71')

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(years)); w = 0.30
    ax.bar(x - w/2, op_income, w, label='영업이익',       color=c['accent'],  alpha=0.85)
    ax.bar(x + w/2, ocf,       w, label='영업현금흐름(OCF)', color=c['primary'], alpha=0.85)

    ratio = [(o / p * 100) if abs(p) > 0.05 else 0.0 for o, p in zip(ocf, op_income)]
    ax2 = ax.twinx()
    ax2.plot(years, ratio, 'D-', color=green, linewidth=2.5, markersize=8, label='OCF/영업이익 (%)')
    for i, (v, p) in enumerate(zip(ratio, op_income)):
        label = f'{v:.0f}%' if abs(p) > 0.05 else 'N/A'
        ax2.annotate(label, (years[i], v),
                     textcoords='offset points', xytext=(0, 10), ha='center', fontsize=9, color=green)

    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel(cfg.get('unit', '억원'))
    ax2.set_ylabel('OCF/영업이익 (%)')
    ax.set_title(f'{company} 영업이익 vs 영업CF — 이익의 질 ({years[0]}-{years[-1]})',
                 fontsize=13, fontweight='bold', pad=15)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='upper left')
    ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    _save(fig, out_dir, 'chart11_earnings_quality.png')


# ══════════════════════════════════════════════════════════
# Chart 12: 투자매력도 레이더
# ══════════════════════════════════════════════════════════
def chart12_radar(cfg, out_dir):
    c       = cfg['colors']
    company = cfg['name']
    radar_categories = cfg['radar_categories']
    radar_scores     = cfg['radar_scores']

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    N = len(radar_categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    scores_plot = radar_scores + [radar_scores[0]]
    angles_plot = angles + [angles[0]]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles), radar_categories, fontsize=11)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='gray')
    ax.grid(color='gray', alpha=0.3)

    ax.fill(angles_plot, scores_plot, color=c['accent'], alpha=0.25)
    ax.plot(angles_plot, scores_plot, 'o-', color=c['accent'], linewidth=2.5, markersize=7)

    for angle, score in zip(angles, radar_scores):
        ax.annotate(f'{score}점', xy=(angle, score),
                    textcoords='offset points', xytext=(5, 5),
                    fontsize=10, fontweight='bold', color=c['primary'])

    ax.set_title(f'{company} 투자매력도 레이더 (10점 만점)',
                 fontsize=13, fontweight='bold', pad=25)
    _save(fig, out_dir, 'chart12_radar.png')


# ══════════════════════════════════════════════════════════
# Chart 13: 분기 모멘텀 (최근 8분기 매출 + 영업이익)
# ══════════════════════════════════════════════════════════
def chart13_quarterly_momentum(cfg, out_dir):
    """config에 quarterly_labels/revenue/op_income 키 있으면 생성, 없으면 스킵"""
    labels   = cfg.get('quarterly_labels')
    rev      = cfg.get('quarterly_revenue')
    op_inc   = cfg.get('quarterly_op_income')
    if not labels or not rev or not op_inc:
        return False

    c = cfg['colors']
    company = cfg['name']
    unit = cfg.get('quarterly_unit', cfg.get('unit', '억원'))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(labels)); w = 0.35
    ax.bar(x - w/2, rev,    w, label=f'매출 ({unit})',     color=c['primary'], alpha=0.85)
    ax.bar(x + w/2, op_inc, w, label=f'영업이익 ({unit})', color=c['accent'],  alpha=0.85)

    rev_max = max(rev) if rev else 1
    op_max  = max([abs(v) for v in op_inc]) if op_inc else 1
    for i, v in enumerate(rev):
        ax.text(i - w/2, v + rev_max * 0.015, f'{v:.1f}', ha='center', fontsize=8,
                fontweight='bold', color=c['primary'])
    for i, v in enumerate(op_inc):
        offset = op_max * 0.04 if v >= 0 else -op_max * 0.06
        ax.text(i + w/2, v + offset, f'{v:.1f}', ha='center', fontsize=8,
                fontweight='bold', color=c['accent'])

    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel(unit)
    ax.set_title(f'{company} 분기 모멘텀 — 최근 {len(labels)}분기 매출·영업이익',
                 fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    ax.axhline(0, color='gray', linewidth=0.5)
    _save(fig, out_dir, 'chart13_quarterly_momentum.png')
    return True


# ══════════════════════════════════════════════════════════
# Chart 14: 애널리스트 목표가 분포
# ══════════════════════════════════════════════════════════
def chart14_analyst_consensus(cfg, out_dir):
    """config['forward']에 target_low/mean/high + current_price 있으면 생성"""
    fwd = cfg.get('forward') or {}
    low  = fwd.get('target_low')
    mean = fwd.get('target_mean')
    high = fwd.get('target_high')
    cur  = fwd.get('current_price')
    if low is None or mean is None or high is None or cur is None:
        return False

    c = cfg['colors']
    company = cfg['name']
    median = fwd.get('target_median', mean)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    points = [
        ('Low',     low,    c.get('gray', '#95A5A6')),
        ('Median',  median, c.get('teal', '#3E80B5')),
        ('Mean',    mean,   c['accent']),
        ('High',    high,   c.get('green', '#2ECC71')),
    ]
    # 수평선: 현재가
    ax.axhline(cur, color=c['primary'], linewidth=2, linestyle='--', label=f'현재가 {cur:.2f}')
    # Low~High 범위 박스
    ax.fill_between([-0.5, len(points) - 0.5], low, high, color=c['accent'], alpha=0.08)

    xs = list(range(len(points)))
    ys = [p[1] for p in points]
    cols = [p[2] for p in points]
    ax.scatter(xs, ys, s=180, c=cols, edgecolors='white', linewidths=2, zorder=5)
    for i, (lbl, val, _) in enumerate(points):
        ax.annotate(f'{lbl}\n{val:.2f}', (i, val), textcoords='offset points',
                    xytext=(0, 14), ha='center', fontsize=10, fontweight='bold')

    upside_mean = (mean / cur - 1) * 100 if cur else 0
    ax.set_xticks(xs); ax.set_xticklabels([p[0] for p in points])
    ax.set_ylabel('목표주가')
    n = fwd.get('analyst_count', '?')
    ax.set_title(f'{company} 애널리스트 목표가 분포 (N={n}) — 평균 상승여력 {upside_mean:+.1f}%',
                 fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3); ax.set_axisbelow(True)
    _save(fig, out_dir, 'chart14_analyst_consensus.png')
    return True


# ══════════════════════════════════════════════════════════
# Chart 15: 애널리스트 추천 분포 (Strong Buy ~ Strong Sell)
# ══════════════════════════════════════════════════════════
def chart15_recommendation_pie(cfg, out_dir):
    """config['forward']['recommendations'] 딕셔너리 있으면 생성"""
    fwd = cfg.get('forward') or {}
    recs = fwd.get('recommendations') or {}
    if not recs or sum(recs.values()) == 0:
        return False

    c = cfg['colors']
    company = cfg['name']

    label_map = {
        'strongBuy':  '적극매수',
        'buy':        '매수',
        'hold':       '중립',
        'sell':       '매도',
        'strongSell': '적극매도',
    }
    color_map = {
        'strongBuy':  c.get('green', '#2ECC71'),
        'buy':        '#52B788',
        'hold':       c.get('gray', '#95A5A6'),
        'sell':       '#E76F51',
        'strongSell': c.get('red', '#E11900'),
    }

    keys = [k for k in ['strongBuy', 'buy', 'hold', 'sell', 'strongSell'] if recs.get(k, 0) > 0]
    sizes = [recs[k] for k in keys]
    labels = [f"{label_map[k]} ({recs[k]})" for k in keys]
    colors = [color_map[k] for k in keys]

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.0f%%',
        startangle=90, pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        textprops=dict(fontsize=10, fontweight='bold'),
    )
    for at in autotexts:
        at.set_color('white')

    rec_key = fwd.get('recommendation_key', '').upper()
    rec_mean = fwd.get('recommendation_mean')
    subtitle = f'종합 등급: {rec_key}'
    if rec_mean is not None:
        subtitle += f' (평균 {rec_mean:.2f} / 1=강력매수, 5=강력매도)'

    ax.set_title(f'{company} 애널리스트 추천 분포\n{subtitle}',
                 fontsize=13, fontweight='bold', pad=20)
    _save(fig, out_dir, 'chart15_recommendation_pie.png')
    return True


# ══════════════════════════════════════════════════════════
# 전체 실행 진입점
# ══════════════════════════════════════════════════════════
def generate_all_charts(cfg, out_dir=None):
    """
    cfg : 회사별 config.py 에서 가져온 CONFIG 딕셔너리
    out_dir : 차트를 저장할 경로 (None이면 cfg['base_dir'] 사용)

    chart13~15는 cfg에 해당 키가 있을 때만 생성된다 (backward-compatible).
    """
    if out_dir is None:
        out_dir = cfg['base_dir']
    os.makedirs(out_dir, exist_ok=True)

    print(f'\n📊 {cfg["name"]} 차트 생성 시작...')
    chart1_revenue_profit(cfg, out_dir)
    chart2_margins(cfg, out_dir)
    chart3_roe_roa(cfg, out_dir)
    chart4_financial_stability(cfg, out_dir)
    chart5_growth_rates(cfg, out_dir)
    chart6_segments(cfg, out_dir)
    chart7_net_income(cfg, out_dir)
    chart8_swot(cfg, out_dir)
    chart9_cashflow(cfg, out_dir)
    chart10_capex_fcf(cfg, out_dir)
    chart11_earnings_quality(cfg, out_dir)
    chart12_radar(cfg, out_dir)

    optional = []
    if chart13_quarterly_momentum(cfg, out_dir): optional.append(13)
    if chart14_analyst_consensus(cfg, out_dir):  optional.append(14)
    if chart15_recommendation_pie(cfg, out_dir): optional.append(15)

    total = 12 + len(optional)
    extra = f' (+ 옵션 차트 {optional})' if optional else ''
    print(f'✅ {cfg["name"]} — 차트 {total}개 생성 완료!{extra}\n')
