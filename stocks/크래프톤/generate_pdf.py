#!/usr/bin/env python3
"""
크래프톤 PDF 보고서 생성
회사 고유 서술 내용만 이 파일에 작성한다.
공통 레이아웃/스타일/빌드는 shared/pdf_utils.py 에서 처리한다.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles
)
from 크래프톤.config import CONFIG

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
    from reportlab.platypus import Spacer, Table, TableStyle
    from reportlab.lib.colors import HexColor, white
    story = []

    # ━━━ 1. 표지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(Spacer(1, 40 * mm))
    story.append(P('크래프톤', 'title'))
    story.append(P('KRAFTON, Inc.  |  259960.KS  (KOSPI)', 'subtitle'))
    story.append(sp(8))
    cover_data = [
        ['항목',      '내용'],
        ['종목코드',  '259960 (KOSPI)'],
        ['현재 주가', '256,500원'],
        ['시가총액',  '약 12조 1,597억원'],
        ['투자의견',  '매수 (BUY)'],
        ['목표주가',  '320,000원 (상승여력 +24.8%)'],
        ['업종',      '국내 게임 (온라인/모바일)'],
        ['작성일',    '2026년 4월 17일'],
    ]
    story.append(tbl(cover_data[0], cover_data[1:], widths=[55*mm, 100*mm]))
    story.append(sp(25))
    story.append(P('본 보고서는 공개된 정보를 기반으로 작성된 투자 참고 자료이며, '
                   '투자 판단의 최종 책임은 투자자 본인에게 있습니다.', 'disclaimer'))
    story.append(PageBreak())

    # ━━━ 2. 목차 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('목 차', 'h1')); story.append(hr()); story.append(sp(3))
    for item in [
        '1. 기업 개요', '2. 비전 & 전략 (인도 전략 포함)', '3. 사업 모델 분석',
        '4. 재무 분석', '5. 수익성 분석', '6. 성장성 분석',
        '7. 재무 안정성 분석', '8. 현금흐름 분석', '9. 산업 & 경쟁 분석',
        '10. SWOT & 리스크 분석', '11. 밸류에이션 & 투자 결론', '12. 면책 고지',
    ]:
        story.append(P(item, 'toc'))
    story.append(PageBreak())

    # ━━━ 3. 기업 개요 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('1. 기업 개요', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '크래프톤(KRAFTON)은 <b>배틀그라운드(PUBG: BATTLEGROUNDS)</b>를 개발한 글로벌 게임사입니다. '
        '2007년 블루홀스튜디오로 설립, 2021년 코스피 상장. '
        '인도 모바일 게임 시장에서 압도적 1위를 차지하고 있으며, 2025년 ADK 그룹 인수를 통해 글로벌 역량을 강화했습니다.'))
    story.append(sp(3))
    story.append(tip('PUBG는 비행기에서 100명이 뛰어내려 마지막 1명이 살아남는 '
                     '"배틀로얄" 장르를 대중화한 게임입니다. 전 세계적으로 역대 가장 많이 팔린 PC게임 중 하나입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '내용'],
        [
            ['대표이사',    '김창한'],
            ['종목코드',    '259960 (KOSPI)'],
            ['주요 게임',   'PUBG: BATTLEGROUNDS, PUBG 모바일, 다크앤다커 모바일'],
            ['글로벌 스튜디오', '한국, 미국, 인도, 유럽, 일본(ADK)'],
            ['시가총액',    '약 12조 1,597억원'],
        ],
        widths=[40*mm, 125*mm]
    ))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 & 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('글로벌 확장 및 M&A 전략', 'h2'))
    story.append(P(
        '인도에서 PUBG 모바일(배틀그라운드 인디아)은 월간 활성 유저 약 1억 명을 보유하며 최고 수익원으로 자리잡았습니다. '
        '2024년 인도 시장 수익화가 본격화되며 매출이 41.8% 급성장했습니다. '
        '2025년에는 일본 ADK 그룹 인수를 통해 게임 퍼블리싱 및 IP 사업 역량을 강화했으며, 다크앤다커 모바일의 글로벌 흥행으로 신규 IP 발굴에도 성공했습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['전략 방향', '내용'],
        [
            ['인도 시장 심화',  '월활 1억 명 기반 수익화 가속, PUBG 인디아 장기 성장 기대'],
            ['신규 IP 발굴',    '다크앤다커 모바일 글로벌 흥행, 인헌즈 등 신작 파이프라인'],
            ['M&A 통한 확장',   'ADK 그룹 인수로 일본 퍼블리싱 및 IP 역량 확보'],
            ['AI 기술 내재화',  '생성형 AI 활용 게임 개발 효율화, NPC AI 고도화'],
        ],
        widths=[42*mm, 123*mm]
    ))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('크래프톤의 수익 모델은 "부분 유료화"입니다. '
                     '게임은 무료, 캐릭터 스킨·의상 등 코스메틱 아이템을 유료로 판매합니다. '
                     '실력과 무관해 유저 거부감이 적고 수익성이 매우 높습니다.'))
    story.append(sp(3))
    story.append(img('chart6_segments.png'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', '매출 비중', '특징'],
        [
            ['PUBG 모바일', '52%', '인도·동남아 중심, 최대 매출원'],
            ['PUBG PC',     '22%', '글로벌 스팀 플랫폼, e스포츠 기반'],
            ['신규 게임',   '16%', '다크앤다커 모바일 등 성장 중'],
            ['기타/로열티', '10%', 'IP 라이선싱, 인디 게임 퍼블리싱'],
        ],
        widths=[45*mm, 25*mm, 95*mm]
    ))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('매출액(얼마나 팔았나), 영업이익(본업으로 얼마 남겼나), '
                     '당기순이익(최종적으로 얼마 남겼나) 세 가지를 먼저 확인하세요.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2021년', '2022년', '2023년', '2024년', '2025년'],
        [
            ['매출액',     '18,854억', '18,540억', '19,106억', '27,098억', '33,266억'],
            ['영업이익',   '6,506억',  '7,516억',  '7,680억',  '11,825억', '10,544억'],
            ['당기순이익', '5,199억',  '5,002억',  '5,941억',  '13,026억', '7,337억'],
            ['영업이익률', '34.51%',  '40.54%',   '40.20%',   '43.64%',   '31.70%'],
        ],
        widths=[30*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]
    ))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('ROE 10.60%는 "주주가 맡긴 100원으로 10.6원을 벌었다"는 의미입니다. '
                     '2025년은 ADK 인수 비용 반영으로 일시 하락했으나, 본업 수익성은 여전히 견조합니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2021', '2022', '2023', '2024', '2025'],
        [
            ['영업이익률', '34.51%', '40.54%', '40.20%', '43.64%', '31.70%'],
            ['순이익률',   '27.58%', '26.98%', '31.09%', '48.07%', '22.05%'],
            ['ROE',        '17.86%', '10.29%', '11.16%', '21.10%', '10.60%'],
            ['ROA',        '13.98%', '8.51%',  '9.52%',  '18.14%', '8.46%'],
        ],
        widths=[30*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]
    ))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '<b>2024년 폭발적 성장:</b> 인도 시장 수익화 본격화와 다크앤다커 모바일 흥행으로 매출 41.8%, 영업이익 54.0% 급증. '
        '<b>2025년 조정:</b> ADK 그룹 인수 비용 및 투자 비용 증가로 영업이익 -10.8%, 순이익 -43.7% 감소. '
        '다만 매출은 22.8% 성장하여 톱라인 성장세는 유지.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2022', '2023', '2024', '2025'],
        [
            ['매출 성장률',    '-1.7%',  '+3.1%',   '+41.8%', '+22.8%'],
            ['영업이익 성장률', '+15.5%', '+2.2%',   '+54.0%', '-10.8%'],
            ['순이익 성장률',  '-3.8%',  '+18.8%',  '+119.3%', '-43.7%'],
        ],
        widths=[38*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    ))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('2025년 ADK 그룹 인수로 부채비율이 31.31%로 상승했으나, '
                     '여전히 업계 평균(50~70%) 대비 매우 낮은 수준입니다. 유동비율 301%로 단기 유동성도 안전합니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['지표', '2021', '2022', '2023', '2024', '2025', '기준'],
        [
            ['부채비율', '24.08%', '18.01%', '15.86%', '15.97%', '31.31%', '100%↓ 매우 양호'],
            ['유동비율', '340%',   '380%',   '410%',   '425%',   '301%',   '200%↑ 매우 양호'],
        ],
        widths=[27*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 32*mm]
    ))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('영업CF가 크고 안정적이면 이익의 질이 높은 기업입니다. '
                     '2024년 영업CF 1조 2,315억원, FCF 1조 1,515억원으로 역대 최고 현금 창출력을 기록했습니다. '
                     '2025년은 ADK 인수로 재무CF가 마이너스로 전환되었습니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['항목', '2021년', '2022년', '2023년', '2024년', '2025년'],
        [
            ['영업활동CF', '6,798억',   '7,250억',  '8,106억',  '12,315억',  '9,880억'],
            ['투자활동CF', '-2,100억',  '-2,400억', '-2,850억', '-3,200억',  '-4,500억'],
            ['재무활동CF', '1,200억',   '900억',    '750억',    '1,100억',   '-2,800억'],
            ['CAPEX',      '480억',     '520억',    '650억',    '800억',     '950억'],
            ['FCF',        '6,318억',   '6,730억',  '7,456억',  '11,515억',  '8,930억'],
        ],
        widths=[30*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm]
    ))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 & 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['기업', '2025년 매출', '영업이익률', 'PER(배)', '특징'],
        [
            ['크래프톤',  '3조 3,266억', '31.7%', '15.94x', 'PUBG IP, 인도 1위, ADK 인수'],
            ['엔씨소프트', '1조 8,500억', '~18%',  '20x',    '리니지 IP, 국내 중심'],
            ['넷마블',    '2조 8,000억', '~8%',   '35x',    '글로벌 M&A, 수익성 회복 중'],
            ['펄어비스',  '4,200억',     '~12%',  '22x',    '검은사막, 도깨비 출시'],
        ],
        widths=[30*mm, 35*mm, 27*mm, 22*mm, 51*mm]
    ))
    story.append(sp(3))
    story.append(P('크래프톤은 국내 경쟁사 중 <b>영업이익률 1위</b>이며 매출의 <b>88%가 해외</b>에서 발생하는 '
                   '진정한 글로벌 기업입니다. 2025년 ADK 인수로 일본 시장 진출 기반을 확보했습니다.'))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT & 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16))
    story.append(sp(5))
    story.append(tbl(
        ['리스크', '심각도', '내용', '모니터링 포인트'],
        [
            ['ADK 인수 비용',     '중상',  'M&A 통합 비용으로 2025년 이익 감소', 'ADK 시너지 발현 시점 추적'],
            ['PUBG 의존도',       '중간',  'PUBG 매출 집중도 여전히 높음',        '신규 게임 매출 비중 증가 여부'],
            ['주가 조정 지속',    '중간',  '52주 고점 대비 -33.5% 조정 중',       '기관·외국인 매수세 회복 여부'],
            ['인도 규제 리스크',  '낮음',  '인도 정부 규제 재발 가능성',          '인도 정책 모니터링'],
            ['환율 변동',         '낮음',  '해외 매출 88%, 달러·원 변동',         '분기 실적 환율 영향 확인'],
        ],
        widths=[32*mm, 18*mm, 50*mm, 65*mm]
    ))
    story.append(PageBreak())

    # ━━━ 13. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('11. 밸류에이션 & 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['지표', '현재값', '해석'],
        [
            ['PER (주가수익비율)',  '15.94배',   '글로벌 게임사 평균(20~25배) 대비 저평가'],
            ['PBR (주가순자산비율)', '1.57배',   'ADK 인수 후 자산 증가, 여전히 저평가 구간'],
            ['EV/EBITDA',          '10.2배',    '동종 업종 평균 하단 (저평가)'],
            ['배당수익률',          '0.6%',      '성장 재투자 중심, 점진적 확대 전망'],
            ['목표주가',            '320,000원', '현재 대비 +24.8% 상승여력'],
        ],
        widths=[45*mm, 35*mm, 85*mm]
    ))
    story.append(sp(5))
    story.append(tip('목표주가 320,000원은 2025~2026년 예상 실적 정상화(ADK 시너지 반영) 기준 '
                     'PER 18배를 적용한 값입니다. 현재 256,500원 대비 +24.8% 상승 여력. '
                     '52주 고점(385,500원) 대비 -33.5% 조정 중으로 중장기 매수 기회 구간.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=14))
    story.append(sp(5))
    story.append(P(
        '<b>핵심 투자 포인트:</b><br/>'
        '① 인도 시장 폭발 성장 — 월간 유저 1억 명, 수익화 본격화<br/>'
        '② 2024년 매출 41.8% 급성장, 2025년 톱라인 22.8% 지속 성장<br/>'
        '③ 다크앤다커 모바일 글로벌 흥행으로 신규 IP 검증 완료<br/>'
        '④ ADK 인수로 일본 퍼블리싱 및 IP 역량 확보<br/>'
        '⑤ 52주 고점 대비 -33.5% 조정 → 중장기 매수 기회<br/>'
        '⑥ PER 15.94배 — 글로벌 게임사 대비 현저한 저평가<br/><br/>'
        '<b>투자 의견: 매수(BUY), 목표주가 320,000원</b><br/>'
        '<i>단기 리스크: ADK 통합 비용 지속 가능성, 주가 조정 국면 지속</i>'
    ))
    story.append(PageBreak())

    # ━━━ 14. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('12. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 투자 분석 보고서는 공개된 정보를 기반으로 투자 참고 목적으로 작성되었습니다. '
        '본 보고서의 내용은 투자 권유 또는 투자 조언을 구성하지 않습니다. '
        '과거의 재무 성과 및 주가 흐름이 미래의 결과를 보장하지 않습니다. '
        '투자 판단의 최종 책임은 전적으로 투자자 본인에게 있습니다. '
        '크래프톤 주식 투자에는 원금 손실 위험이 있습니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
