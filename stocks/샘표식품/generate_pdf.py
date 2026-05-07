#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
샘표식품(248170) 투자 분석 PDF 보고서 생성
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, '샘표식품_investment_report.pdf')

# ── 색상 ──
PRIMARY = HexColor('#1E3A5F')
ACCENT = HexColor('#2563EB')
LIGHT_BG = HexColor('#EFF6FF')
HEADER_BG = HexColor('#1E3A5F')
ROW_ALT = HexColor('#F8FAFC')
ORANGE = HexColor('#F97316')
GREEN = HexColor('#10B981')
RED = HexColor('#EF4444')

# ── 폰트 등록 ──
FONT_PATH = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
if not os.path.exists(FONT_PATH):
    FONT_PATH = '/System/Library/Fonts/AppleGothic.ttf'
pdfmetrics.registerFont(TTFont('AppleGothic', FONT_PATH))

# ── 스타일 ──
styles = getSampleStyleSheet()

def make_style(name, parent='Normal', **kwargs):
    base = styles[parent]
    kwargs.setdefault('fontName', 'AppleGothic')
    return ParagraphStyle(name, parent=base, **kwargs)

title_style = make_style('TitleKR', fontSize=24, alignment=TA_CENTER, textColor=PRIMARY,
                          spaceAfter=6, leading=30)
h1_style = make_style('H1KR', fontSize=16, textColor=PRIMARY, spaceAfter=8,
                        spaceBefore=14, leading=22)
h2_style = make_style('H2KR', fontSize=13, textColor=ACCENT, spaceAfter=6,
                        spaceBefore=10, leading=18)
body_style = make_style('BodyKR', fontSize=10, leading=16, spaceAfter=4,
                          alignment=TA_JUSTIFY)
small_style = make_style('SmallKR', fontSize=8, leading=12, textColor=HexColor('#6B7280'))
tip_style = make_style('TipKR', fontSize=9.5, leading=14, backColor=LIGHT_BG,
                         spaceAfter=6, spaceBefore=4, borderPadding=6)
center_style = make_style('CenterKR', fontSize=10, alignment=TA_CENTER, leading=14)
right_style = make_style('RightKR', fontSize=9, alignment=TA_RIGHT, leading=12,
                           textColor=HexColor('#6B7280'))
cover_sub = make_style('CoverSub', fontSize=12, alignment=TA_CENTER, textColor=HexColor('#64748B'),
                         leading=16)

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

def header_footer(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFont('AppleGothic', 8)
    canvas.setFillColor(HexColor('#64748B'))
    canvas.drawString(MARGIN, PAGE_H - 12*mm, '샘표식품(248170) 투자 분석 보고서')
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 12*mm, '2026.04.02')
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, PAGE_H - 14*mm, PAGE_W - MARGIN, PAGE_H - 14*mm)
    # Footer
    canvas.setFont('AppleGothic', 8)
    canvas.setFillColor(HexColor('#94A3B8'))
    canvas.drawCentredString(PAGE_W/2, 10*mm, f'- {doc.page} -')
    canvas.restoreState()

def make_table(data, col_widths=None, has_header=True):
    """표준 테이블 생성"""
    if col_widths is None:
        col_widths = [170*mm / len(data[0])] * len(data[0])
    t = Table(data, colWidths=col_widths)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'AppleGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#E2E8F0')),
    ]
    if has_header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t

def tip_box(text):
    return Paragraph(f'<font color="#2563EB"><b>[Tip]</b></font> {text}', tip_style)

def add_chart(filename, width=150*mm, max_height=130*mm):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        img = Image(path, width=width, height=width * 0.55)
        # Respect aspect ratio but cap height
        orig_ratio = 10.0 / 5.5  # figsize ratio from chart script
        desired_h = width / orig_ratio
        if desired_h > max_height:
            desired_h = max_height
            width = max_height * orig_ratio
        img = Image(path, width=width, height=desired_h)
        return img
    return Paragraph(f'[차트 파일 없음: {filename}]', body_style)


# ══════════════════════════════════════════
# 보고서 작성
# ══════════════════════════════════════════
doc = SimpleDocTemplate(PDF_PATH, pagesize=A4,
                         topMargin=18*mm, bottomMargin=18*mm,
                         leftMargin=MARGIN, rightMargin=MARGIN)
story = []

