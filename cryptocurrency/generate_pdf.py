"""
가상화폐(비트코인) 투자 적절성 분석 보고서 - PDF 생성
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
C_ACCENT    = HexColor('#F7931A')  # 비트코인 오렌지
C_BLUE      = HexColor('#2563EB')
C_GREEN     = HexColor('#10B981')
C_RED       = HexColor('#EF4444')
C_GRAY      = HexColor('#6B7280')
C_LIGHT_BG  = HexColor('#FFF8F0')
C_WHITE     = HexColor('#FFFFFF')
C_DARK      = HexColor('#2C3E50')

WIDTH, HEIGHT = A4
MARGIN = 2 * cm

# ── 스타일 ──
def make_styles():
    return {
        'title': ParagraphStyle('Title', fontName=FONT, fontSize=24, leading=32,
                                textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=6*mm),
        'subtitle': ParagraphStyle('Subtitle', fontName=FONT, fontSize=12, leading=16,
                                   textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=10*mm),
        'h1': ParagraphStyle('H1', fontName=FONT, fontSize=18, leading=24,
                             textColor=C_PRIMARY, spaceBefore=8*mm, spaceAfter=4*mm),
        'h2': ParagraphStyle('H2', fontName=FONT, fontSize=14, leading=18,
                             textColor=C_ACCENT, spaceBefore=6*mm, spaceAfter=3*mm),
        'h3': ParagraphStyle('H3', fontName=FONT, fontSize=12, leading=16,
                             textColor=C_DARK, spaceBefore=4*mm, spaceAfter=2*mm),
        'body': ParagraphStyle('Body', fontName=FONT, fontSize=10, leading=16,
                               textColor=black, alignment=TA_JUSTIFY, spaceAfter=3*mm),
        'body_small': ParagraphStyle('BodySmall', fontName=FONT, fontSize=9, leading=14,
                                     textColor=C_GRAY, alignment=TA_JUSTIFY, spaceAfter=2*mm),
        'callout': ParagraphStyle('Callout', fontName=FONT, fontSize=10, leading=15,
                                  textColor=C_PRIMARY, alignment=TA_LEFT, spaceAfter=4*mm,
                                  leftIndent=10*mm, borderPadding=3*mm),
        'verdict': ParagraphStyle('Verdict', fontName=FONT, fontSize=11, leading=16,
                                  textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=4*mm),
    }

S = make_styles()


def hr():
    return HRFlowable(width='100%', thickness=0.5, color=HexColor('#E0E0E0'), spaceAfter=4*mm, spaceBefore=2*mm)

def spacer(h=4):
    return Spacer(1, h*mm)

def img(name, w=160):
    path = os.path.join(DIR, name)
    if os.path.exists(path):
        return Image(path, width=w*mm, height=w*mm*0.6)
    return Spacer(1, 5*mm)

def make_table(data, col_widths=None, header=True):
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
        ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), HexColor('#F8FAFC')))

    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf():
    output = os.path.join(DIR, 'cryptocurrency_investment_report.pdf')
    doc = SimpleDocTemplate(output, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)

    story = []

    # ══════════════════════════════════════════
    # 표지
    # ══════════════════════════════════════════
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph('가상화폐(비트코인)', S['title']))
    story.append(Paragraph('투자 적절성 분석 보고서', S['title']))
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width='60%', thickness=2, color=C_ACCENT, spaceAfter=8*mm))
    story.append(Paragraph('2026년 4월 1일', S['subtitle']))
    story.append(Spacer(1, 10*mm))

    cover_data = [
        ['항목', '내용'],
        ['현재 가격', '$68,680 (약 9,500만원)'],
        ['사상 최고가', '$126,198 (2025.10.06)'],
        ['ATH 대비', '-45.6%'],
        ['공포·탐욕 지수', '8/100 (극단적 공포)'],
        ['투자의견', '단기 중립 / 중장기 매수'],
    ]
    story.append(make_table(cover_data, col_widths=[60*mm, 100*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 1. 핵심 요약
    # ══════════════════════════════════════════
    story.append(Paragraph('1. 핵심 요약 (Executive Summary)', S['h1']))
    story.append(hr())

    story.append(Paragraph(
        '비트코인은 2025년 10월 사상 최고가 $126,198을 기록한 후, 약 45% 하락하여 현재 $68,680에 거래되고 있습니다. '
        '2026년 들어 이란 전쟁 발발, 유가 급등(브렌트유 $106/배럴), 거시경제 불확실성으로 인해 '
        '공포·탐욕 지수가 8(극단적 공포)까지 하락했습니다.',
        S['body']))

    verdict_data = [
        ['시간 프레임', '평가', '근거'],
        ['단기 (1~3개월)', '중립', '이란 전쟁, 유가 급등, 추가 하락 가능 ($56K~$60K)'],
        ['중기 (3~6개월)', '조건부 긍정', '2분기 반등 변곡점, 극단적 공포 역사적 반등 확률 78%'],
        ['장기 (6~12개월)', '긍정', 'ETF 구조적 수요, 반감기 사이클, 제도권 편입 가속화'],
    ]
    story.append(make_table(verdict_data, col_widths=[40*mm, 35*mm, 90*mm]))
    story.append(spacer(4))

    story.append(Paragraph(
        '<b>결론: 현재 시점은 일시불 매수보다 분할매수(DCA)가 적절한 구간입니다.</b> '
        '극단적 공포 구간은 역사적으로 좋은 매수 기회였으나, 이란 전쟁이라는 전례 없는 '
        '지정학적 리스크가 존재하므로 신중한 접근이 필요합니다.',
        S['callout']))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 2. 가격 역사 및 현재 국면
    # ══════════════════════════════════════════
    story.append(Paragraph('2. 비트코인 가격 역사 및 현재 국면 분석', S['h1']))
    story.append(hr())

    story.append(Paragraph(
        '비트코인은 2020년 코로나 양적완화 시기 $7,200에서 시작해, 2021년 $69,000, '
        '2022년 FTX 파산으로 $15,500까지 하락, 2024년 ETF 승인과 반감기를 거쳐 '
        '2025년 10월 사상 최고가 $126,198을 기록했습니다. 이번 사이클은 기관 자본의 구조적 유입으로 '
        '과거 80~90% 하락과 달리 약 45% 조정에 그치고 있으나, 이란 전쟁이라는 외생 변수가 '
        '추가 하락 압력을 가하고 있습니다.',
        S['body']))

    story.append(spacer(2))
    story.append(img('chart1_price_history.png', w=165))
    story.append(spacer(4))

    story.append(Paragraph('반감기 사이클 비교', S['h2']))
    story.append(Paragraph(
        '2024년 4월 반감기 이후 약 710일이 경과한 현재, 과거 사이클 대비 상승폭이 현저히 낮습니다 '
        '(+8% vs 과거 +700~9,000%). 기관 자본 유입으로 변동성이 구조적으로 감소한 반면, '
        '거시경제 요인에 대한 의존도가 높아졌습니다.',
        S['body']))
    story.append(img('chart2_halving_cycles.png', w=160))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 3. 주요 이벤트 타임라인
    # ══════════════════════════════════════════
    story.append(Paragraph('3. 2024~2026 주요 이벤트 타임라인', S['h1']))
    story.append(hr())

    story.append(Paragraph('2024년: 제도권 편입의 원년', S['h2']))
    events_2024 = [
        ['날짜', '이벤트', '영향'],
        ['2024.01', '미국 현물 비트코인 ETF 승인', '블랙록 IBIT 등 출시, 역사적 전환점'],
        ['2024.04', '4차 비트코인 반감기', '보상 3.125 BTC, 인플레이션 <1%'],
        ['2024.11', '트럼프 대통령 당선', '친가상화폐 정책 기대'],
    ]
    story.append(make_table(events_2024, col_widths=[30*mm, 55*mm, 80*mm]))
    story.append(spacer(4))

    story.append(Paragraph('2025년: 정점과 정책 전환', S['h2']))
    events_2025 = [
        ['날짜', '이벤트', '영향'],
        ['2025.01', 'BTC $100,000 돌파', '심리적 대관문 통과'],
        ['2025.07', 'GENIUS Act 서명', '스테이블코인 비증권 분류'],
        ['2025 중반', '전략적 비트코인 비축 시작', '국가 안보 자산 규정'],
        ['2025.10', 'ATH $126,198', '반감기+ETF+정책 수혜 정점'],
    ]
    story.append(make_table(events_2025, col_widths=[30*mm, 55*mm, 80*mm]))
    story.append(spacer(4))

    story.append(Paragraph('2026년: 조정과 불확실성', S['h2']))
    events_2026 = [
        ['날짜', '이벤트', '영향'],
        ['2026.02~03', '미국-이란 전쟁 발발', '유가 60% 급등, 리스크 오프'],
        ['2026.03', 'SEC/CFTC 공동 규칙', '16개 자산 디지털 상품 분류'],
        ['2026.03', 'OCC 디지털자산 은행 인가', 'BitGo, Circle 등 5개사'],
        ['2026.04', 'BTC $68,680', '극단적 공포(8), 바닥 탐색'],
    ]
    story.append(make_table(events_2026, col_widths=[30*mm, 55*mm, 80*mm]))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 4. 거시경제 환경
    # ══════════════════════════════════════════
    story.append(Paragraph('4. 거시경제 환경 분석', S['h1']))
    story.append(hr())

    story.append(Paragraph('이란 전쟁의 영향', S['h2']))
    story.append(Paragraph(
        '2026년 가상화폐 시장의 최대 변수는 미국-이란 전쟁입니다. 브렌트유가 $106/배럴까지 급등하고, '
        'IEA는 호르무즈 해협 상황을 "역사상 최대 공급 차질"로 경고했습니다. WEF는 1970년대 석유 위기와 '
        '유사한 스태그플레이션 위험을 지적하며, 이는 모든 위험자산에 부정적입니다. '
        '유가 상승은 채굴 비용 증가, 인플레이션 재점화, Fed 금리 인하 지연을 초래하여 '
        '비트코인에 삼중 악재로 작용합니다.',
        S['body']))

    macro_data = [
        ['항목', '현황', '가상화폐 영향'],
        ['유가', '브렌트유 $106 (+60%)', '채굴비 증가, 인플레이션'],
        ['호르무즈 해협', 'IEA "역사상 최대 차질" 경고', '글로벌 경기침체 리스크'],
        ['인플레이션', '유가발 재점화 우려', 'Fed 금리 인하 지연/재인상'],
        ['달러', '안전자산 수요로 강세', '위험자산 전반 압박'],
    ]
    story.append(make_table(macro_data, col_widths=[35*mm, 55*mm, 75*mm]))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 5. 온체인 지표 & 시장 심리
    # ══════════════════════════════════════════
    story.append(Paragraph('5. 온체인 지표 및 시장 심리 분석', S['h1']))
    story.append(hr())

    story.append(Paragraph('공포·탐욕 지수와 가격의 관계', S['h2']))
    story.append(Paragraph(
        '현재 공포·탐욕 지수 8은 극도의 공포 상태입니다. 역사적으로 지수가 10 이하일 때 매수하면 '
        '14일 후 수익이 플러스인 확률이 78%, 중앙값 수익률 +12.4%를 기록했습니다. '
        '이는 "남들이 두려워할 때 탐욕스러워져라"는 원칙이 데이터로 뒷받침되는 구간입니다.',
        S['body']))
    story.append(img('chart3_fear_greed.png', w=160))
    story.append(spacer(4))

    story.append(Paragraph('온체인 핵심 지표', S['h2']))
    onchain_data = [
        ['지표', '현황', '해석'],
        ['거래소 보유량', '230만 BTC 이하 (2018년 이후 최저)', '매도 압력 감소'],
        ['장기보유자 비율', '총 공급의 78%+', '강한 홀딩 의지'],
        ['24h 거래소 유출', '8,400 BTC (3주 최대)', '기관/고래 축적'],
        ['거래량', '$1,185억 (30일 +23%)', '바닥권 거래 활발'],
        ['BTC 도미넌스', '56.3%', 'BTC 선호 지속'],
    ]
    story.append(make_table(onchain_data, col_widths=[40*mm, 55*mm, 70*mm]))
    story.append(spacer(4))
    story.append(img('chart9_onchain.png', w=165))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # ETF 자금 흐름
    # ══════════════════════════════════════════
    story.append(Paragraph('ETF 자금 흐름', S['h2']))
    story.append(Paragraph(
        '2025년 비트코인 ETF에 $230억이 순유입되었으며, 2026년에는 보수적으로 $150억, '
        '낙관적으로 $400억 유입이 전망됩니다. ETF 보유 BTC가 130만 개(총 공급의 6%+)에 달하며, '
        'ETF가 연간 순발행량의 100% 이상을 흡수할 것으로 예상되어 장기적으로 강력한 가격 지지 요인입니다.',
        S['body']))
    story.append(img('chart4_etf_flows.png', w=160))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 6. 상승 시나리오
    # ══════════════════════════════════════════
    story.append(Paragraph('6. 상승 시나리오 (Bull Case)', S['h1']))
    story.append(hr())
    story.append(Paragraph('목표: 2026년 말 $100,000~$150,000+', S['h2']))

    story.append(Paragraph('<b>1. 극단적 공포 = 역사적 매수 기회</b>', S['body']))
    story.append(Paragraph(
        '공포 지수 10 이하에서 78% 확률로 2주 내 반등. 현재 ATH 대비 45% 할인 수준.',
        S['body_small']))

    story.append(Paragraph('<b>2. 구조적 수요 > 공급</b>', S['body']))
    story.append(Paragraph(
        '반감기 이후 인플레이션율 1% 미만, ETF가 신규 발행량의 100%+ 흡수, 거래소 보유량 역사적 저점.',
        S['body_small']))

    story.append(Paragraph('<b>3. 제도권 편입 가속화</b>', S['body']))
    story.append(Paragraph(
        'OCC 5개 은행 인가, SEC/CFTC 디지털 상품 분류, 모건스탠리·웰스파고·메릴린치 배분 확대.',
        S['body_small']))

    story.append(Paragraph('<b>4. 미국 전략적 비축자산</b>', S['body']))
    story.append(Paragraph(
        '비트코인의 디지털 금 지위 공식화, 타국 연쇄 채택 가능성.',
        S['body_small']))

    bull_data = [
        ['애널리스트', '2026년 말 목표가'],
        ['비트마이닝 수석 이코노미스트', '$225,000'],
        ['일부 전문가 (낙관)', '$150,000~$200,000'],
        ['스탠다드차타드 (하향 조정)', '$100,000'],
    ]
    story.append(make_table(bull_data, col_widths=[80*mm, 85*mm]))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 7. 하락 시나리오
    # ══════════════════════════════════════════
    story.append(Paragraph('7. 하락 시나리오 (Bear Case)', S['h1']))
    story.append(hr())
    story.append(Paragraph('위험: $56,000~$60,000 또는 그 이하', S['h2']))

    story.append(Paragraph('<b>1. 지정학적 리스크 심화</b>', S['body']))
    story.append(Paragraph(
        '호르무즈 해협 봉쇄 시 유가 $120~$130 전망. 글로벌 경기침체로 위험자산 동반 하락.',
        S['body_small']))

    story.append(Paragraph('<b>2. 매크로 역풍</b>', S['body']))
    story.append(Paragraph(
        '유가발 인플레이션으로 Fed 금리 인하 불가 또는 재인상. 달러 강세 지속.',
        S['body_small']))

    story.append(Paragraph('<b>3. 기관 행동 변화</b>', S['body']))
    story.append(Paragraph(
        'ETF 유입 둔화, 기업 재무 비트코인 매각 시 구조적 충격. 리테일 부재로 유동성 공백.',
        S['body_small']))

    bear_data = [
        ['시나리오', '바닥 전망'],
        ['기본 시나리오', '$60,000~$68,000'],
        ['악화 시나리오 (Q3 2026)', '$56,000~$60,000'],
        ['극단 시나리오 (레버리지 청산)', '일시적 $50,000 이하'],
    ]
    story.append(make_table(bear_data, col_widths=[80*mm, 85*mm]))
    story.append(spacer(4))
    story.append(img('chart5_scenarios.png', w=160))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 8. 리스크 분석
    # ══════════════════════════════════════════
    story.append(Paragraph('8. 리스크 요인 분석', S['h1']))
    story.append(hr())

    risk_data = [
        ['리스크', '발생 확률', '영향도', '설명'],
        ['이란 전쟁 확대', '높음', '매우 높음', '호르무즈 해협 봉쇄 시 글로벌 충격'],
        ['스태그플레이션', '중간', '높음', '1970년대형 경기침체+인플레이션'],
        ['ETF 순유출', '낮음~중간', '높음', '기관 수요 기반 붕괴'],
        ['레버리지 위기', '중간', '높음', '숨겨진 레버리지 청산'],
        ['규제 역풍', '낮음', '중간', '전쟁 시 자본통제 가능'],
        ['양자컴퓨터', '매우 낮음', '낮음', '심리적 공포 요인'],
    ]
    story.append(make_table(risk_data, col_widths=[35*mm, 25*mm, 25*mm, 80*mm]))
    story.append(spacer(4))
    story.append(img('chart6_risk_matrix.png', w=140))

    story.append(Paragraph('리스크 vs 기회 비율', S['h2']))
    rr_data = [
        ['방향', '목표가', '변동폭'],
        ['하방 리스크', '$56,000', '-18%'],
        ['기본 목표', '$100,000', '+46%'],
        ['ATH 회복', '$126,000', '+84%'],
        ['리스크/리워드', '', '1:2.5 ~ 1:4.7'],
    ]
    story.append(make_table(rr_data, col_widths=[55*mm, 55*mm, 55*mm]))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 9. 투자 결론 및 전략
    # ══════════════════════════════════════════
    story.append(Paragraph('9. 투자 결론 및 전략 제안', S['h1']))
    story.append(hr())

    story.append(Paragraph('종합 평가', S['h2']))
    story.append(img('chart10_radar.png', w=130))
    story.append(spacer(2))

    eval_data = [
        ['평가 항목', '점수', '설명'],
        ['장기 펀더멘털', '8/10', 'ETF 수요, 반감기, 제도화'],
        ['단기 모멘텀', '3/10', '이란 전쟁, 유가, 거시경제 역풍'],
        ['밸류에이션', '7/10', 'ATH 대비 45% 할인, 극단적 공포'],
        ['리스크/리워드', '7/10', '하방 대비 상방 비율 양호'],
        ['시장 심리 (역발상)', '8/10', '극단적 공포 = 역사적 매수 기회'],
        ['제도화 수준', '9/10', 'ETF, 전략비축, 디지털상품 분류'],
        ['종합', '7.0/10', '중립~조건부 긍정'],
    ]
    story.append(make_table(eval_data, col_widths=[45*mm, 25*mm, 95*mm]))

    story.append(PageBreak())

    # ── 투자 전략 ──
    story.append(Paragraph('투자 성향별 전략', S['h2']))

    story.append(Paragraph('<b>A. 보수적 투자자 (리스크 회피형)</b>', S['body']))
    story.append(Paragraph(
        '현재 진입 보류. 이란 전쟁 추이 관망 후 유가 안정화 확인 시 진입. '
        '진입 시 전체 투자금의 20~30%만 가상화폐에 배분.',
        S['body_small']))

    story.append(Paragraph('<b>B. 균형형 투자자 (권장)</b>', S['body']))
    story.append(Paragraph(
        '분할매수(DCA) 전략. 6개월간 매월 동일 금액 투자. '
        '$60,000 이하 추가 하락 시 비중 확대. 포트폴리오의 5~10% 이내.',
        S['body_small']))

    story.append(Paragraph('<b>C. 적극적 투자자 (수익 추구형)</b>', S['body']))
    story.append(Paragraph(
        '현재 가격대($65K~$70K) 30% 진입, $60K 이하 30% 추가, '
        '$56K 이하 40% 추가. 손절선: $48,000 (-30%).',
        S['body_small']))
    story.append(spacer(4))

    story.append(img('chart7_allocation.png', w=165))
    story.append(spacer(4))
    story.append(img('chart8_dca_simulation.png', w=165))

    story.append(PageBreak())

    # ── 공통 원칙 ──
    story.append(Paragraph('공통 투자 원칙', S['h2']))
    principles = [
        '전체 자산의 5~15% 이내로 가상화폐 배분 (고위험 자산)',
        '6개월 이상의 투자 기간 확보 (단기 변동성 감내)',
        '여유자금으로만 투자 (생활비, 비상금 제외)',
        '레버리지 절대 금지 (현재 환경에서 파산 위험)',
        '비트코인 중심 배분 (알트코인은 하락장에서 더 큰 폭 하락)',
    ]
    for i, p in enumerate(principles, 1):
        story.append(Paragraph(f'{i}. {p}', S['body']))

    story.append(spacer(4))

    story.append(Paragraph('모니터링 지표', S['h2']))
    monitor_data = [
        ['지표', '확인 방법', '주의 신호'],
        ['이란 전쟁', '주요 뉴스', '호르무즈 봉쇄, 전쟁 확대'],
        ['유가', '브렌트유 선물', '$120 이상 지속'],
        ['Fed 금리', 'FOMC 회의', '재인상 시사'],
        ['ETF 유출', 'SoSoValue.com', '3일 연속 대규모 유출'],
        ['공포·탐욕', 'alternative.me', '50+ 시 차익실현 고려'],
        ['거래소 보유량', 'CryptoQuant', '급격한 유입 (매도 신호)'],
    ]
    story.append(make_table(monitor_data, col_widths=[35*mm, 50*mm, 80*mm]))

    story.append(spacer(10))
    story.append(HRFlowable(width='100%', thickness=1, color=C_ACCENT))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>면책조항</b>: 본 보고서는 정보 제공 목적으로 작성되었으며, 투자 권유나 투자 자문이 아닙니다. '
        '가상화폐 투자는 원금 손실의 위험이 있으며, 모든 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다. '
        '과거의 수익률이 미래의 수익률을 보장하지 않습니다.',
        S['body_small']))

    doc.build(story)
    print(f'\nPDF 생성 완료: {output}')


if __name__ == '__main__':
    build_pdf()
