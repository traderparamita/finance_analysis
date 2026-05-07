#!/usr/bin/env python3
"""
Uber Technologies (UBER) PDF 보고서 생성
회사 고유 서술 내용만 이 파일에 작성한다.
공통 레이아웃/스타일/빌드는 shared/pdf_utils.py 에서 처리한다.

데이터: yfinance 2026-04-27 조회분 (FY2022~FY2025)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles
)
from stocks.uber.config import CONFIG

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
    story.append(P('Uber Technologies', 'title'))
    story.append(P('UBER  |  NYSE  (Technology / Mobility Platform)', 'subtitle'))
    story.append(sp(8))
    cover_data = [
        ['항목',      '내용'],
        ['종목코드',  'UBER (NYSE)'],
        ['현재 주가', '$74.64'],
        ['시가총액',  '$153.6B (≈ 약 1,536억 달러)'],
        ['투자의견',  '매수 (BUY)'],
        ['목표주가',  '$90 (상승여력 +20.6%)'],
        ['업종',      '글로벌 모빌리티 / 배달 플랫폼'],
        ['작성일',    '2026년 04월 27일'],
        ['데이터 출처', 'yfinance 실시간 조회 (2026-04-27)'],
    ]
    story.append(tbl(cover_data[0], cover_data[1:], widths=[55*mm, 100*mm]))
    story.append(sp(20))
    story.append(P('본 보고서는 yfinance API로 조회한 공개 재무 데이터를 기반으로 작성된 투자 참고 자료이며, '
                   '투자 판단의 최종 책임은 투자자 본인에게 있습니다.', 'disclaimer'))
    story.append(PageBreak())

    # ━━━ 2. 목차 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('목 차', 'h1')); story.append(hr()); story.append(sp(3))
    for item in [
        '1. 기업 개요', '2. 비전 & 전략', '3. 사업 모델 분석',
        '4. 재무 분석', '5. 수익성 분석', '6. 성장성 분석',
        '7. 재무 안정성 분석', '8. 현금흐름 분석', '9. 산업 & 경쟁 분석',
        '10. SWOT & 리스크 분석', '11. 밸류에이션 & 투자 결론', '12. 면책 고지',
    ]:
        story.append(P(item, 'toc'))
    story.append(PageBreak())

    # ━━━ 3. 기업 개요 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('1. 기업 개요', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>Uber Technologies</b>는 전 세계 70개 이상 국가, 1만 개 이상 도시에서 서비스되는 '
        '글로벌 No.1 모빌리티 플랫폼입니다. 2009년 샌프란시스코에서 차량 호출(Ride-hailing) 서비스로 시작해 '
        '음식 배달(Uber Eats), 화물 운송(Uber Freight)으로 사업을 확장했으며, '
        '2019년 NYSE에 상장한 이후 2023년 첫 GAAP 영업흑자, 2025년 영업이익 $5.6B를 기록하며 '
        '구조적 흑자 가속 단계에 진입했습니다.'))
    story.append(sp(3))
    story.append(tip('우버는 차량을 직접 보유하지 않고, 운전자(공급)와 승객(수요)을 앱으로 연결하는 '
                     "\"플랫폼\" 사업입니다. 차량 자산이 거의 없어 매출이 늘수록 영업이익률이 빠르게 개선되는 구조입니다."))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '내용'],
        [
            ['CEO',           'Dara Khosrowshahi (다라 코스로샤히)'],
            ['종목코드',       'UBER (NYSE)'],
            ['설립연도',       '2009년 (캘리포니아 샌프란시스코)'],
            ['직원 수',        '약 31,000명'],
            ['주요 사업',      'Mobility(차량호출), Delivery(Uber Eats), Freight(화물)'],
            ['월간 활성 사용자', '약 1.7억 명 (Monthly Active Platform Consumers)'],
            ['시가총액',       '$153.6B (약 1,536억 달러)'],
        ],
        widths=[40*mm, 125*mm]
    ))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 & 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('흑자 가속 단계의 차세대 성장 전략', 'h2'))
    story.append(P(
        '우버는 2023년 첫 GAAP 영업흑자($1.1B) → 2024년 $2.8B → 2025년 $5.6B로 매년 영업이익이 두 배 가까이 증가했습니다. '
        '2025년 매출은 $52B(+18.3% YoY), FCF는 $9.8B로 시가총액 대비 약 6.4%의 현금 창출력을 기록했습니다. '
        'CEO Dara Khosrowshahi는 "Profitable Growth(수익성 있는 성장)"을 새 챕터의 핵심 메시지로 제시했습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['전략 방향', '내용'],
        [
            ['플랫폼 통합 강화',  'Uber One 멤버십 — 가입자 3,000만+, 라이드+이츠 락인'],
            ['자율주행 파트너십', 'Waymo, Wayve, Aurora 제휴 — 자체 개발 포기 후 비용 절감'],
            ['광고 사업 확대',    '광고 매출 $1B+ 돌파 (FY2024) — 70%+ 마진 고수익 사업'],
            ['신사업 인접 확장',  '식료품(Cornershop), 헬스케어, 비즈니스 출장(Uber for Business)'],
            ['주주 환원 가속',    '$7B 자사주 매입 프로그램 발표, 2025년 재무CF -$5.7B 환원'],
        ],
        widths=[42*mm, 123*mm]
    ))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('우버의 수익 모델은 "거래액(Gross Bookings)의 일부를 수수료(Take Rate)로 가져가는" 구조입니다. '
                     'Mobility는 약 28%, Delivery는 약 18%의 Take Rate를 적용하며, '
                     '광고 매출(고마진)이 빠르게 성장하면서 전체 마진을 끌어올리고 있습니다.'))
    story.append(sp(3))
    story.append(img('chart6_segments.png'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', '매출 비중', '특징'],
        [
            ['Mobility (차량호출)',  '58%',  '핵심 캐시카우, Take Rate ~28%, 마진 본격 확대'],
            ['Delivery (Uber Eats)', '32%',  'COVID 이후 안정화, 광고·구독 매출 성장 견인'],
            ['Freight (화물)',       '10%',  'B2B 화물 중개, 경기 민감 — 회복 진행 중'],
        ],
        widths=[55*mm, 25*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(P('<b>지역별 매출 비중:</b> 미국·캐나다 58% / EMEA 22% / APAC 10% / LATAM 10%', 'body'))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('단위: 십억달러 ($B). 우버의 핵심 스토리는 '
                     '"4년 만에 매출 1.6배 + 적자 → 본격 흑자 가속". 2024년 순이익 $9.9B는 '
                     '이연법인세 자산 평가충당금 환입($6.4B 일회성)을 포함하며, 2025년 정상화된 $10.1B로 안정.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['매출액',     '$31.9B', '$37.3B', '$44.0B', '$52.0B'],
            ['영업이익',   '-$1.8B', '+$1.1B', '+$2.8B', '+$5.6B'],
            ['당기순이익', '-$9.1B', '+$1.9B', '+$9.9B', '+$10.1B'],
            ['영업이익률', '-5.75%', '+2.98%', '+6.36%', '+10.70%'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('영업이익률이 -5.75%(2022) → +10.70%(2025)로 16%p 개선되었습니다. '
                     '플랫폼 사업의 본질인 "스케일 효과"가 본격적으로 발현된 것입니다. '
                     '단, 2024 ROE 45.72%는 일회성 세금 효과 포함 — 2025년 정상화 ROE 37.18%.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025'],
        [
            ['영업이익률', '-5.75%',   '+2.98%', '+6.36%',  '+10.70%'],
            ['순이익률',   '-28.68%',  '+5.06%', '+22.41%', '+19.33%'],
            ['ROE',        '-124.54%', '+16.77%','+45.72%', '+37.18%'],
            ['ROA',        '-28.47%',  '+4.88%', '+19.23%', '+16.27%'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>4년간 매출 1.6배 성장:</b> $31.9B(2022) → $52.0B(2025). '
        '매출 성장률은 +17~18%대로 안정적으로 유지되고 있으며, '
        '<b>이익 곡선의 진정한 변화는 영업이익에서 발생:</b> '
        '2023년 첫 영업흑자 → 2024년 $2.8B(+152%) → 2025년 $5.6B(+99%)로 매년 거의 두 배씩 증가.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2023', '2024', '2025'],
        [
            ['매출 성장률',     '+17.0%',     '+18.0%',  '+18.3%'],
            ['영업이익 성장률', '흑자 전환',   '+152.2%', '+98.8%'],
            ['순이익 성장률',   '흑자 전환',   '+422.3%', '+2.0%'],
        ],
        widths=[40*mm, 41*mm, 41*mm, 41*mm]
    ))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('우버의 부채비율은 2022년 321.59% → 2025년 124.70%로 크게 개선되었습니다. '
                     '여전히 빅테크 평균(50~70%) 대비 높은 편이지만, 흑자 가속과 자기자본 회복으로 추세는 우호적입니다. '
                     '유동비율 113.6%로 단기 유동성도 양호합니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025', '기준'],
        [
            ['부채비율', '321.59%', '231.28%', '133.44%', '124.70%', '100%↓ 양호'],
            ['유동비율', '104.5%',  '119.5%',  '106.7%',  '113.6%',  '100%↑ 양호'],
        ],
        widths=[27*mm, 26*mm, 26*mm, 26*mm, 26*mm, 32*mm]
    ))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('우버의 현금흐름은 "마이너스에서 본격 플러스로의 대전환". '
                     '영업CF $0.6B(2022) → $10.1B(2025), FCF $0.4B → $9.8B로 4년간 폭발적으로 증가. '
                     'FCF 9.8B는 시가총액($153.6B) 대비 약 6.4% 수준 — 본격적인 자사주 매입의 토대.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['영업활동CF', '+$0.6B', '+$3.6B', '+$7.1B', '+$10.1B'],
            ['투자활동CF', '-$1.6B', '-$3.2B', '-$3.2B', '-$3.6B'],
            ['재무활동CF', '$0.0B',  '-$0.1B', '-$2.1B', '-$5.7B'],
            ['CAPEX',      '$0.3B',  '$0.2B',  '$0.2B',  '$0.3B'],
            ['FCF',        '+$0.4B', '+$3.4B', '+$6.9B', '+$9.8B'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 & 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['기업', '2025년 매출(추정)', '영업이익률', '특징'],
        [
            ['Uber',        '$52.0B', '+10.7%', '글로벌 1위, 모빌리티+배달 통합'],
            ['Lyft',        '$6.5B',  '+2~3%',  '북미 라이드쉐어 2위'],
            ['DoorDash',    '$12B',   '~0%',    '미국 배달 1위, 흑자 임박'],
            ['Didi (滴滴)', '$30B',   '+5%',    '중국 시장 지배'],
        ],
        widths=[35*mm, 40*mm, 30*mm, 60*mm]
    ))
    story.append(sp(3))
    story.append(P('우버는 글로벌 라이드쉐어 시장 점유율 <b>약 75%</b>(중국 제외) 압도적 1위, '
                   'Uber Eats는 글로벌 배달 시장 1위입니다. '
                   '2025년 영업이익률 10.7%로 경쟁사 대비 압도적 수익성을 확보했습니다.'))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT & 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16))
    story.append(sp(5))
    story.append(tbl(
        ['리스크', '심각도', '내용', '모니터링 포인트'],
        [
            ['Tesla 로보택시',   '중상',  '직접 경쟁 위협 — 장기 마진 압박 가능성',          'Tesla FSD/로보택시 상용화 진척도'],
            ['운전자 분류 규제', '중상',  'EU·UK·캘리포니아 — 직원화 시 비용 급증',          '주요 판결 및 입법 동향'],
            ['경기 침체',        '중간',  '라이드쉐어/배달은 경기 민감 소비',                'Gross Bookings 성장률'],
            ['자율주행 지연',    '중간',  '비용 절감 시점 후퇴 시 마진 개선 둔화',           'Waymo 파트너십 도시 확장'],
            ['주주 희석',        '낮음',  '스톡옵션 비중 큼, 자사주 매입으로 일부 상쇄',     '발행주식수 증감 추적'],
        ],
        widths=[32*mm, 18*mm, 50*mm, 65*mm]
    ))
    story.append(PageBreak())

    # ━━━ 13. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('11. 밸류에이션 & 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['지표', '현재값', '해석'],
        [
            ['PER (TTM, GAAP)',   '약 15x',  '2024년 일회성 세금효과 영향, Forward 기준 ~25x'],
            ['EV/EBITDA',         '약 22x',  '구조적 흑자 가속 + 마진 확대 기대 반영'],
            ['EV/Sales',          '약 3.0x', '플랫폼 기업 평균 수준'],
            ['FCF Yield',         '6.4%',    'FCF $9.8B / 시총 $153.6B — 자사주 매입 재원'],
            ['배당',              '없음',    '주주환원은 자사주 매입 중심 ($7B 프로그램)'],
            ['목표주가',          '$90',     '현재 $74.64 대비 +20.6% 상승여력'],
        ],
        widths=[45*mm, 35*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(tip('목표주가 $90은 2026년 예상 EBITDA 약 $9B에 EV/EBITDA 22배를 적용하여 산출. '
                     '플랫폼 기업의 본격적 흑자 가속 + Waymo 파트너십을 통한 장기 마진 개선 가능성을 반영. '
                     '단, 단기 자율주행 경쟁 본격화 시 멀티플 디레이팅 가능성에 유의해야 합니다.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=14))
    story.append(sp(5))
    story.append(P(
        '<b>핵심 투자 포인트:</b><br/>'
        '① 4년 만에 매출 1.6배 성장 ($31.9B → $52.0B), 글로벌 라이드쉐어 점유율 75%<br/>'
        '② 2025년 영업이익 $5.6B(+99%) — 매년 거의 2배 증가하는 흑자 가속<br/>'
        '③ FCF $9.8B(2025), FCF Yield 6.4% — 본격 현금창출 단계<br/>'
        '④ 광고·구독(Uber One 3,000만 가입자) 등 고마진 신성장 동력<br/>'
        '⑤ Waymo·Wayve 자율주행 파트너십 — 장기 비용 절감 옵션<br/>'
        '⑥ $7B 자사주 매입 프로그램 — 본격 주주 환원 시작<br/><br/>'
        '<b>투자 의견: 매수(BUY), 목표주가 $90 (현재 $74.64 대비 +20.6%)</b><br/>'
        '<i>단기 리스크: Tesla 로보택시 경쟁, 운전자 분류 규제, 경기 침체</i>'
    ))
    story.append(PageBreak())

    # ━━━ 14. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('12. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 투자 분석 보고서는 yfinance API로 조회한 공개 재무 데이터(SEC 10-K, 분기 실적 등)를 기반으로 '
        '투자 참고 목적으로 작성되었습니다. 본 보고서의 내용은 투자 권유 또는 투자 조언을 구성하지 않습니다. '
        '시세 데이터(주가, 시가총액)는 보고일 기준이며 실시간으로 변동됩니다. '
        '과거의 재무 성과 및 주가 흐름이 미래의 결과를 보장하지 않습니다. '
        '투자 판단의 최종 책임은 전적으로 투자자 본인에게 있습니다. '
        '미국 주식 투자에는 환율 변동 위험과 원금 손실 위험이 있습니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