# ─────────────────────────────────────────
# 1. 표지
# ─────────────────────────────────────────
story.append(Spacer(1, 50*mm))
story.append(Paragraph('샘표식품', title_style))
story.append(Paragraph('Sempio Foods Company', make_style('EN', fontSize=14,
              alignment=TA_CENTER, textColor=HexColor('#94A3B8'), leading=18)))
story.append(Spacer(1, 8*mm))
story.append(Paragraph('종합 투자 분석 보고서', make_style('Sub', fontSize=18,
              alignment=TA_CENTER, textColor=ACCENT, leading=24)))
story.append(Spacer(1, 15*mm))

cover_data = [
    ['종목코드', 'KRX: 248170 (KOSPI)'],
    ['현재 주가', '28,300원 (2026.04.01)'],
    ['시가총액', '1,293억원'],
    ['투자의견', '관심 (중립)'],
    ['PER / PBR', '6.50배 / 0.49배'],
    ['52주 최고/최저', '37,800원 / 22,300원'],
]
cover_table = Table(cover_data, colWidths=[70*mm, 100*mm])
cover_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'AppleGothic'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('LEADING', (0, 0), (-1, -1), 16),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#64748B')),
    ('TEXTCOLOR', (1, 0), (1, -1), PRIMARY),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor('#E2E8F0')),
]))
story.append(cover_table)
story.append(Spacer(1, 20*mm))
story.append(Paragraph('작성일: 2026년 4월 2일', cover_sub))
story.append(Spacer(1, 5*mm))
story.append(Paragraph('<font color="#94A3B8" size="8">본 보고서는 투자 참고 자료이며, 투자 결정에 따른 모든 책임은 투자자 본인에게 있습니다.</font>',
                         make_style('Disc', fontSize=8, alignment=TA_CENTER, leading=12)))
story.append(PageBreak())


# ─────────────────────────────────────────
# 2. 목차
# ─────────────────────────────────────────
story.append(Paragraph('목차', h1_style))
story.append(Spacer(1, 5*mm))
toc_items = [
    '1. 회사 개요',
    '2. 비전과 경영철학',
    '3. 사업모델 분석',
    '4. 재무제표 분석 - 초보자 가이드',
    '5. 수익성 분석',
    '6. 성장성 분석',
    '7. 재무 안정성 분석',
    '8. 현금흐름 분석 - 초보자 가이드',
    '9. 산업 분석 및 경쟁 환경',
    '10. SWOT 분석 및 투자 리스크',
    '11. 밸류에이션 및 투자 결론',
]
for item in toc_items:
    story.append(Paragraph(item, make_style('TOC', fontSize=12, leading=20,
                  leftIndent=10*mm, textColor=PRIMARY)))
story.append(PageBreak())


# ─────────────────────────────────────────
# 3. 회사 개요
# ─────────────────────────────────────────
story.append(Paragraph('1. 회사 개요', h1_style))
story.append(Paragraph(
    '샘표식품은 1946년 창립 이래 80년 가까운 역사를 가진 대한민국 대표 전통식품 기업입니다. '
    '간장, 된장, 고추장 등 장류를 기반으로 소스, 양념, 면류, 차류, 통조림까지 사업을 확장해왔습니다. '
    '2016년 7월 샘표(주)에서 인적분할되어 사업회사인 샘표식품(주)로 설립되었으며, '
    '현재 KOSPI(코스피)에 종목코드 248170으로 상장되어 있습니다. '
    '지주회사인 샘표(주)(007540)가 49.38%의 지분을 보유하고 있습니다.', body_style))
story.append(Spacer(1, 3*mm))

info_data = [
    ['항목', '내용'],
    ['설립일', '1946년 (분할설립: 2016.07.04)'],
    ['대표이사', '박진선 (3세 경영, 오너 일가)'],
    ['본사', '서울특별시 중구'],
    ['종목코드', 'KRX 248170 (KOSPI)'],
    ['발행주식수', '약 457만주'],
    ['시가총액', '약 1,293억원'],
    ['직원수', '약 620명'],
    ['R&D 인력비중', '전체 임직원의 약 20%'],
    ['주요 자회사', '양포식품, 조치원식품, 샘표아이에스피'],
]
story.append(make_table(info_data, col_widths=[50*mm, 120*mm]))
story.append(Spacer(1, 4*mm))

