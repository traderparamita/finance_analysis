#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""샘표(007540) 종합 투자 분석 PDF 보고서 생성"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# 폰트 등록
# ============================================================
FONT_PATH = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
pdfmetrics.registerFont(TTFont('AppleGothic', FONT_PATH))

# ============================================================
# 색상
# ============================================================
PRIMARY = HexColor('#1E3A5F')
ACCENT = HexColor('#2563EB')
LIGHT_BG = HexColor('#EFF6FF')
NAVY_HDR = HexColor('#1E3A5F')
ROW_ALT = HexColor('#F8FAFC')
ORANGE = HexColor('#F97316')
GREEN = HexColor('#10B981')
RED = HexColor('#EF4444')
GRAY = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#E5E7EB')

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUT_DIR, '샘표_investment_report.pdf')

# ============================================================
# 스타일 정의
# ============================================================
styles = getSampleStyleSheet()

style_title = ParagraphStyle('Title_KR', fontName='AppleGothic', fontSize=28, leading=36,
                              alignment=TA_CENTER, textColor=PRIMARY, spaceAfter=10)
style_subtitle = ParagraphStyle('Subtitle_KR', fontName='AppleGothic', fontSize=14, leading=20,
                                 alignment=TA_CENTER, textColor=ACCENT, spaceAfter=6)
style_h1 = ParagraphStyle('H1_KR', fontName='AppleGothic', fontSize=18, leading=24,
                           textColor=PRIMARY, spaceAfter=12, spaceBefore=16)
style_h2 = ParagraphStyle('H2_KR', fontName='AppleGothic', fontSize=14, leading=18,
                           textColor=ACCENT, spaceAfter=8, spaceBefore=10)
style_body = ParagraphStyle('Body_KR', fontName='AppleGothic', fontSize=10, leading=16,
                             alignment=TA_JUSTIFY, spaceAfter=6)
style_body_center = ParagraphStyle('Body_Center', fontName='AppleGothic', fontSize=10, leading=16,
                                    alignment=TA_CENTER, spaceAfter=6)
style_tip = ParagraphStyle('Tip_KR', fontName='AppleGothic', fontSize=9, leading=14,
                            alignment=TA_LEFT, spaceAfter=6, textColor=HexColor('#1E40AF'))
style_small = ParagraphStyle('Small_KR', fontName='AppleGothic', fontSize=8, leading=12,
                              textColor=GRAY, spaceAfter=4)
style_cover_info = ParagraphStyle('CoverInfo', fontName='AppleGothic', fontSize=11, leading=18,
                                   alignment=TA_CENTER, textColor=HexColor('#374151'))
style_disclaimer = ParagraphStyle('Disclaimer', fontName='AppleGothic', fontSize=8, leading=12,
                                   alignment=TA_CENTER, textColor=GRAY, spaceAfter=4)
style_toc = ParagraphStyle('TOC', fontName='AppleGothic', fontSize=12, leading=22,
                            textColor=PRIMARY, leftIndent=20)

# ============================================================
# 헬퍼 함수
# ============================================================
def make_table(headers, data, col_widths=None):
    """네이비 헤더 + 교차 행 색상 테이블"""
    tdata = [headers] + data
    if col_widths is None:
        col_widths = [170 * mm / len(headers)] * len(headers)
    t = Table(tdata, colWidths=col_widths)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_HDR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'AppleGothic'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(tdata)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t


def tip_box(text):
    """연파란 배경 팁 박스"""
    tip_data = [[Paragraph(f'[Tip] {text}', style_tip)]]
    t = Table(tip_data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def add_chart(filename, width=160):
    """차트 이미지 삽입"""
    path = os.path.join(OUT_DIR, filename)
    if os.path.exists(path):
        return Image(path, width=width * mm, height=width * 0.55 * mm)
    return Paragraph(f'[차트 누락: {filename}]', style_body)


def header_footer(canvas, doc):
    """헤더/푸터"""
    canvas.saveState()
    # 헤더
    canvas.setFont('AppleGothic', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(20 * mm, A4[1] - 12 * mm, '샘표(007540) 투자 분석 보고서')
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, '2026.04.02')
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.8)
    canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
    # 푸터
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(A4[0] / 2, 12 * mm, f'- {doc.page} -')
    canvas.restoreState()


