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

# ── 한글 폰트 등록 (cross-platform fallback) ──────────────────
# OS별 한글 폰트 후보 — 첫 번째로 발견되는 파일을 등록한다.
# 신규 OS·폰트를 추가하려면 아래 리스트에 경로만 덧붙이면 된다.
FONT = 'KoreanFont'  # ReportLab 내부 식별자 (실제 글꼴 파일명과 무관)

_FONT_CANDIDATES = [
    # ── macOS ──
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
    '/System/Library/Fonts/AppleGothic.ttf',
    '/Library/Fonts/AppleSDGothicNeo.ttc',
    '/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc',
    # ── Linux (Noto / Nanum) ──
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/nanum/NanumGothic.ttf',
    # ── Windows ──
    'C:/Windows/Fonts/malgun.ttf',
    'C:/Windows/Fonts/NanumGothic.ttf',
    'C:/Windows/Fonts/MalgunGothic.ttf',
    # ── 사용자 설치 (cross-platform) ──
    os.path.expanduser('~/.fonts/NotoSansKR-Regular.otf'),
    os.path.expanduser('~/.fonts/NanumGothic.ttf'),
    os.path.expanduser('~/Library/Fonts/NotoSansKR-Regular.otf'),
    os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/NotoSansKR-Regular.otf'),
    # ── 환경변수 오버라이드 (최우선 — 위에서 못 찾으면 뒤로 빠지지만 사용자가 직접 지정 시 위로 끌어옴) ──
]
# 환경변수 FINANCE_KOREAN_FONT가 있으면 최우선으로 시도
_env_font = os.environ.get('FINANCE_KOREAN_FONT')
if _env_font:
    _FONT_CANDIDATES.insert(0, os.path.expanduser(_env_font))

_FONT_REGISTERED = False
for _fp in _FONT_CANDIDATES:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont(FONT, _fp))
            _FONT_REGISTERED = True
            break
        except Exception as e:
            # ttc 일부 인덱스 실패 등은 다음 후보로 폴백
            continue

if not _FONT_REGISTERED:
    # 폰트를 못 찾았을 때 명확한 에러 메시지로 안내 (PDF 빌드 시 한글 깨짐 방지)
    import warnings
    warnings.warn(
        '\n' + '=' * 60 + '\n'
        '⚠️  한글 폰트를 찾지 못했습니다. PDF에서 한글이 깨질 수 있습니다.\n'
        '\n'
        '해결 방법:\n'
        '  • macOS:   기본 AppleGothic이 있어야 합니다 (보통 자동)\n'
        '  • Linux:   sudo apt install fonts-noto-cjk-extra fonts-nanum\n'
        '  • Windows: 기본 malgun.ttf가 있어야 합니다 (보통 자동)\n'
        '  • 또는 환경변수 지정:\n'
        '       export FINANCE_KOREAN_FONT=/path/to/your/korean-font.ttf\n'
        '=' * 60,
        RuntimeWarning,
    )
    # 폴백: ReportLab 기본 영문 폰트 (한글은 깨지지만 빌드는 성공)
    FONT = 'Helvetica'

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
_TABLE_HEADER_STYLE = ParagraphStyle(
    'TableHeader_', fontName=FONT, fontSize=9, leading=12,
    textColor=white, alignment=TA_CENTER)
_TABLE_BODY_STYLE = ParagraphStyle(
    'TableBody_', fontName=FONT, fontSize=8.5, leading=12,
    textColor=HexColor('#1E293B'), alignment=TA_CENTER)


def _wrap_cell(cell, style):
    """셀 값이 문자열이면 Paragraph로 감싸 자동 줄바꿈 활성화."""
    if isinstance(cell, str):
        return Paragraph(cell.replace('\n', '<br/>'), style)
    return cell


