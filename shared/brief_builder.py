#!/usr/bin/env python3
"""
shared/brief_builder.py — 1~2페이지 압축 투자 브리프 빌더 (finance-brief 스킬용)

구성:
  Page 1 — 헤더 + 회사 개요 + Valuation 표 + 차트 1
  Page 2 — Forward(촉매·리스크·시나리오) + 차트 2 + 결론·면책

사용법:
    from shared.brief_builder import build_brief
    from stocks.{종목}.config import CONFIG
    build_brief(CONFIG)

config.py 신규 권장 키 (선택, 없으면 자동 폴백):
    'forward_thesis': {
        'catalysts':    ['• 향후 12~24M 핵심 촉매 1', '...'],   # 3~4개
        'risks':        ['• 단기·중기 리스크 1', '...'],         # 3~4개
        'scenarios': [
            {'case': 'Bull', 'price': '$110', 'prob': 25, 'thesis': '...'},
            {'case': 'Base', 'price': '$85',  'prob': 50, 'thesis': '...'},
            {'case': 'Bear', 'price': '$55',  'prob': 25, 'thesis': '...'},
        ],
        'one_line':     '한 줄 결론 (투자 의견·핵심 베팅 포인트)',
        'overview':     '3~4문장 회사 개요 (생략 시 fallback)',
    }
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak,
)

from shared.pdf_utils import FONT, make_table, chart_image, sp


# ══════════════════════════════════════════════════════════
# 압축 스타일
# ══════════════════════════════════════════════════════════
def _styles(primary_hex: str, accent_hex: str):
    primary = HexColor(primary_hex)
    accent  = HexColor(accent_hex)
    dark    = HexColor('#1A202C')
    sub     = HexColor('#475569')

    return {
        'h1':    ParagraphStyle('BH1_',    fontName=FONT, fontSize=14, leading=20,
                                textColor=primary, spaceBefore=4, spaceAfter=6),
        'h2':    ParagraphStyle('BH2_',    fontName=FONT, fontSize=11, leading=17,
                                textColor=accent, spaceBefore=6, spaceAfter=4),
        'body':  ParagraphStyle('BBody_',  fontName=FONT, fontSize=9.5, leading=15,
                                textColor=dark, alignment=TA_JUSTIFY, spaceAfter=4),
        'small': ParagraphStyle('BSmall_', fontName=FONT, fontSize=8, leading=12,
                                textColor=sub),
        'cover_label': ParagraphStyle('BCoverLabel_', fontName=FONT, fontSize=8,
                                      leading=11, textColor=HexColor('#FFFFFF99')),
        'cover_value': ParagraphStyle('BCoverValue_', fontName=FONT, fontSize=12,
                                      leading=15, textColor=white,
                                      alignment=TA_LEFT),
        'discl': ParagraphStyle('BDiscl_', fontName=FONT, fontSize=7.5, leading=11,
                                textColor=sub, alignment=TA_CENTER),
    }


# ══════════════════════════════════════════════════════════
# 헤더 박스 (종목·가격·의견·목표가)
# ══════════════════════════════════════════════════════════
def _header_box(cfg, sty):
    primary = cfg['colors']['primary']
    accent  = cfg['colors']['accent']

    name_html = f"<b><font size='17'>{cfg['name']}</font></b>"
    sub_html  = f"<font size='9' color='#FFFFFFB0'>{cfg['ticker']}  |  {cfg.get('exchange', '')}  |  {cfg['report_date']}</font>"
    left_p = Paragraph(f"{name_html}<br/>{sub_html}", ParagraphStyle(
        'BHName_', fontName=FONT, fontSize=17, leading=22,
        textColor=white, alignment=TA_LEFT))

    # 우측 4분할 메트릭
    def metric(label, value, color=white):
        lbl = Paragraph(f"<font size='7.5' color='#FFFFFFA0'>{label}</font>",
                        sty['cover_label'])
        val = Paragraph(f"<b><font size='11.5' color='#FFFFFF'>{value}</font></b>",
                        sty['cover_value'])
        return [lbl, val]

    fwd = cfg.get('forward', {}) or {}
    cur = fwd.get('current_price')
    target = cfg.get('target', '')
    upside_str = ''
    if cur and 'forward_thesis' in cfg and cfg['forward_thesis'].get('scenarios'):
        # Base 시나리오 가격에서 상승여력 계산은 target 문자열에 있음
        pass
    metrics_data = [
        metric('현재가', cfg['price']),
        metric('시가총액', cfg['mkt_cap'].split('(')[0].strip()),
        metric('투자의견', cfg['opinion']),
        metric('목표주가', target),
    ]
    # 4개 metric을 2x2 또는 1x4 — 좁은 공간이라 1x4 가로 배열
    metric_table = Table(
        [[m[0] for m in metrics_data],
         [m[1] for m in metrics_data]],
        colWidths=[28*mm]*4,
    )
    metric_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN',  (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING',    (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING',   (0, 0), (-1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
    ]))

    # 좌(이름) | 우(메트릭)
    outer = Table([[left_p, metric_table]], colWidths=[68*mm, 112*mm])
    outer.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(primary)),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 14),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('LINEABOVE',  (0, 0), (-1, 0), 4, HexColor(accent)),
        ('LINEBELOW',  (0, 0), (-1, -1), 4, HexColor(accent)),
    ]))
    return outer


# ══════════════════════════════════════════════════════════
# Valuation 표 (압축형)
# ══════════════════════════════════════════════════════════
def _valuation_table(cfg, sty):
    fwd = cfg.get('forward', {}) or {}
    primary_hex = cfg['colors']['primary']

    rows = []
    def add(label, val, fmt='{}'):
        if val is None or val == '':
            return
        if isinstance(val, (int, float)):
            rows.append([label, fmt.format(val)])
        else:
            rows.append([label, str(val)])

    add('현재 주가',         cfg.get('price', ''))
    if fwd.get('forward_pe') is not None:
        add('Forward PER',   fwd['forward_pe'], '{:.1f}x')
    if fwd.get('trailing_pe') is not None:
        add('TTM PER',       fwd['trailing_pe'], '{:.1f}x')

    # FCF Yield
    fcf = cfg.get('fcf') or []
    if fcf:
        # 시총 파싱 시도 (간단)
        mkt = cfg.get('mkt_cap', '').split('(')[0].strip()
        try:
            # '$42.2B' 또는 '6,967억원'
            num = ''.join(ch for ch in mkt if ch.isdigit() or ch == '.' or ch == ',')
            num = float(num.replace(',', ''))
            # 단위 동일하면 fcf[-1] / mkt
            if cfg.get('unit') == '십억달러':
                # mkt $XX.XB 형태
                yld = fcf[-1] / num * 100
                add('FCF Yield (TTM)', yld, '{:.1f}%')
            elif cfg.get('unit') == '억원':
                # mkt 'X,XXX억원'
                yld = fcf[-1] / num * 100
                add('FCF Yield (TTM)', yld, '{:.1f}%')
        except Exception:
            pass

    # 컨센서스
    if fwd.get('target_mean'):
        cur = fwd.get('current_price') or 0
        upside = (fwd['target_mean'] / cur - 1) * 100 if cur else 0
        add('컨센 평균 목표가',
            f"{fwd['target_mean']:,.0f}{'원' if cfg.get('unit') == '억원' else ''}  ({upside:+.1f}%)")
        if fwd.get('analyst_count'):
            add('애널리스트 수', fwd['analyst_count'], '{:.0f}명')
    add('본 보고서 목표가', cfg.get('target', ''))

    if not rows:
        return None
    return make_table(['지표', '값'], rows,
                      col_widths=[55*mm, 125*mm], primary_hex=primary_hex)


# ══════════════════════════════════════════════════════════
# 시나리오 표 (Bull/Base/Bear)
# ══════════════════════════════════════════════════════════
def _scenario_table(thesis, primary_hex):
    scenarios = thesis.get('scenarios') or []
    if not scenarios:
        return None
    rows = []
    color_map = {
        'Bull': HexColor('#27AE60'),
        'Base': HexColor('#3498DB'),
        'Bear': HexColor('#E74C3C'),
    }
    headers = ['시나리오', '목표가', '확률', '핵심 전제']
    for s in scenarios:
        rows.append([
            s.get('case', ''),
            s.get('price', ''),
            f"{s.get('prob', 0)}%" if s.get('prob') is not None else '-',
            s.get('thesis', ''),
        ])
    return make_table(headers, rows,
                      col_widths=[22*mm, 28*mm, 18*mm, 112*mm],
                      primary_hex=primary_hex)


# ══════════════════════════════════════════════════════════
# 스냅샷 패널 — 52주 위치 · 최근 분기 · 다음 이벤트 (★ Tier 1)
# ══════════════════════════════════════════════════════════
def _last_quarter_summary(cfg) -> str | None:
    """forward_thesis.last_quarter 우선, 없으면 quarterly_* 데이터에서 자동 생성."""
    thesis = cfg.get('forward_thesis') or {}
    override = thesis.get('last_quarter')
    if override:
        return override

    qlbl = cfg.get('quarterly_labels') or []
    qrev = cfg.get('quarterly_revenue') or []
    qop  = cfg.get('quarterly_op_income') or []
    if not qlbl or not qrev:
        return None

    qunit = cfg.get('quarterly_unit', cfg.get('unit', '억원'))
    last_q = qlbl[-1]
    rev    = qrev[-1]

    # YoY 매출 성장률 (5개 분기 이상이면 계산)
    yoy_str = ''
    if len(qrev) >= 5 and qrev[-5]:
        yoy = (rev / qrev[-5] - 1) * 100
        yoy_str = f" (YoY {yoy:+.0f}%)"

    parts = [f"{last_q}: 매출 {rev:.1f}{qunit}{yoy_str}"]
    if qop and qop[-1] is not None:
        parts.append(f"OP {qop[-1]:+.1f}{qunit}")
    ocf = cfg.get('ocf') or []
    if ocf and ocf[-1] is not None:
        parts.append(f"OCF {ocf[-1]:+.1f}{cfg.get('unit', '억원')}")
    dr = cfg.get('debt_ratio') or []
    if dr and dr[-1] is not None:
        parts.append(f"부채비율 {dr[-1]:.0f}%")

    return ' / '.join(parts)


def _format_price_position(cfg) -> str | None:
    """price_position dict → '52주: 14,200~28,900원 / 75% 분위 / 20일 이평 +3.2%' 한 줄 문자열."""
    pos = cfg.get('price_position') or {}
    if not pos:
        return None

    high = pos.get('high_52w_str') or 'N/A'
    low  = pos.get('low_52w_str')  or 'N/A'
    if high == 'N/A' and low == 'N/A':
        return None

    parts = [f"52주: {low} ~ {high}"]
    pct = pos.get('percentile')
    if pct is not None:
        parts.append(f"{pct:.0f}% 분위")
    md = pos.get('ma20_diff')
    if md is not None:
        parts.append(f"20일 이평 {md:+.1f}%")
    return ' / '.join(parts)


def _format_next_catalyst(cfg) -> dict | None:
    """forward_thesis.next_catalyst dict → 정규화된 dict 반환 (없으면 None)."""
    thesis = cfg.get('forward_thesis') or {}
    nc = thesis.get('next_catalyst')
    if not nc:
        return None
    return {
        'date':       nc.get('date', ''),
        'event':      nc.get('event', ''),
        'consensus':  nc.get('consensus', ''),
        'checkpoint': nc.get('checkpoint', ''),
    }


def _snapshot_panel(cfg, sty):
    """스냅샷 패널 — 52주 위치 + 최근 분기 + 다음 이벤트를 한 박스에 압축."""
    primary_hex = cfg['colors']['primary']
    accent_hex  = cfg['colors']['accent']

    pp_str = _format_price_position(cfg)
    lq_str = _last_quarter_summary(cfg)
    nc     = _format_next_catalyst(cfg)

    # 데이터가 모두 없으면 패널 자체 생략
    if not any([pp_str, lq_str, nc]):
        return None

    label_color = HexColor('#64748B')
    value_color = HexColor('#1A202C')
    accent      = HexColor(accent_hex)

    label_style = ParagraphStyle(
        'BSnapLabel_', fontName=FONT, fontSize=8, leading=11,
        textColor=label_color, alignment=TA_LEFT)
    value_style = ParagraphStyle(
        'BSnapValue_', fontName=FONT, fontSize=9.5, leading=14,
        textColor=value_color, alignment=TA_LEFT)

    rows = []

    if pp_str:
        rows.append([
            Paragraph('주가 포지션', label_style),
            Paragraph(pp_str, value_style),
        ])
    if lq_str:
        rows.append([
            Paragraph('최근 분기', label_style),
            Paragraph(lq_str, value_style),
        ])
    if nc:
        nc_text_parts = []
        if nc['date']:
            nc_text_parts.append(f"<b>{nc['date']}</b>")
        if nc['event']:
            nc_text_parts.append(nc['event'])
        if nc['consensus']:
            nc_text_parts.append(f"컨센 {nc['consensus']}")
        if nc['checkpoint']:
            nc_text_parts.append(f"<font color='{accent_hex}'>체크: {nc['checkpoint']}</font>")
        nc_value = ' · '.join(nc_text_parts)
        rows.append([
            Paragraph('다음 이벤트', label_style),
            Paragraph(nc_value, value_style),
        ])

    panel = Table(rows, colWidths=[26*mm, 154*mm])
    cmds = [
        ('BACKGROUND',    (0, 0), (-1, -1), HexColor('#F8FAFC')),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, accent),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (0, -1), 12),
        ('LEFTPADDING',   (1, 0), (1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]
    # 행 구분선 (마지막 행 제외)
    for i in range(len(rows) - 1):
        cmds.append(('LINEBELOW', (0, i), (-1, i), 0.4, HexColor('#E2E8F0')))
    panel.setStyle(TableStyle(cmds))
    return panel


# ══════════════════════════════════════════════════════════
# 컨빅션 + 체크리스트 + 피어 비교 (★ Tier 2)
# ══════════════════════════════════════════════════════════
def _score_color(score):
    """0~10 점수에 따른 배지 (hex string, 마크) 반환."""
    if score is None:
        return '#94A3B8', '–'
    if score >= 7:
        return '#27AE60', '●'   # 양호
    if score >= 5:
        return '#F59E0B', '●'   # 보통
    return '#E74C3C', '●'       # 취약


def _build_checklist(cfg):
    """checklist 우선, 없으면 radar_categories + radar_scores에서 자동 생성."""
    thesis = cfg.get('forward_thesis') or {}
    checklist = thesis.get('checklist')
    if checklist:
        return checklist

    cats   = cfg.get('radar_categories') or []
    scores = cfg.get('radar_scores') or []
    if not cats or not scores:
        return []
    return [
        {'label': str(cat), 'score': float(scr)}
        for cat, scr in zip(cats, scores)
    ]


def _build_conviction(cfg):
    """conviction 우선, 없으면 radar_scores 평균."""
    thesis = cfg.get('forward_thesis') or {}
    if thesis.get('conviction') is not None:
        return float(thesis['conviction'])
    scores = cfg.get('radar_scores') or []
    if scores:
        return sum(scores) / len(scores)
    return None


def _conviction_panel(cfg, sty):
    """컨빅션 점수 + 체크리스트(점수 배지) + 피어 비교를 한 줄에 압축."""
    primary_hex = cfg['colors']['primary']
    accent_hex  = cfg['colors']['accent']

    conviction = _build_conviction(cfg)
    checklist  = _build_checklist(cfg)
    peer       = (cfg.get('forward_thesis') or {}).get('peer_comparison')

    if conviction is None and not checklist and not peer:
        return None

    label_color = HexColor('#64748B')

    # 좌측: 체크리스트 배지 (예: 수익성 ●4 / 성장성 ●9 / ...)
    badge_html_parts = []
    for item in checklist:
        label = item.get('label', '')
        score = item.get('score')
        color_hex, mark = _score_color(score)
        score_str = f"{int(score)}" if isinstance(score, (int, float)) else ''
        badge_html_parts.append(
            f"<font color='#475569' size='8.5'>{label}</font> "
            f"<font color='{color_hex}' size='9.5'><b>{mark}{score_str}</b></font>"
        )
    badges_html = ' &nbsp; '.join(badge_html_parts)

    badge_para = Paragraph(
        badges_html,
        ParagraphStyle('BConvBadges_', fontName=FONT, fontSize=9.5, leading=14,
                       alignment=TA_LEFT)
    ) if badges_html else None

    # 우측: 컨빅션 점수
    if conviction is not None:
        conv_color = '#27AE60' if conviction >= 7 else ('#F59E0B' if conviction >= 5 else '#E74C3C')
        conv_html = (
            f"<font size='8.5' color='#64748B'>컨빅션</font>&nbsp;"
            f"<font size='14' color='{conv_color}'><b>{conviction:.1f}</b></font>"
            f"<font size='9' color='#94A3B8'>/10</font>"
        )
        conv_para = Paragraph(
            conv_html,
            ParagraphStyle('BConvScore_', fontName=FONT, fontSize=14, leading=18,
                           alignment=TA_LEFT)
        )
    else:
        conv_para = Paragraph('', sty['small'])

    # 1행: 배지(좌) | 컨빅션 점수(우)
    header_row = Table(
        [[badge_para or Paragraph('', sty['small']), conv_para]],
        colWidths=[140*mm, 40*mm],
    )
    header_row.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))

    # 2행: 피어 비교 (있을 때만)
    rows = [[header_row]]
    if peer:
        peer_para = Paragraph(
            f"<font size='8.5' color='#64748B'>피어 비교</font>&nbsp;&nbsp;"
            f"<font size='9.5' color='#1A202C'>{peer}</font>",
            ParagraphStyle('BPeer_', fontName=FONT, fontSize=9.5, leading=13,
                           alignment=TA_LEFT)
        )
        rows.append([peer_para])

    panel = Table(rows, colWidths=[180*mm])
    panel_cmds = [
        ('BACKGROUND',    (0, 0), (-1, -1), HexColor('#FFFEF7')),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, HexColor(primary_hex)),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]
    if len(rows) > 1:
        panel_cmds.append(('LINEBELOW', (0, 0), (-1, 0), 0.4, HexColor('#E2E8F0')))
    panel.setStyle(TableStyle(panel_cmds))
    return panel


def _kill_switch_panel(cfg, sty):
    """의사결정 트리거 (Kill Switch) — 발생 시 비중 축소 신호."""
    thesis = cfg.get('forward_thesis') or {}
    triggers = thesis.get('kill_switch') or []
    if not triggers:
        return None

    primary_hex = cfg['colors']['primary']

    title = Paragraph(
        "<font size='10' color='#C0392B'><b>🚨 의사결정 트리거 (Kill Switch)</b></font>"
        "<font size='8.5' color='#64748B'>&nbsp;&nbsp;다음 중 하나라도 발생 시 비중 축소·재평가</font>",
        ParagraphStyle('BKSTitle_', fontName=FONT, fontSize=10, leading=14,
                       alignment=TA_LEFT, spaceAfter=2)
    )
    body_html = '<br/>'.join(triggers)
    body = Paragraph(
        body_html,
        ParagraphStyle('BKSBody_', fontName=FONT, fontSize=9, leading=14,
                       textColor=HexColor('#1A202C'), alignment=TA_LEFT)
    )

    panel = Table([[title], [body]], colWidths=[180*mm])
    panel.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), HexColor('#FDF2F2')),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, HexColor('#C0392B')),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (0,  0), 7),
        ('BOTTOMPADDING', (0, 0), (0,  0), 2),
        ('TOPPADDING',    (0, 1), (0,  1), 0),
        ('BOTTOMPADDING', (0, 1), (0,  1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return panel


# ══════════════════════════════════════════════════════════
# Forward 폴백 (forward_thesis 없을 때 swot/web_issues에서 추론)
# ══════════════════════════════════════════════════════════
def _fallback_thesis(cfg):
    swot   = cfg.get('swot', {})
    issues = cfg.get('web_issues', []) or []
    catalysts = (swot.get('기회') or [])[:4]
    risks     = (swot.get('위협') or [])[:4]
    return {
        'catalysts': catalysts,
        'risks':     risks,
        'scenarios': [],
        'one_line':  f"투자 의견: {cfg.get('opinion', '')} / 목표가: {cfg.get('target', '')}",
        'overview':  '',
    }


# ══════════════════════════════════════════════════════════
# 차트 폴백 (분기 → 연간, 컨센서스 → 레이더)
# ══════════════════════════════════════════════════════════
def _pick_chart(base_dir, *candidates):
    for c in candidates:
        if os.path.exists(os.path.join(base_dir, c)):
            return c
    return None


# ══════════════════════════════════════════════════════════
# 메인 빌드 함수
# ══════════════════════════════════════════════════════════
def build_brief(cfg, output_filename: str = None):
    base = cfg['base_dir']
    primary_hex = cfg['colors']['primary']
    accent_hex  = cfg['colors']['accent']
    sty = _styles(primary_hex, accent_hex)

    output_filename = output_filename or cfg.get(
        'brief_filename',
        cfg['pdf_filename'].replace('_investment_report.pdf', '_brief.pdf')
    )
    output_path = os.path.join(base, output_filename)

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=12*mm, bottomMargin=12*mm,
    )

    story = []

    # ── PAGE 1 ─────────────────────────────────────────────
    story.append(_header_box(cfg, sty))
    story.append(sp(3))

    # 스냅샷 패널 — 52주 위치 + 최근 분기 + 다음 이벤트 (★ Tier 1)
    snap = _snapshot_panel(cfg, sty)
    if snap is not None:
        story.append(snap)
        story.append(sp(4))

    # 회사 개요
    thesis = cfg.get('forward_thesis') or _fallback_thesis(cfg)
    overview = thesis.get('overview') or cfg.get('overview') or (
        f"{cfg['name']}({cfg['ticker']})는 {cfg.get('exchange', '')} 상장 기업으로, "
        f"최신 보고일 {cfg['report_date']} 기준 시가총액 {cfg.get('mkt_cap', '')} 규모의 종목이다. "
        f"본 브리프는 yfinance 실시간 재무 데이터와 공개 자료를 기반으로 압축 작성되었다."
    )
    story.append(Paragraph('1. 회사 개요', sty['h1']))
    story.append(Paragraph(overview, sty['body']))
    story.append(sp(3))

    # Valuation 표
    story.append(Paragraph('2. Valuation', sty['h1']))
    vt = _valuation_table(cfg, sty)
    if vt is not None:
        story.append(vt)
    story.append(sp(3))

    # 차트 1 — 페이지 1 잔여 공간에 맞도록 폭 125mm (높이 ~69mm)
    chart_main = _pick_chart(base,
                             'chart13_quarterly_momentum.png',
                             'chart1_revenue_profit.png')
    if chart_main:
        story.append(chart_image(base, chart_main, width=125*mm, styles=sty))

    story.append(PageBreak())

    # 컨빅션 + 체크리스트 + 피어 비교 (★ Tier 2) — 페이지 2 상단에 배치
    conv = _conviction_panel(cfg, sty)
    if conv is not None:
        story.append(conv)
        story.append(sp(3))

    # ── PAGE 2 ─────────────────────────────────────────────
    story.append(Paragraph('3. Forward 관점 — 향후 12~24개월', sty['h1']))

    # 핵심 촉매
    catalysts = thesis.get('catalysts') or []
    if catalysts:
        story.append(Paragraph('핵심 촉매 (Catalysts)', sty['h2']))
        bullets = '<br/>'.join(catalysts)
        story.append(Paragraph(bullets, sty['body']))
        story.append(sp(2))

    # 핵심 리스크
    risks = thesis.get('risks') or []
    if risks:
        story.append(Paragraph('핵심 리스크 (Risks)', sty['h2']))
        bullets = '<br/>'.join(risks)
        story.append(Paragraph(bullets, sty['body']))
        story.append(sp(2))

    # 의사결정 트리거 (Kill Switch) (★ Tier 2)
    ks = _kill_switch_panel(cfg, sty)
    if ks is not None:
        story.append(ks)
        story.append(sp(2))

    # 시나리오 표
    scen_table = _scenario_table(thesis, primary_hex)
    if scen_table is not None:
        story.append(Paragraph('시나리오 (Bull / Base / Bear)', sty['h2']))
        story.append(scen_table)
        story.append(sp(2))

    # 차트 2 (애널리스트 컨센서스 또는 레이더) — Tier 2 추가로 공간 압박, 폭 축소
    chart_secondary = _pick_chart(base,
                                  'chart14_analyst_consensus.png',
                                  'chart12_radar.png')
    if chart_secondary:
        story.append(chart_image(base, chart_secondary, width=110*mm, styles=sty))
        story.append(sp(2))

    # 한 줄 결론
    one_line = thesis.get('one_line') or f"투자 의견: {cfg.get('opinion', '')} / 목표가: {cfg.get('target', '')}"
    story.append(Paragraph(
        f"<b>결론:</b> {one_line}",
        ParagraphStyle('BConcl_', fontName=FONT, fontSize=10.5, leading=17,
                       textColor=HexColor(primary_hex), alignment=TA_LEFT,
                       borderPadding=10, borderWidth=0,
                       backColor=HexColor('#FFF8E1'), leftIndent=4)))
    story.append(sp(4))

    # 면책
    story.append(Paragraph(
        '※ 본 브리프는 yfinance + 공개 자료 기반 투자 참고 자료이며, '
        '시세는 보고일 기준이다. 투자 권유·조언이 아니며 최종 책임은 투자자 본인에게 있다.',
        sty['discl']))

    doc.build(story)
    print(f'\n✅ Brief PDF 생성 완료: {output_path}')
    return output_path