# ============================================================
# PDF 빌드
# ============================================================
doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
)

story = []

# ============================================================
# 1. 표지
# ============================================================
story.append(Spacer(1, 60 * mm))
story.append(Paragraph('샘표', style_title))
story.append(Paragraph('Sempio Co., Ltd.', ParagraphStyle('sub', fontName='AppleGothic',
                        fontSize=13, leading=18, alignment=TA_CENTER, textColor=GRAY)))
story.append(Spacer(1, 15 * mm))
story.append(Paragraph('종합 투자 분석 보고서', style_subtitle))
story.append(Spacer(1, 20 * mm))

cover_data = [
    ['종목코드', 'KRX: 007540 (KOSPI)'],
    ['현재 주가', '54,900원 (2026.04.01)'],
    ['시가총액', '약 1,579억원'],
    ['투자의견', '관심 (중립)'],
    ['PER / PBR', '14.43배 / 0.58배'],
    ['52주 최고/최저', '65,000원 / 40,950원'],
]
cover_tbl = Table(cover_data, colWidths=[50 * mm, 70 * mm])
cover_tbl.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'AppleGothic'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('TEXTCOLOR', (0, 0), (0, -1), GRAY),
    ('TEXTCOLOR', (1, 0), (1, -1), PRIMARY),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
]))
story.append(cover_tbl)
story.append(Spacer(1, 20 * mm))
story.append(Paragraph('작성일: 2026년 4월 2일', style_body_center))
story.append(Spacer(1, 5 * mm))
story.append(Paragraph('본 보고서는 투자 참고 자료이며, 투자 결정에 따른 모든 책임은 투자자 본인에게 있습니다.',
                        style_disclaimer))
story.append(PageBreak())

# ============================================================
# 2. 목차
# ============================================================
story.append(Paragraph('목차', style_h1))
story.append(Spacer(1, 5 * mm))
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
    story.append(Paragraph(item, style_toc))
story.append(PageBreak())

# ============================================================
# 3. 회사 개요
# ============================================================
story.append(Paragraph('1. 회사 개요', style_h1))
story.append(Paragraph(
    '샘표(주)는 1946년 창업주 박규회가 충무로 삼지장유 양조장을 인수하며 출발한 대한민국 대표 식품 기업의 '
    '지주회사입니다. 2016년 7월 인적분할을 통해 사업회사인 샘표식품(주)(248170)과 분리되었으며, '
    '2017년 공정거래법상 지주회사로 전환되었습니다. 핵심 자회사인 샘표식품(지분 49.38%)을 통해 '
    '간장, 된장, 고추장 등 장류와 연두, 폰타나 등 소스류를 생산·판매합니다.',
    style_body))
story.append(Spacer(1, 5 * mm))

info_headers = ['항목', '내용']
info_data = [
    ['설립일', '1946년 (분할: 2016.07, 지주전환: 2017)'],
    ['대표이사', '박진선 (3세 경영, 오너 일가)'],
    ['본사', '서울특별시 중구 충무로'],
    ['종목코드', 'KRX 007540 (KOSPI)'],
    ['발행주식수', '약 287.6만주 (자사주 29.92% 포함)'],
    ['시가총액', '약 1,579억원'],
    ['직원수', '약 2명 (지주회사 본체)'],
    ['핵심 자회사', '샘표식품(49.38%), 양포식품, 조치원식품'],
]
story.append(make_table(info_headers, info_data, col_widths=[45 * mm, 125 * mm]))
story.append(Spacer(1, 8 * mm))

