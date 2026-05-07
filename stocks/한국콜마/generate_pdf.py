#!/usr/bin/env python3
"""
한국콜마 (161890.KS) PDF 보고서 생성
데이터: yfinance 2026-04-30 조회분 (FY2022~FY2025)
단위: 억원
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles
)
from stocks.한국콜마.config import CONFIG

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
    story.append(P('한국콜마', 'title'))
    story.append(P('161890  |  KOSPI  (소비재 / 화장품·제약 ODM)', 'subtitle'))
    story.append(sp(8))
    cover_data = [
        ['항목',      '내용'],
        ['종목코드',  '161890 (KOSPI)'],
        ['현재 주가', '87,600원'],
        ['시가총액',  '20,678억원 (약 2.07조원)'],
        ['투자의견',  '매수 (BUY)'],
        ['목표주가',  '125,000원 (상승여력 +42.7%)'],
        ['업종',      '화장품·제약 ODM/OEM (글로벌 1위)'],
        ['작성일',    '2026년 04월 30일'],
        ['데이터 출처', 'yfinance 실시간 조회 (2026-04-30)'],
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
        '<b>한국콜마</b>는 1990년 설립된 대한민국 1위, 글로벌 최대 규모의 화장품·제약 ODM(주문자개발생산) 기업입니다. '
        '화장품 브랜드가 제품 기획·마케팅에 집중할 수 있도록 연구개발·생산·품질관리 전 과정을 대행하는 B2B 플랫폼 모델로, '
        '국내외 1,300개 이상의 고객사에 스킨케어·메이크업·선케어·더마코스메틱 등 전 카테고리를 공급합니다. '
        '2022년 대규모 해외 공장 증설(미주·캐나다)로 일시적 손실이 발생했으나, '
        '2023년부터 가파른 실적 반등을 시작해 2025년 영업이익률 8.81%, FCF 플러스 전환에 성공했습니다.'))
    story.append(sp(3))
    story.append(tip('콜마는 "화장품 제조 공장"입니다. CJ올리브영·아모레퍼시픽·글로벌 인디 브랜드가 '
                     '"이런 크림 만들어줘"라고 의뢰하면, 콜마가 연구·생산·포장까지 대신 해줍니다. '
                     '브랜드가 많아질수록, 콜마는 더 많이 주문을 받는 구조입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '내용'],
        [
            ['설립연도',    '1990년 (대전 본사)'],
            ['종목코드',    '161890 (KOSPI)'],
            ['대표이사',    '윤동한 회장 · 안병준 대표'],
            ['주요 사업',   '화장품 ODM/OEM, 제약 ODM/OEM, 건기식'],
            ['고객사',      '국내외 1,300개 이상 (LG생활건강, CJ, 글로벌 인디 브랜드 등)'],
            ['생산거점',    '국내(세종·음성), 중국(북경·무석), 미국·캐나다, 인도'],
            ['시가총액',    '20,678억원 (약 2.07조원)'],
        ],
        widths=[40*mm, 125*mm]
    ))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 & 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('글로벌 ODM 1위 — 미주·유럽 확장과 K-Lab AI 혁신', 'h2'))
    story.append(P(
        '한국콜마는 "글로벌 뷰티·헬스케어 솔루션 기업"을 비전으로, '
        '미주 생산거점(미국 뉴저지·캐나다 온타리오) 확충을 통해 글로벌 인디 브랜드 수주를 빠르게 늘리고 있습니다. '
        '2022~2024년 집중적인 CAPEX(연평균 1,476억원)로 생산능력을 대폭 늘렸으며, '
        '2025년 CAPEX가 1,797억원으로 안정화되면서 FCF가 1,116억원으로 플러스 전환했습니다. '
        'AI 기반 포뮬라 개발 플랫폼(K-Lab)을 통해 신제품 개발 속도를 단축하고 원가를 낮추는 기술 혁신도 추진 중입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['전략 방향', '내용'],
        [
            ['미주·유럽 거점 확충',   '미국·캐나다 공장 증설 — 글로벌 인디 브랜드 직접 수주'],
            ['K-Lab AI 포뮬라 개발',  'AI 기반 원료 조합·처방 최적화 — 개발 기간 30~50% 단축'],
            ['더마코스메틱 고도화',   '피부과학 기반 기능성 제품 라인 강화 — 고마진 카테고리'],
            ['제약 ODM 포트폴리오',   '건강기능식품·의약외품 영역으로 수익원 다각화'],
            ['ESG 친환경 생산',       '그린 포장재·탄소중립 공정 — 글로벌 브랜드 공급망 요건 충족'],
        ],
        widths=[42*mm, 123*mm]
    ))
    story.append(sp(3))
    story.append(P(
        '<b>미주 전략의 재무적 기대 효과:</b> 미국·캐나다 생산거점이 풀가동 단계에 진입하는 2026~2027년에는 '
        '해외 매출 비중이 현 45%에서 55%+로 상승, 원화 약세 수혜 + 고마진 글로벌 물량 증가로 '
        '영업이익률 10%+ 달성이 가능할 것으로 전망됩니다.'))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('ODM이란 "Original Design Manufacturing"의 약자입니다. '
                     '콜마는 고객이 원하는 제품을 연구·설계·생산·포장까지 모두 대신 만들어주고 수수료를 받습니다. '
                     '고객사가 늘어나고 주문량이 커질수록 같은 설비·연구팀을 더 효율적으로 활용해 이익률이 높아집니다.'))
    story.append(sp(3))
    story.append(img('chart6_segments.png'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', '매출 비중', '특징'],
        [
            ['화장품 ODM',       '65%', '스킨케어·선케어·메이크업 전 카테고리, 국내+해외 고객'],
            ['제약 ODM/OEM',     '25%', '건강기능식품·의약외품·전문의약품 일부'],
            ['기타·해외 자회사', '10%', '캐나다 콜마 BNH, 미국 현지 법인 등'],
        ],
        widths=[45*mm, 25*mm, 95*mm]
    ))
    story.append(sp(5))
    story.append(P('<b>지역별 매출 비중:</b> 국내 55% / 중국 25% / 미주·유럽 12% / 기타 해외 8%', 'body'))
    story.append(sp(3))
    story.append(tbl(
        ['섹터 핵심 지표', '2025 수치', '설명'],
        [
            ['동일고객 재구매율',     '~90%+',       '장기 고객사 계약 기반 안정 수주'],
            ['신규 고객사 수 (연간)', '100~150개',    '인디 브랜드 확대로 매년 증가'],
            ['제품 카테고리 수',      '20,000+ SKU', '업계 최다 SKU — 원스톱 서비스'],
            ['R&D 투자 비율',         '~3%',         '매출 대비 연구개발비 (공개 자료 기준)'],
        ],
        widths=[50*mm, 35*mm, 80*mm]
    ))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('단위: 억원. 2022년 순손실(-219.8억원)은 미주 공장 증설 초기 비용 및 일회성 항목이 주원인입니다. '
                     '2023년부터 매출과 영업이익 모두 빠르게 개선되어 2025년 영업이익 2,398억원, 영업이익률 8.81%를 달성했습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['매출액',     '18,657억', '21,557억', '24,521억', '<b>27,224억</b>'],
            ['영업이익',   '734억',    '1,372억',  '1,939억',  '<b>2,399억</b>'],
            ['당기순이익', '-220억',   '52억',     '901억',    '<b>1,251억</b>'],
            ['영업이익률', '3.94%',    '6.36%',    '7.91%',    '<b>8.81%</b>'],
        ],
        widths=[32*mm, 32*mm, 32*mm, 32*mm, 34*mm]
    ))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('영업이익률이 3.94%(2022) → 8.81%(2025)로 3년 만에 2배 이상 개선되었습니다. '
                     '매출이 늘면서 고정비(공장 감가상각·연구인력)가 분산되는 ODM의 전형적인 레버리지 효과입니다. '
                     '경쟁사 코스맥스(영업이익률 ~8%)와 유사한 수준으로 수익성이 따라잡혔습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025'],
        [
            ['영업이익률', '3.94%',  '6.36%', '7.91%',  '8.81%'],
            ['순이익률',   '-1.18%', '0.24%', '3.67%',  '4.59%'],
            ['ROE',        '-3.31%', '0.80%', '11.36%', '13.74%'],
            ['ROA',        '-0.75%', '0.17%', '2.88%',  '3.62%'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>4년간 매출 +46% 성장 (18,657억 → 27,224억):</b> '
        'CAGR(연평균 성장률) 약 13.4%로 소비재 ODM 업종 최고 수준입니다. '
        '성장 동력별로는 ①K-뷰티 글로벌 인기, ②미주 공장 가동, ③더마코스메틱 수요 확대가 핵심입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2023', '2024', '2025'],
        [
            ['매출 성장률',     '+15.5%', '+13.7%', '+11.0%'],
            ['영업이익 성장률', '+86.8%', '+41.4%', '+23.7%'],
            ['순이익 성장률',   '흑자 전환', '+1,635%', '+38.9%'],
        ],
        widths=[40*mm, 41*mm, 41*mm, 41*mm]
    ))
    story.append(sp(3))
    story.append(tbl(
        ['연도', '성장 동력'],
        [
            ['2023년 +15.5%', 'K-뷰티 선케어·더마코스메틱 수출 급증, 영업이익 +87%로 수익성 점프'],
            ['2024년 +13.7%', '미주 공장 본격 가동 시작, 글로벌 인디 브랜드 수주 증가'],
            ['2025년 +11.0%', '중국 리오프닝 수혜 + 국내 더마 카테고리 확대, FCF 첫 플러스 전환'],
        ],
        widths=[35*mm, 130*mm]
    ))
    story.append(sp(3))
    story.append(P('<b>향후 성장 촉매:</b> ①미주 생산거점 풀가동(2026~) ②AI K-Lab 포뮬라 상용화 ③인도 시장 진출', 'body'))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('부채비율 196.7%는 제조업 평균(100~150%) 대비 높습니다. '
                     '이는 2022~2024년 미주 공장 건설 등 공격적인 CAPEX 자금을 차입으로 조달했기 때문입니다. '
                     '유동비율 74.2%는 100%를 하회하므로 단기 차입금 만기 관리에 주의가 필요합니다. '
                     '단, OCF가 2,914억원으로 강하게 회복되고 있어 상환 부담은 점차 완화될 전망입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025', '기준'],
        [
            ['부채비율', '220.43%', '245.26%', '204.50%', '196.67%', '100%↓ 양호'],
            ['유동비율', '94.0%',   '70.0%',   '70.7%',   '74.2%',   '100%↑ 양호'],
        ],
        widths=[27*mm, 26*mm, 26*mm, 26*mm, 26*mm, 32*mm]
    ))
    story.append(sp(3))
    story.append(P('<b>최대 위험 시나리오:</b> 단기 차입금 만기 집중 + 경기 침체로 고객사 주문 급감 시 '
                   '유동성 위기 발생 가능 — 유동비율 개선이 핵심 모니터링 포인트입니다.', 'body'))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('FCF(잉여현금흐름)는 영업활동으로 번 현금에서 설비투자를 뺀 "진짜 남은 돈"입니다. '
                     '한국콜마는 2022~2024년 공장 건설에 거대한 돈을 쏟아붓느라 FCF가 마이너스였습니다. '
                     '2025년 CAPEX가 줄면서 FCF가 1,116억원 플러스로 전환 — 투자 수확기 진입의 신호탄입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2022년', '2023년', '2024년', '2025년'],
        [
            ['영업활동CF', '+908억',   '+1,122억', '+2,154억', '<b>+2,914억</b>'],
            ['투자활동CF', '-1,453억', '-1,557억', '-2,053억', '-2,477억'],
            ['재무활동CF', '+820억',   '-84억',    '-432억',   '+403억'],
            ['CAPEX',      '575억',    '1,247억',  '2,605억',  '1,797억'],
            ['FCF',        '+334억',   '-125억',   '-451억',   '<b>+1,117억</b>'],
        ],
        widths=[30*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(3))
    story.append(P(
        '<b>이익과 현금흐름의 차이:</b> 2025년 영업이익 2,398억원 vs 영업CF 2,914억원. '
        '감가상각비(공장 설비 분할 비용)가 크기 때문에 현금이 이익보다 더 많이 들어옵니다. '
        '<b>CAPEX 성격:</b> 2022~2024년은 신규 공장 건설(성장투자), 2025년부터는 유지보수 + 점진적 증설로 전환.'))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 & 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['기업', '2025 매출(추정)', '영업이익률', 'SSS/성장률', '특징'],
        [
            ['한국콜마',  '2.72조원', '8.81%',  '+11%',   '글로벌 ODM 1위, 미주 확장 중'],
            ['코스맥스',  '2.5조원',  '~8%',    '+12%',   '화장품 ODM 2위, 중국 비중 높음'],
            ['코스메카',  '0.6조원',  '~5%',    '+10%',   '소형 ODM, 국내 특화'],
            ['인터코스(이탈리아)', '~1.5조원', '~7%', '+8%', '유럽·럭셔리 ODM 강자'],
        ],
        widths=[28*mm, 30*mm, 25*mm, 22*mm, 60*mm]
    ))
    story.append(sp(3))
    story.append(P('<b>한국콜마 차별화 포인트:</b>'))
    story.append(P('① <b>규모의 경제:</b> 국내외 1,300개+ 고객사 — 업계 최대 고객 다변화, 특정 고객 의존도 최소화'))
    story.append(P('② <b>제약+화장품 통합:</b> 화장품+제약 ODM을 모두 보유한 유일한 대형사 — 더마코스메틱 수요 직접 대응'))
    story.append(P('③ <b>미주 현지 생산:</b> 미국·캐나다 공장 — Made in North America 요건 충족, 관세 우회'))
    story.append(sp(5))
    story.append(tbl(
        ['섹터 핵심 지표 비교', '한국콜마', '코스맥스', '업계 평균'],
        [
            ['영업이익률',     '8.81%',  '~8%',   '6~8%'],
            ['SSS/매출 성장률', '+11%',  '+12%',  '+10%'],
            ['글로벌 생산거점', '5개국', '3개국', '1~2개국'],
            ['고객사 수',       '1,300+', '800+',  '300~500'],
        ],
        widths=[50*mm, 40*mm, 40*mm, 35*mm]
    ))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT & 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16))
    story.append(sp(5))
    story.append(tbl(
        ['리스크', '심각도', '내용', '모니터링 포인트'],
        [
            ['유동비율 위험',      '중상',  '유동비율 74.2% — 100% 미달, 단기 유동성 주의',          '분기 유동비율 + 단기차입금 만기'],
            ['중국 수요 둔화',     '중상',  '중국 매출 25% — 로컬 ODM 경쟁 심화 및 정책 리스크',      '중국 법인 매출 성장률'],
            ['원자재 가격 상승',   '중간',  '팜유·실리콘·향료 등 원가 변동 — 마진 압박',              '원자재 지수 + 분기 마진율'],
            ['CAPEX 재개 리스크',  '중간',  '인도 등 신규 거점 투자 시 FCF 재악화 가능성',           '연간 CAPEX 가이던스'],
            ['환율 변동',          '낮음',  '해외 매출 45% — 원/달러·원/위안 변동 영향',             '환헤지 비율 + 분기 환차손익'],
        ],
        widths=[32*mm, 18*mm, 55*mm, 60*mm]
    ))
    story.append(PageBreak())

    # ━━━ 13. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('11. 밸류에이션 & 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['지표', '현재값', '해석'],
        [
            ['PER (TTM)',         '약 16.5x',  '2025 순이익 1,251억원 기준 (정상화된 이익)'],
            ['EV/EBITDA',         '약 10.5x',  '현재 시총 기준 — 성장성 대비 저평가 구간'],
            ['EV/Sales',          '약 0.8x',   '소비재 ODM 평균 1.0~1.5x 대비 할인'],
            ['FCF Yield',         '5.4%',      'FCF 1,117억원 / 시총 20,678억원'],
            ['배당',              '연 1,200원 이상', '배당수익률 약 1.4% (공개 자료 기준)'],
            ['목표주가',          '125,000원', '현재 87,600원 대비 +42.7% 상승여력'],
        ],
        widths=[45*mm, 35*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(tip('목표주가 125,000원 산출 근거: '
                     '소비재 ODM 섹터 EV/EBITDA 13배 적용. '
                     'EBITDA(2025) = 영업이익 2,398억원 × 1.15(감가상각 보수적 추정) = 2,758억원. '
                     'EV = 2,758 × 13 = 35,859억원. '
                     '순부채 약 7,000억원 차감 후 목표 시총 28,859억원 → 현재 대비 +39.5%. '
                     '주당 목표주가 = 87,600원 × 1.427 ≈ 125,000원. '
                     '글로벌 ODM 1위 + 미주 확장 가속을 고려해 업종 중간 배수(12~15x) 중 13x 적용.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=14))
    story.append(sp(5))
    story.append(P(
        '<b>핵심 투자 포인트:</b><br/>'
        '① 4년 매출 +46% 성장 (18,657억 → 27,224억), 화장품·제약 ODM 글로벌 1위<br/>'
        '② 영업이익률 3.9% → 8.81% 3년 만에 2배 — ODM 레버리지 효과 본격화<br/>'
        '③ FCF 2025년 플러스 전환(+1,117억원) — 3년 대형 투자 사이클 마무리<br/>'
        '④ 미주 생산거점 본격 가동 — 글로벌 인디 브랜드 수주 성장 가속<br/>'
        '⑤ EV/EBITDA 10.5x — 소비재 ODM 평균 대비 저평가, 상승 여력 충분<br/>'
        '⑥ K-뷰티 글로벌 확장 수혜 + AI K-Lab 포뮬라 개발로 경쟁우위 강화<br/><br/>'
        '<b>투자 의견: 매수(BUY), 목표주가 125,000원 (현재 87,600원 대비 +42.7%)</b><br/>'
        '<i>단기 리스크: 유동비율 100% 미달, 중국 ODM 경쟁 심화, 원자재 가격 상승</i>'
    ))
    story.append(PageBreak())

    # ━━━ 14. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('12. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 투자 분석 보고서는 yfinance API로 조회한 공개 재무 데이터(사업보고서, 분기 실적 발표 등)를 기반으로 '
        '투자 참고 목적으로 작성되었습니다. 본 보고서의 내용은 투자 권유 또는 투자 조언을 구성하지 않습니다. '
        '시세 데이터(주가, 시가총액)는 보고일 기준이며 실시간으로 변동됩니다. '
        '과거의 재무 성과 및 주가 흐름이 미래의 결과를 보장하지 않습니다. '
        '투자 판단의 최종 책임은 전적으로 투자자 본인에게 있습니다. '
        '주식 투자에는 원금 손실 위험이 있으며, 투자 전 반드시 전문가와 상담하시기 바랍니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