def make_table(headers, rows, col_widths=None, primary_hex='#1A3A6B'):
    """헤더 + 데이터 행 → 스타일된 Table 반환.
    문자열 셀은 자동으로 Paragraph로 감싸 좁은 컬럼에서도 줄바꿈된다."""
    wrapped_headers = [_wrap_cell(h, _TABLE_HEADER_STYLE) for h in headers]
    wrapped_rows = [
        [_wrap_cell(c, _TABLE_BODY_STYLE) for c in row]
        for row in rows
    ]
    data = [wrapped_headers] + wrapped_rows
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
        ('LEFTPADDING',   (0, 0), (-1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
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


# ══════════════════════════════════════════════════════════
# 창업자 카드 + 타임라인 (v4.1 신규)
# ══════════════════════════════════════════════════════════
FOUNDER_BG = HexColor('#FAF7F2')
FOUNDER_BORDER = HexColor('#8B7355')


def founder_card(founder: dict, styles, primary_hex: str = '#1A3A6B'):
    """
    창업자 정보 카드 — v4.1 가독성 개선판.

    상단: 이름·역할 헤더 (색상 배경)
    중앙: 라벨/값 2열 표 (출생, 약력)
    하단: 철학 강조 박스

    데이터 부재 시 None 반환 → 섹션 자동 스킵.
    """
    if not founder or not founder.get('name'):
        return None

    name       = founder.get('name', '').replace('&', '&amp;')
    role       = founder.get('role', '').replace('&', '&amp;')
    born       = founder.get('born', '').replace('&', '&amp;')
    background = founder.get('background', '').replace('&', '&amp;')
    philosophy = founder.get('philosophy', '').replace('&', '&amp;')

    primary_color = HexColor(primary_hex)
    label_color   = HexColor('#64748B')
    value_color   = HexColor('#1A202C')

    # ── 1) 헤더 박스: 이름 + 역할 (색상 배경 + 흰색 텍스트) ──
    header_html = f"<font size='15'><b>{name}</b></font>"
    if role:
        header_html += f"<br/><font size='10.5' color='#FFFFFF99'>{role}</font>"
    header_inner = Paragraph(header_html, ParagraphStyle(
        'FounderHeader_', fontName=FONT, fontSize=15, leading=22,
        textColor=HexColor('#FFFFFF'), alignment=TA_LEFT, spaceAfter=0))
    header = Table([[header_inner]], colWidths=[170 * mm])
    header.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), primary_color),
        ('TOPPADDING',    (0, 0), (-1, -1), 13),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 13),
        ('LEFTPADDING',   (0, 0), (-1, -1), 18),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 18),
    ]))

    # ── 2) 본문: 라벨/값 2열 표 ──
    info_rows = []
    if born:
        info_rows.append(['출 생',  born])
    if background:
        info_rows.append(['약 력',  background])

    info_table = None
    if info_rows:
        info_paras = []
        for label, value in info_rows:
            label_p = Paragraph(
                f"<b>{label}</b>",
                ParagraphStyle('FLabel_', fontName=FONT, fontSize=10, leading=16,
                               textColor=label_color, alignment=TA_LEFT))
            value_p = Paragraph(
                value,
                ParagraphStyle('FValue_', fontName=FONT, fontSize=10.5, leading=18,
                               textColor=value_color, alignment=TA_LEFT))
            info_paras.append([label_p, value_p])
        info_table = Table(info_paras, colWidths=[26 * mm, 144 * mm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), FOUNDER_BG),
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',    (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING',   (0, 0), (0, -1), 18),
            ('LEFTPADDING',   (1, 0), (1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 14),
            ('LINEBELOW',     (0, 0), (-1, -2), 0.5, HexColor('#E2E8F0')),
        ]))

    # ── 3) 철학 강조 박스 ──
    phil_table = None
    if philosophy:
        phil_html = f"<font size='10' color='#64748B'><b>철 학</b></font>&nbsp;&nbsp;&nbsp;<font size='11' color='{primary_hex}'><b><i>{philosophy}</i></b></font>"
        phil_inner = Paragraph(phil_html, ParagraphStyle(
            'FPhil_', fontName=FONT, fontSize=11, leading=19,
            textColor=value_color, alignment=TA_LEFT))
        phil_table = Table([[phil_inner]], colWidths=[170 * mm])
        phil_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), HexColor('#FFF8E1')),
            ('LINEBEFORE',    (0, 0), (0, -1), 4, HexColor(primary_hex)),
            ('TOPPADDING',    (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING',   (0, 0), (-1, -1), 16),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 14),
        ]))

    # ── 컨테이너: 헤더 → 본문 → 철학 (Spacer로 구분) ──
    parts = [[header]]
    if info_table:
        parts.append([info_table])
    if phil_table:
        parts.append([phil_table])

    container = Table(parts, colWidths=[170 * mm])
    container.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    return container


