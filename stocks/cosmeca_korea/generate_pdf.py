"""
코스메카코리아 투자 보고서 - PDF 생성 스크립트
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 폰트 등록 ──
FONT = 'AppleGothic'
pdfmetrics.registerFont(TTFont(FONT, '/System/Library/Fonts/Supplemental/AppleGothic.ttf'))

DIR = os.path.dirname(os.path.abspath(__file__))

# ── 색상 ──
C_PRIMARY   = HexColor('#1E3A5F')
C_ACCENT    = HexColor('#2563EB')
C_ORANGE    = HexColor('#F97316')
C_GREEN     = HexColor('#10B981')
C_RED       = HexColor('#EF4444')
C_GRAY      = HexColor('#6B7280')
C_LIGHT_BG  = HexColor('#F8FAFC')
C_TABLE_HEAD = HexColor('#1E3A5F')
C_TABLE_ALT  = HexColor('#F1F5F9')

# ── 스타일 ──
def make_styles():
    s = {}
    s['title'] = ParagraphStyle('Title', fontName=FONT, fontSize=24, leading=32,
                                 textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=4*mm)
    s['subtitle'] = ParagraphStyle('Subtitle', fontName=FONT, fontSize=11, leading=16,
                                    textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=8*mm)
    s['h1'] = ParagraphStyle('H1', fontName=FONT, fontSize=18, leading=26,
                              textColor=C_PRIMARY, spaceBefore=10*mm, spaceAfter=5*mm)
    s['h2'] = ParagraphStyle('H2', fontName=FONT, fontSize=14, leading=20,
                              textColor=C_ACCENT, spaceBefore=7*mm, spaceAfter=3*mm)
    s['h3'] = ParagraphStyle('H3', fontName=FONT, fontSize=12, leading=17,
                              textColor=HexColor('#374151'), spaceBefore=5*mm, spaceAfter=2*mm)
    s['body'] = ParagraphStyle('Body', fontName=FONT, fontSize=10, leading=16,
                                textColor=HexColor('#1F2937'), alignment=TA_JUSTIFY, spaceAfter=3*mm)
    s['body_indent'] = ParagraphStyle('BodyIndent', parent=s['body'], leftIndent=8*mm, rightIndent=8*mm)
    s['tip'] = ParagraphStyle('Tip', fontName=FONT, fontSize=9.5, leading=15,
                               textColor=HexColor('#1E40AF'), leftIndent=8*mm, rightIndent=8*mm,
                               spaceBefore=2*mm, spaceAfter=3*mm, backColor=HexColor('#EFF6FF'),
                               borderPadding=(3*mm, 3*mm, 3*mm, 3*mm))
    s['caption'] = ParagraphStyle('Caption', fontName=FONT, fontSize=9, leading=13,
                                   textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=5*mm)
    s['small'] = ParagraphStyle('Small', fontName=FONT, fontSize=8.5, leading=13,
                                 textColor=C_GRAY, alignment=TA_CENTER)
    s['disclaimer'] = ParagraphStyle('Disclaimer', fontName=FONT, fontSize=8, leading=12,
                                      textColor=C_GRAY, alignment=TA_CENTER, spaceBefore=5*mm)
    return s

STY = make_styles()

# ── 헬퍼 함수 ──
def P(text, style='body'):
    return Paragraph(text, STY[style])

def chart_img(filename, width=160*mm):
    path = os.path.join(DIR, filename)
    if os.path.exists(path):
        img = Image(path, width=width, height=width * 0.55)
        img.hAlign = 'CENTER'
        return img
    return Spacer(1, 5*mm)

def chart_img_square(filename, width=130*mm):
    path = os.path.join(DIR, filename)
    if os.path.exists(path):
        img = Image(path, width=width, height=width)
        img.hAlign = 'CENTER'
        return img
    return Spacer(1, 5*mm)

def make_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), C_TABLE_HEAD),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
        ]
    # Alternating rows
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    t.hAlign = 'CENTER'
    return t

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor('#E5E7EB'),
                       spaceAfter=3*mm, spaceBefore=3*mm)

# ── 페이지 번호 / 헤더 ──
def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
    canvas.setFont(FONT, 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawString(20*mm, A4[1] - 13*mm, "코스메카코리아 (241710.KQ) 투자 분석 보고서")
    canvas.drawRightString(A4[0] - 20*mm, A4[1] - 13*mm, "2026년 4월 1일")
    # Footer
    canvas.setStrokeColor(HexColor('#E5E7EB'))
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, 15*mm, A4[0] - 20*mm, 15*mm)
    canvas.setFont(FONT, 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawCentredString(A4[0] / 2, 9*mm, f"- {doc.page} -")
    canvas.restoreState()

# ── 문서 빌드 ──
def build():
    pdf_path = os.path.join(DIR, 'cosmeca_korea_investment_report.pdf')
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        topMargin=22*mm, bottomMargin=22*mm,
        leftMargin=20*mm, rightMargin=20*mm,
    )
    story = []

    # ════════════════════════════════════════
    # 표지 (PAGE 1)
    # ════════════════════════════════════════
    story.append(Spacer(1, 35*mm))
    story.append(P("코스메카코리아", 'title'))
    story.append(P("(241710.KQ)", 'subtitle'))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="60%", thickness=2, color=C_ACCENT, spaceAfter=8*mm))
    story.append(P("투자 분석 보고서", 'h1'))
    story[-1].style = ParagraphStyle('CenterH1', parent=STY['h1'], alignment=TA_CENTER, spaceBefore=0)
    story.append(Spacer(1, 15*mm))

    cover_data = [
        ['항목', '내용'],
        ['종목코드', '241710 (코스닥)'],
        ['현재 주가', '약 80,000원'],
        ['시가총액', '약 8,512억원'],
        ['투자의견', '매수 (BUY)'],
        ['목표주가', '89,000 ~ 125,000원'],
        ['작성일', '2026년 4월 1일'],
    ]
    story.append(make_table(cover_data, col_widths=[55*mm, 80*mm]))
    story.append(Spacer(1, 30*mm))
    story.append(P("본 보고서는 공개된 정보를 기반으로 작성된 투자 참고 자료이며,<br/>"
                    "투자 판단의 최종 책임은 투자자 본인에게 있습니다.", 'disclaimer'))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 목차 (PAGE 2)
    # ════════════════════════════════════════
    story.append(P("목 차", 'h1'))
    story[-1].style = ParagraphStyle('TOC_Title', parent=STY['h1'], alignment=TA_CENTER)
    story.append(Spacer(1, 8*mm))
    toc_items = [
        "1. 회사 개요",
        "2. 비전과 경영철학",
        "3. 사업모델 분석",
        "4. 재무제표 분석 (초보자 가이드)",
        "5. 수익성 분석",
        "6. 성장성 분석",
        "7. 재무 안정성 분석",
        "8. 현금흐름 분석 (초보자 가이드)",
        "9. 산업 분석 및 경쟁 환경",
        "10. SWOT 분석 및 투자 리스크",
        "11. 밸류에이션 및 투자 결론",
    ]
    for item in toc_items:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}", 'body'))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 1. 회사 개요 (PAGE 3)
    # ════════════════════════════════════════
    story.append(P("1. 회사 개요", 'h1'))
    story.append(P("코스메카코리아는 어떤 회사인가?", 'h2'))
    story.append(P(
        "코스메카코리아는 <b>화장품을 대신 만들어주는 회사</b>입니다. "
        "여러분이 편의점이나 올리브영에서 보는 다양한 화장품 브랜드들이 직접 공장을 짓고 화장품을 만드는 것이 아니라, "
        "코스메카코리아 같은 전문 제조업체에 '이런 화장품을 만들어주세요'라고 주문합니다. "
        "이것을 <b>ODM</b>(Original Design Manufacturing, 설계부터 생산까지) 또는 "
        "<b>OEM</b>(Original Equipment Manufacturing, 주문자 상표 부착 생산)이라고 합니다."
    ))
    story.append(P(
        "<b>쉬운 비유</b>: 코스메카코리아는 화장품 업계의 '삼성전자 파운드리'입니다. "
        "삼성전자가 다른 회사의 반도체를 대신 만들어주듯, "
        "코스메카코리아는 다른 브랜드의 화장품을 대신 만들어줍니다.", 'tip'
    ))

    story.append(Spacer(1, 3*mm))
    info_data = [
        ['항목', '내용'],
        ['정식 명칭', '(주)코스메카코리아 (Cosmecca Korea Co., Ltd.)'],
        ['설립일', '1999년 10월 15일'],
        ['창업자/회장', '조임래'],
        ['종목코드', '241710 (코스닥)'],
        ['업종', '화장품 ODM/OEM'],
        ['본사/공장', '충청북도 음성군'],
        ['R&D 센터', '경기도 성남시 판교 제2테크노밸리 (2025년 신축)'],
        ['직원 수', '약 445~498명'],
        ['해외 법인', '미국(Cosmecca USA), 중국(코스메카차이나)'],
        ['시가총액', '약 8,512억원 (2026.3.31 기준)'],
        ['발행주식수', '10,680,000주'],
    ]
    story.append(make_table(info_data, col_widths=[45*mm, 120*mm]))

    story.append(P("주요 주주 구성", 'h3'))
    sh_data = [
        ['주주', '지분율', '비고'],
        ['박은희 외 3인 (특수관계인)', '38.95%', '경영권 안정적'],
        ['국민연금공단', '11.99%', '장기 기관투자자'],
        ['KB자산운용', '6.11%', ''],
        ['트러스톤자산운용', '6.06%', ''],
        ['외국인 투자자 합계', '16.85%', ''],
    ]
    story.append(make_table(sh_data, col_widths=[60*mm, 35*mm, 70*mm]))
    story.append(P(
        "<b>초보자 해설</b>: 최대주주(경영진 가족)가 약 39%를 보유하여 경영권이 안정적입니다. "
        "국민연금과 같은 대형 기관투자자가 12%를 보유한 것은 전문 투자자들도 이 회사의 성장성을 인정한다는 신호입니다.", 'tip'
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 2. 비전과 경영철학 (PAGE 4)
    # ════════════════════════════════════════
    story.append(P("2. 비전과 경영철학", 'h1'))
    story.append(P("2026년 경영 키워드: '비천도해(飛天渡海)'", 'h2'))
    story.append(P(
        "조임래 회장은 2026년 경영 키워드로 <b>'비천도해(飛天渡海)'</b> -- '하늘을 날고 바다를 건넌다'를 제시했습니다. "
        "기존의 한계를 넘어 기술, 조직, 글로벌 전략 전반의 혁신을 추진하겠다는 강한 의지를 담고 있습니다."
    ))
    story.append(P(
        "<b>핵심 비전</b>: \"Global Best OGM Company\" -- 글로벌 최고의 OGM 기업 도약", 'tip'
    ))

    story.append(P("4대 전략 방향", 'h3'))
    strat_data = [
        ['전략', '내용'],
        ['기술 고도화', 'AI, 바이오, 신소재 기반 고부가가치 제형 기술 개발'],
        ['AX 전환', '연구/생산/품질/마케팅 전 영역에 AI와 데이터 적용'],
        ['스마트팩토리', '디지털 트윈 기반 지능형 제조 체계 구축'],
        ['ESG 경영', '환경 대응, 인재 중심 문화, 투명한 윤리경영'],
    ]
    story.append(make_table(strat_data, col_widths=[40*mm, 125*mm]))

    story.append(P("ESG (환경/사회/지배구조) 성과", 'h2'))
    story.append(P(
        "- ESG 등급: 서스틴베스트(Sustinvest) <b>A등급</b> 획득<br/>"
        "- 정부포상: '2025 지속가능경영 유공' 산업통상자원부 장관표창 수상<br/>"
        "- 업사이클링 원료 기술, 4R 전략(Reduce/Reuse/Replace/Recycle), 태양광 패널 설치"
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 3. 사업모델 분석 (PAGE 5)
    # ════════════════════════════════════════
    story.append(P("3. 사업모델 분석", 'h1'))
    story.append(P("OGM 시스템: 단순 대리 생산이 아닌 '토탈 솔루션'", 'h2'))
    story.append(P(
        "코스메카코리아는 단순히 '남의 화장품을 대신 만들어주는 것'이 아닙니다. "
        "자체 개발한 <b>OGM(Original Global Standard and Good Manufacturing) 시스템</b>을 통해 "
        "트렌드 분석 및 기획 → 원료/제형 R&D → 규제 검토(각국 인허가) → 시제품 제작 및 테스트 → "
        "대량 생산 → 포장 설계 및 완제품 출하까지 <b>원스톱(One-Stop) 서비스</b>를 제공합니다."
    ))
    story.append(P(
        "<b>쉬운 비유</b>: 브랜드사가 '보습력이 좋은 크림을 만들고 싶어요'라고만 말하면, "
        "코스메카코리아가 원료 선정부터 디자인, 생산, 포장까지 처음부터 끝까지 해결해줍니다.", 'tip'
    ))

    story.append(P("제품 포트폴리오", 'h3'))
    story.append(P(
        "- <b>스킨케어</b> (기초화장품) -- 핵심 매출원<br/>"
        "- <b>메이크업</b> (색조화장품)<br/>"
        "- <b>클렌징</b><br/>"
        "- <b>헤어/바디 케어</b><br/>"
        "- 20여 가지 이상의 효능제품, 비건제품"
    ))

    story.append(P("지역별 매출 비중 (2024년 상반기)", 'h2'))
    story.append(chart_img('chart6_region.png', width=120*mm))

    region_data = [
        ['지역', '비중', '설명'],
        ['한국', '51%', 'K-뷰티 인디 브랜드 수주 호조'],
        ['미국', '31%', 'Cosmecca USA 법인 통한 현지 생산'],
        ['중국', '8%', '중국 법인 운영 (변동성 있음)'],
        ['유럽', '7%', 'K-뷰티 유럽 진출 확대'],
        ['기타', '3%', '동남아, 캐나다 등'],
    ]
    story.append(make_table(region_data, col_widths=[30*mm, 25*mm, 110*mm]))

    story.append(P("5대 경쟁우위 (경제적 해자)", 'h3'))
    story.append(P(
        "1. <b>'Made in Korea' 프리미엄</b>: K-뷰티 글로벌 열풍의 핵심 수혜<br/>"
        "2. <b>인디 브랜드 중심 다변화된 고객군</b>: 특정 대형 고객 의존도 낮음<br/>"
        "3. <b>OGM 원스톱 서비스</b>: 기획~생산~포장까지 통합 제공<br/>"
        "4. <b>3국 생산거점</b>: 한국/미국/중국 로컬 생산 가능<br/>"
        "5. <b>R&D 역량 강화</b>: 판교 중앙연구원 신설 (2025년)"
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 4. 재무제표 분석 (PAGE 6)
    # ════════════════════════════════════════
    story.append(P("4. 재무제표 분석 (초보자 가이드)", 'h1'))
    story.append(P(
        "<b>재무제표란?</b> 회사의 '성적표'입니다. 학교에서 국어, 수학, 영어 점수를 보듯, "
        "회사는 매출, 이익, 부채 등의 숫자로 경영 성과를 보여줍니다.", 'tip'
    ))

    story.append(P("핵심 재무 지표 한눈에 보기", 'h2'))
    story.append(chart_img('chart1_revenue_profit.png'))

    fin_data = [
        ['항목', '2021년', '2022년', '2023년', '2024년', '2025년'],
        ['매출액', '3,965억', '3,994억', '4,707억', '5,243억', '6,409억'],
        ['영업이익', '201억', '104억', '492억', '604억', '835억'],
        ['당기순이익', '89억', '27억', '223억', '428억', '454억'],
    ]
    story.append(make_table(fin_data, col_widths=[28*mm] * 6))

    story.append(P("초보자를 위한 용어 해설", 'h2'))

    story.append(P("<b>매출액 (Revenue) -- '얼마나 팔았나?'</b>", 'h3'))
    story.append(P(
        "회사가 물건이나 서비스를 팔아서 벌어들인 <b>총 금액</b>입니다. "
        "코스메카코리아는 2025년에 <b>6,409억원</b>어치의 화장품을 만들어 납품했습니다. "
        "2021년 3,965억원에서 5년간 <b>62% 성장</b>하여 매우 건강한 성장세를 보여줍니다."
    ))

    story.append(P("<b>영업이익 (Operating Profit) -- '본업으로 얼마 남겼나?'</b>", 'h3'))
    story.append(P(
        "매출에서 원재료비, 인건비, 임대료 등 사업 운영에 드는 비용을 뺀 금액입니다. "
        "2025년 영업이익 <b>835억원</b>은 역대 최대입니다. "
        "영업이익은 '본업의 실력'을 보여주는 핵심 지표입니다."
    ))

    story.append(P("<b>당기순이익 (Net Income) -- '최종적으로 얼마 남겼나?'</b>", 'h3'))
    story.append(P(
        "영업이익에서 이자비용, 세금 등 모든 비용을 빼고 <b>최종적으로 남은 순수한 이익</b>입니다. "
        "2025년 순이익 <b>454억원</b>으로, 2022년(27억원) 대비 <b>16.8배</b> 증가했습니다."
    ))

    story.append(chart_img('chart8_net_income.png'))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 5. 수익성 분석 (PAGE 7)
    # ════════════════════════════════════════
    story.append(P("5. 수익성 분석", 'h1'))
    story.append(P(
        "<b>수익성이란?</b> '100원을 팔면 얼마가 남는가?'를 보여줍니다. "
        "아무리 많이 팔아도 남는 게 없으면 좋은 사업이 아닙니다.", 'tip'
    ))

    story.append(chart_img('chart2_profitability.png'))

    prof_data = [
        ['지표', '2021', '2022', '2023', '2024', '2025', '의미'],
        ['영업이익률', '5.1%', '2.6%', '10.4%', '11.5%', '13.0%', '100원당 13원'],
        ['순이익률', '4.3%', '1.5%', '7.2%', '10.2%', '9.0%', '100원당 9원'],
        ['매출총이익률', '18.4%', '16.3%', '22.8%', '23.8%', '24.7%', '원가 후 마진'],
    ]
    story.append(make_table(prof_data, col_widths=[27*mm, 17*mm, 17*mm, 17*mm, 17*mm, 17*mm, 30*mm]))

    story.append(P("수익성 해석", 'h3'))
    story.append(P(
        "<b>2022년이 바닥</b>이었습니다. 코로나 이후 원재료 가격 상승과 물류비 증가로 영업이익률이 2.6%까지 떨어졌습니다. "
        "그러나 <b>2023년부터 극적인 반등</b>을 시작하여, K-뷰티 열풍이 본격화되면서 매출이 늘어나고 원가 관리 효율화로 "
        "영업이익률이 10%대로 올라섰습니다."
    ))
    story.append(P(
        "<b>2025년 영업이익률 13%는 업계 최고 수준</b>입니다. "
        "경쟁사인 코스맥스(약 6~7%), 한국콜마(약 5~6%)와 비교하면 코스메카코리아의 수익성이 월등히 높습니다.", 'tip'
    ))

    story.append(P("ROE & ROA -- '주주의 돈을 얼마나 잘 불려주는가?'", 'h2'))
    story.append(chart_img('chart3_roe_roa.png'))

    roe_data = [
        ['지표', '2021', '2022', '2023', '2024', '2025'],
        ['ROE', '9.2%', '3.0%', '15.1%', '19.5%', '18.0%'],
        ['ROA', '4.5%', '1.5%', '8.2%', '11.3%', '10.1%'],
    ]
    story.append(make_table(roe_data, col_widths=[28*mm] * 6))

    story.append(P(
        "<b>ROE(자기자본이익률)</b>: '주주가 맡긴 돈 100원으로 18원을 벌었다'는 뜻입니다. "
        "일반적으로 ROE 15% 이상이면 '우수', 20% 이상이면 '매우 우수'로 평가합니다. "
        "코스메카코리아의 ROE 18%는 주주의 돈을 매우 효율적으로 활용하고 있다는 증거입니다.", 'tip'
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 6. 성장성 분석 (PAGE 8)
    # ════════════════════════════════════════
    story.append(P("6. 성장성 분석", 'h1'))
    story.append(P(
        "<b>성장성이란?</b> '작년보다 얼마나 더 벌었는가?'를 보여줍니다. "
        "주가는 미래의 성장을 반영하므로, 투자에서 가장 중요한 지표 중 하나입니다.", 'tip'
    ))

    story.append(chart_img('chart5_growth.png'))

    growth_data = [
        ['지표', '2021', '2022', '2023', '2024', '2025'],
        ['매출 성장률', '+16.9%', '+0.7%', '+17.9%', '+11.4%', '+22.2%'],
        ['영업이익 성장률', '+103%', '-48.4%', '+374%', '+22.8%', '+38.4%'],
        ['순이익 성장률', '+240%', '-70.2%', '+740%', '+91.8%', '+6.2%'],
    ]
    story.append(make_table(growth_data, col_widths=[30*mm, 26*mm, 26*mm, 26*mm, 26*mm, 26*mm]))

    story.append(P("성장 스토리 해석", 'h3'))
    story.append(P(
        "코스메카코리아의 성장은 <b>'V자 반등' 후 '가속 성장'</b> 패턴을 보입니다.<br/><br/>"
        "- <b>2021년</b>: 코로나 이후 회복, 매출 성장세 시작<br/>"
        "- <b>2022년</b>: 성장 정체기 (매출 +0.7%, 영업이익 -48%). 원재료비 상승과 중국 봉쇄의 영향<br/>"
        "- <b>2023년</b>: K-뷰티 붐과 함께 폭발적 반등 (영업이익 +374%)<br/>"
        "- <b>2024년</b>: 안정적 성장 궤도 진입 (매출 5,243억원)<br/>"
        "- <b>2025년</b>: 역대 최대 실적 달성 (매출 6,409억원, 영업이익 835억원)"
    ))

    story.append(P("2026년 전망 (증권사 컨센서스)", 'h2'))
    forecast_data = [
        ['항목', '2025년 실적', '2026년 전망', '성장률'],
        ['매출액', '6,409억원', '7,190억원', '+12.2%'],
        ['영업이익', '835억원', '1,016억원', '+21.7%'],
    ]
    story.append(make_table(forecast_data, col_widths=[35*mm, 40*mm, 40*mm, 35*mm]))
    story.append(P(
        "증권사들은 2026년에도 코스메카코리아가 <b>역대 최대 실적을 경신</b>할 것으로 예상합니다. "
        "특히 영업이익 <b>1,000억원 돌파</b>가 기대됩니다!", 'tip'
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 7. 재무 안정성 분석 (PAGE 9)
    # ════════════════════════════════════════
    story.append(P("7. 재무 안정성 분석", 'h1'))
    story.append(P(
        "<b>안정성이란?</b> '이 회사가 망하지 않을까?'를 판단하는 지표입니다. "
        "아무리 잘 벌어도 빚이 너무 많으면 위험합니다.", 'tip'
    ))

    story.append(chart_img('chart4_stability.png'))

    stab_data = [
        ['지표', '2021', '2022', '2023', '2024', '2025', '기준'],
        ['부채비율', '99.4%', '89.7%', '78.7%', '68.4%', '87.9%', '200%↓ 양호'],
        ['자기자본비율', '50.1%', '52.7%', '56.0%', '59.4%', '53.2%', '50%↑ 양호'],
        ['유동비율', '135.7%', '130.6%', '143.1%', '149.8%', '133.1%', '100%↑ 양호'],
        ['이자보상비율', '6.8배', '2.8배', '12.2배', '18.9배', '23.6배', '3배↑ 양호'],
    ]
    story.append(make_table(stab_data, col_widths=[25*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 28*mm]))

    story.append(P("안정성 용어 해설", 'h2'))

    story.append(P("<b>부채비율 -- '빌린 돈이 얼마나 되나?'</b>", 'h3'))
    story.append(P(
        "내 돈(자기자본) 대비 빌린 돈(부채)의 비율입니다. "
        "2025년 87.9%는 '내 돈 100원에 빌린 돈 88원' 수준으로, <b>매우 양호</b>합니다. "
        "일반적으로 200% 이하면 안전하다고 봅니다."
    ))

    story.append(P("<b>이자보상비율 -- '이자를 갚을 능력이 있는가?'</b>", 'h3'))
    story.append(P(
        "영업이익으로 이자를 몇 번이나 갚을 수 있는지를 보여줍니다. "
        "2025년 <b>23.6배</b>는 '이자의 23.6배를 벌고 있다'는 뜻으로, "
        "<b>이자 부담이 거의 없다</b>는 의미입니다."
    ))

    story.append(P("<b>유동비율 -- '당장 갚아야 할 빚을 갚을 수 있는가?'</b>", 'h3'))
    story.append(P(
        "1년 안에 현금화할 수 있는 자산 ÷ 1년 안에 갚아야 할 빚. "
        "133%는 '빚보다 현금화 가능한 자산이 1.33배 더 많다'는 뜻으로, 단기 안정성 양호입니다."
    ))

    story.append(P(
        "<b>초보자 결론</b>: 코스메카코리아는 빚이 적고, 이자를 넉넉하게 갚을 수 있으며, "
        "단기 유동성도 충분합니다. <b>재무적으로 매우 건전한 회사</b>입니다.", 'tip'
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 8. 현금흐름 분석 (NEW)
    # ════════════════════════════════════════
    story.append(P("8. 현금흐름 분석 (초보자 가이드)", 'h1'))
    story.append(P(
        "<b>현금흐름이란?</b> 손익계산서의 이익은 '장부상 이익'이지만, 현금흐름은 '실제로 현금이 얼마나 들어오고 나갔는지'를 보여줍니다. "
        "이익이 나더라도 현금이 부족하면 회사는 위험해질 수 있습니다. 그래서 현금흐름 분석은 기업의 '진짜 건강상태'를 확인하는 핵심 도구입니다.", 'tip'
    ))

    story.append(P("현금흐름의 3가지 종류", 'h2'))
    story.append(P(
        "회사의 현금흐름은 크게 3가지로 나뉩니다:<br/><br/>"
        "1. <b>영업활동현금흐름</b>: 본업(화장품 ODM)으로 벌어들인 현금. 양(+)이 정상<br/>"
        "2. <b>투자활동현금흐름</b>: 공장/설비/R&D센터 등에 투자한 현금. 성장하는 기업은 음(-) 정상<br/>"
        "3. <b>재무활동현금흐름</b>: 빌린 돈, 갚은 돈, 배당금 지급 등"
    ))

    story.append(P(
        "<b>건강한 기업의 현금흐름 패턴</b>: 영업CF(+), 투자CF(-), 재무CF(상황에 따라). "
        "본업으로 현금을 벌어서(+), 미래를 위해 투자하고(-), 필요시 자금을 조달하는 것이 이상적입니다.", 'tip'
    ))

    story.append(P("현금흐름 추이 (2021~2025)", 'h2'))
    story.append(chart_img('chart10_cashflow.png'))

    cf_data = [
        ['항목', '2021', '2022', '2023', '2024', '2025'],
        ['영업활동CF', '79억', '167억', '420억', '695억', '550억'],
        ['투자활동CF', '-85억', '-104억', '-221억', '-526억', '-638억'],
        ['재무활동CF', '-18억', '-103억', '-132억', '20억', '238억'],
    ]
    story.append(make_table(cf_data, col_widths=[28*mm] * 6))

    story.append(P("현금흐름 해석", 'h3'))
    story.append(P(
        "<b>영업활동현금흐름</b>: 2021년 79억원 → 2024년 695억원으로 <b>5년간 약 9배 급증</b>했습니다. "
        "2025년에는 550억원으로 소폭 감소했지만, 이는 매출채권 증가 등 일시적 요인으로 여전히 높은 수준입니다. "
        "본업에서 현금을 충분히 창출하고 있다는 뜻입니다."
    ))
    story.append(P(
        "<b>투자활동현금흐름</b>: 2024~2025년 투자가 대폭 확대(-526억 → -638억)되었습니다. "
        "이는 <b>판교 중앙연구원 신축</b>(2025년 개소)과 <b>생산능력 확장</b>을 위한 적극적 투자입니다. "
        "성장하는 회사가 미래를 위해 투자하는 것이므로, 음(-)이 큰 것 자체는 부정적이지 않습니다."
    ))
    story.append(P(
        "<b>재무활동현금흐름</b>: 2025년 238억원 유입은 대규모 투자를 뒷받침하기 위한 차입금 조달로 추정됩니다. "
        "이자보상비율이 23.6배로 매우 높아 추가 차입에 대한 부담은 크지 않습니다."
    ))

    story.append(PageBreak())

    story.append(P("CAPEX, FCF & 현금보유 추이", 'h2'))
    story.append(chart_img('chart11_fcf_cash.png'))

    fcf_data = [
        ['항목', '2021', '2022', '2023', '2024', '2025'],
        ['CAPEX', '90억', '116억', '186억', '487억', '614억'],
        ['FCF (잉여현금)', '-11억', '51억', '234억', '208억', '-64억'],
        ['기말 현금보유', '301억', '260억', '329억', '538억', '689억'],
    ]
    story.append(make_table(fcf_data, col_widths=[28*mm] * 6))

    story.append(P("<b>FCF(잉여현금흐름)란?</b>", 'h3'))
    story.append(P(
        "FCF = 영업활동현금흐름 - CAPEX(설비투자). 즉, 본업으로 번 현금에서 필수 투자를 빼고 "
        "<b>진짜 자유롭게 쓸 수 있는 현금</b>입니다. 배당, 자사주 매입, 부채 상환 등에 사용할 수 있습니다."
    ))
    story.append(P(
        "<b>2023년 FCF 234억원이 정점</b>이었고, 2025년에는 대규모 CAPEX(614억원) 투입으로 "
        "FCF가 일시적으로 마이너스 전환되었습니다. 이는 판교 R&D센터 건설 등 <b>미래 성장을 위한 투자</b>의 결과이며, "
        "투자가 마무리되면 FCF가 다시 큰 폭으로 회복될 것으로 예상됩니다.", 'tip'
    ))

    story.append(P("<b>현금보유</b>: 기말 현금이 2021년 301억원 → 2025년 689억원으로 <b>꾸준히 증가</b>하고 있어, "
                    "대규모 투자에도 불구하고 현금 여력을 잘 유지하고 있습니다."
    ))

    story.append(P("이익의 질 분석: 영업이익 vs 영업활동현금흐름", 'h2'))
    story.append(chart_img('chart12_earnings_quality.png'))
    story.append(P(
        "<b>'이익의 질'이란?</b> 장부상 이익(영업이익)이 실제 현금 유입(영업CF)과 얼마나 일치하는지를 보여줍니다. "
        "영업CF가 영업이익보다 크면 '이익의 질이 높다'고 평가합니다.<br/><br/>"
        "코스메카코리아는 2022~2024년 영업CF가 영업이익을 크게 초과하여 <b>이익의 질이 매우 높습니다</b>. "
        "장부상 이익이 '허수'가 아니라 실제 현금으로 뒷받침되고 있다는 의미입니다.", 'tip'
    ))

    story.append(P("현금흐름 종합 평가", 'h2'))
    cf_score = [
        ['항목', '평가', '근거'],
        ['영업CF 창출력', '★★★★★', '5년간 9배 성장, 본업 현금 창출력 탁월'],
        ['투자 적극성', '★★★★☆', '판교 R&D + CAPEX 확대, 미래 성장 투자'],
        ['FCF 건전성', '★★★☆☆', 'CAPEX 투자기로 일시적 (-), 투자 완료 후 회복 전망'],
        ['현금보유', '★★★★☆', '689억원, 대규모 투자에도 현금 여력 유지'],
        ['이익의 질', '★★★★★', '영업CF > 영업이익, 실질적 현금 뒷받침'],
    ]
    story.append(make_table(cf_score, col_widths=[30*mm, 28*mm, 102*mm]))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 9. 산업 분석
    # ════════════════════════════════════════
    story.append(P("9. 산업 분석 및 경쟁 환경", 'h1'))
    story.append(P("글로벌 화장품 OEM/ODM 시장", 'h2'))
    story.append(P(
        "- <b>2025년 시장 규모</b>: 약 6,781억 달러 (약 900조원)<br/>"
        "- <b>2032년 전망</b>: 약 1조 469억 달러 (연평균 성장률 6.4%)<br/>"
        "- <b>성장 동력</b>: K-뷰티 글로벌 확산, 인디 뷰티 브랜드 증가, 맞춤형 화장품 수요"
    ))

    story.append(P("한국 화장품 ODM/OEM Top 3 비교", 'h2'))
    story.append(chart_img('chart7_competitors.png'))

    comp_data = [
        ['기업', '2024년 매출', '영업이익률', '특징'],
        ['한국콜마', '2조 4,521억', '~5-6%', '업계 1위, 규모의 경제'],
        ['코스맥스', '2조 1,661억', '~6-7%', '업계 2위, 글로벌 네트워크'],
        ['코스메카코리아', '5,243억', '~13%', '업계 3위, 최고 수익성'],
    ]
    story.append(make_table(comp_data, col_widths=[37*mm, 35*mm, 28*mm, 60*mm]))

    story.append(P("코스메카코리아의 차별화 포인트", 'h3'))
    story.append(P(
        "매출 규모로는 상위 2사의 약 1/4 수준이지만, <b>수익성은 2배 이상</b> 높습니다.<br/><br/>"
        "1. <b>인디 브랜드 집중</b>: 대형 브랜드보다 마진이 높은 중소형 인디 브랜드 위주 수주<br/>"
        "2. <b>고부가가치 제품</b>: 단순 OEM보다 R&D 비중이 높은 ODM/OGM 중심<br/>"
        "3. <b>효율적 운영</b>: 선택과 집중 전략으로 자원 배분 최적화"
    ))
    story.append(P(
        "<b>초보자 핵심</b>: '크기는 작지만 알짜배기'인 회사입니다. "
        "많이 파는 것보다 <b>남기는 것</b>이 중요한데, 코스메카코리아는 업계에서 가장 많이 남기는 회사입니다.", 'tip'
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 10. SWOT 분석
    # ════════════════════════════════════════
    story.append(P("10. SWOT 분석 및 투자 리스크", 'h1'))
    story.append(chart_img_square('chart9_swot.png', width=155*mm))

    story.append(P("주요 투자 리스크", 'h2'))
    risk_data = [
        ['리스크', '심각도', '설명'],
        ['경기 침체', '중', 'K-뷰티 수요 둔화 가능성'],
        ['환율 변동', '중', '원/달러 환율 변동이 실적에 직접 영향'],
        ['경쟁 심화', '중', '대형사의 인디 브랜드 시장 진출'],
        ['지배구조', '낮음', '코스피 이전 실패, 장기적 개선 필요'],
        ['중국 리스크', '낮음', '중국 매출 비중 8%로 제한적 영향'],
    ]
    story.append(make_table(risk_data, col_widths=[35*mm, 25*mm, 100*mm]))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 11. 밸류에이션 및 투자 결론
    # ════════════════════════════════════════
    story.append(P("11. 밸류에이션 및 투자 결론", 'h1'))
    story.append(P("현재 밸류에이션", 'h2'))

    val_data = [
        ['지표', '현재 값', '해석'],
        ['PER (주가수익비율)', '약 15.7~18.7배', '성장주 기준 적정~저평가'],
        ['PBR (주가순자산비율)', '약 2.81배', '성장 프리미엄 반영'],
        ['EPS (주당순이익)', '4,255원', ''],
        ['BPS (주당순자산)', '~20,450원', ''],
        ['배당금', '370원 (수익률 ~0.5%)', '성장 재투자 중심'],
    ]
    story.append(make_table(val_data, col_widths=[45*mm, 45*mm, 70*mm]))

    story.append(P(
        "<b>PER이란?</b> '이 회사의 1년 이익 대비 주가가 몇 배인가?'를 보여줍니다. "
        "PER 18배라면 '이 회사가 지금처럼 벌면 18년 만에 투자금을 회수할 수 있다'는 뜻입니다. "
        "그런데 2026년 예상 실적 기준 Forward PER은 <b>약 13배</b>로, "
        "연간 20% 이상 이익이 성장하는 회사치고 <b>저평가 영역</b>입니다.", 'tip'
    ))

    story.append(P("증권사 투자의견", 'h2'))
    analyst_data = [
        ['증권사', '투자의견', '목표주가', '현재 대비'],
        ['삼성증권', 'BUY', '125,000원', '+56%'],
        ['KB증권', 'BUY', '120,000원', '+50%'],
        ['NH투자증권', 'BUY', '-', '시총 1조원 전망'],
    ]
    story.append(make_table(analyst_data, col_widths=[38*mm, 30*mm, 40*mm, 40*mm]))

    story.append(P("최근 주요 뉴스 (2025~2026년)", 'h2'))
    news_data = [
        ['시기', '뉴스', '영향'],
        ['2025년', '역대 최대 실적: 매출 6,409억(+22%), 영업이익 835억(+38%)', '긍정'],
        ['2025.10', '판교 중앙연구원 개소 (지하5층~지상11층)', '긍정'],
        ['2025.11', '3Q 어닝 서프라이즈: 매출+44% YoY, 주가 14% 급등', '긍정'],
        ['2025', '코스피 이전상장 불발 (지배구조 이슈)', '부정'],
        ['2026.02', '증권사 목표주가 대폭 상향 (삼성 12.5만, KB 12만)', '긍정'],
    ]
    story.append(make_table(news_data, col_widths=[25*mm, 100*mm, 25*mm]))

    story.append(hr())
    story.append(P("종합 투자 결론", 'h2'))

    score_data = [
        ['항목', '평가', '코멘트'],
        ['성장성', '★★★★★', 'K-뷰티 확산 + 인디 브랜드 수주 확대로 고성장 지속'],
        ['수익성', '★★★★★', '업계 최고 수준의 영업이익률 (13%)'],
        ['안정성', '★★★★☆', '건전한 재무구조, 부채 관리 양호'],
        ['밸류에이션', '★★★★☆', 'Forward PER 13배, 성장 대비 저평가'],
        ['경영진', '★★★☆☆', '비전은 우수하나 지배구조 개선 필요'],
    ]
    story.append(make_table(score_data, col_widths=[32*mm, 30*mm, 98*mm]))

    story.append(Spacer(1, 5*mm))
    story.append(P(
        "<b>코스메카코리아는 K-뷰티 글로벌 확산의 핵심 수혜주입니다.</b><br/><br/>"
        "- 5년간 매출 62% 성장, 영업이익률 5% → 13%로 극적 개선<br/>"
        "- 2026년 영업이익 1,000억원 돌파 전망<br/>"
        "- Forward PER 13배로 성장 대비 밸류에이션 매력적<br/>"
        "- 한/미/중 3국 생산거점 + 판교 R&D센터로 장기 성장 기반 구축<br/><br/>"
        "<b>주요 모니터링 포인트</b>: 중국 법인 실적, 환율 변동, 지배구조 개선 여부, K-뷰티 트렌드 지속성", 'tip'
    ))

    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(P(
        "본 보고서는 투자 참고 자료이며, 투자 판단의 최종 책임은 투자자 본인에게 있습니다.<br/>"
        "과거 실적이 미래 수익을 보장하지 않습니다.<br/><br/>"
        "보고서 작성: 2026년 4월 1일 기준 공개 정보 기반", 'disclaimer'
    ))

    # ── 빌드 ──
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF 생성 완료: {pdf_path}")

if __name__ == '__main__':
    build()