story.append(Paragraph('주주 구성', style_h2))
sh_headers = ['주주', '지분율']
sh_data = [
    ['박진선 (대표이사, 최대주주)', '34.05%'],
    ['자사주 (자기주식)', '29.92% (86만주)'],
    ['박용학 (장남, 4세)', '6.58%'],
    ['고계원 (배우자)', '3.47%'],
    ['외국인 투자자', '소규모'],
    ['기타 소액주주', '약 26%'],
]
story.append(make_table(sh_headers, sh_data, col_widths=[85 * mm, 85 * mm]))
story.append(Spacer(1, 3 * mm))
story.append(tip_box(
    '자사주 29.92%가 핵심 포인트입니다. 2026년 개정 상법에 따라 자사주 소각이 의무화되면, '
    '소각 시 박진선 대표의 지분율이 34.05%에서 약 48.6%로 자동 상승합니다. '
    '동시에 주당순자산(BPS)도 약 43% 상승하는 효과가 있어 주주가치 제고가 기대됩니다.'
))
story.append(PageBreak())

# ============================================================
# 4. 비전과 경영철학
# ============================================================
story.append(Paragraph('2. 비전과 경영철학', style_h1))
story.append(Paragraph(
    '샘표의 창업 정신은 "내 가족이 먹지 못하는 것은 만들지도 팔지도 않는다"입니다. '
    '"우리 발효"를 핵심 키워드로 삼아, 80년간 축적한 식물성 발효 기술을 바탕으로 '
    'K-푸드(K-Food)의 세계화를 선도하겠다는 비전을 추진하고 있습니다.',
    style_body))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('핵심 전략 방향', style_h2))
strategy_items = [
    '1) 글로벌 K-소스 기업: 간장, 연두, 고추장 3대 제품을 세계시장에 확대. '
    '연두는 미국 Whole Foods, Albertsons 등 주요 유통채널에 입점. 아마존 매출 매년 세 자릿수 성장.',
    '2) 발효 기술 R&D 강화: 매출의 4~5%를 R&D에 투자. 2013년 설립한 "우리발효연구중심"은 '
    '아시아 유일의 식물성 발효 전문 연구소로, 3,000종 이상의 미생물 자원 보유.',
    '3) 바이오 소재 신사업: 미생물 발효 기술을 활용한 Pepreach(단백질 유래 기능성 소재), '
    'Savoryrich(천연 조미 소재) 등 B2B 바이오 소재 시장 진출.',
    '4) 제조 인프라 확장: 2028년까지 충북 제천 제2산업단지에 8.1만m² 규모 신공장 건설. 글로벌 수요 확대 대비.',
    '5) 연두 단일 브랜드 연매출 1조원 목표 (10년 내).',
]
for item in strategy_items:
    story.append(Paragraph(item, style_body))

story.append(Spacer(1, 5 * mm))
story.append(Paragraph('ESG 관련', style_h2))
story.append(Paragraph(
    '중소형 지주회사 특성상 별도의 ESG 보고서는 발간하지 않으나, 발효 기반 식물성 제품 확대(비건/Non-GMO), '
    '친환경 포장재 도입, 지역사회 공헌 활동 등을 통해 ESG 가치를 실천하고 있습니다. '
    '연두 제품은 100% 식물성 원료 기반으로 지속가능한 식품 트렌드에 부합합니다.',
    style_body))
story.append(PageBreak())

# ============================================================
# 5. 사업모델 분석
# ============================================================
story.append(Paragraph('3. 사업모델 분석', style_h1))
story.append(Paragraph(
    '샘표(주)는 지주회사로서 자체 영업활동은 거의 없으며, 수익의 대부분이 자회사인 '
    '샘표식품의 실적에 연동됩니다. 연결 기준 매출의 98% 이상이 식품사업 부문에서 발생합니다.',
    style_body))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('지주회사 수익 구조', style_h2))