def founder_quote_card(quote: dict, styles, accent_hex: str = '#FF6B00'):
    """
    창업자 직접 인용 1건 — v4.1 가독성 개선: 큰 따옴표 마크 + 인용문 + 출처 분리.
    """
    text   = (quote.get('text') or '').replace('&', '&amp;')
    source = (quote.get('source') or '').replace('&', '&amp;')
    date   = quote.get('date', '')
    meta   = ' · '.join(filter(None, [source, date]))

    accent = HexColor(accent_hex)

    # 큰 따옴표 마크 (왼쪽 컬럼)
    quote_mark = Paragraph(
        f"<font size='36' color='{accent_hex}'><b>&ldquo;</b></font>",
        ParagraphStyle('FQMark_', fontName=FONT, fontSize=36, leading=40,
                       textColor=accent, alignment=TA_LEFT, spaceAfter=0))

    # 인용문 본문 (오른쪽 컬럼)
    body_para = Paragraph(
        f"<font size='12'><i>{text}</i></font>",
        ParagraphStyle('FQText_', fontName=FONT, fontSize=12, leading=21,
                       textColor=HexColor('#1E293B'), alignment=TA_LEFT, spaceAfter=4))

    # 메타(출처·날짜)
    meta_para = None
    if meta:
        meta_para = Paragraph(
            f"<font size='9'>— {meta}</font>",
            ParagraphStyle('FQMeta_', fontName=FONT, fontSize=9, leading=14,
                           textColor=HexColor('#64748B'), alignment=TA_LEFT))

    right_cell = Table(
        [[body_para]] + ([[meta_para]] if meta_para else []),
        colWidths=[150 * mm],
    )
    right_cell.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))

    t = Table([[quote_mark, right_cell]], colWidths=[16 * mm, 154 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), HexColor('#FFFEF5')),
        ('LINEBEFORE',    (0, 0), (0, -1), 3, accent),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING',   (0, 0), (0, -1), 16),
        ('LEFTPADDING',   (1, 0), (1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 16),
    ]))
    return t


def founder_timeline_table(timeline: list, primary_hex: str = '#1A3A6B'):
    """
    창업~성장 변곡점 타임라인 표 — v4.1 가독성 개선: 큰 폰트, 넓은 행 높이.
    """
    if not timeline:
        return None

    primary  = HexColor(primary_hex)
    accent   = HexColor('#E2E8F0')
    light    = HexColor('#F8FAFC')

    headers = ['연도', '핵심 사건', '의미·맥락']
    data    = [headers]

    label_style = ParagraphStyle('TLLabel_', fontName=FONT, fontSize=11, leading=16,
                                 textColor=HexColor('#FFFFFF'), alignment=TA_CENTER)
    year_style  = ParagraphStyle('TLYear_',  fontName=FONT, fontSize=12, leading=18,
                                 textColor=primary, alignment=TA_CENTER, spaceAfter=0)
    event_style = ParagraphStyle('TLEvent_', fontName=FONT, fontSize=10.5, leading=17,
                                 textColor=HexColor('#1A202C'), alignment=TA_LEFT)
    note_style  = ParagraphStyle('TLNote_',  fontName=FONT, fontSize=9.5, leading=15,
                                 textColor=HexColor('#475569'), alignment=TA_LEFT)

    for t in timeline:
        data.append([
            Paragraph(f"<b>{t.get('year', '')}</b>", year_style),
            Paragraph(f"<b>{t.get('event', '')}</b>", event_style),
            Paragraph(t.get('note', ''), note_style),
        ])
    # 헤더 행을 Paragraph로 감싸기
    data[0] = [Paragraph(f"<b>{h}</b>", label_style) for h in headers]

    col_widths = [22 * mm, 68 * mm, 80 * mm]
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('BACKGROUND',     (0, 0), (-1, 0), primary),
        ('VALIGN',         (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',     (0, 0), (-1,  0), 10),
        ('BOTTOMPADDING',  (0, 0), (-1,  0), 10),
        ('TOPPADDING',     (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING',  (0, 1), (-1, -1), 9),
        ('LEFTPADDING',    (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',   (0, 0), (-1, -1), 8),
        ('LINEBELOW',      (0, 0), (-1, -1), 0.5, accent),
    ]
    for i in range(2, len(data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0, i), (-1, i), light))
    tbl.setStyle(TableStyle(cmds))
    return tbl


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
