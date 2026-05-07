#!/usr/bin/env python3
"""
shared/pdf_utils.py
PDF 생성 공통 유틸리티 — 회사별 config + story(섹션 내용)를 받아 A4 PDF를 빌드한다.

사용법:
    from shared.pdf_utils import build_pdf, make_table, tip_box, chart_image, hr_line
    from 미래에셋생명.config import CONFIG
    story = [...]
    build_pdf(CONFIG, story)
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 한글 폰트 등록 ──────────────────────────────────────
FONT = 'AppleGothic'
_font_paths = [
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
    '/System/Library/Fonts/AppleGothic.ttf',
]
for _fp in _font_paths:
    if os.path.exists(_fp):
        pdfmetrics.registerFont(TTFont(FONT, _fp))
        break

# ── 공통 색상 ──────────────────────────────────────────
TIP_BG     = HexColor('#FFF9E6')
TIP_BORDER = HexColor('#F0C040')
LIGHT_GRAY = HexColor('#F8FAFC')
MEDIUM_TEXT = HexColor('#475569')


# ══════════════════════════════════════════════════════════
# 스타일 팩토리
# ══════════════════════════════════════════════════════════
def make_styles(primary_hex, accent_hex):
    """주색/포인트색을 받아 문서 전용 스타일 딕셔너리 반환"""
    primary = HexColor(primary_hex)
    accent  = HexColor(accent_hex)
    dark    = HexColor('#1E293B')

    s = {}
    s['title'] = ParagraphStyle(
        'Title_', fontName=FONT, fontSize=28, leading=36,
        textColor=primary, alignment=TA_CENTER, spaceAfter=6)
    s['subtitle'] = ParagraphStyle(
        'Subtitle_', fontName=FONT, fontSize=14, leading=22,
        textColor=MEDIUM_TEXT, alignment=TA_CENTER, spaceAfter=20)
    s['h1'] = ParagraphStyle(
        'H1_', fontName=FONT, fontSize=18, leading=26,
        textColor=primary, spaceBefore=18, spaceAfter=10)
    s['h2'] = ParagraphStyle(
        'H2_', fontName=FONT, fontSize=13, leading=20,
        textColor=accent, spaceBefore=12, spaceAfter=8)
    s['h3'] = ParagraphStyle(
        'H3_', fontName=FONT, fontSize=11, leading=17,
        textColor=HexColor('#374151'), spaceBefore=8, spaceAfter=4)
    s['body'] = ParagraphStyle(
        'Body_', fontName=FONT, fontSize=10, leading=17,
        textColor=dark, alignment=TA_JUSTIFY, spaceAfter=6)
    s['tip'] = ParagraphStyle(
        'Tip_', fontName=FONT, fontSize=9.5, leading=15,
        textColor=HexColor('#7B4F00'), spaceAfter=6)
    s['small'] = ParagraphStyle(
        'Small_', fontName=FONT, fontSize=8.5, leading=13,
        textColor=MEDIUM_TEXT)
    s['toc'] = ParagraphStyle(
        'TOC_', fontName=FONT, fontSize=11, leading=23,
        spaceBefore=2, spaceAfter=2)
    s['center'] = ParagraphStyle(
        'Center_', fontName=FONT, fontSize=10, leading=16,
        alignment=TA_CENTER, spaceAfter=6)
    s['disclaimer'] = ParagraphStyle(
        'Disclaimer_', fontName=FONT, fontSize=8, leading=13,
        textColor=MEDIUM_TEXT, alignment=TA_CENTER, spaceBefore=5)
    return s


# ══════════════════════════════════════════════════════════
# 공통 컴포넌트
# ══════════════════════════════════════════════════════════
def make_table(headers, rows, col_widths=None, primary_hex='#1A3A6B'):
    """헤더 + 데이터 행 → 스타일된 Table 반환"""
    data = [headers] + rows
    if col_widths is None:
        col_widths = [170 * mm / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(primary_hex)),
        ('TEXTCOLOR',  (0, 0), (-1, 0), white),
        ('FONTNAME',   (0, 0), (-1, -1), FONT),
        ('FONTSIZE',   (0, 0), (-1,  0), 9),
        ('FONTSIZE',   (0, 1), (-1, -1), 8.5),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID',       (0, 0), (-1, -1), 0.5, HexColor('#CBD5E1')),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(cmds))
    return t


def tip_box(text, styles):
    """💡 초보자 가이드 박스 — 노란 배경, 금색 테두리"""
    inner = Paragraph(f'💡 <b>초보자 가이드:</b> {text}', styles['tip'])
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), TIP_BG),
        ('BOX',           (0, 0), (-1, -1), 1.0, TIP_BORDER),
        ('TOPPADDING',    (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return t


def chart_image(base_dir, filename, width=16 * cm, styles=None):
    """차트 PNG 삽입 — 파일 없으면 대체 Spacer"""
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        return Image(path, width=width, height=width * 0.55)
    return Spacer(1, 5 * mm)


def hr_line(accent_hex='#FF6B00'):
    return HRFlowable(width='100%', thickness=1, color=HexColor(accent_hex))


def sp(n_mm=5):
    return Spacer(1, n_mm * mm)


# ══════════════════════════════════════════════════════════
# 뉴스 / 이슈 카드 (Phase 1.5 신규)
# ══════════════════════════════════════════════════════════
NEWS_BG     = HexColor('#F0F7FF')
NEWS_BORDER = HexColor('#3E80B5')
ISSUE_BG    = HexColor('#FFF5F5')
ISSUE_BORDER = HexColor('#E76F51')


def news_card(item: dict, styles, accent_hex: str = '#3E80B5'):
    """
    yfinance 뉴스 1건을 카드로 렌더링.

    item: {'title', 'publisher', 'link', 'published', 'summary'}
    """
    title     = item.get('title', '').replace('&', '&amp;')
    publisher = item.get('publisher', '')
    published = item.get('published', '')
    summary   = (item.get('summary') or '').replace('&', '&amp;')[:280]

    meta_line = f"<font color='#475569'>{publisher} · {published}</font>" if (publisher or published) else ''
    body_html = f"<b>{title}</b>"
    if meta_line:
        body_html += f"<br/>{meta_line}"
    if summary:
        body_html += f"<br/><font size='9'>{summary}</font>"

    inner = Paragraph(body_html, styles['body'])
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), NEWS_BG),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, HexColor(accent_hex)),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return t


def issue_card(headline: str, body: str, source: str, url: str, date: str, styles,
               severity: str = '중간'):
    """
    WebSearch + WebFetch로 수집한 핵심 이슈 1건을 카드로 렌더링.

    severity : '상'/'중상'/'중간'/'낮음'
    """
    sev_hex_map = {
        '상':   '#E11900',
        '중상': '#E76F51',
        '중간': '#F0C040',
        '낮음': '#52B788',
    }
    sev_hex = sev_hex_map.get(severity, '#95A5A6')
    sev_color = HexColor(sev_hex)

    headline = headline.replace('&', '&amp;')
    body     = body.replace('&', '&amp;')

    meta = f"<font color='#475569' size='8'>{source} · {date}</font>" if (source or date) else ''
    sev_tag = f"<font color='{sev_hex}'><b>[심각도: {severity}]</b></font>"

    html = f"{sev_tag}  <b>{headline}</b>"
    if meta:
        html += f"<br/>{meta}"
    if body:
        html += f"<br/><font size='9.5'>{body}</font>"
    if url:
        html += f"<br/><font color='#3E80B5' size='8'>{url[:120]}</font>"

    inner = Paragraph(html, styles['body'])
    t = Table([[inner]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), ISSUE_BG),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, sev_color),
        ('TOPPADDING',    (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return t


def quarterly_momentum_table(cfg, primary_hex: str = '#1A3A6B'):
    """
    cfg에 quarterly_* 키 있을 때 분기 매출/영업이익 테이블 반환. 없으면 None.
    """
    labels = cfg.get('quarterly_labels')
    rev    = cfg.get('quarterly_revenue')
    op     = cfg.get('quarterly_op_income')
    ni     = cfg.get('quarterly_net_income')
    if not labels or not rev:
        return None

    unit = cfg.get('quarterly_unit', cfg.get('unit', '억원'))
    headers = ['항목'] + labels
    rows = []
    if rev:    rows.append([f'매출 ({unit})']     + [f'{v:.1f}' for v in rev])
    if op:     rows.append([f'영업이익 ({unit})'] + [f'{v:.1f}' for v in op])
    if ni:     rows.append([f'순이익 ({unit})']   + [f'{v:.1f}' for v in ni])

    n_cols = len(headers)
    col_widths = [28 * mm] + [(170 - 28) * mm / (n_cols - 1)] * (n_cols - 1)
    return make_table(headers, rows, col_widths=col_widths, primary_hex=primary_hex)


def forward_consensus_table(cfg, primary_hex: str = '#1A3A6B'):
    """
    cfg['forward'] 기반 컨센서스 요약 테이블. 데이터 없으면 None.
    """
    fwd = cfg.get('forward') or {}
    if not fwd:
        return None

    cur = fwd.get('current_price')
    rows = []

    def add(label, val, fmt='{:.2f}'):
        if val is not None:
            rows.append([label, fmt.format(val) if isinstance(val, (int, float)) else str(val)])

    add('현재 주가',         cur)
    add('애널리스트 평균 목표가',  fwd.get('target_mean'))
    add('애널리스트 중위 목표가',  fwd.get('target_median'))
    add('최저 목표가',       fwd.get('target_low'))
    add('최고 목표가',       fwd.get('target_high'))
    if cur and fwd.get('target_mean'):
        upside = (fwd['target_mean'] / cur - 1) * 100
        rows.append(['평균 상승여력',   f'{upside:+.1f}%'])
    add('애널리스트 수',     fwd.get('analyst_count'), '{:.0f}명')
    add('Forward PER',       fwd.get('forward_pe'))
    add('Trailing PER',      fwd.get('trailing_pe'))
    if fwd.get('recommendation_key'):
        rows.append(['종합 등급', f"{fwd['recommendation_key'].upper()}  (평균 {fwd.get('recommendation_mean', 0):.2f})"])

    if not rows:
        return None
    return make_table(['지표', '값'], rows, col_widths=[60 * mm, 100 * mm], primary_hex=primary_hex)


# ══════════════════════════════════════════════════════════
# 페이지 헤더/푸터 콜백 팩토리
# ══════════════════════════════════════════════════════════
def make_header_footer(cfg):
    """cfg를 클로저로 캡처하는 헤더/푸터 콜백 반환"""
    accent = HexColor(cfg['colors']['accent'])

    def callback(canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFont(FONT, 9)
        canvas.setFillColor(MEDIUM_TEXT)
        canvas.drawString(20 * mm, h - 12 * mm, cfg['header_text'])
        canvas.drawRightString(w - 20 * mm, h - 12 * mm, cfg['report_date'])
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(1.5)
        canvas.line(20 * mm, h - 14 * mm, w - 20 * mm, h - 14 * mm)
        canvas.setFont(FONT, 8)
        canvas.setFillColor(MEDIUM_TEXT)
        canvas.drawCentredString(w / 2, 10 * mm, f'- {doc.page} -')
        canvas.restoreState()

    return callback


# ══════════════════════════════════════════════════════════
# PDF 빌드
# ══════════════════════════════════════════════════════════
def build_pdf(cfg, story):
    """
    cfg      : CONFIG 딕셔너리
    story    : ReportLab Flowable 리스트 (각 generate_pdf.py 에서 조립)
    """
    output_path = os.path.join(cfg['base_dir'], cfg['pdf_filename'])
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
    )
    cb = make_header_footer(cfg)
    doc.build(story, onFirstPage=cb, onLaterPages=cb)
    print(f'\n✅ PDF 생성 완료: {output_path}')
    return output_path