story.append(Paragraph('<b>주주 구성</b>', h2_style))
sh_data = [
    ['주주', '지분율'],
    ['샘표(주) (지주회사)', '49.38%'],
    ['박진선 외 특수관계인', '48.44% (지주회사 기준)'],
    ['외국인 투자자', '7.67%'],
    ['자사주', '0.04%'],
    ['기타 소액주주', '약 42.9%'],
]
story.append(make_table(sh_data, col_widths=[85*mm, 85*mm]))
story.append(tip_box(
    '오너 일가가 지주회사를 통해 강력한 지배력을 행사하고 있습니다. '
    '4세 승계(박용학 상무)가 진행 중이며, 약 290억원의 증여세 이슈가 있습니다. '
    '외국인 지분율 7.67%는 소형주 치고는 양호한 수준입니다.'))
story.append(PageBreak())


# ─────────────────────────────────────────
# 4. 비전과 경영철학
# ─────────────────────────────────────────
story.append(Paragraph('2. 비전과 경영철학', h1_style))
story.append(Paragraph(
    '샘표식품의 핵심 비전은 <b>"발효 기술 기반의 글로벌 식품 기업"</b>으로의 도약입니다. '
    '"우리 발효"를 핵심 키워드로 삼아, 80년간 축적한 식물성 발효 기술을 바탕으로 '
    'K-푸드(K-Food)의 세계화를 선도하겠다는 전략을 추진하고 있습니다.', body_style))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>핵심 전략 방향</b>', h2_style))
strategies = [
    '<b>1) 글로벌 K-소스 기업</b>: 간장, 연두, 고추장 3대 제품을 세계시장에 확대. '
    '연두는 미국 Whole Foods, Albertsons 등 주요 유통채널에 입점. 아마존 매출 매년 세 자릿수 성장.',
    '<b>2) 발효 기술 R&D 강화</b>: 매출의 4~5%를 R&D에 투자. 2013년 설립한 "우리발효연구중심"은 '
    '아시아 유일의 식물성 발효 전문 연구소로, 3,000종 이상의 미생물 자원 보유.',
    '<b>3) 바이오 소재 신사업</b>: 미생물 발효 기술을 활용한 Pepreach(단백질 유래 기능성 소재), '
    'Savoryrich(천연 조미 소재) 등 B2B 바이오 소재 시장 진출.',
    '<b>4) 제조 인프라 확장</b>: 2028년까지 충북 제천 제2산업단지에 8.1만㎡ 규모 신공장 건설. '
    '글로벌 수요 확대 대비.',
]
for s in strategies:
    story.append(Paragraph(f'  {s}', body_style))
    story.append(Spacer(1, 1*mm))