biz_headers = ['수익원', '비중', '설명']
biz_data = [
    ['지분법이익', '87.7%', '자회사(샘표식품 등) 실적 반영'],
    ['브랜드 로열티', '9.7%', '샘표 브랜드 사용료'],
    ['배당수익', '1.5%', '자회사 배당금 수취'],
    ['임대수익', '1.1%', '부동산 임대'],
]
story.append(make_table(biz_headers, biz_data, col_widths=[40 * mm, 30 * mm, 100 * mm]))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('주요 제품/브랜드 (자회사 샘표식품 기준)', style_h2))
prod_headers = ['제품군', '대표 브랜드/제품', '특징']
prod_data = [
    ['장류', '샘표 간장, 된장, 고추장', '국내 간장 시장 1위 (57%)'],
    ['소스/양념', '연두, 새미네부엌, 차오차이', '연두: 글로벌 히트상품'],
    ['양식소스', '폰타나 (파스타소스)', '프리미엄 양식 소스'],
    ['아시안소스', '티아시아', '동남아/중화 요리소스'],
    ['면류', '질러 (라면)', '젊은층 타겟 라면'],
    ['차류', '조치원식품 생산', '전통 차 제품'],
    ['통조림', '양포식품 생산', '참치, 콩 통조림 등'],
    ['B2B 소재', 'Pepreach, Savoryrich', '발효 기반 기능성 소재'],
]
story.append(make_table(prod_headers, prod_data, col_widths=[35 * mm, 60 * mm, 75 * mm]))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart6_segment.png'))
story.append(Spacer(1, 3 * mm))
story.append(tip_box(
    '샘표의 투자 포인트를 이해하려면, 지주회사(007540)가 아닌 자회사 샘표식품(248170)의 '
    '사업 실적을 함께 봐야 합니다. 지주회사 자체 매출은 미미하지만, 연결재무제표에는 '
    '자회사 실적이 모두 포함되어 있어 전체 그룹의 실적을 파악할 수 있습니다.'
))
story.append(PageBreak())

# ============================================================
# 6. 재무제표 분석 - 초보자 가이드
# ============================================================
story.append(Paragraph('4. 재무제표 분석 - 초보자 가이드', style_h1))
story.append(Paragraph(
    '아래는 샘표(007540)의 연결 기준 손익계산서 핵심 항목입니다. '
    '연결 기준이란 지주회사와 자회사(샘표식품 등)의 실적을 합산한 것입니다.',
    style_body))
story.append(Spacer(1, 3 * mm))

fin_headers = ['구분', '2020', '2021', '2022', '2023', '2024', '2025']
fin_data = [
    ['매출액 (억원)', '3,191', '3,490', '3,718', '3,839', '4,050', '4,090'],
    ['영업이익 (억원)', '411', '219', '103', '81', '59', '241'],
    ['당기순이익 (억원)', '353', '230', '162', '106', '107', '188'],
    ['영업이익률 (%)', '12.88', '6.28', '2.78', '2.12', '1.45', '5.90'],
    ['순이익률 (%)', '11.1', '3.40', '2.81', '1.58', '1.62', '2.38'],
]
story.append(make_table(fin_headers, fin_data,
                         col_widths=[35 * mm] + [22.5 * mm] * 6))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart1_revenue_profit.png'))
story.append(Spacer(1, 3 * mm))

story.append(tip_box(
    '매출액은 "가게의 총 판매금액", 영업이익은 "장사해서 남은 돈", 순이익은 "세금까지 다 내고 진짜 남은 돈"이라고 '
    '생각하면 됩니다. 샘표는 매출이 매년 성장했지만, 영업이익은 2020년 411억에서 2024년 59억까지 급락했습니다. '
    '이는 연두 등 신제품 마케팅에 대규모 투자를 했기 때문입니다. 2025년에 241억으로 대폭 반등한 것은 '
    '투자 효과가 나타나기 시작했다는 긍정적 신호입니다.'
))
story.append(PageBreak())

# ============================================================
# 7. 수익성 분석
# ============================================================
story.append(Paragraph('5. 수익성 분석', style_h1))
story.append(Paragraph(
    '수익성 지표는 기업이 매출에서 얼마나 효율적으로 이익을 창출하는지를 보여줍니다.',
    style_body))
story.append(Spacer(1, 3 * mm))

prof_headers = ['지표', '2020', '2021', '2022', '2023', '2024', '2025']
prof_data = [
    ['영업이익률 (%)', '12.88', '6.28', '2.78', '2.12', '1.45', '5.90'],
    ['순이익률 (%)', '11.1', '3.40', '2.81', '1.58', '1.62', '2.38'],
    ['ROE (%)', '10.50', '6.42', '5.35', '3.06', '3.26', '4.63'],
    ['ROA (%)', '8.50', '5.58', '3.57', '2.26', '2.25', '3.88'],
]
story.append(make_table(prof_headers, prof_data,
                         col_widths=[35 * mm] + [22.5 * mm] * 6))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart2_profitability.png'))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart3_roe_roa.png'))
