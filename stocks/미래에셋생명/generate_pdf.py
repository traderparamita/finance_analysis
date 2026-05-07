#!/usr/bin/env python3
"""
미래에셋생명 PDF 보고서 생성
회사 고유 서술 내용만 이 파일에 작성한다.
공통 레이아웃/스타일/빌드는 shared/pdf_utils.py 에서 처리한다.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles
)
from stocks.미래에셋생명.config import CONFIG

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
    story = []

    # ━━━ 1. 표지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from reportlab.platypus import Spacer, Table, TableStyle
    from reportlab.lib.colors import HexColor, white
    story.append(Spacer(1, 55 * mm))
    story.append(P('미래에셋생명', 'title'))
    story.append(P('종합 투자 분석 보고서', 'subtitle'))
    story.append(sp(14))
    cover_data = [
        ['종목코드',    '085620 (KRX)'],
        ['현재 주가',   '17,270원'],
        ['시가총액',    '2조 8,844억원'],
        ['투자의견',    '중립 (Hold)'],
        ['목표주가',    '18,000원 (상승여력 +4.2%)'],
        ['보고서 날짜', '2026년 4월 17일'],
    ]
    ct = Table(cover_data, colWidths=[55 * mm, 115 * mm])
    from reportlab.lib.colors import HexColor as HC
    ct.setStyle(TableStyle([
        ('FONTNAME',      (0, 0), (-1, -1), 'AppleGothic'),
        ('FONTSIZE',      (0, 0), (-1, -1), 11),
        ('ALIGN',         (0, 0), (0, -1),  'RIGHT'),
        ('ALIGN',         (1, 0), (1, -1),  'LEFT'),
        ('TEXTCOLOR',     (0, 0), (0, -1),  HC('#475569')),
        ('TEXTCOLOR',     (1, 0), (1, -1),  HC(PRIMARY_HEX)),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW',     (0, 0), (-1, -2), 0.5, HC('#E2E8F0')),
    ]))
    story.append(ct)
    story.append(sp(20))
    story.append(P('본 보고서는 공개 정보를 바탕으로 작성된 투자 참고 자료이며, '
                   '최종 투자 판단의 책임은 투자자 본인에게 있습니다.', 'small'))
    story.append(PageBreak())

    # ━━━ 2. 목차 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('목차', 'h1')); story.append(hr()); story.append(sp(5))
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
        '미래에셋생명보험(주)은 미래에셋그룹 계열의 국내 생명보험사로, '
        '변액보험 시장 업계 3위권을 유지하며 그룹사와의 시너지를 기반으로 '
        '종합 금융 솔루션을 제공합니다. 수입보험료 기준 시장점유율은 약 3.71%(2024년 기준)입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['설립연도', '대표이사', '본사', '주요 사업'],
        [['1988년 (동양생명)', '변재상', '서울 중구', '변액·보장성·연금보험']],
        widths=[42*mm, 35*mm, 35*mm, 58*mm]
    ))
    story.append(sp(3))
    story.append(tip('생명보험사의 부채비율이 수백~천 %로 보이는 것은 보험계약자에게 돌려줄 '
                     '"책임준비금"이 부채로 잡히기 때문입니다. 일반 제조업 부채와 성격이 다릅니다!'))
    story.append(PageBreak())

    # ━━━ 4. 비전 & 전략 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('2. 비전 & 전략', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P('<b>미션:</b> "고객의 평생 자산 파트너로서 안정적인 미래를 설계한다"'))
    story.append(sp(3))
    story.append(P('디지털 혁신 전략', 'h2'))
    story.append(P('국내 생보업계 최초 100% 비대면 가입 프로세스 도입. '
                   '2025년 신계약의 35%가 디지털 채널을 통해 이루어지며 매년 5~7%p 증가 추세입니다.'))
    story.append(sp(3))
    story.append(P('IFRS17 도입 대응 전략', 'h2'))
    story.append(P('2023년 IFRS17 도입으로 보험료수익 인식 방식이 근본적으로 변경되었습니다. '
                   'CSM(계약서비스마진) 잔액을 업계 상위 수준으로 축적하여 '
                   '안정적인 미래 수익 가시성을 확보하고 있습니다.'))
    story.append(PageBreak())

    # ━━━ 5. 사업 모델 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('3. 사업 모델 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '미래에셋생명의 영업수익은 보험료수익(33.6%), 유가증권평가및처분이익(46.2%), '
        '이자수익(9.5%), 기타(10.7%)로 구성됩니다 (2025년 기준). '
        'IFRS17 특성상 투자수익이 영업수익에 포함됩니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['사업부문', '비중', '주요 상품', '특징'],
        [
            ['보장성보험', '32%', '종신·건강·CI보험',     '사차익 중심, 마진 안정적'],
            ['변액보험',   '30%', '변액종신, 변액연금',   '펀드 수익 연동, 업계 3위권'],
            ['연금보험',   '25%', '종신연금, 즉시연금',   '고령화 수요 수혜'],
            ['기타',       '13%', '단체보험, 단기납 저축', '기업 고객 중심'],
        ],
        widths=[28*mm, 18*mm, 45*mm, 79*mm]
    ))
    story.append(sp(5)); story.append(img('chart6_segments.png')); story.append(sp(5))
    story.append(PageBreak())

    # ━━━ 6. 재무 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('4. 재무 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('2023년 IFRS17 도입으로 보험료수익 인식 방식이 변경되었습니다. '
                     '2022년 보험료수익 4조원대에서 2023년 1.5조원대로 급감한 것은 '
                     '회계기준 변경이지 실제 보험 사업 축소가 아닙니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['구분', '2022', '2023', '2024', '2025'],
        [
            ['보험료수익(억원)',   '40,946', '15,137', '12,832', '17,441'],
            ['영업이익(억원)',     '1,624',  '1,487',  '1,221',  '1,945'],
            ['당기순이익(억원)',   '1,248',  '1,014',  '1,361',  '1,308'],
            ['영업이익률(%)',      '2.6',    '2.9',    '2.6',    '3.8'],
        ],
        widths=[38*mm, 32*mm, 32*mm, 32*mm, 32*mm]
    ))
    story.append(sp(3))
    story.append(P(
        '2025년 영업이익 1,945억원(+59.3% YoY)으로 대폭 회복하며 IFRS17 도입 이후 최고 실적을 기록했습니다. '
        '보험료수익도 1조 7,441억원으로 2024년 대비 35.9% 반등하며 회계기준 전환 충격에서 벗어나는 모습입니다.'))
    story.append(sp(5)); story.append(img('chart1_revenue_profit.png')); story.append(sp(5))
    story.append(img('chart7_net_income.png')); story.append(PageBreak())

    # ━━━ 7. 수익성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('5. 수익성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('ROE 5.22%는 업계 평균(4~5%)과 유사한 수준입니다. '
                     '보험사의 ROA가 0.3~0.5%로 매우 낮은 것은 총자산(33조원) 대비 순이익 규모가 작은 '
                     '자산 규모 의존형 사업 특성 때문입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['구분', '2022', '2023', '2024', '2025'],
        [
            ['영업이익률', '2.6%', '2.9%', '2.6%', '3.8%'],
            ['순이익률',   '2.0%', '2.0%', '2.8%', '2.5%'],
            ['ROE',        '4.17%', '2.86%', '4.88%', '5.22%'],
            ['ROA',        '0.32%', '0.30%', '0.42%', '0.40%'],
        ],
        widths=[30*mm, 34*mm, 34*mm, 34*mm, 34*mm]
    ))
    story.append(sp(5)); story.append(img('chart2_margins.png')); story.append(sp(5))
    story.append(img('chart3_roe_roa.png')); story.append(PageBreak())

    # ━━━ 8. 성장성 분석 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('6. 성장성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(P(
        '2023년 보험료수익 급감(-63.0%)은 IFRS17 회계기준 전환에 따른 것으로 실질적 사업 축소가 아닙니다. '
        '2025년 영업이익이 +59.3% 성장하며 IFRS17 체제 하 최고 실적을 달성한 점이 주목됩니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['구분', '2023', '2024', '2025'],
        [
            ['보험료수익 성장률', '-63.0%', '-15.2%',  '+35.9%'],
            ['영업이익 성장률',   '-8.4%',  '-17.9%', '+59.3%'],
            ['순이익 성장률',     '-18.8%',  '+34.2%', '-3.9%'],
        ],
        widths=[40*mm, 40*mm, 40*mm, 40*mm]
    ))
    story.append(sp(5)); story.append(img('chart5_growth_rates.png')); story.append(PageBreak())

    # ━━━ 9. 재무 안정성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('7. 재무 안정성 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('보험사 재무 안정성의 핵심 지표는 지급여력비율(K-ICS)입니다. '
                     '금융당국 권고치 150% 이상. 자기자본 축소(4조→2.4조)는 금리 상승에 따른 '
                     '채권 평가손실이 자본에서 차감된 것이며, 실제 재무 위기와는 다릅니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['구분', '2022', '2023', '2024', '2025'],
        [
            ['부채비율(%)',     '757',    '997',    '1,168',  '1,245'],
            ['자기자본(억원)',  '40,869', '30,155', '25,637', '24,481'],
        ],
        widths=[38*mm, 32*mm, 32*mm, 32*mm, 32*mm]
    ))
    story.append(sp(5)); story.append(img('chart4_financial_stability.png')); story.append(PageBreak())

    # ━━━ 10. 현금흐름 분석 ━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('8. 현금흐름 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tip('보험사의 영업CF가 2022~2024년 마이너스인 것은 보험계약부채(책임준비금) '
                     '적립 증가에 따른 회계 처리입니다. 2025년 영업CF +2,845억원 흑자 전환은 '
                     '체질 개선의 긍정적 신호입니다.'))
    story.append(sp(3))
    story.append(tbl(
        ['구분', '2022', '2023', '2024', '2025'],
        [
            ['영업CF(억원)',  '-6,716', '-9,907', '-2,532',  '+2,845'],
            ['투자CF(억원)',  '+5,994', '+17,753', '+69',    '-3,205'],
            ['재무CF(억원)',  '+4,722', '-4,864',  '-617',   '+859'],
        ],
        widths=[38*mm, 32*mm, 32*mm, 32*mm, 32*mm]
    ))
    story.append(sp(5)); story.append(img('chart9_cashflow.png')); story.append(sp(5))
    story.append(img('chart10_capex_fcf.png')); story.append(sp(5))
    story.append(img('chart11_earnings_quality.png')); story.append(PageBreak())

    # ━━━ 11. 산업 & 경쟁 분석 ━━━━━━━━━━━━━━━━━━━━━
    story.append(P('9. 산업 & 경쟁 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['회사', '수입보험료', '시장점유율', '강점'],
        [
            ['삼성생명',     '약 28조원',  '약 23%', '업계 1위, 브랜드 파워'],
            ['한화생명',     '약 20조원',  '약 17%', '방카슈랑스 강점'],
            ['교보생명',     '약 19조원',  '약 16%', '전통 대리점 채널'],
            ['미래에셋생명', '약 5.5조원', '약 3.7%', '변액보험 강점, 디지털'],
            ['신한라이프',   '약 6조원',   '약 5%',  '금융그룹 시너지'],
        ],
        widths=[33*mm, 28*mm, 28*mm, 81*mm]
    ))
    story.append(PageBreak())

    # ━━━ 12. SWOT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('10. SWOT & 리스크 분석', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(img('chart8_swot.png', width_cm=16.5))
    story.append(sp(5))
    story.append(P('주요 투자 리스크', 'h2'))
    story.append(P(
        '<b>1. 밸류에이션 부담:</b> PER 25.99배(업종 평균 11.5배의 2.3배), PBR 1.21배로 '
        '과거 극단적 저평가 상태는 이미 해소됨. 추가 상승 여력 제한적.<br/><br/>'
        '<b>2. 자기자본 축소 추세:</b> 자기자본이 4조원(2022)→2.4조원(2025)으로 축소. '
        '금리 상승에 따른 채권 평가손실이 원인이나 지속 시 건전성 우려.<br/><br/>'
        '<b>3. 저출산·인구 감소:</b> 신규 보험 가입자 풀 감소. '
        '고령 친화 상품과 연금 전환 상품으로 대응 중.'
    ))
    story.append(PageBreak())

    # ━━━ 13. 밸류에이션 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('11. 밸류에이션 & 투자 결론', 'h1')); story.append(hr()); story.append(sp(3))
    story.append(tbl(
        ['구분', '현재값', '비고'],
        [
            ['PBR',        '1.21배', '저평가 해소 (과거 0.35배에서 급등)'],
            ['PER',        '25.99배', '업종 평균(11.5배) 대비 2.3배 프리미엄'],
            ['EPS',        '663원', '2025년 결산 기준'],
            ['BPS',        '14,301원', '주가(17,270원)가 BPS를 상회'],
        ],
        widths=[38*mm, 30*mm, 102*mm]
    ))
    story.append(sp(5))
    story.append(tip('주가가 52주 최저 4,955원에서 17,270원으로 약 3.5배 급등했습니다. '
                     'PBR이 1.21배로 상승하여 과거 "극단적 저평가" 투자 테마는 이미 소멸했습니다. '
                     '현 밸류에이션에서는 실적 개선 지속 여부가 관건입니다.'))
    story.append(sp(5))
    story.append(img('chart12_radar.png', width_cm=13))
    story.append(sp(5))
    story.append(P(
        '<b>투자 결론:</b> 미래에셋생명은 2025년 영업이익 +59.3% 성장, 영업CF 첫 흑자 전환 등 '
        '펀더멘털이 개선되고 있으나, 주가가 이미 3.5배 급등하여 PER 26배·PBR 1.2배로 '
        '밸류에이션 부담이 존재합니다. 목표주가 18,000원(상승여력 +4.2%)으로 '
        '투자의견을 <b>중립(Hold)</b>으로 제시합니다.'
    ))
    story.append(PageBreak())

    # ━━━ 14. 면책 고지 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    story.append(P('12. 면책 고지', 'h2')); story.append(hr())
    story.append(P(
        '본 보고서는 공개된 정보를 바탕으로 작성된 투자 참고 자료이며, '
        '특정 종목의 매수 또는 매도를 권유하지 않습니다. '
        '투자에 대한 최종 판단과 책임은 투자자 본인에게 있습니다. '
        '과거 실적이 미래 성과를 보장하지 않으며, 투자 전 반드시 전문가와 상담하시기 바랍니다.',
        'disclaimer'
    ))

    build_pdf(CFG, story)


if __name__ == '__main__':
    build()