story.append(Spacer(1, 3*mm))
story.append(Paragraph('<b>ESG 관련</b>', h2_style))
story.append(Paragraph(
    '샘표식품은 중소형 기업 특성상 별도의 ESG 보고서를 발간하지 않으나, '
    '발효 기반 식물성 제품 확대(비건/Non-GMO/글루텐프리 라인업), 친환경 포장재 도입, '
    '지역 사회 공헌 활동 등을 통해 ESG 가치를 실천하고 있습니다. '
    '연두 제품은 100% 식물성 원료 기반으로 지속가능한 식품 트렌드에 부합합니다.', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 5. 사업모델 분석
# ─────────────────────────────────────────
story.append(Paragraph('3. 사업모델 분석', h1_style))
story.append(Paragraph(
    '샘표식품은 <b>발효 기술 기반의 종합 식품 제조 기업</b>입니다. '
    '전통 장류(간장/된장/고추장)에서 출발하여 소스, 양념, 간편식, 면류, 차류, 통조림까지 '
    '제품 라인업을 지속적으로 확장하고 있습니다.', body_style))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>주요 제품/브랜드</b>', h2_style))
prod_data = [
    ['제품군', '대표 브랜드/제품', '특징'],
    ['장류', '샘표 간장, 된장, 고추장', '국내 간장 시장 1위'],
    ['소스/양념', '연두, 새미네부엌, 차오차이', '연두: 글로벌 히트상품'],
    ['양식소스', '폰타나 (파스타소스)', '프리미엄 양식 소스'],
    ['아시안소스', '티아시아', '동남아/중화 요리소스'],
    ['면류', '질러 (라면)', '젊은층 타겟 라면'],
    ['차류', '조치원식품 생산', '전통 차 제품'],
    ['통조림', '양포식품 생산', '참치, 콩 통조림 등'],
    ['B2B 소재', 'Pepreach, Savoryrich', '발효 기반 기능성 소재'],
]
story.append(make_table(prod_data, col_widths=[35*mm, 60*mm, 75*mm]))
story.append(Spacer(1, 4*mm))

story.append(PageBreak())
story.append(Paragraph('<b>매출 구성 변화</b>', h2_style))
story.append(Paragraph(
    '핵심 변화는 <b>장류 중심에서 비장류로의 매출 다각화</b>입니다. '
    '2019년 장류 58.5% vs 비장류 41.5%였던 구성이, 2023년에는 장류 49.9% vs 비장류 50.1%로 '
    '비장류가 처음으로 과반을 넘겼습니다. 비장류 매출은 5년간 73% 급증했습니다.', body_style))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart6_segment.png', width=110*mm))
story.append(Spacer(1, 4*mm))

story.append(Paragraph('<b>경쟁우위</b>', h2_style))
adv_items = [
    '<b>80년 브랜드 파워</b>: 1946년부터 이어온 "샘표 간장"은 국내 간장 시장 부동의 1위.',
    '<b>독보적 발효 R&D</b>: 3,000종 이상의 미생물 자원과 다수의 발효 특허 보유.',
    '<b>글로벌 검증</b>: 연두는 영국 Great Taste Awards 최우수상, 고추장은 2025 세계일류상품 선정.',
    '<b>높은 R&D 투자</b>: 매출의 4~5%, 인력의 20%를 연구개발에 투입하는 기술 중심 기업.',
]
for a in adv_items:
    story.append(Paragraph(f'  - {a}', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 6. 재무제표 분석
# ─────────────────────────────────────────
story.append(Paragraph('4. 재무제표 분석 - 초보자 가이드', h1_style))
story.append(tip_box(
    '<b>재무제표란?</b> 회사의 "성적표"입니다. 매출액은 "총 벌어들인 돈", '
    '영업이익은 "본업으로 남긴 돈", 당기순이익은 "세금까지 다 내고 최종적으로 남은 돈"입니다.'))
story.append(Spacer(1, 3*mm))

fin_data = [
    ['항목 (억원)', '2021', '2022', '2023', '2024', '2025'],
    ['매출액', '3,487', '3,712', '3,834', '4,049', '4,089'],
    ['영업이익', '235', '111', '98', '65', '245'],
    ['당기순이익', '237', '131', '104', '101', '199'],
    ['영업이익률(%)', '6.7', '3.0', '2.6', '1.6', '6.0'],
    ['순이익률(%)', '6.8', '3.5', '2.7', '2.5', '4.9'],
    ['EPS(원)', '5,186', '2,868', '2,283', '2,203', '4,366'],
    ['BPS(원)', '47,073', '49,788', '51,784', '53,866', '58,050'],
    ['배당금(원)', '200', '200', '200', '200', '200'],
]
story.append(make_table(fin_data, col_widths=[36*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]))
story.append(Spacer(1, 4*mm))
story.append(add_chart('chart1_revenue_profit.png'))
story.append(Spacer(1, 4*mm))

story.append(Paragraph('<b>해석</b>', h2_style))
story.append(Paragraph(
    '매출은 2021~2025년 동안 꾸준히 성장하여 4,089억원까지 도달했습니다. '
    '그러나 영업이익은 2021년 235억원에서 2024년 65억원까지 급락했다가 '
    '2025년 245억원으로 극적으로 반등했습니다. ', body_style))
story.append(Paragraph(
    '<b>수익성 악화의 원인</b>은 비장류 사업 확대를 위한 공격적 마케팅 투자입니다. '
    '판매관리비가 2020년 1,084억원에서 2024년 1,476억원으로 36% 급증했습니다. '
    '연두, 폰타나, 차오차이 등 신규 브랜드 런칭에 막대한 광고비가 투입된 것입니다. '
    '2025년의 반등은 이러한 투자가 성과를 내기 시작했음을 보여줍니다.', body_style))
story.append(tip_box(
    '<b>EPS(주당순이익)</b>란 "주식 1주당 벌어들인 순이익"입니다. '
    '2024년 2,203원에서 2025년 4,366원으로 거의 2배 증가해, 주당 가치가 높아졌습니다. '
    '<b>BPS(주당순자산)</b>는 "주식 1주당 회사의 순자산 가치"로, 58,050원입니다. '
    '현재 주가 28,300원은 BPS의 절반에도 미치지 못해 PBR 0.49배로 자산 대비 저평가 상태입니다.'))
story.append(PageBreak())


# ─────────────────────────────────────────
# 7. 수익성 분석
# ─────────────────────────────────────────
story.append(Paragraph('5. 수익성 분석', h1_style))
story.append(add_chart('chart2_profitability.png'))
story.append(Spacer(1, 3*mm))

prof_data = [
    ['지표', '2021', '2022', '2023', '2024', '2025'],
    ['영업이익률(%)', '6.7', '3.0', '2.6', '1.6', '6.0'],
    ['순이익률(%)', '6.8', '3.5', '2.7', '2.5', '4.9'],
    ['ROE(%)', '11.64', '5.92', '4.50', '4.17', '7.81'],
    ['ROA(%)', '7.95', '3.87', '2.91', '2.73', '5.32'],
]
story.append(make_table(prof_data, col_widths=[36*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart3_roe_roa.png'))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    'ROE는 <b>"주주의 돈(자기자본)으로 얼마나 효율적으로 이익을 냈는가"</b>를 보여주는 지표입니다. '
    '2024년 4.17%에서 2025년 7.81%로 회복한 것은 긍정적이지만, '
    '아직 2021년 수준(11.64%)에는 미치지 못합니다. '
    '일반적으로 ROE 10% 이상이면 우량 기업으로 평가합니다.', body_style))
story.append(tip_box(
    '<b>ROE(자기자본이익률)</b>는 "100만원 투자해서 얼마를 벌었나"와 같습니다. '
    'ROE 7.81%란 자기자본 100원당 약 7.8원의 순이익을 냈다는 의미입니다. '
    '은행 예금금리(3~4%)보다는 높으므로 투자 가치가 있다고 볼 수 있습니다.'))
story.append(PageBreak())


# ─────────────────────────────────────────
# 8. 성장성 분석
# ─────────────────────────────────────────
story.append(Paragraph('6. 성장성 분석', h1_style))
story.append(add_chart('chart5_growth.png'))
story.append(Spacer(1, 3*mm))

growth_data = [
    ['성장률(%)', '2022', '2023', '2024', '2025'],
    ['매출 성장률', '6.4', '3.3', '5.6', '1.0'],
    ['영업이익 성장률', '-52.8', '-11.7', '-33.7', '276.9'],
    ['순이익 성장률', '-44.7', '-20.6', '-2.9', '97.0'],
]
story.append(make_table(growth_data, col_widths=[40*mm, 32*mm, 32*mm, 32*mm, 32*mm]))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    '매출은 연평균 4% 내외로 안정적 성장을 이어가고 있습니다. '
    '영업이익은 2022~2024년간 지속적으로 감소했으나 2025년에 <b>+276.9%</b>라는 경이적인 반등을 보였습니다. '
    '이는 신규 브랜드 투자의 성과가 본격화되면서 매출 확대와 비용 효율화가 동시에 이루어진 결과입니다.', body_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph('<b>미래 성장 동력</b>', h2_style))
story.append(Paragraph(
    '(1) <b>연두의 글로벌 확장</b>: 연평균 30%+ 해외 매출 성장, 누적 3,500만 병 판매<br/>'
    '(2) <b>K-소스 수출 확대</b>: 간장/연두/고추장 모두 "세계일류상품" 선정<br/>'
    '(3) <b>제천 신공장</b>: 2028년 완공으로 생산능력 대폭 확대<br/>'
    '(4) <b>바이오 소재 사업</b>: 발효 기술 기반 B2B 소재 시장 진출<br/>'
    '(5) <b>매출 1조원 목표</b>: 현재 4,089억원에서 중장기 1조원 달성 목표', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 9. 재무 안정성 분석
# ─────────────────────────────────────────
story.append(Paragraph('7. 재무 안정성 분석', h1_style))
story.append(tip_box(
    '<b>부채비율</b>은 "빌린 돈 / 내 돈"의 비율입니다. 100% 이하면 빌린 돈보다 내 돈이 더 많다는 뜻이라 안전합니다. '
    '<b>유동비율</b>은 "1년 내 갚아야 할 빚 대비, 1년 내 현금화할 수 있는 자산의 비율"입니다. '
    '100% 이상이면 단기 자금 사정이 양호합니다.'))
story.append(Spacer(1, 3*mm))

stab_data = [
    ['지표', '2021', '2022', '2023', '2024', '2025'],
    ['부채비율(%)', '52.4', '54.1', '55.1', '50.4', '43.5'],
    ['자기자본비율(%)', '65.6', '64.9', '64.5', '66.5', '69.7'],
    ['유동비율(%)', '203.9', '174.1', '131.3', '141.1', '165.1'],
    ['이자보상비율(배)', '37.0', '19.3', '12.2', '3.5', '12.1'],
]
story.append(make_table(stab_data, col_widths=[38*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart4_stability.png'))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    '샘표식품의 재무 안정성은 <b>매우 우수</b>합니다. '
    '부채비율 43.5%는 제조업 평균(약 80~100%)보다 훨씬 낮고, '
    '자기자본비율 69.7%는 전체 자산의 약 70%가 자기 돈이라는 의미입니다. '
    '유동비율 165%는 단기 채무 이행 능력이 충분함을 보여줍니다.', body_style))
story.append(Paragraph(
    '이자보상비율은 2024년 3.5배로 일시적으로 하락했으나 2025년 12.1배로 회복했습니다. '
    '이는 영업이익 회복의 직접적인 영향입니다. 전반적으로 부도 리스크가 매우 낮은 기업입니다.', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 10. 현금흐름 분석
# ─────────────────────────────────────────
story.append(Paragraph('8. 현금흐름 분석 - 초보자 가이드', h1_style))
story.append(tip_box(
    '<b>현금흐름표</b>는 회사에 실제로 돈이 얼마나 들어오고 나갔는지를 보여줍니다. '
    '재무제표의 이익은 "장부상 이익"이지만, 현금흐름은 "실제 현금의 움직임"입니다. '
    '회사가 흑자인데 현금이 없으면 부도가 날 수 있으므로 매우 중요합니다.'))
story.append(Spacer(1, 3*mm))

cf_data = [
    ['항목 (억원)', '2021', '2022', '2023', '2024', '2025'],
    ['영업활동CF', '320', '152', '205', '335', '583'],
    ['투자활동CF', '-633', '-311', '-316', '-142', '-374'],
    ['재무활동CF', '317', '-8', '135', '-87', '-236'],
    ['CAPEX', '-', '416', '312', '198', '223'],
    ['FCF (영업CF-CAPEX)', '-', '-264', '-107', '137', '360'],
]
story.append(make_table(cf_data, col_widths=[38*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart10_cashflow.png'))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    '2025년 영업활동 현금흐름이 583억원으로 전년 대비 74% 급증한 것은 매우 긍정적입니다. '
    'FCF(잉여현금흐름)도 360억원으로 크게 개선되었습니다.', body_style))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart12_earnings_quality.png'))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>이익의 질 분석</b>', h2_style))
story.append(Paragraph(
    '영업활동CF가 영업이익보다 큰 것은 <b>"이익의 질이 높다"</b>는 의미입니다. '
    '2025년 영업이익 245억원 vs 영업활동CF 583억원으로, 장부상 이익보다 실제 현금 유입이 2.4배 많습니다. '
    '이는 감가상각비 등 비현금 비용이 포함되어 있고, 운전자본 관리가 잘 되고 있다는 뜻입니다.', body_style))
story.append(tip_box(
    '<b>FCF(잉여현금흐름)</b>는 "영업으로 벌어들인 현금에서 설비투자비를 뺀 순수한 여유 현금"입니다. '
    'FCF가 플러스이면 배당, 부채 상환, 신규 투자 등에 쓸 여유가 있다는 뜻입니다. '
    '2025년 360억원의 FCF는 회사 재정이 건강하다는 강력한 신호입니다.'))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart11_fcf_cash.png'))
story.append(PageBreak())


# ─────────────────────────────────────────
# 11. 산업 분석 및 경쟁 환경
# ─────────────────────────────────────────
story.append(Paragraph('9. 산업 분석 및 경쟁 환경', h1_style))
story.append(Paragraph('<b>국내 장류 시장</b>', h2_style))
story.append(Paragraph(
    '국내 장류 시장은 2010년대 중후반 약 1조 2,000~3,000억원 규모에서 정점을 찍은 후 '
    '매년 감소하여 현재 약 <b>9,900억원</b> 규모로 추정됩니다. 1인 가구 증가와 인구 감소로 '
    '전통 장류 소비는 줄어드는 반면, <b>소스류와 간편 양념 시장은 성장</b>하고 있습니다.', body_style))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>글로벌 소스/조미료 시장</b>', h2_style))
story.append(Paragraph(
    '글로벌 소스 및 조미료 시장은 2024년 약 433억 달러(약 58조원)에서 연평균 5~6% 성장하여 '
    '2030년 약 595억 달러에 이를 전망입니다. 글로벌 발효식품 시장은 2024년 1,265억 달러에서 '
    '연평균 7% 성장이 예상됩니다. K-푸드 열풍으로 한국산 소스 수출이 빠르게 성장 중입니다.', body_style))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>경쟁사 비교</b>', h2_style))
comp_data = [
    ['기업', '2024 매출', '주요 제품', '특징'],
    ['CJ제일제당', '11.4조원\n(식품부문)', '해찬들, 비비고,\n다시다', '국내 1위, 글로벌 전개'],
    ['대상', '4.1조원', '청정원, 종가집', '소스/김치 시장 강자'],
    ['오뚜기', '3.2조원', '오뚜기 카레,\n진라면, 소스류', '라면/소스 종합식품'],
    ['샘표식품', '4,049억원', '샘표 간장, 연두,\n폰타나', '간장 1위, 발효기술'],
]
story.append(make_table(comp_data, col_widths=[30*mm, 30*mm, 40*mm, 70*mm]))
story.append(Spacer(1, 3*mm))
story.append(add_chart('chart7_competitors.png'))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    '샘표식품은 경쟁사 대비 <b>매출 규모가 작지만</b>, 간장 시장 1위와 독보적 발효 기술이라는 '
    '확실한 차별점을 보유하고 있습니다. 특히 연두를 통한 글로벌 시장 공략은 대기업과 차별화된 전략입니다.', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 12. SWOT 분석 및 투자 리스크
# ─────────────────────────────────────────
story.append(Paragraph('10. SWOT 분석 및 투자 리스크', h1_style))
story.append(add_chart('chart9_swot.png'))
story.append(Spacer(1, 4*mm))

story.append(Paragraph('<b>주요 투자 리스크</b>', h2_style))
risks = [
    '<b>수익성 회복의 지속성</b>: 2025년 수익성 반등이 일시적인지, 구조적 개선인지 확인 필요.',
    '<b>경쟁 심화</b>: CJ제일제당, 대상 등 대기업의 소스 시장 공세가 심화되고 있음.',
    '<b>원재료 가격</b>: 대두, 밀 등 원재료 가격 변동에 직접적 영향을 받는 구조.',
    '<b>소형주 유동성</b>: 시가총액 1,293억원의 소형주로 거래량이 적어 매매 시 주가 변동 리스크.',
    '<b>승계 리스크</b>: 3세에서 4세로의 경영권 승계 과정에서 증여세(약 290억원) 이슈.',
    '<b>내수 시장 정체</b>: 국내 장류 시장 축소 추세로 내수 성장에 한계.',
]
for r in risks:
    story.append(Paragraph(f'  - {r}', body_style))
story.append(PageBreak())


# ─────────────────────────────────────────
# 13. 밸류에이션 및 투자 결론
# ─────────────────────────────────────────
story.append(Paragraph('11. 밸류에이션 및 투자 결론', h1_style))

story.append(Paragraph('<b>밸류에이션 지표</b>', h2_style))
val_data = [
    ['지표', '샘표식품', '업종 평균', '해석'],
    ['PER', '6.50배', '15~20배', '업종 대비 크게 저평가'],
    ['PBR', '0.49배', '1.0~1.5배', '순자산 대비 절반 가격'],
    ['ROE', '7.81%', '8~12%', '평균 수준, 회복 추세'],
    ['배당수익률', '0.70%', '1.5~2.5%', '배당 매력 낮음'],
    ['EV/EBITDA', '-', '8~12배', '-'],
]
story.append(make_table(val_data, col_widths=[32*mm, 30*mm, 30*mm, 78*mm]))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    'PER 6.50배, PBR 0.49배는 업종 평균 대비 <b>현저히 저평가</b>된 수준입니다. '
    'BPS(주당순자산) 58,050원 대비 주가 28,300원으로, 순자산의 절반도 안 되는 가격에 거래되고 있습니다. '
    '다만 소형주의 구조적 할인(낮은 유동성, 지배구조 할인)을 감안해야 합니다.', body_style))
story.append(Spacer(1, 3*mm))

story.append(Paragraph('<b>주가 성과</b>', h2_style))
price_data = [
    ['항목', '수치'],
    ['현재 주가', '28,300원 (2026.04.01)'],
    ['52주 최고', '37,800원'],
    ['52주 최저', '22,300원'],
    ['시가총액', '1,293억원'],
    ['베타(1년)', '0.36 (시장 대비 변동성 낮음)'],
]
story.append(make_table(price_data, col_widths=[55*mm, 115*mm]))
story.append(Spacer(1, 4*mm))

story.append(Paragraph('<b>최근 주요 뉴스 (2025~2026)</b>', h2_style))
news_items = [
    '2025년 영업이익 245억원으로 전년 대비 277% 급증, 수익성 회복 확인',
    '2025년 3분기 영업이익 128억원(+171% YoY), 순이익 125억원(+394% YoY) 서프라이즈',
    '충북 제천 제2산업단지 공장 신설 투자 협약 체결 (2028년 완공 목표)',
    '연두, "아누가 2025" 혁신제품 선정 / 고추장, 2025 세계일류상품 선정',
    '사업 목적 변경: 건강기능식품, 전자상거래 등으로 사업 영역 확대',
    '바이오 소재 신사업 (Pepreach, Savoryrich) 본격 추진',
]
for n in news_items:
    story.append(Paragraph(f'  - {n}', body_style))
story.append(Spacer(1, 4*mm))

# 종합 평가
story.append(Paragraph('<b>종합 투자 평가</b>', h2_style))

score_data = [
    ['평가 항목', '점수', '코멘트'],
    ['성장성', '3.5 / 5', '매출 안정 성장, 글로벌 확장 기대'],
    ['수익성', '3.0 / 5', '2025년 회복, 지속성 확인 필요'],
    ['안정성', '4.5 / 5', '낮은 부채비율, 우수한 재무구조'],
    ['밸류에이션', '4.0 / 5', 'PER/PBR 극저평가, 자산가치 매력'],
    ['배당 매력', '1.5 / 5', '연 200원, 수익률 0.7% 미흡'],
    ['경영진/지배구조', '3.0 / 5', '오너 경영, 승계 이슈 주의'],
    ['종합 점수', '3.3 / 5', '가치주 관점에서 매력적'],
]
story.append(make_table(score_data, col_widths=[40*mm, 25*mm, 105*mm]))
story.append(Spacer(1, 4*mm))

story.append(Paragraph(
    '<b>투자의견: 관심(중립)</b><br/>'
    '샘표식품은 PBR 0.49배의 극단적 저평가 상태에서 2025년 수익성 반등이라는 '
    '긍정적 모멘텀이 발생한 종목입니다. 80년 전통의 간장 1위 브랜드, 독보적 발효기술, '
    '연두의 글로벌 히트 등 장기 성장 스토리가 분명합니다.<br/><br/>'
    '다만, (1) 수익성 회복의 지속성 검증, (2) 소형주 유동성 리스크, (3) 시가총액 대비 거래량 부족, '
    '(4) 낮은 배당 매력 등을 고려하면 단기 트레이딩보다는 <b>장기 가치투자 관점</b>에서 접근이 바람직합니다.<br/><br/>'
    '특히 제천 신공장 완공(2028년)과 바이오 소재 사업 본격화 시점이 중요한 모니터링 포인트입니다.', body_style))
story.append(Spacer(1, 8*mm))

# 면책 조항
story.append(Paragraph(
    '<font color="#94A3B8" size="8">'
    '면책 조항: 본 보고서는 공개된 정보를 바탕으로 작성된 투자 참고 자료이며, '
    '투자 권유를 목적으로 하지 않습니다. 모든 투자 판단과 그에 따른 손익의 책임은 '
    '투자자 본인에게 있습니다. 보고서 내 데이터는 작성 시점 기준이며, 이후 변동될 수 있습니다.'
    '</font>', make_style('Disclaimer', fontSize=8, alignment=TA_CENTER, leading=12,
                           textColor=HexColor('#94A3B8'))))


# ── PDF 생성 ──
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF 보고서 생성 완료: {PDF_PATH}")