story.append(Spacer(1, 3 * mm))
story.append(tip_box(
    'ROE는 "내 돈(자본)으로 얼마를 벌었나"를 보여주는 지표입니다. 2020년 10.5%에서 2024년 3.26%로 '
    '급락한 것은 이익이 줄었기 때문입니다. 2025년 4.63%로 반등했지만, 아직 2020년 수준에는 못 미칩니다. '
    '식품업 평균 ROE가 5~8% 수준인 점을 고려하면, 회복 추세가 지속될지 지켜봐야 합니다.'
))
story.append(PageBreak())

# ============================================================
# 8. 성장성 분석
# ============================================================
story.append(Paragraph('6. 성장성 분석', style_h1))
story.append(Paragraph(
    '매출은 꾸준히 성장했지만 이익 성장은 2025년에야 반등했습니다.',
    style_body))

growth_headers = ['지표', '2021', '2022', '2023', '2024', '2025']
growth_data = [
    ['매출 성장률 (%)', '+9.4', '+6.6', '+3.3', '+5.5', '+1.0'],
    ['영업이익 성장률 (%)', '-46.7', '-52.8', '-21.3', '-27.7', '+310.9'],
    ['순이익 성장률 (%)', '-34.8', '-29.6', '-34.6', '+0.9', '+75.7'],
]
story.append(make_table(growth_headers, growth_data,
                         col_widths=[40 * mm] + [26 * mm] * 5))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart5_growth.png'))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph(
    '2025년 영업이익 성장률 +310.9%는 극적인 V자 반등입니다. 이는 ① 마케팅비 효율화, '
    '② 연두/폰타나 등 프리미엄 제품의 매출 비중 확대, ③ 원재료 비용 안정화가 '
    '복합적으로 작용한 결과로 분석됩니다. 다만 매출 성장률은 +1.0%로 둔화되어, '
    '이익 반등이 비용 절감에 의존한 측면이 있어 지속성 확인이 필요합니다.',
    style_body))
story.append(tip_box(
    '매출은 꾸준히 늘었는데 이익이 줄었다는 것은 "많이 팔았지만 남는 게 적었다"는 뜻입니다. '
    '2025년 이익 반등은 "드디어 투자한 보람이 나타나기 시작했다"고 해석할 수 있습니다.'
))
story.append(PageBreak())

# ============================================================
# 9. 재무 안정성 분석
# ============================================================
story.append(Paragraph('7. 재무 안정성 분석', style_h1))
story.append(Paragraph(
    '재무 안정성은 기업이 빚을 갚을 능력이 얼마나 되는지를 보여줍니다. '
    '샘표는 매우 건전한 재무구조를 유지하고 있습니다.',
    style_body))

stab_headers = ['지표', '2020', '2021', '2022', '2023', '2024', '2025']
stab_data = [
    ['부채비율 (%)', '30.98', '41.27', '42.37', '43.89', '40.80', '35.85'],
    ['자기자본비율 (%)', '76.3', '70.8', '70.2', '69.5', '71.0', '73.6'],
    ['유동비율 (%)', '250', '248', '211', '150', '169', '199'],
    ['이자보상배율 (배)', '-', '36.5', '18.1', '10.2', '3.1', '11.7'],
]
story.append(make_table(stab_headers, stab_data,
                         col_widths=[40 * mm] + [21.7 * mm] * 6))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart4_stability.png'))
story.append(Spacer(1, 3 * mm))

story.append(tip_box(
    '부채비율은 "빌린 돈 ÷ 내 돈"입니다. 100% 이하면 양호, 200% 이상이면 주의가 필요합니다. '
    '샘표는 35.85%로 매우 낮아 재무적으로 매우 안전합니다. 유동비율 199%는 "1년 내 갚아야 할 돈의 '
    '약 2배에 해당하는 현금성 자산을 보유"한다는 뜻으로, 단기 부도 위험이 거의 없습니다.'
))
story.append(PageBreak())

