#!/usr/bin/env python3
"""
코스맥스 PDF 보고서 생성
회사 고유 서술 내용만 이 파일에 작성한다.
재무 수치는 CONFIG(yfinance 실시간)에서 동적으로 가져온다.
공통 레이아웃/스타일/빌드는 shared/pdf_utils.py 에서 처리한다.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.platypus import PageBreak, Paragraph, Spacer
from reportlab.lib.units import mm, cm
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles
)
from stocks.코스맥스.config import CONFIG

CFG    = CONFIG
BASE   = CFG['base_dir']
STY    = make_styles(CFG['colors']['primary'], CFG['colors']['accent'])
PRIMARY_HEX = CFG['colors']['primary']


def P(text, key='body'):
    return Paragraph(text, STY[key])
def img(name, width_cm=16):
    return chart_image(BASE, name, width=width_cm * cm, styles=STY)
def tip(text):
    return tip_box(text, STY)
def hr():
    return hr_line(CFG['colors']['accent'])
def tbl(headers, rows, widths=None):
    return make_table(headers, rows, col_widths=widths, primary_hex=PRIMARY_HEX)


def fmt_amt(v, unit='억원'):
    """숫자를 천단위 콤마 + 단위 문자열로 변환."""
    try:
        return f"{float(v):,.0f}{unit}"
    except Exception:
        return str(v)

def fmt_pct(v):
    try:
        return f"{float(v):,.2f}%"
    except Exception:
        return str(v)

def fmt_growth(v):
    try:
        f = float(v)
        sign = '+' if f > 0 else ''
        return f"{sign}{f:.1f}%"
    except Exception:
        return str(v)


def build():
    story = []
    years = CFG['years']                  # ex) ['2022','2023','2024','2025']
    n = len(years)
    unit = CFG.get('unit', '억원')

    # 재무 테이블용 컬럼 폭 계산
    fin_col_widths = [30*mm] + [ (165-30) / n * mm ] * n

    # ━━━ 1. 표지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Spacer(1, 40 * mm))
    story.append(P('코스맥스', 'title'))
    story.append(P('COSMAX, Inc.  |  192820.KS  (KOSPI)', 'subtitle'))
    story.append(sp(8))
    cover_data = [
        ['항목',      '내용'],
        ['종목코드',  '192820 (KOSPI)'],
        ['현재 주가', CFG['price']],
        ['시가총액',  CFG['mkt_cap']],
        ['투자의견',  CFG['opinion']],
        ['목표주가',  CFG['target']],
        ['업종',      '화장품 ODM/OEM (제조자개발생산)'],
        ['작성일',    CFG['report_date']],
    ]
    story.append(tbl(cover_data[0], cover_data[1:], widths=[55*mm, 100*mm]))
    story.append(sp(25))
    story.append(P('본 보고서는 공개된 정보를 기반으로 작성된 투자 참고 자료이며, '
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
        '코스맥스(COSMAX)는 <b>화장품 ODM/OEM 글로벌 1위 기업</b>입니다. '
        '1992년 설립되어 2014년 코스피 상장, 매출 기준 세계 최대의 화장품 제조자개발생산(ODM) 회사로 '
        '국내외 600여 개 브랜드에 제품을 공급합니다. 한국, 중국(상해·광저우), 미국, 인도네시아, 태국에 생산기지를 보유하며 '
        'K뷰티의 글로벌 확산과 인디 브랜드 급성장의 최대 수혜 기업입니다.'))
    story.append(sp(3))
    story.append(tip('ODM(Original Design Manufacturer)은 "제조자가 직접 기획·개발·생산"까지 도맡는 방식입니다. '
                     '브랜드는 마케팅과 판매만 집중하면 돼 인디 뷰티 브랜드가 급성장하는 구조의 최대 수혜자입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '내용'],
        [
            ['대표이사',      '이경수 회장 (창업자), 이병주 대표이사'],
            ['종목코드',      '192820 (KOSPI)'],
            ['주요 사업',     '화장품 ODM/OEM (색조·기초·선케어·건기식 등)'],
            ['글로벌 거점',   '한국·중국(상해/광저우)·미국·인도네시아·태국'],
            ['주요 고객사',   '국내외 대형 브랜드 + 글로벌 인디 브랜드 600+'],
            ['시가총액',      CFG['mkt_cap']],
        ],
        widths=[40*mm, 125*mm]
    ))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 & 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('글로벌 ODM 리더십 강화 & 지역 다변화', 'h2'))
    story.append(P(
        '코스맥스는 2024~2025년 K뷰티의 글로벌 확산, 특히 <b>미국·일본·유럽 시장 폭발적 성장</b>의 최대 수혜 기업입니다. '
        'Amazon·세포라 등 글로벌 채널에서 국내 인디 브랜드 매출이 급증하면서 ODM 수주가 크게 늘고 있습니다. '
        '2025년 영업이익 1,958억원(+11.6%), 순이익 1,231억원(+43.4%)으로 수익성·성장성이 동시에 개선되었습니다. '
        '미국 관세 대응을 위한 현지 생산 확대, 인도네시아·태국 거점을 통한 동남아 시장 공략을 병행하고 있습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['전략 방향', '내용'],
        [
            ['미국 시장 확장',   '미국 오하이오 공장 증설, 인디 브랜드 ODM 수주 급증'],
            ['K뷰티 수출 수혜', 'Amazon·세포라 확장, 글로벌 유통 파트너십 확대'],
            ['중국 수익성 회복', '리오프닝 이후 현지 생산 효율화, 신규 고객 다변화'],
            ['동남아 거점 강화', '인도네시아·태국 생산능력 확대, 할랄 화장품 시장 공략'],
            ['친환경·비건 확장', 'ESG 화장품 포뮬러 개발, 비건 인증 라인업 확대'],
        ],
        widths=[42*mm, 123*mm]
    ))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('코스맥스의 수익 모델은 "B2B ODM"입니다. 브랜드사가 기획을 의뢰하면 연구개발·원료 조달·생산·포장까지 일괄 수행하고 단가에 마진을 얹어 납품합니다. '
                     '인디 브랜드 급증 → 소량·다품종 ODM 수요 폭발이 매출 성장의 핵심입니다.'))
    story.append(sp(3))
    story.append(img('chart6_segments.png'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', '매출 비중', '특징'],
        [
            ['색조화장품', '35%', '립·아이·파운데이션, 고마진 핵심 카테고리'],
            ['기초화장품', '30%', '스킨케어·앰플, 안정적 수주 기반'],
            ['선케어',     '20%', '글로벌 수요 급증, 수출 비중 높음'],
            ['기타/건기식','15%', '마스크팩, 이너뷰티 건강기능식품'],
        ],
        widths=[45*mm, 25*mm, 95*mm]
    ))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('매출액(얼마나 팔았나), 영업이익(본업으로 얼마 남겼나), '
                     '당기순이익(최종적으로 얼마 남겼나) 세 가지를 먼저 확인하세요. '
                     '코스맥스는 2022년 이후 <b>3년 연속 두 자릿수 매출 성장 + 영업이익 급증</b> 구간입니다.'))
    story.append(sp(3))
    fin_rows = [
        ['매출액']     + [fmt_amt(v, unit) for v in CFG['revenue']],
        ['영업이익']   + [fmt_amt(v, unit) for v in CFG['op_income']],
        ['당기순이익'] + [fmt_amt(v, unit) for v in CFG['net_income']],
        ['영업이익률'] + [fmt_pct(v) for v in CFG['op_margin']],
    ]
    story.append(tbl(['항목'] + [f'{y}년' for y in years], fin_rows, widths=fin_col_widths))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    roe_last = CFG['roe'][-1]
    story.append(tip(f'ROE {roe_last:.2f}%는 "주주가 맡긴 100원으로 {roe_last:.1f}원을 벌었다"는 의미입니다. '
                     '2022년 3.59% → 2025년 22.05%로 <b>6배 이상 개선</b>되었습니다. 수익성이 구조적으로 정상화되는 국면입니다.'))
    story.append(sp(3))
    prof_rows = [
        ['영업이익률'] + [fmt_pct(v) for v in CFG['op_margin']],
        ['순이익률']   + [fmt_pct(v) for v in CFG['net_margin']],
        ['ROE']        + [fmt_pct(v) for v in CFG['roe']],
        ['ROA']        + [fmt_pct(v) for v in CFG['roa']],
    ]
    story.append(tbl(['지표'] + years, prof_rows, widths=fin_col_widths))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>3년 연속 고성장:</b> 매출 2023년 +11.1%, 2024년 +21.9%, 2025년 +10.7% — 지속적 두 자릿수 성장. '
        '<b>영업이익 폭발:</b> 2023년 +117.9%, 2024년 +51.6%, 2025년 +11.6% — 중국 손실 축소 & 미국/수출 증가 효과. '
        '<b>순이익 레버리지:</b> 매출 성장률 대비 훨씬 큰 폭으로 이익이 늘어나는 전형적인 <b>영업 레버리지 국면</b>입니다.'))
    story.append(sp(3))
    g_years = years[1:]  # 첫 해는 YoY 0이므로 생략
    g_rows = [
        ['매출 성장률']    + [fmt_growth(v) for v in CFG['rev_growth'][1:]],
        ['영업이익 성장률'] + [fmt_growth(v) for v in CFG['op_growth'][1:]],
        ['순이익 성장률']  + [fmt_growth(v) for v in CFG['ni_growth'][1:]],
    ]
    g_col_widths = [38*mm] + [(165-38) / len(g_years) * mm] * len(g_years)
    story.append(tbl(['지표'] + g_years, g_rows, widths=g_col_widths))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    debt_last = CFG['debt_ratio'][-1]
    curr_last = CFG['current_ratio'][-1]
    story.append(tip(f'부채비율 {debt_last:.1f}%, 유동비율 {curr_last:.1f}% — 코스맥스의 <b>가장 큰 약점</b>입니다. '
                     '부채비율 200% 이상은 주의가 필요하며, 유동비율이 100% 미만이면 단기 유동성 부담이 있습니다. '
                     '다만 2023년 330% → 2025년 271%로 부채비율은 개선 추세입니다.'))
    story.append(sp(3))
    stab_rows = [
        ['부채비율'] + [fmt_pct(v) for v in CFG['debt_ratio']] + ['100%↓ 양호 / 200%↑ 주의'],
        ['유동비율'] + [fmt_pct(v) for v in CFG['current_ratio']] + ['200%↑ 양호 / 100%↓ 주의'],
    ]
    stab_col_widths = [27*mm] + [(165-27-40) / n * mm] * n + [40*mm]
    story.append(tbl(['지표'] + years + ['기준'], stab_rows, widths=stab_col_widths))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('영업CF가 크고 안정적이면 이익의 질이 높은 기업입니다. '
                     '2024~2025년 <b>CAPEX 대폭 확대</b>(각 1,685·1,927억원)로 FCF가 마이너스 전환되었습니다. '
                     '미국·인니 생산능력 확장 투자 구간으로, 2026년 이후 수주 회수 시 FCF 정상화가 관건입니다.'))
    story.append(sp(3))
    cf_rows = [
        ['영업활동CF'] + [fmt_amt(v, unit) for v in CFG['ocf']],
        ['투자활동CF'] + [fmt_amt(v, unit) for v in CFG['icf']],
        ['재무활동CF'] + [fmt_amt(v, unit) for v in CFG['fin_cf']],
        ['CAPEX']      + [fmt_amt(v, unit) for v in CFG['capex']],
        ['FCF']        + [fmt_amt(v, unit) for v in CFG['fcf']],
    ]
    story.append(tbl(['항목'] + [f'{y}년' for y in years], cf_rows, widths=fin_col_widths))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 & 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['기업', '2025년 매출', '영업이익률', '특징'],
        [
            ['코스맥스',        '2조 3,988억', '8.2%',  '글로벌 ODM 1위, K뷰티 최대 수혜'],
            ['한국콜마',        '2조 4,000억', '~9%',   'ODM 2위, 국내·미국·중국 생산'],
            ['코스메카코리아',  '5,000억',    '~8%',   '중견 ODM, 미국 잉글우드랩 보유'],
            ['인터코스(글로벌)', '€9억',       '~12%',  '이탈리아 기반 글로벌 ODM 2위'],
        ],
        widths=[35*mm, 32*mm, 25*mm, 73*mm]
    ))
    story.append(sp(3))
    story.append(P('코스맥스는 <b>매출 규모 기준 글로벌 1위</b>의 화장품 ODM 기업으로, '
                   '국내외 600여 개 브랜드 고객사를 보유하고 있습니다. K뷰티의 북미·유럽 확산과 '
                   '인디 브랜드 ODM 수요 폭발의 직접 수혜주입니다.'))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT & 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16))
    story.append(sp(5))
    story.append(tbl(
        ['리스크', '심각도', '내용', '모니터링 포인트'],
        [
            ['재무 레버리지',     '중상',  f'부채비율 {debt_last:.0f}%, 유동비율 {curr_last:.0f}%', '이자비용·차입금 만기구조'],
            ['미국 관세 리스크',  '중상',  '한국산 화장품 수출 관세 인상 가능성',      '현지 생산능력 확충 진도'],
            ['FCF 마이너스',       '중간',  '2024~25 대규모 CAPEX로 현금창출력 훼손',  'CAPEX 정상화 시점, 수주잔고'],
            ['중국 경쟁 심화',    '중간',  '로컬 ODM 가격 경쟁, 한한령 여진',          '중국 법인 실적 회복 여부'],
            ['환율 변동',         '낮음',  '수출 비중 높아 원화 환율 민감',           '분기 실적 환율 영향'],
        ],
        widths=[32*mm, 18*mm, 55*mm, 60*mm]
    ))
    story.append(PageBreak())

    # ━━━ 13. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('11. 밸류에이션 & 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['지표', '현재값', '해석'],
        [
            ['PER (주가수익비율)',   '약 20배',   '화장품 업종 평균 수준, 실적 개선 반영'],
            ['PBR (주가순자산비율)', '약 4.0배',  'ROE 22% 고려 시 타당한 수준'],
            ['EV/EBITDA',           '약 10배',   '동종 ODM 업종 평균 수준'],
            ['배당수익률',           '약 0.5%',  '성장 재투자 중심, 점진적 확대'],
            ['목표주가',             CFG['target'], '실적 정상화 + K뷰티 수혜 반영'],
        ],
        widths=[45*mm, 35*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(tip(f'목표주가 {CFG["target"]}는 2026~2027년 예상 실적 기준 PER 22~25배를 적용한 값입니다. '
                     f'현재 {CFG["price"]} 대비 상승여력이 있으며, K뷰티 수출 지속과 미국 증설 효과가 관건입니다. '
                     '다만 부채비율·FCF 부담은 지속적 모니터링이 필요한 중기 리스크입니다.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=14))
    story.append(sp(5))
    story.append(P(
        '<b>핵심 투자 포인트:</b><br/>'
        '① 글로벌 화장품 ODM <b>매출 1위</b> — K뷰티 확산 최대 수혜<br/>'
        '② 3년 연속 매출 두 자릿수 성장(+11/+22/+11%) 지속<br/>'
        '③ ROE 2022년 3.6% → 2025년 22.1%로 <b>수익성 구조적 개선</b><br/>'
        '④ 인디 브랜드 급증 → 소량·다품종 ODM 수주 폭증<br/>'
        '⑤ 미국·인니 생산 증설 완료 시 2026년 FCF 정상화 기대<br/>'
        '⑥ 영업이익률 3.3% → 8.2%로 개선 — 마진 확장 여력 존재<br/><br/>'
        '<b>투자 의견: ' + CFG['opinion'] + ', 목표주가 ' + CFG['target'] + '</b><br/>'
        '<i>단기 리스크: 부채비율 271%, FCF 마이너스, 미국 관세 불확실성</i>'
    ))
    story.append(PageBreak())

    # ━━━ 14. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('12. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 투자 분석 보고서는 공개된 정보를 기반으로 투자 참고 목적으로 작성되었습니다. '
        '본 보고서의 내용은 투자 권유 또는 투자 조언을 구성하지 않습니다. '
        '과거의 재무 성과 및 주가 흐름이 미래의 결과를 보장하지 않습니다. '
        '투자 판단의 최종 책임은 전적으로 투자자 본인에게 있습니다. '
        '코스맥스 주식 투자에는 원금 손실 위험이 있습니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
