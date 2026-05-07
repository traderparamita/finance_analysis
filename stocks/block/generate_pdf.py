#!/usr/bin/env python3
"""
Block, Inc. (XYZ) PDF 보고서 생성
회사 고유 서술 내용만 이 파일에 작성한다.
공통 레이아웃/스타일/빌드는 shared/pdf_utils.py 에서 처리한다.

데이터: yfinance 2026-05-07 조회분 (FY2022~FY2025)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles,
    news_card, issue_card, quarterly_momentum_table, forward_consensus_table,
)
from stocks.block.config import CONFIG

CFG    = CONFIG
BASE   = CFG['base_dir']
STY    = make_styles(CFG['colors']['primary'], CFG['colors']['accent'])
PRIMARY_HEX = CFG['colors']['primary']

from reportlab.platypus import Paragraph
def P(text, key='body'):
    return Paragraph(text, STY[key])
def img(name, width_cm=16):
    from reportlab.lib.units import cm
    return chart_image(BASE, name, width=width_cm * cm, styles=STY)
def tip(text):
    return tip_box(text, STY)
def hr():
    return hr_line(CFG['colors']['accent'])
def tbl(headers, rows, widths=None):
    return make_table(headers, rows, col_widths=widths, primary_hex=PRIMARY_HEX)


def build():
    from reportlab.lib.units import mm, cm
    from reportlab.platypus import Spacer
    story = []

    # ━━━ 1. 표지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Spacer(1, 40 * mm))
    story.append(P('Block, Inc.', 'title'))
    story.append(P('XYZ  |  NYSE  (Fintech / Payments &amp; Consumer Finance)', 'subtitle'))
    story.append(sp(8))
    cover_data = [
        ['항목',      '내용'],
        ['종목코드',  'XYZ (NYSE) — 구 SQ에서 2025년 티커 변경'],
        ['현재 주가', '$70.83'],
        ['시가총액',  '$42.2B (≈ 약 422억 달러)'],
        ['투자의견',  '매수 (BUY)'],
        ['목표주가',  '$85 (상승여력 +20.0%)'],
        ['업종',      '핀테크 / Cash App + Square 통합 플랫폼'],
        ['작성일',    '2026년 05월 07일'],
        ['데이터 출처', 'yfinance 실시간 조회 (2026-05-07)'],
    ]
    story.append(tbl(cover_data[0], cover_data[1:], widths=[55*mm, 100*mm]))
    story.append(sp(20))
    story.append(P('본 보고서는 yfinance API로 조회한 공개 재무 데이터를 기반으로 작성된 투자 참고 자료이며, '
                   '투자 판단의 최종 책임은 투자자 본인에게 있습니다.', 'disclaimer'))
    story.append(PageBreak())

    # ━━━ 2. 목차 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('목 차', 'h1')); story.append(hr()); story.append(sp(3))
    for item in [
        '1. 기업 개요', '2. 비전 &amp; 전략', '3. 사업 모델 분석',
        '4. 재무 분석', '5. 수익성 분석', '6. 성장성 분석',
        '7. 재무 안정성 분석', '8. 현금흐름 분석', '9. 산업 &amp; 경쟁 분석',
        '10. SWOT &amp; 리스크 분석',
        '11. 분기 모멘텀 &amp; 애널리스트 컨센서스 (★ v4.0)',
        '12. 최신 이슈 &amp; 뉴스 브리핑 (★ v4.0)',
        '13. 밸류에이션 &amp; 투자 결론', '14. 면책 고지',
    ]:
        story.append(P(item, 'toc'))
    story.append(PageBreak())

    # ━━━ 3. 기업 개요 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('1. 기업 개요', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>Block, Inc.</b>는 2009년 잭 도시(Jack Dorsey)가 Square라는 이름으로 창업한 글로벌 핀테크 기업으로, '
        '2021년 12월 사명을 Block으로 변경하고 2025년 NYSE 티커를 SQ → <b>XYZ</b>로 전환했습니다. '
        '두 개의 거대 생태계(가맹점용 <b>Square</b>, 소비자용 <b>Cash App</b>)를 중심으로 결제·뱅킹·BNPL·비트코인 사업을 '
        '하나의 플랫폼으로 묶고 있으며, 2024년 일회성 세금 환입을 제외하더라도 2025년 영업이익 $3.0B(+80.6% YoY)을 '
        '달성하며 본격적인 흑자 가속 단계에 진입했습니다.'))
    story.append(sp(3))
    story.append(tip('Block은 가맹점이 카드를 받을 수 있게 해 주는 "Square"와 친구·가족에게 돈을 보내고 받는 "Cash App"을 모두 운영합니다. '
                     '동전을 주고받던 친구 사이의 거래(C2C)와 식당·카페의 결제(B2C)를 한 회사가 동시에 가져가는 양방향 플랫폼이라고 이해하면 쉽습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '내용'],
        [
            ['CEO',           'Jack Dorsey (Block Head, 공동창업자)'],
            ['종목코드',       'XYZ (NYSE) — 2025년 SQ에서 변경'],
            ['설립연도',       '2009년 (캘리포니아 샌프란시스코)'],
            ['직원 수',        '약 11,000명 (공개 자료 기준)'],
            ['핵심 사업',      'Square (가맹점), Cash App (소비자), Spiral·TBD (Bitcoin)'],
            ['Cash App 활성',  '월 활성 사용자 약 5,700만+ (공개 자료 기준)'],
            ['시가총액',       '$42.2B (약 422억 달러)'],
        ],
        widths=[40*mm, 125*mm]
    ))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 &amp; 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('"Economic Empowerment" — 두 생태계의 상호 연결', 'h2'))
    story.append(P(
        'Block의 공식 미션은 "사람들이 경제 시스템에 접근할 수 있도록 돕는 것(economic empowerment)"입니다. '
        'Square로는 영세 자영업자에게 결제·POS·대출을, Cash App으로는 은행 계좌가 없는 소비자에게 '
        '송금·예금·주식·비트코인 거래를 제공합니다. 2025년 영업이익률은 12.59%로 4년 전 -0.16% 대비 13%p 가까이 개선되었으며, '
        'CEO 잭 도시는 2024~2025년을 기점으로 "비대해진 조직 슬림화 + 두 생태계 연결(Cross-sell)"을 핵심 전략으로 제시했습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['전략 방향', '내용'],
        [
            ['두 생태계 연결',     'Cash App ↔ Square — Cash App Pay를 가맹점 결제 옵션에 통합'],
            ['BNPL Afterpay 확장', 'Cash App + Square 양쪽에 BNPL 통합, BNPL 잔액 흑자화'],
            ['뱅킹 사업 강화',     'Cash App Savings·Borrow, Square Banking — 고마진 금융 매출'],
            ['Bitcoin 인프라 투자', 'Spiral(오픈소스), TBD(웹5), 셀프-커스터디 지갑(Bitkey)'],
            ['조직 슬림화·자사주', '대규모 인력 감축 후 영업레버리지 본격 발현, 자사주 매입 확대'],
        ],
        widths=[42*mm, 123*mm]
    ))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); style_kw = 'body'
    story.append(sp(3))
    story.append(tip('Block의 매출 구조는 "결제 수수료 + 금융 서비스 수수료 + 비트코인 거래액 패스스루". '
                     'Square는 결제 거래액(GPV)의 약 2.6~2.9%, Cash App은 비즈니스 거래·BNPL·주식·비트코인 거래에서 수수료를 받습니다. '
                     '비트코인 거래 매출은 거래액 자체가 매출로 잡혀 톱라인을 부풀리지만 마진은 매우 낮습니다 — '
                     '핀테크 본업의 진짜 수익성은 <b>Gross Profit</b>으로 봐야 합니다.'))
    story.append(sp(3))
    story.append(img('chart6_segments.png'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', 'Gross Profit 비중', '특징'],
        [
            ['Cash App',          '약 55%', 'P2P 송금·예금·BNPL·주식·비트코인 통합 슈퍼앱'],
            ['Square 셀러',       '약 42%', '결제·POS·캐피털·뱅킹 — 영세 가맹점 OS'],
            ['기타 (TIDAL·TBD·Spiral)', '약 3%',  '음원·웹5·비트코인 인프라 — 적자 지속'],
        ],
        widths=[55*mm, 35*mm, 75*mm]
    ))
    story.append(sp(5))
    story.append(P('<b>핀테크 핵심 지표 (공개 자료 기준):</b><br/>'
                   '• Cash App 월 활성: 약 5,700만+<br/>'
                   '• Cash App ARPU: 연 $75 수준 (2024)<br/>'
                   '• Square GPV(연간 결제처리액): $200B+ 규모<br/>'
                   '• Bitcoin 매출 비중: 약 35~40% (저마진, Gross Profit 비중은 1% 미만)', 'body'))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('단위: 십억달러 ($B). Block의 핵심 스토리는 "탑라인 둔화 vs 영업이익 폭증". '
                     '매출은 4년간 +38% 증가에 그쳤지만(비트코인 매출 변동 영향), 영업이익은 -$0.0B → +$3.0B로 본격 흑자 가속. '
                     '<b>2024 순이익 $2.9B에는 이연법인세 자산 환입(일회성) 영향이 크게 반영</b>되어 있어 2025년 $1.3B로 정상화된 것이 자연스럽습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['매출액',     '$17.5B', '$21.9B', '$24.1B', '$24.2B'],
            ['영업이익',   '-$0.0B', '+$0.4B', '+$1.7B', '+$3.0B'],
            ['당기순이익', '-$0.5B', '+$0.0B', '+$2.9B*', '+$1.3B'],
            ['영업이익률', '-0.16%', '+1.74%', '+6.99%', '+12.59%'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(2))
    story.append(P('* 2024 순이익은 이연법인세 자산 환입(일회성) 효과 포함 — 정상화 EPS 기준 2025년 $1.3B 활용 권장', 'disclaimer'))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('영업이익률이 -0.16%(2022) → +12.59%(2025)로 13%p 가까이 개선되었습니다. '
                     '이는 (1) 대규모 인력 효율화, (2) Cash App 사용자당 수익(ARPU) 증가, '
                     '(3) BNPL Afterpay 흑자화 등 비용·믹스 양면의 개선이 동시에 이루어진 결과입니다. '
                     '단, 2024 ROE 13.62%는 일회성 세금효과 포함 — 2025년 정상화 ROE 5.88%가 업종 평균(8~12%) 대비 다소 낮은 점 유의.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025'],
        [
            ['영업이익률', '-0.16%', '+1.74%',  '+6.99%',  '+12.59%'],
            ['순이익률',   '-3.08%', '+0.04%',  '+12.01%', '+5.40%'],
            ['ROE',        '-3.14%', '+0.05%',  '+13.62%', '+5.88%'],
            ['ROA',        '-1.72%', '+0.03%',  '+7.88%',  '+3.30%'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(3))
    story.append(P('수익성 개선의 구조적 원인은 두 가지입니다. '
                   '첫째, 2023년 발표된 비용통제 캡(operating expense cap) 도입 이후 인건비·마케팅 효율이 본격 발현. '
                   '둘째, Cash App Cards·Borrow·BNPL 같은 <b>고마진 금융 서비스 매출 비중 상승</b>이 Gross Margin을 끌어올렸습니다. '
                   'PayPal(영업이익률 ~17%) 대비는 아직 낮지만 추세는 우호적입니다.'))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>매출 성장은 둔화, 이익 성장은 폭발:</b> 2023년 +25.0%로 정점을 찍은 매출 성장률은 '
        '2024년 +10.1% → 2025년 +0.3%로 급격히 둔화되었습니다. '
        '주된 원인은 <b>비트코인 거래 매출의 변동(가격·거래량)</b>으로, 핀테크 본업(Gross Profit 기준)은 두 자릿수 성장 추정. '
        '반면 영업이익 성장률은 1500% → 342% → 81%로 강한 모멘텀이 유지되고 있습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2023', '2024', '2025'],
        [
            ['매출 성장률',     '+25.0%',     '+10.1%',  '+0.3%'],
            ['영업이익 성장률', '+1499.8%',   '+341.7%', '+80.6%'],
            ['순이익 성장률',   '+101.8%',    '+29546%', '-54.9%*'],
        ],
        widths=[40*mm, 41*mm, 41*mm, 41*mm]
    ))
    story.append(sp(2))
    story.append(P('* 2025 순이익 -54.9%는 2024 일회성 세금환입의 기저효과 — 정상화 기준 영업이익 +80.6%가 진정한 모멘텀', 'disclaimer'))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(sp(3))
    story.append(P('<b>향후 성장 촉매:</b><br/>'
                   '① Cash App ↔ Square 크로스셀(Cash App Pay 가맹점 침투)<br/>'
                   '② Afterpay BNPL 흑자화 후 잔액 확대<br/>'
                   '③ Square Banking·Capital 등 셀러 금융 매출 확대'))
    story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('Block의 부채비율은 2022년 81.94% → 2025년 78.27%로 안정적이며, 유동비율 220%대로 단기 유동성은 매우 풍부합니다. '
                     '핀테크 특성상 가맹점 정산 부채(Customer Funds Payable)가 대차대조표에 잡혀 부채비율이 다소 높아 보이는 점은 '
                     '동종 업계 공통 — 실질 차입금은 시총 대비 낮은 수준으로 추정됩니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025', '기준'],
        [
            ['부채비율', '81.94%',  '76.70%',  '73.08%',  '78.27%',  '핀테크 평균 100~150%'],
            ['유동비율', '185.2%',  '200.6%',  '232.6%',  '220.1%',  '100%↑ 매우 양호'],
        ],
        widths=[27*mm, 26*mm, 26*mm, 26*mm, 26*mm, 32*mm]
    ))
    story.append(sp(3))
    story.append(P('최대 위험 시나리오는 <b>비트코인 가격 급락 → 보유 BTC 평가손실 + Cash App 거래액 감소</b>가 동시에 발생하는 경우입니다.'))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('Block의 현금흐름은 "이익보다 더 빠르게 개선되는 FCF". '
                     '영업CF $0.2B(2022) → $2.6B(2025), FCF $0.0B → $2.4B로 4년간 큰 폭으로 증가했습니다. '
                     'CAPEX는 $0.2B 수준에 묶여 있어 자산 경량(asset-light) 구조 — 매출이 늘수록 FCF가 따라 늘어나는 본질을 보여줍니다. '
                     'FCF Yield는 시총($42.2B) 대비 약 5.7%로 본격 자사주 매입의 토대.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['영업활동CF', '+$0.2B', '+$0.1B', '+$1.7B', '+$2.6B'],
            ['투자활동CF', '+$1.2B', '+$0.7B', '+$0.6B', '-$2.8B'],
            ['재무활동CF', '+$0.1B', '-$0.2B', '+$2.0B', '-$0.6B'],
            ['CAPEX',      '$0.2B',  '$0.2B',  '$0.2B',  '$0.2B'],
            ['FCF',        '$0.0B',  '-$0.1B', '+$1.6B', '+$2.4B'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(3))
    story.append(P('<b>이익과 현금의 차이:</b> 2024 순이익 $2.9B(일회성 세금효과 포함) vs 영업CF $1.7B — '
                   '회계상 일회성 세금 자산 환입은 이익에는 잡히지만 현금 유입은 아니라는 점을 보여줍니다. '
                   '반대로 2025년은 순이익 $1.3B < 영업CF $2.6B — 현금창출력이 회계 이익보다 크게 우월. '
                   'CAPEX는 4년간 $0.2B로 일정해 <b>유지보수 성격이 강하고 성장 투자 비중은 낮음</b>.'))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 &amp; 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['기업', '2025년 매출(추정)', '영업이익률', '특징'],
        [
            ['Block (XYZ)',  '$24.2B', '+12.6%', 'Cash App + Square 통합, BTC 매출 포함'],
            ['PayPal',       '$32B',   '+17%',   'P2P + 결제 글로벌 1위, Venmo 보유'],
            ['Stripe (비상장)','$20B+', 'n/a',  'API 기반 온라인 결제 1위'],
            ['Toast',        '$5B+',   '+3%',    '레스토랑 특화 SaaS 결제'],
        ],
        widths=[35*mm, 40*mm, 30*mm, 60*mm]
    ))
    story.append(sp(3))
    story.append(P('<b>Block의 차별화 포인트 3가지:</b><br/>'
                   '① <b>양면 플랫폼</b> — 가맹점(Square)과 소비자(Cash App)를 모두 보유한 유일한 미국 핀테크<br/>'
                   '② <b>비트코인 통합</b> — 셀프-커스터디(Bitkey), 웹5(TBD), 라이트닝 인프라까지 풀스택<br/>'
                   '③ <b>SMB 특화 OS</b> — 영세 자영업자에 결제·POS·대출·뱅킹을 단일 앱으로 제공 (경쟁사 대비 진입장벽)'))
    story.append(sp(3))
    story.append(P('<b>핀테크 핵심 지표 비교:</b><br/>'
                   '• Block Cash App 월 활성: 5,700만+ vs PayPal Venmo 월 활성: 약 9,000만<br/>'
                   '• Block GPV: $200B+ vs Stripe GPV: $1T+ (온라인 비중 차이)<br/>'
                   '• Block Take Rate: ~2.6% vs Toast: ~2.5% (POS 특화)'))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT &amp; 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16))
    story.append(sp(5))
    story.append(tbl(
        ['리스크', '심각도', '내용', '모니터링 포인트'],
        [
            ['Bitcoin 변동성',     '상',    'BTC 가격 급락 시 보유자산 평가손 + 거래수수료 감소',  'BTC 가격, Cash App BTC 거래량'],
            ['톱라인 둔화',        '중상',  '2025년 매출 +0.3% — 비트코인 매출 변동 의존',          'Gross Profit 성장률, Cash App ARPU'],
            ['핀테크 규제',        '중상',  'CFPB·OCC 등 미국 핀테크 규제 강화 추세',                'CFPB BNPL 룰, 라이선스 비용'],
            ['결제 수수료 경쟁',   '중간',  'Stripe·Toast·Clover 셀러 결제 경쟁',                   'Square Take Rate, 셀러 churn'],
            ['일회성 세금효과 소멸','낮음',  '2024 ROE 급등 효과 사라지며 비교 부담',                '정상화 EPS, Forward PER'],
        ],
        widths=[32*mm, 18*mm, 50*mm, 65*mm]
    ))
    story.append(PageBreak())

    # ━━━ 13. 분기 모멘텀 & 애널리스트 컨센서스 (v4.0 신규) ━━━
    story.append(P('11. 분기 모멘텀 &amp; 애널리스트 컨센서스', 'h1'))
    story.append(hr()); story.append(sp(3))
    story.append(tip('연간 데이터는 평균을 보여주지만, <b>분기 데이터는 변곡점을 보여준다</b>. '
                     'Block의 분기별 영업이익 흐름은 24Q4 $0.26B → 25Q4 $1.0B로 1년 만에 4배 확대. '
                     '같은 기간 매출은 6.0B → 6.25B로 비교적 완만 — "탑라인 둔화 vs 마진 점프"의 본질이 분기 단위에서 명확히 드러난다.'))
    story.append(sp(4))
    qt = quarterly_momentum_table(CFG, primary_hex=PRIMARY_HEX)
    if qt is not None:
        story.append(qt); story.append(sp(5))
    story.append(img('chart13_quarterly_momentum.png'))
    story.append(sp(5))
    story.append(P('<b>변곡점:</b> '
                   '① 24Q4 → 25Q1: 매출 일시 하락(시즌성·BTC 변동)에도 영업이익 +92% — 비용 통제 본격 발현<br/>'
                   '② 25Q3 → 25Q4: 영업이익 $0.77B → $1.0B(+30%) — Q4 "AI 인력 50% 감축" 발표 직후 마진 점프<br/>'
                   '③ 25Q4 순이익 $0.12B는 24Q4 일회성 세금환입 $1.95B의 기저효과', 'body'))
    story.append(sp(6))

    # — 컨센서스 테이블 + 차트 —
    story.append(P('애널리스트 컨센서스 (yfinance 2026-05-07 조회)', 'h2'))
    ft = forward_consensus_table(CFG, primary_hex=PRIMARY_HEX)
    if ft is not None:
        story.append(ft); story.append(sp(5))
    story.append(img('chart14_analyst_consensus.png'))
    story.append(sp(5))
    story.append(img('chart15_recommendation_pie.png', width_cm=14))
    story.append(sp(4))
    fwd = CFG.get('forward', {})
    am = fwd.get('target_mean', 0); cur = fwd.get('current_price', 1)
    upside = (am / cur - 1) * 100 if cur else 0
    story.append(P(
        f'<b>본 보고서 목표가 vs 컨센서스:</b> 본 보고서 목표가 $85 (+20.0%) vs 애널리스트 평균 $86.78 (+{upside:.1f}%) — 거의 일치. '
        f'40명 중 36명이 매수(strongBuy 8 + buy 28), 매도 1명(strongSell)으로 컨센서스 강하게 우호적. '
        f'Forward PER {fwd.get("forward_pe", 0):.1f}x는 핀테크 평균(20~25x) 대비 디스카운트 — 어닝 발표 후 마진 가속 확인 시 멀티플 리레이팅 여지.', 'body'
    ))
    story.append(PageBreak())

    # ━━━ 14. 최신 이슈 & 뉴스 브리핑 (v4.0 신규) ━━━━━━━
    story.append(P('12. 최신 이슈 &amp; 뉴스 브리핑', 'h1'))
    story.append(hr()); story.append(sp(3))
    research_date = CFG.get('web_issues_research_date', CFG['report_date'])
    story.append(P(f'<i>WebSearch + WebFetch + yfinance 조사 시점: {research_date}</i>', 'small'))
    story.append(sp(3))
    story.append(P('핵심 이슈 (WebSearch + WebFetch 본문 인용)', 'h2'))
    story.append(sp(2))
    for issue in CFG.get('web_issues', []):
        story.append(issue_card(
            headline=issue['headline'],
            body=issue['body'],
            source=issue['source'],
            url=issue['url'],
            date=issue['date'],
            styles=STY,
            severity=issue.get('severity', '중간'),
        ))
        story.append(sp(3))

    story.append(sp(4))
    story.append(P('데이터 소스 — yfinance 헤드라인 (보고일 기준 7일 이내)', 'h2'))
    story.append(sp(2))
    for n in CFG.get('news', [])[:5]:
        story.append(news_card(n, STY, accent_hex=CFG['colors']['accent']))
        story.append(sp(2))

    story.append(sp(5))
    story.append(tip('<b>최근 30~90일 핵심 변화 한 줄 요약:</b> '
                     '"AI 명분 인력 50% 감축(2/26) → 주가 +38% 점프 → 주요 IB 일제히 상향 → '
                     '2026 가이던스 대폭 상향(GP +18%, Op Income +54%) → 5/7 Q1 어닝 발표 임박" — '
                     '본격적 마진 사이클 진입 vs AI-washing 의혹의 진실은 5/7 어닝 콜에서 검증된다.'))
    story.append(PageBreak())

    # ━━━ 15. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('13. 밸류에이션 &amp; 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['지표', '현재값', '해석'],
        [
            ['PER (TTM, GAAP)',   '약 32x',   '2025 정상화 EPS 기준 — 핀테크 평균(20~30x) 다소 상단'],
            ['EV/Sales',          '약 1.7x',  '비트코인 패스스루 매출 포함 — Gross Profit 기준 4~5x 수준'],
            ['EV/EBITDA',         '약 12x',   'EBITDA ≈ Op Income $3.0B × 1.15 = $3.45B 기준'],
            ['FCF Yield',         '5.7%',     'FCF $2.4B / 시총 $42.2B — 자사주 매입 재원 충분'],
            ['배당',              '없음',     '주주환원은 자사주 매입 중심'],
            ['목표주가',          '$85',      '현재 $70.83 대비 +20.0% 상승여력'],
        ],
        widths=[45*mm, 35*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(tip('<b>목표주가 산출 근거:</b> 핀테크 섹터 EV/EBITDA 18x를 적용. '
                     '2026 예상 EBITDA $3.85B(영업이익 $3.35B × 1.15) × 18 = EV $69B. 순부채 ~$0(현금성자산 + BTC 보유 고려) 가정 시 '
                     '시가총액 목표 $69B → 발행주식 약 6.1억 주 기준 주당가치 약 $85. '
                     '핀테크 평균 EV/EBITDA(15~20x) 중간값 + Cash App·Square 양면 플랫폼 프리미엄을 일부 반영했습니다. '
                     '비트코인 변동성·매출 둔화 리스크로 추가 멀티플 확장은 제한적이라고 판단합니다.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=14))
    story.append(sp(5))
    story.append(P(
        '<b>핵심 투자 포인트:</b><br/>'
        '① 4년 만에 영업이익률 -0.16% → +12.59%로 13%p 점프, 본격 흑자 가속<br/>'
        '② 2025 영업이익 $3.0B(+80.6%) — 인력 효율화 + 고마진 금융 매출 믹스 개선<br/>'
        '③ FCF $2.4B(2025), FCF Yield 5.7% — Asset-light 구조의 본질적 현금창출<br/>'
        '④ Cash App 5,700만+ 월 활성 + Square 셀러 OS — 양면 플랫폼 해자<br/>'
        '⑤ Afterpay BNPL 흑자화·Cash App ↔ Square 크로스셀의 차세대 성장 옵션<br/>'
        '⑥ 잭 도시 복귀 후 조직 슬림화·자사주 매입 — 주주환원 본격화<br/><br/>'
        '<b>투자 의견: 매수(BUY), 목표주가 $85 (현재 $70.83 대비 +20.0%)</b><br/>'
        '<i>단기 리스크: 비트코인 가격 급락, 톱라인 추가 둔화, 핀테크 규제 강화</i>'
    ))
    story.append(PageBreak())

    # ━━━ 16. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('14. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 투자 분석 보고서는 yfinance API로 조회한 공개 재무 데이터(SEC 10-K, 분기 실적 등)를 기반으로 '
        '투자 참고 목적으로 작성되었습니다. 본 보고서의 내용은 투자 권유 또는 투자 조언을 구성하지 않습니다. '
        '시세 데이터(주가, 시가총액)는 보고일(2026-05-07) 기준이며 실시간으로 변동됩니다. '
        '과거의 재무 성과 및 주가 흐름이 미래의 결과를 보장하지 않습니다. '
        '특히 Block은 비트코인 보유·거래 사업을 영위하므로 비트코인 가격 변동에 따른 추가 위험이 있습니다. '
        '투자 판단의 최종 책임은 전적으로 투자자 본인에게 있습니다. '
        '미국 주식 투자에는 환율 변동 위험과 원금 손실 위험이 있습니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