# ============================================================
# 10. 현금흐름 분석 - 초보자 가이드
# ============================================================
story.append(Paragraph('8. 현금흐름 분석 - 초보자 가이드', style_h1))
story.append(Paragraph(
    '현금흐름은 기업의 실제 현금 입출금 내역입니다. 이익이 나더라도 현금이 부족하면 '
    '위험할 수 있으므로, 현금흐름 분석은 매우 중요합니다.',
    style_body))

cf_headers = ['구분', '2022', '2023', '2024', '2025']
cf_data = [
    ['영업활동CF (억원)', '183', '229', '351', '618'],
    ['투자활동CF (억원)', '-313', '-265', '-149', '-389'],
    ['재무활동CF (억원)', '-38', '+60', '-75', '-249'],
    ['CAPEX (억원)', '418', '312', '206', '227'],
    ['FCF (억원)', '-235', '-83', '+145', '+391'],
]
story.append(make_table(cf_headers, cf_data,
                         col_widths=[40 * mm] + [32.5 * mm] * 4))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart10_cashflow.png'))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart11_fcf_cash.png'))
story.append(Spacer(1, 3 * mm))

story.append(tip_box(
    'FCF(잉여현금흐름)는 "장사해서 번 현금 - 시설투자에 쓴 현금"입니다. '
    'FCF가 플러스면 투자를 하고도 현금이 남는다는 뜻입니다. 샘표는 2022~2023년 대규모 시설투자(CAPEX)로 '
    'FCF가 마이너스였지만, 2024년부터 플러스로 전환되어 2025년에는 391억원의 잉여현금을 창출했습니다. '
    '이는 재무 건전성이 더 강화되고 있다는 신호입니다.'
))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('이익의 질 (Earnings Quality)', style_h2))
story.append(Paragraph(
    '"이익의 질"이란 회계상 이익이 실제 현금으로 뒷받침되는지를 보는 지표입니다. '
    '영업활동CF가 영업이익보다 크면, 이익의 질이 높다고 평가합니다.',
    style_body))
story.append(add_chart('chart12_earnings_quality.png'))
story.append(Spacer(1, 3 * mm))
story.append(tip_box(
    '2025년 영업이익 241억원에 대해 영업활동CF는 618억원으로, 약 2.6배입니다. '
    '이는 "회계상 이익보다 실제 들어온 현금이 훨씬 많다"는 뜻으로, 이익의 질이 매우 높습니다. '
    '감가상각비 등 현금 유출이 없는 비용이 포함되어 있기 때문입니다.'
))
story.append(PageBreak())

# ============================================================
# 11. 산업 분석 및 경쟁 환경
# ============================================================
story.append(Paragraph('9. 산업 분석 및 경쟁 환경', style_h1))
story.append(Paragraph(
    '한국 장류(간장/된장/고추장) 시장은 약 1.5조원 규모로, 성숙기에 접어든 시장입니다. '
    '인구 감소와 1인 가구 증가로 전통 장류 소비는 완만히 감소하는 반면, '
    '프리미엄 소스류와 간편식 양념 시장은 성장하고 있습니다.',
    style_body))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('경쟁사 비교', style_h2))
comp_headers = ['기업', '시가총액', 'PER', 'PBR', '배당수익률', 'ROE']
comp_data = [
    ['샘표 (007540)', '1,579억', '14.43배', '0.58배', '0.36%', '4.63%'],
    ['오뚜기 (007310)', '14,669억', '21.19배', '0.61배', '2.46%', '3.35%'],
    ['대상홀딩스 (084690)', '3,248억', 'N/A', '0.55배', '3.28%', '-15.42%'],
    ['CJ (001040)', '55,145억', '42.80배', '1.34배', '1.64%', '2.69%'],
]
story.append(make_table(comp_headers, comp_data,
                         col_widths=[35 * mm, 25 * mm, 22 * mm, 22 * mm, 28 * mm, 25 * mm]))
story.append(Spacer(1, 5 * mm))
story.append(add_chart('chart7_competitors.png'))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph(
    '샘표는 시총 기준 동종업계 최소 규모이지만, PER이 14.43배로 CJ(42.80배), 오뚜기(21.19배) 대비 '
    '상대적으로 저렴합니다. PBR도 0.58배로 순자산 대비 42% 할인 거래 중입니다. '
    '다만 배당수익률 0.36%는 동종 대비 극히 낮아 소액주주 불만 요인입니다.',
    style_body))
