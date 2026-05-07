#!/usr/bin/env python3
"""Alphabet Inc. (GOOGL) - 투자 분석 PDF 보고서 생성"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 경로 설정 ──
BASE = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE, 'google_investment_report.pdf')

# ── 색상 ──
PRIMARY = HexColor('#1E3A5F')
ACCENT = HexColor('#2563EB')
LIGHT_BLUE = HexColor('#EFF6FF')
LIGHT_GRAY = HexColor('#F8FAFC')
DARK_TEXT = HexColor('#1E293B')
MEDIUM_TEXT = HexColor('#475569')
ORANGE = HexColor('#F97316')
GREEN = HexColor('#10B981')
RED = HexColor('#EF4444')

# ── 폰트 등록 ──
FONT_PATH = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
if not os.path.exists(FONT_PATH):
    FONT_PATH = '/System/Library/Fonts/AppleGothic.ttf'
pdfmetrics.registerFont(TTFont('AppleGothic', FONT_PATH))
FONT = 'AppleGothic'

# ── 스타일 ──
styles = getSampleStyleSheet()

def make_style(name, parent='Normal', **kw):
    defaults = {'fontName': FONT, 'textColor': DARK_TEXT, 'leading': kw.pop('leading', 18)}
    defaults.update(kw)
    return ParagraphStyle(name, parent=styles[parent], **defaults)

title_style = make_style('TitleCustom', fontSize=28, textColor=PRIMARY, alignment=TA_CENTER, leading=34, spaceAfter=6)
subtitle_style = make_style('SubTitle', fontSize=14, textColor=MEDIUM_TEXT, alignment=TA_CENTER, leading=20, spaceAfter=20)
h1_style = make_style('H1Custom', fontSize=18, textColor=PRIMARY, spaceBefore=18, spaceAfter=10, leading=24)
h2_style = make_style('H2Custom', fontSize=14, textColor=ACCENT, spaceBefore=12, spaceAfter=8, leading=20)
body_style = make_style('BodyCustom', fontSize=10, leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
tip_style = make_style('Tip', fontSize=9.5, leading=15, textColor=HexColor('#1E40AF'), spaceAfter=6)
small_style = make_style('Small', fontSize=8.5, textColor=MEDIUM_TEXT, leading=13)
toc_style = make_style('TOC', fontSize=11, leading=22, spaceBefore=2, spaceAfter=2)
center_style = make_style('CenterBody', fontSize=10, alignment=TA_CENTER, leading=16, spaceAfter=6)


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # 헤더
    canvas.setFont(FONT, 9)
    canvas.setFillColor(MEDIUM_TEXT)
    canvas.drawString(20*mm, h - 12*mm, 'Alphabet Inc. (GOOGL) 투자 분석 보고서')
    canvas.drawRightString(w - 20*mm, h - 12*mm, '2026년 4월 1일')
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(20*mm, h - 14*mm, w - 20*mm, h - 14*mm)
    # 푸터
    canvas.setFont(FONT, 8)
    canvas.setFillColor(MEDIUM_TEXT)
    canvas.drawCentredString(w/2, 10*mm, f'- {doc.page} -')
    canvas.restoreState()


def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if col_widths is None:
        col_widths = [170*mm / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,-1), FONT),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


def tip_box(text):
    """초보자 팁 박스"""
    inner = Paragraph(f'💡 <b>초보자 가이드:</b> {text}', tip_style)
    t = Table([[inner]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t


def chart_image(filename, width=160*mm):
    path = os.path.join(BASE, filename)
    if os.path.exists(path):
        return Image(path, width=width, height=width*0.55)
    return Paragraph(f'[차트 미생성: {filename}]', body_style)


def build():
    doc = SimpleDocTemplate(
        PDF_PATH, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )
    story = []

    # ═══════════════════════════════════════
    # 1. 표지
    # ═══════════════════════════════════════
    story.append(Spacer(1, 60*mm))
    story.append(Paragraph('Alphabet Inc. (GOOGL)', title_style))
    story.append(Paragraph('종합 투자 분석 보고서', make_style('ST2', fontSize=20, textColor=ACCENT, alignment=TA_CENTER, leading=28)))
    story.append(Spacer(1, 15*mm))

    cover_data = [
        ['종목코드', 'GOOGL (NASDAQ)'],
        ['현재 주가', '~$285'],
        ['시가총액', '~$3.48조 (약 4,700조원)'],
        ['투자의견 (컨센서스)', '매수 (Buy)'],
        ['목표주가 (중간값)', '$387.50 (상승여력 ~36%)'],
    ]
    ct = Table(cover_data, colWidths=[60*mm, 110*mm])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('TEXTCOLOR', (0,0), (0,-1), MEDIUM_TEXT),
        ('TEXTCOLOR', (1,0), (1,-1), PRIMARY),
        ('FONTSIZE', (1,0), (1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor('#E2E8F0')),
    ]))
    story.append(ct)
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('2026년 4월 1일', subtitle_style))
    story.append(Paragraph('본 보고서는 투자 참고 자료이며, 최종 투자 판단의 책임은 투자자 본인에게 있습니다.', small_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 2. 목차
    # ═══════════════════════════════════════
    story.append(Paragraph('목차', h1_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=ACCENT))
    story.append(Spacer(1, 5*mm))
    toc_items = [
        '1. 회사 개요',
        '2. 비전과 경영철학',
        '3. 사업모델 분석',
        '4. 재무제표 분석 — 초보자 가이드',
        '5. 수익성 분석',
        '6. 성장성 분석',
        '7. 재무 안정성 분석',
        '8. 현금흐름 분석 — 초보자 가이드',
        '9. 산업 분석 및 경쟁 환경',
        '10. SWOT 분석 및 투자 리스크',
        '11. 밸류에이션 및 투자 결론',
    ]
    for item in toc_items:
        story.append(Paragraph(item, toc_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 3. 회사 개요
    # ═══════════════════════════════════════
    story.append(Paragraph('1. 회사 개요', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        'Alphabet Inc.은 2015년 Google의 지주회사로 설립되었으며, 세계 최대의 검색 엔진, '
        '디지털 광고 플랫폼, 클라우드 서비스를 운영합니다. 공동 창업자 Larry Page와 Sergey Brin이 '
        '1998년 Google을 설립한 이래, 전 세계 정보 접근 방식을 혁신해왔습니다.',
        body_style))

    info_data = [
        ['설립일', '2015년 10월 2일\n(Google: 1998년)', 'CEO', 'Sundar Pichai'],
        ['본사', 'Mountain View, CA', '직원 수', '~190,820명'],
        ['종목코드', 'GOOGL / GOOG\n(NASDAQ)', '시가총액', '~$3.48조'],
        ['주요 사업', '검색, 광고, 클라우드,\nAI, YouTube', '주가 (현재)', '~$285'],
    ]
    it = Table(info_data, colWidths=[30*mm, 55*mm, 30*mm, 55*mm])
    it.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (0,-1), HexColor('#F1F5F9')),
        ('BACKGROUND', (2,0), (2,-1), HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (0,-1), PRIMARY),
        ('TEXTCOLOR', (2,0), (2,-1), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(it)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('주주 구성', h2_style))
    share_data = [
        ['주주', '지분율', '의결권'],
        ['Larry Page (공동창업자)', '~5.0%', '~26%'],
        ['Sergey Brin (공동창업자)', '~4.9%', '~25%'],
        ['Vanguard Group', '~7.5%', '제한적'],
        ['BlackRock', '~6.5%', '제한적'],
        ['State Street', '~3.5%', '제한적'],
        ['기관투자자 합계', '~64.5%', '소수'],
    ]
    st = make_table(share_data[0], share_data[1:], col_widths=[60*mm, 55*mm, 55*mm])
    story.append(st)
    story.append(Spacer(1, 3*mm))
    story.append(tip_box(
        '알파벳은 차등의결권 구조를 가지고 있어요. 창업자인 Larry Page와 Sergey Brin이 '
        '경제적 지분은 약 10%에 불과하지만, Class B 주식(1주당 10표)을 통해 '
        '의결권의 약 51%를 장악하고 있습니다. 이는 창업자가 회사의 장기적 비전을 '
        '외부 압력 없이 추구할 수 있다는 장점이 있지만, 소수 주주의 목소리가 '
        '제한될 수 있다는 단점도 있습니다.'
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 4. 비전과 경영철학
    # ═══════════════════════════════════════
    story.append(Paragraph('2. 비전과 경영철학', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('<b>미션:</b> "전 세계의 정보를 체계화하여 누구나 접근하고 활용할 수 있게 만든다"', body_style))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('AI-First 전략', h2_style))
    story.append(Paragraph(
        '알파벳은 모든 제품과 서비스를 AI 중심으로 전환하고 있습니다. '
        'Gemini AI 모델을 검색, 클라우드, YouTube, Android, Workspace 등 전 제품에 통합하고 있으며, '
        '2025년 말 출시된 Gemini 3 Pro는 멀티모달 추론에서 GPT-5.2를 능가하는 성과를 보였습니다. '
        'Gemini AI 앱은 7.5억 월간 활성 사용자를 돌파했습니다.',
        body_style))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('ESG 경영', h2_style))
    story.append(Paragraph(
        '• 2030년까지 모든 사업장에서 탄소 순 배출 제로(Net-Zero) 목표<br/>'
        '• 모든 데이터 센터에서 24시간 탄소 무배출 에너지 사용 목표<br/>'
        '• 차세대 원자력 및 지열 에너지 투자<br/>'
        '• AI를 활용한 기후변화 대응 (전 세계 온실가스 5-10% 감축 목표)',
        body_style))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('2026년 전략 방향', h2_style))
    story.append(Paragraph(
        '2026년 설비투자(CAPEX) 가이던스를 $1,750~1,850억으로 제시하며, '
        '전년 대비 2배 이상 증가한 AI 인프라 투자를 계획하고 있습니다. '
        '이는 AI 경쟁에서의 기술적 우위를 유지하고, 구글 클라우드의 시장 점유율을 '
        '확대하기 위한 공격적인 투자입니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 5. 사업모델 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('3. 사업모델 분석', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        '알파벳의 핵심 사업은 ①디지털 광고(검색+YouTube+네트워크), ②구글 클라우드, '
        '③구독/플랫폼/디바이스, ④미래 사업(Other Bets)으로 구분됩니다.',
        body_style))
    story.append(Spacer(1, 3*mm))

    seg_data = [
        ['사업부문', 'FY2024 매출', '비중', '특징'],
        ['Google Search', '$198.1B', '56.6%', '검색 광고 (세계 1위)'],
        ['Google Cloud', '$43.2B', '12.4%', 'AI/ML 차별화 클라우드'],
        ['구독/플랫폼/디바이스', '$40.3B', '11.5%', 'Play, Pixel, YouTube Premium'],
        ['YouTube 광고', '$36.2B', '10.3%', '세계 최대 동영상 플랫폼'],
        ['Google Network', '$30.4B', '8.7%', '제3자 사이트 광고'],
        ['Other Bets', '$1.7B', '0.5%', 'Waymo, Verily 등'],
    ]
    story.append(make_table(seg_data[0], seg_data[1:], col_widths=[35*mm, 25*mm, 20*mm, 60*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart6_segment.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('경쟁 우위 (Economic Moat)', h2_style))
    story.append(Paragraph(
        '<b>1. 검색 독점:</b> 전 세계 검색 시장 점유율 90% 이상. 방대한 데이터가 검색 품질을 높이고, '
        '더 많은 사용자를 유인하는 선순환 구조(데이터 플라이휠)<br/>'
        '<b>2. 광고 플랫폼 지배력:</b> 세계 최대 디지털 광고 플랫폼 (검색+YouTube+네트워크)<br/>'
        '<b>3. 생태계 락인:</b> Android(30억+ 기기), Chrome, Gmail, Maps, Workspace 등 '
        '통합 생태계로 사용자 이탈 방지<br/>'
        '<b>4. AI 인프라 규모:</b> 자체 TPU 칩과 세계 최대 규모의 AI 컴퓨팅 인프라<br/>'
        '<b>5. 현금 창출력:</b> 연간 FCF $72.8B — 어마어마한 R&D와 투자를 감당할 체력',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 6. 재무제표 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('4. 재무제표 분석 — 초보자 가이드', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(tip_box(
        '재무제표는 기업의 "건강검진 결과표"와 같아요. '
        '<b>매출액</b>은 "총 벌어들인 돈", <b>영업이익</b>은 "본업으로 남긴 돈", '
        '<b>순이익</b>은 "세금까지 다 내고 최종적으로 남은 돈"이에요. '
        '마치 월급(매출)에서 생활비(비용)를 빼면 저축(이익)이 남는 것과 비슷해요!'
    ))
    story.append(Spacer(1, 3*mm))

    fin_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['매출액 ($B)', '182.5', '257.6', '282.8', '307.4', '350.0'],
        ['영업이익 ($B)', '41.2', '78.7', '74.8', '84.3', '112.4'],
        ['순이익 ($B)', '40.3', '76.0', '60.0', '73.8', '100.1'],
        ['EPS ($)', '2.93', '5.61', '4.56', '5.80', '8.04'],
    ]
    story.append(make_table(fin_data[0], fin_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart1_revenue_profit.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>해석:</b> 알파벳의 매출은 5년간 $182.5B → $350.0B로 약 92% 성장했습니다. '
        '특히 2024년에는 영업이익이 $112.4B로 역대 최고치를 기록했는데, 이는 AI 기반 '
        '광고 효율화와 구글 클라우드의 흑자 전환이 기여했습니다. '
        '주당순이익(EPS)도 $2.93 → $8.04로 3배 가까이 증가하여, '
        '주주 가치가 크게 향상되었습니다.',
        body_style))
    story.append(Spacer(1, 3*mm))
    story.append(chart_image('chart8_net_income.png'))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 7. 수익성 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('5. 수익성 분석', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(tip_box(
        '<b>영업이익률</b>은 "매출 100원 중 본업으로 몇 원을 남기는지"를 보여줘요. '
        '<b>ROE</b>(자기자본이익률)는 "주주가 맡긴 돈으로 얼마를 벌었는지"예요. '
        'ROE가 높을수록 주주의 돈을 효율적으로 운용한다는 뜻이에요. 일반적으로 ROE 15% 이상이면 우수합니다!'
    ))
    story.append(Spacer(1, 3*mm))

    prof_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['영업이익률', '22.6%', '30.6%', '26.5%', '27.4%', '32.1%'],
        ['순이익률', '22.1%', '29.5%', '21.2%', '24.0%', '28.6%'],
        ['ROE', '18.1%', '32.1%', '23.6%', '27.4%', '32.9%'],
        ['ROA', '12.6%', '14.5%', '12.9%', '13.7%', '16.5%'],
    ]
    story.append(make_table(prof_data[0], prof_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart2_profitability.png'))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart3_roe_roa.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>해석:</b> 영업이익률이 2024년 32.1%로 사상 최고치를 기록했습니다. '
        '이는 100달러의 매출 중 32달러가 본업의 이익으로 남는다는 뜻입니다. '
        'ROE도 32.9%로 매우 우수한데, 이는 주주가 투자한 100달러로 약 33달러를 벌어들이고 있다는 의미예요. '
        '테크 대기업 중에서도 최상위권의 수익성입니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 8. 성장성 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('6. 성장성 분석', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    growth_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['매출 성장률', '+12.8%', '+41.2%', '+9.8%', '+8.7%', '+13.9%'],
        ['영업이익 성장률', '+20.4%', '+91.0%', '-5.0%', '+12.7%', '+33.3%'],
        ['순이익 성장률', '+17.3%', '+88.8%', '-21.1%', '+23.0%', '+35.7%'],
    ]
    story.append(make_table(growth_data[0], growth_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart5_growth.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>해석:</b> 2021년은 코로나 기저효과로 매출이 41% 폭증했고, 2022년은 디지털 광고 시장 둔화로 성장이 주춤했습니다. '
        '하지만 2024년 다시 매출 +13.9%, 영업이익 +33.3%, 순이익 +35.7%의 강력한 성장세를 보이며 '
        'AI 기반 사업 모델의 효과가 가시화되고 있습니다.',
        body_style))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('FY2025 프리뷰 & 미래 전망', h2_style))
    story.append(Paragraph(
        '• FY2025 매출: $403B+ (최초로 $400B 돌파)<br/>'
        '• FY2025 순이익: $132.2B (전년 대비 +32%)<br/>'
        '• 구글 클라우드: Q4 2025 48% 성장, 연간 $58B+ 런레이트<br/>'
        '• AI 투자 확대: 2026년 CAPEX $1,750~1,850억 가이던스 — 장기 성장 동력 구축 중',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 9. 재무 안정성
    # ═══════════════════════════════════════
    story.append(Paragraph('7. 재무 안정성 분석', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(tip_box(
        '<b>부채비율</b>은 "빚이 자기 돈의 몇 배인지"를 보여줘요. 낮을수록 안전합니다. '
        '<b>유동비율</b>은 "1년 안에 갚아야 할 빚을 당장 갚을 수 있는지"를 보여주는데, '
        '1배 이상이면 안전하고, 2배 이상이면 매우 여유로운 편이에요. '
        '<b>이자보상비율</b>이 100배 이상이라는 건 "이자를 100번은 갚을 수 있다"는 뜻으로, 초우량 재무 건전성을 의미해요!'
    ))
    story.append(Spacer(1, 3*mm))

    stab_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['부채비율 (D/A)', '30.0%', '30.0%', '30.0%', '30.0%', '28.0%'],
        ['자기자본비율', '70.0%', '70.0%', '70.0%', '70.0%', '72.0%'],
        ['유동비율', '3.07x', '2.93x', '2.38x', '2.10x', '1.84x'],
        ['D/E 비율', '0.12x', '0.11x', '0.12x', '0.11x', '0.09x'],
        ['이자보상비율', '>100x', '>100x', '>100x', '>100x', '>100x'],
    ]
    story.append(make_table(stab_data[0], stab_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart4_stability.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>해석:</b> 알파벳은 빅테크 중에서도 가장 건전한 재무구조를 보유하고 있습니다. '
        'D/E 비율이 0.09배에 불과해 사실상 무차입 경영에 가깝고, 이자보상비율이 100배 이상이라 '
        '부채 부담이 거의 없습니다. 다만, 유동비율이 3.07 → 1.84로 하락 추세인데, '
        '이는 AI 투자 확대에 따른 자연스러운 현상이며, 1.84배 수준은 여전히 안전합니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 10. 현금흐름 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('8. 현금흐름 분석 — 초보자 가이드', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(tip_box(
        '현금흐름은 기업에 실제로 들어오고 나간 "현금"을 보여줘요. <b>영업CF</b>는 "장사해서 번 현금", '
        '<b>투자CF</b>는 "미래를 위해 쓴 현금", <b>재무CF</b>는 "빚 갚거나 배당/자사주 매입에 쓴 현금"이에요. '
        '<b>FCF(잉여현금흐름)</b>는 "영업CF에서 투자비용을 뺀 것"으로, 기업이 자유롭게 쓸 수 있는 현금이에요. '
        'FCF가 꾸준히 플러스이면 재무적으로 매우 건강한 기업입니다!'
    ))
    story.append(Spacer(1, 3*mm))

    cf_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['영업CF ($B)', '65.1', '91.7', '91.5', '101.7', '125.3'],
        ['투자CF ($B)', '-32.8', '-35.5', '-20.3', '-27.1', '-45.5'],
        ['재무CF ($B)', '-24.4', '-61.4', '-69.8', '-72.1', '-79.7'],
        ['CAPEX ($B)', '22.3', '24.6', '31.5', '32.3', '52.5'],
        ['FCF ($B)', '42.8', '67.0', '60.0', '69.5', '72.8'],
        ['기말현금 ($B)', '26.5', '20.9', '21.9', '24.0', '23.5'],
    ]
    story.append(make_table(cf_data[0], cf_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart10_cashflow.png'))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart11_fcf_cash.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('이익의 질 분석', h2_style))
    story.append(Paragraph(
        '영업현금흐름(OCF)이 영업이익보다 많다면, 이익이 실제 현금으로 뒷받침되고 있다는 뜻입니다. '
        '알파벳의 OCF/영업이익 비율은 평균 약 130~160%로, 회계상 이익보다 실제 현금 유입이 '
        '훨씬 많아 "이익의 질"이 매우 우수합니다.',
        body_style))
    story.append(Spacer(1, 3*mm))
    story.append(chart_image('chart12_earnings_quality.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>해석:</b> 2024년 영업CF $125.3B는 역대 최고치이며, CAPEX $52.5B을 차감해도 '
        'FCF가 $72.8B에 달합니다. 재무CF가 크게 음수(-$79.7B)인 이유는 대규모 자사주 매입($62.2B)과 '
        '배당금 지급 때문입니다. 즉, 본업에서 벌어들인 현금이 너무 풍부해서 공격적으로 '
        '주주에게 환원하고 있다는 의미입니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 11. 산업 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('9. 산업 분석 및 경쟁 환경', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    mkt_data = [
        ['시장', '2025년 규모', '2026년 전망', 'CAGR'],
        ['글로벌 디지털 광고', '~$312B', '~$355B', '~13.8%'],
        ['글로벌 클라우드 컴퓨팅', '~$913B', '~$1.04T', '~20.6%'],
        ['글로벌 AI 시장', '~$294B', '~$376B', '~26.6%'],
    ]
    story.append(make_table(mkt_data[0], mkt_data[1:], col_widths=[40*mm, 35*mm, 35*mm, 30*mm]))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('경쟁사 비교', h2_style))
    comp_data = [
        ['기업', 'FY2024 매출', '주요 경쟁 영역'],
        ['Amazon', '$620B', '클라우드(AWS #1), 광고 사업 확대'],
        ['Apple', '$400B', '모바일 생태계, 개인정보 기반 광고'],
        ['Alphabet', '$350B', '검색, 광고, 클라우드, AI'],
        ['Microsoft', '$265B', '클라우드(Azure #2), AI(OpenAI), 검색(Bing)'],
        ['Meta', '$165B', '디지털 광고 (복점 경쟁자)'],
    ]
    story.append(make_table(comp_data[0], comp_data[1:], col_widths=[30*mm, 30*mm, 80*mm]))
    story.append(Spacer(1, 5*mm))
    story.append(chart_image('chart7_competitors.png'))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>클라우드 시장 점유율 (2024):</b> AWS ~32% > Azure ~23% > Google Cloud ~11%<br/><br/>'
        '<b>해석:</b> 알파벳은 세 개의 거대한 성장 시장(디지털 광고, 클라우드, AI)의 핵심 플레이어입니다. '
        '디지털 광고 시장에서는 Meta와 함께 복점 체제를 유지하고 있으며, 클라우드는 3위이지만 '
        'AI/ML 차별화로 가장 빠르게 성장하고 있습니다. AI 시장에서는 자체 Gemini 모델과 '
        'TPU 칩으로 핵심적 위치를 차지하고 있습니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 12. SWOT 분석
    # ═══════════════════════════════════════
    story.append(Paragraph('10. SWOT 분석 및 투자 리스크', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))
    story.append(chart_image('chart9_swot.png', width=165*mm))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('주요 투자 리스크', h2_style))
    story.append(Paragraph(
        '<b>1. 반독점 규제:</b> 검색 반독점 소송에서 크롬/안드로이드 강제 매각은 면했지만, '
        '독점 계약 제한(애플과의 디폴트 검색 계약 연간 갱신 의무화) 등 행동 규제가 부과되었습니다. '
        '더 큰 리스크는 광고 기술(Ad-Tech) 재판으로, 2026년 말 Google Ad Manager/AdX의 '
        '강제 분리 판결 가능성이 있습니다.<br/><br/>'
        '<b>2. 과잉 투자 리스크:</b> 2026년 CAPEX $1,750~1,850억은 전례 없는 규모입니다. '
        'AI 인프라 투자가 기대만큼 수익을 창출하지 못할 경우, 대규모 감가상각 부담이 수익성을 압박할 수 있습니다.<br/><br/>'
        '<b>3. AI 경쟁 심화:</b> OpenAI/Microsoft, Meta, Anthropic 등과의 AI 경쟁이 치열해지고 있으며, '
        'AI 검색이 기존 검색 광고 모델을 잠식할 가능성도 있습니다.<br/><br/>'
        '<b>4. 애플 계약 불확실성:</b> 구글은 애플에 연간 ~$260억을 지불하고 기본 검색 엔진 지위를 유지하는데, '
        '반독점 판결로 이 계약 구조가 변경될 수 있습니다.',
        body_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════
    # 13. 밸류에이션 및 투자 결론
    # ═══════════════════════════════════════
    story.append(Paragraph('11. 밸류에이션 및 투자 결론', h1_style))
    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('밸류에이션 지표', h2_style))
    val_data = [
        ['구분', '2020', '2021', '2022', '2023', '2024'],
        ['PER (배)', '29.3', '25.3', '19.1', '23.8', '23.2'],
        ['PBR (배)', '5.7', '7.6', '4.5', '6.2', '7.2'],
        ['EPS ($)', '2.93', '5.61', '4.56', '5.80', '8.04'],
        ['BPS ($)', '16.3', '18.7', '19.4', '23.0', '26.5'],
        ['배당금 ($)', '-', '-', '-', '-', '0.84'],
    ]
    story.append(make_table(val_data[0], val_data[1:], col_widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 5*mm))

    story.append(tip_box(
        '<b>PER</b>(주가수익비율)은 "주가가 1년 이익의 몇 배인지"를 보여줘요. '
        'PER 23배라면 "현재 이익 수준으로 투자금을 회수하는데 23년 걸린다"는 뜻이에요. '
        '하지만 이익이 매년 30% 이상 성장한다면, 실제 회수 기간은 훨씬 짧아져요! '
        '<b>PBR</b>은 "주가가 장부 가치(순자산)의 몇 배인지"인데, 기술주는 보통 PBR이 높은 편이에요.'
    ))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('증권사 컨센서스', h2_style))
    cons_data = [
        ['항목', '내용'],
        ['투자의견', '매수 (Buy) — 60 Buy / 7 Hold / 0 Sell'],
        ['목표주가 (중간값)', '$387.50'],
        ['목표주가 (최고)', '$443.00'],
        ['목표주가 (최저)', '$185.00'],
        ['현재주가 대비 상승여력', '~36% (중간값 기준)'],
    ]
    story.append(make_table(cons_data[0], cons_data[1:], col_widths=[50*mm, 120*mm]))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph('최근 주요 뉴스 & 이슈', h2_style))
    story.append(Paragraph(
        '• FY2025 매출 $403B 돌파, 순이익 $132.2B로 사상 최대 실적<br/>'
        '• Gemini 3 Pro 출시 — 멀티모달 AI에서 업계 선도<br/>'
        '• 2024년 4월 사상 첫 배당 개시 (분기당 $0.20)<br/>'
        '• $70B 규모 자사주 매입 프로그램 승인<br/>'
        '• 2026년 1월 시가총액 $4조 돌파 (빅테크 4번째)<br/>'
        '• 검색 반독점 행동 규제 확정 / 광고 기술 재판 진행 중',
        body_style))
    story.append(Spacer(1, 5*mm))

    # 종합 평가
    story.append(Paragraph('종합 투자 평가', h2_style))

    score_data = [
        ['평가 항목', '점수', '코멘트'],
        ['수익성', '★★★★★', '영업이익률 32%, ROE 33% — 초우량'],
        ['성장성', '★★★★☆', 'AI/클라우드 성장 강력, 광고 안정적'],
        ['재무 안정성', '★★★★★', '사실상 무차입, 이자보상비율 100배+'],
        ['현금 창출력', '★★★★★', 'FCF $72.8B, 영업CF/영업이익 130%+'],
        ['밸류에이션', '★★★★☆', 'PER 23배 — 성장 대비 합리적'],
        ['리스크', '★★★☆☆', '반독점, AI CAPEX 과잉투자 우려'],
        ['종합', '★★★★☆ (4.2/5)', '강력한 펀더멘털, 합리적 밸류에이션'],
    ]
    st2 = make_table(score_data[0], score_data[1:], col_widths=[35*mm, 30*mm, 105*mm])
    story.append(st2)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        '<b>투자 결론:</b> 알파벳은 검색 광고 독점, AI 기술 선도, 클라우드 고성장이라는 '
        '세 가지 강력한 성장 엔진을 보유한 기업입니다. PER 23배에 순이익 성장률 30%+를 감안하면 '
        'PEG 비율이 약 0.7배로, 성장성 대비 저평가된 수준입니다. '
        '반독점 리스크와 대규모 AI 투자가 단기적 불확실성 요인이지만, '
        '장기 투자 관점에서는 매력적인 투자 기회로 판단됩니다.',
        body_style))
    story.append(Spacer(1, 10*mm))

    # 면책 조항
    story.append(HRFlowable(width='100%', thickness=0.5, color=MEDIUM_TEXT))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        '<b>면책 조항:</b> 본 보고서는 공개된 정보를 바탕으로 작성된 투자 참고 자료이며, '
        '특정 종목의 매수 또는 매도를 권유하지 않습니다. 투자에 대한 최종 판단과 책임은 '
        '투자자 본인에게 있으며, 본 보고서의 내용으로 인한 어떠한 손실에 대해서도 책임을 지지 않습니다. '
        '투자 전 반드시 전문가와 상담하시기 바랍니다.',
        make_style('Disclaimer', fontSize=8, textColor=MEDIUM_TEXT, leading=12)))

    # 빌드
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f'\n✅ PDF 생성 완료: {PDF_PATH}')


if __name__ == '__main__':
    build()