story.append(tip_box(
    '샘표의 간장 시장 점유율 57%는 압도적 1위입니다. 2위 대상(청정원)과 큰 격차를 유지하고 있어, '
    '가격 결정력과 브랜드 충성도가 높습니다. 다만 간장 시장 자체가 성장하지 않기 때문에, '
    '연두 같은 신제품의 성장이 미래 실적의 핵심 변수입니다.'
))
story.append(PageBreak())

# ============================================================
# 12. SWOT 분석 및 투자 리스크
# ============================================================
story.append(Paragraph('10. SWOT 분석 및 투자 리스크', style_h1))
story.append(add_chart('chart9_swot.png', width=155))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('핵심 투자 리스크', style_h2))
risks = [
    ['자사주 소각 이슈', '개정 상법에 따라 29.92% 자사주 소각 의무화. 소각 시 주당가치 상승이지만, '
     '승계 과정에서의 증여세 부담(약 290억원)과 충돌. 회사 측은 아직 구체적 계획 미발표.'],
    ['극도로 낮은 배당', '2016년 이후 DPS 200원 동결. 누적 순이익 859억원 대비 배당금 37억원(배당성향 4.3%)으로 '
     '소액주주와의 갈등 소지. 2021년 소액주주 배당 증액 내용증명 발송 사례 존재.'],
    ['승계 불확실성', '4세 박용학 상무의 경영 승계가 진행 중이나, 290억원의 증여세 부담이 상당. '
     '자사주 소각 의무화와 맞물려 승계 전략 재검토가 불가피한 상황.'],
    ['소형주 유동성', '시총 1,579억원으로 기관투자자 관심 부족. 증권사 커버리지 부재로 정보 비대칭 존재.'],
    ['해외사업 부진', '미국법인 적자 지속(2024년 영업손실 12억), 중국법인 수익성 급감. '
     'K-Food 트렌드 대비 수혜가 제한적.'],
    ['국세청 조사', '원가 하락에도 가격 인상으로 이익을 관계사에 이전했다는 의혹으로 국세청 조사 보도.'],
]
risk_headers = ['리스크', '상세 내용']
story.append(make_table(risk_headers, risks, col_widths=[35 * mm, 135 * mm]))
story.append(PageBreak())

# ============================================================
# 13. 밸류에이션 및 투자 결론
# ============================================================
story.append(Paragraph('11. 밸류에이션 및 투자 결론', style_h1))

story.append(Paragraph('밸류에이션 지표', style_h2))
val_headers = ['지표', '2020', '2021', '2022', '2023', '2024', '2025']
val_data = [
    ['PER (배)', '7.88', '10.33', '13.06', '23.41', '16.50', '14.43'],
    ['PBR (배)', '0.61', '0.59', '0.62', '0.63', '0.47', '0.58'],
    ['EPS (원)', '6,217', '4,130', '3,629', '2,114', '2,284', '3,388'],
    ['BPS (원)', '80,786', '72,054', '75,948', '77,969', '80,416', '84,351'],
    ['DPS (원)', '200', '200', '200', '200', '200', '200'],
    ['배당수익률 (%)', '0.41', '0.47', '0.42', '0.40', '0.53', '0.41'],
]
story.append(make_table(val_headers, val_data,
                         col_widths=[35 * mm] + [22.5 * mm] * 6))
story.append(Spacer(1, 5 * mm))

story.append(tip_box(
    'PBR 0.58배는 "회사를 지금 해산하면 받을 수 있는 돈(순자산)의 58%에 주식이 거래되고 있다"는 뜻입니다. '
    'BPS 84,351원인데 주가가 54,900원이니, 순자산 대비 약 35% 할인된 가격입니다. '
    '만약 자사주 29.92%가 소각되면 BPS는 약 120,000원 수준으로 상승하여 할인율이 더 커집니다.'
))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('증권사 의견', style_h2))
story.append(Paragraph(
    '샘표(007540)는 소형주로 증권사 커버리지가 거의 없어 공식적인 목표주가나 투자의견이 부재합니다. '
    '이는 기관투자자의 관심이 적다는 의미이며, 동시에 시장에서 충분히 분석되지 않은 '
    '"숨겨진 가치"가 있을 수 있다는 뜻이기도 합니다.',
    style_body))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('최근 주요 뉴스/이슈', style_h2))
news_data = [
    ['2026.03', '개정 상법 시행 - 자사주 소각 의무화 (1년 6개월 내)'],
    ['2025.11', '3분기 영업이익 128억원 (+191% YoY) 어닝 서프라이즈'],
    ['2025.09', '4세 박용학 상무 해외사업 총괄 발탁'],
    ['2025.07', '연두, 미국 Whole Foods 전 매장 입점 확대'],
    ['2025.03', '2024년 실적 발표: 매출 4,050억(+5.5%), 영업이익 59억(-27.7%)'],
    ['2024.12', '국세청 원가/가격 관련 조사 보도'],
]
story.append(make_table(['시기', '내용'], news_data, col_widths=[25 * mm, 145 * mm]))
story.append(Spacer(1, 8 * mm))

# 종합 평가
story.append(Paragraph('종합 투자 평가', style_h2))
score_headers = ['평가 항목', '점수 (5점 만점)', '코멘트']
score_data = [
    ['수익성', '★★★☆☆ (3.0)', '2025년 반등, 지속성 확인 필요'],
    ['성장성', '★★★☆☆ (3.0)', '매출 안정 성장, 연두 글로벌 확대'],
    ['재무 안정성', '★★★★★ (5.0)', '부채비율 36%, 유동비율 199%'],
    ['현금흐름', '★★★★☆ (4.0)', 'FCF 391억, 이익의 질 우수'],
    ['밸류에이션', '★★★★☆ (4.0)', 'PBR 0.58배, 자사주 소각 시 상승 여력'],
    ['배당매력', '★☆☆☆☆ (1.0)', 'DPS 200원 동결, 배당수익률 0.36%'],
    ['지배구조', '★★☆☆☆ (2.0)', '짠물 배당, 승계 이슈, 국세청 조사'],
    ['종합', '★★★☆☆ (3.1)', '가치투자 관점 매력적, 촉매 필요'],
]
story.append(make_table(score_headers, score_data,
                         col_widths=[35 * mm, 40 * mm, 95 * mm]))
story.append(Spacer(1, 5 * mm))

story.append(Paragraph('투자의견: 관심 (중립)', ParagraphStyle(
    'Opinion', fontName='AppleGothic', fontSize=14, leading=20,
    textColor=ACCENT, alignment=TA_CENTER, spaceBefore=8, spaceAfter=8)))
story.append(Paragraph(
    '샘표는 PBR 0.58배의 전형적인 저PBR 가치주입니다. 2025년 실적 턴어라운드와 자사주 소각 의무화는 '
    '주당가치 상승의 촉매가 될 수 있습니다. 그러나 극도로 낮은 배당, 승계 불확실성, 소형주 유동성 부족이 '
    '주가 재평가의 걸림돌입니다. 자사주 소각 시점과 배당 정책 변화를 확인한 후 투자 비중 확대를 검토하는 '
    '전략이 바람직합니다. 장기 가치투자 관점에서 간장 시장 1위 + 연두 글로벌 성장 스토리는 '
    '매력적이나, 단기 촉매가 부족한 상황입니다.',
    style_body))
story.append(Spacer(1, 10 * mm))

# 면책 조항
story.append(Paragraph(
    '면책 조항: 본 보고서는 투자 참고 자료로 작성되었으며, 특정 종목의 매수/매도를 권유하지 않습니다. '
    '투자 결정에 따른 모든 책임은 투자자 본인에게 있습니다. 본 보고서에 포함된 정보는 공개된 자료를 기반으로 '
    '작성되었으며, 정확성을 보장하지 않습니다. 작성일: 2026년 4월 2일.',
    style_disclaimer))

# ============================================================
# PDF 생성
# ============================================================
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"\n✅ PDF 생성 완료: {PDF_PATH}")
