"""
Block, Inc. (XYZ) — 투자 분석 설정
이 파일만 수정하면 차트·PDF 모두 자동 반영된다.

데이터 출처: yfinance (shared/data_fetcher.py)
조회일: 2026-05-07 (KST)
단위: 십억달러 ($B = $1,000M)
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # ── 기본 정보 (yfinance 실시간 — 2026-05-07 조회) ──
    'name':        'Block, Inc.',
    'ticker':      'XYZ',
    'exchange':    'NYSE',
    'price':       '$70.83',
    'mkt_cap':     '$42.2B (≈ 약 422억 달러)',
    'opinion':     '매수 (Buy)',
    'target':      '$85 (상승여력 +20.0%)',
    'report_date': '2026년 05월 07일',
    'header_text': 'Block, Inc. (XYZ) 투자 분석 보고서',
    'pdf_filename': 'block_investment_report.pdf',
    'base_dir':    BASE_DIR,
    'unit':        '십억달러',
    'revenue_label': '매출액',

    # ── 브랜드 컬러 (Block / Cash App) ──────────────
    'colors': {
        'primary': '#000000',   # Block Black
        'accent':  '#00D54B',   # Cash App Green
        'green':   '#00D54B',
        'red':     '#E11900',
        'purple':  '#8E44AD',
        'gray':    '#6C757D',
        'teal':    '#3E80B5',
    },

    # ── 연도 (yfinance 회계연도, 4개년 반환됨) ─────
    'years': ['2022', '2023', '2024', '2025'],

    # ── 손익계산서 ($B) ──────────────────────────────
    'revenue':    [17.5, 21.9, 24.1, 24.2],
    'op_income':  [-0.0,  0.4,  1.7,  3.0],
    'net_income': [-0.5,  0.0,  2.9,  1.3],

    # ── 수익성 (%) ──────────────────────────────────
    # 2024 ROE/순이익률 급등은 이연법인세 자산 환입 일회성 효과 포함
    'op_margin':  [-0.16,  1.74,  6.99, 12.59],
    'net_margin': [-3.08,  0.04, 12.01,  5.40],
    'roe':        [-3.14,  0.05, 13.62,  5.88],
    'roa':        [-1.72,  0.03,  7.88,  3.30],

    # ── 재무 안정성 ─────────────────────────────────
    'debt_ratio':    [81.94, 76.70, 73.08, 78.27],
    'current_ratio': [185.20, 200.60, 232.60, 220.10],
    'debt_label':    '부채비율 (%)',
    'stability_secondary_label': '유동비율 (%)',

    # ── 성장률 YoY (%) ──────────────────────────────
    'rev_growth': [0.0,  25.0,  10.1,   0.3],
    'op_growth':  [0.0, 1499.8, 341.7,  80.6],
    'ni_growth':  [0.0,  101.8, 29546.4, -54.9],

    # ── 현금흐름 ($B) ───────────────────────────────
    'ocf':    [ 0.2,  0.1,  1.7,  2.6],
    'icf':    [ 1.2,  0.7,  0.6, -2.8],
    'fin_cf': [ 0.1, -0.2,  2.0, -0.6],
    'capex':  [ 0.2,  0.2,  0.2,  0.2],
    'fcf':    [ 0.0, -0.1,  1.6,  2.4],

    # ── 사업부문 (공개 자료 기준 — 2024~2025 Gross Profit 비중) ─
    'seg_labels': ['Cash App (55%)', 'Square 셀러 (42%)', '기타·신사업 (3%)'],
    'seg_sizes':  [55, 42, 3],
    'sub_labels': ['North America', 'International'],
    'sub_sizes':  [88, 12],
    'sub_title':  '지역별 매출 비중 (공개 자료 기준)',

    # ── SWOT (공개 자료·섹터 분석 기반) ─────────────
    'swot': {
        '강점': [
            '• Cash App 월 활성 5,700만+ 글로벌 P2P/Banking 슈퍼앱',
            '• Square 셀러 생태계 — 결제·POS·캐피털·뱅킹 통합',
            '• 4년 만에 매출 1.4배 + 영업이익률 -0.16% → +12.59% 점프',
            '• 2025년 영업이익 $3.0B(+80.6%) — 본격 흑자 가속',
            '• FCF $2.4B(2025), FCF Yield 5.7% — 자사주 매입 재원',
        ],
        '약점': [
            '• 2024 순이익 $2.9B 중 상당 부분 일회성 세금 환입 포함',
            '• 2025 매출 성장 +0.3% — 톱라인 둔화 우려',
            '• 비트코인 매출(저마진) 비중 큼 — Gross Margin 희석',
            '• Cash App 사용자 증가율 둔화 (월 5,700만 정체)',
            '• Tidal·TBD·Spiral 등 신사업 적자 지속',
        ],
        '기회': [
            '• Cash App Borrow·Afterpay BNPL 흑자화 가속',
            '• 셀러 Square Banking·Capital — 고마진 금융 매출 확대',
            '• Bitcoin Lightning Network·셀프-커스터디 지갑 보급',
            '• AI 기반 가맹점 운영 자동화(SaaS화) 매출 확대',
            '• 신흥국 Cash App·Square 글로벌 확장',
        ],
        '위협': [
            '• PayPal·Venmo·Zelle와 P2P 송금 경쟁 격화',
            '• Stripe·Toast·Clover 등 셀러 결제 경쟁 심화',
            '• Bitcoin 가격 변동성 — 비트코인 보유 자산 평가손익',
            '• 미국 금리 사이클 → Cash App 예금·BNPL 마진 압박',
            '• 핀테크 규제(CFPB, OCC) 강화 — 라이선스·컴플라이언스 비용',
        ],
    },

    # ── 투자매력도 레이더 (10점 만점) ────────────────
    'radar_categories': ['수익성', '성장성', '안정성', '밸류에이션', '플랫폼파워', '핀테크경쟁력'],
    'radar_scores':     [7, 6, 7, 8, 8, 8],

    # ══════════════════════════════════════════════════════
    # v4.0 신규 — 분기 데이터 (24Q3 NaN 제외, 5분기만 사용)
    # ══════════════════════════════════════════════════════
    'quarterly_labels':     ['24Q4', '25Q1', '25Q2', '25Q3', '25Q4'],
    'quarterly_revenue':    [6.03, 5.77, 6.05, 6.11, 6.25],
    'quarterly_op_income':  [0.26, 0.50, 0.78, 0.77, 1.00],
    'quarterly_net_income': [1.95, 0.19, 0.54, 0.46, 0.12],
    'quarterly_unit':       '십억달러',

    # ══════════════════════════════════════════════════════
    # v4.0 신규 — Forward 컨센서스 (yfinance, 2026-05-07)
    # ══════════════════════════════════════════════════════
    'forward': {
        'forward_pe':       14.74,
        'trailing_pe':      33.73,
        'target_mean':      86.78,
        'target_high':      119.16,
        'target_low':       51.0,
        'target_median':    87.0,
        'analyst_count':    40,
        'recommendation_mean': 1.6,
        'recommendation_key':  'buy',
        'current_price':    70.83,
        'recommendations': {
            'strongBuy': 8, 'buy': 28, 'hold': 8, 'sell': 0, 'strongSell': 1,
        },
    },

    # ══════════════════════════════════════════════════════
    # v4.0 신규 — yfinance 뉴스 헤드라인 (최근 5건, 2026-05-07 조회)
    # ══════════════════════════════════════════════════════
    'news': [
        {
            'title':     'Analyst predicts 35% upside for Dorsey\'s Block ahead of earnings',
            'publisher': 'TheStreet',
            'link':      'https://www.thestreet.com/crypto/markets/analyst-predicts-35-upside-for-dorseys-block-ahead-of-earnings',
            'published': '2026-05-06',
            'summary':   'Block은 2026년 5월 7일 Q1 2026 실적 발표. 잭 도시의 비트코인 옹호 전략과 Cash App 수익화 가속이 핵심 관전 포인트.',
        },
        {
            'title':     'AI Layoffs Hit Crypto And Payments As Block Cuts 50%',
            'publisher': 'GuruFocus.com',
            'link':      'https://finance.yahoo.com/markets/crypto/articles/ai-layoffs-hit-crypto-payments-173606377.html',
            'published': '2026-05-06',
            'summary':   'Block, Coinbase, PayPal, Crypto.com 등이 AI를 이유로 인력 감축. 실제 효율화인지 약세 사이클의 비용 절감인지 의구심 상존.',
        },
        {
            'title':     'Block Gears Up to Report Q1 Earnings: What\'s in the Offing?',
            'publisher': 'Zacks',
            'link':      'https://finance.yahoo.com/markets/stocks/articles/block-gears-report-q1-earnings-172200454.html',
            'published': '2026-05-06',
            'summary':   'Q1 매출·EPS 컨센서스 상승 기대. 다만 비트코인 매출 컨센서스는 하락, 애널리스트 센티먼트는 다소 약화.',
        },
        {
            'title':     "What Block (XYZ)'s New AI Commerce Tools and Partnerships Mean For Shareholders",
            'publisher': 'Simply Wall St.',
            'link':      'https://finance.yahoo.com/markets/stocks/articles/block-sq-ai-commerce-tools-061520606.html',
            'published': '2026-05-06',
            'summary':   'Bank of America 4월 신규 커버리지. Square Managerbot + Uber Eats 파트너십 확대 — AI 기반 효율성·가맹점 락인 강화.',
        },
        {
            'title':     'Unlocking Q1 Potential of Block (XYZ): Exploring Wall Street Estimates for Key Metrics',
            'publisher': 'Zacks',
            'link':      'https://finance.yahoo.com/markets/stocks/articles/unlocking-q1-potential-block-xyz-131508888.html',
            'published': '2026-05-05',
            'summary':   'Wall Street Q1 핵심 지표(GPV, Cash App ARPU 등) 추정치 분석. Top-line·Bottom-line뿐 아니라 사용자 지표가 주가 모멘텀 결정.',
        },
    ],

    # ══════════════════════════════════════════════════════
    # v4.0 신규 — WebSearch + WebFetch 핵심 이슈 (2026-05-07 조사)
    # ══════════════════════════════════════════════════════
    'web_issues': [
        {
            'headline': 'Q1 2026 어닝 발표 (5/7) — 2026 가이던스 대폭 상향',
            'body':     'Block은 2026년 5월 7일 시간외에 Q1 결과를 발표한다. Zacks 컨센서스 매출 $6.11B(+5.79% YoY), EPS $0.68. 회사는 2026 연간 가이던스를 상향: '
                        'Gross Profit +18% → $12.2B, Adj. Operating Income $3.2B(+54% YoY), Adj. EPS $3.66. Q4 2025에 Cash App MAU 5,900만 회복 + Cash App GP +33% YoY.',
            'source':   'TheStreet · Zacks · Investor Relations',
            'url':      'https://investors.block.xyz/investor-news/news-details/2026/Block-to-Announce-First-Quarter-2026-Results/',
            'date':     '2026-05-07',
            'severity': '상',
        },
        {
            'headline': 'AI 명분 인력 50% 감축 (4,000명) — 2026.02 발표, 주가 +38% 점프',
            'body':     '잭 도시 CEO는 2026년 2월 직원 4,000명(전체 ~10,000명)을 해고하고 "AI-native, 린 조직"으로 재편한다고 발표했다. '
                        'Bloomberg는 "AI-washing" 의혹을 제기했고, Guardian은 "AI 생성 코드의 95%가 여전히 사람의 수정을 필요로 한다"고 보도. '
                        '발표 후 주가는 38% 상승했으나 본질적 효율 개선인지, 약세 사이클의 비용 삭감인지 의견이 엇갈린다.',
            'source':   'Bloomberg · CNN Business · The Guardian',
            'url':      'https://www.bloomberg.com/news/articles/2026-02-26/jack-dorsey-s-block-slashes-nearly-half-of-workforce-in-ai-bet',
            'date':     '2026-02-26',
            'severity': '상',
        },
        {
            'headline': 'CFPB $175M + NY DFS $40M 제재 (2025년) — Cash App 보안·AML 미흡',
            'body':     '2025년 1월 CFPB는 Cash App의 약한 보안 프로토콜로 사용자가 위험에 노출됐다며 환불 $120M + 벌금 $55M(총 $175M)을 명령. '
                        '같은 해 4월 뉴욕 DFS와는 BSA/AML 컴플라이언스 결함으로 $40M 합의. CFPB의 BNPL 규제 후퇴로 NY가 BNPL 라이선싱 입법을 선도, '
                        'CA·IL·MA가 따를 전망 — Block의 Afterpay 사업에 주(州)별 규제 비용 증가 우려.',
            'source':   'Consumer Financial Protection Bureau · American Banker',
            'url':      'https://www.consumerfinance.gov/enforcement/actions/block-inc/',
            'date':     '2025-04-15',
            'severity': '중상',
        },
        {
            'headline': 'AI Commerce 본격화 — Square Managerbot + Uber Eats 파트너십 + BoA 신규 커버리지',
            'body':     '2026년 4월 Bank of America Securities는 Block을 신규 커버리지 개시. AI 기반 효율성과 Square Managerbot, '
                        'Uber Eats 통합 파트너십을 핵심 동력으로 지목. Simply Wall St. 분석: "Block is using AI and integrated commerce '
                        'tools to deepen its role in both consumer payments and complex multi-location business operations". 다만 결제·소비자금융 경쟁 심화는 구조적 리스크로 잔존.',
            'source':   'Simply Wall St. · Bank of America Securities',
            'url':      'https://finance.yahoo.com/markets/stocks/articles/block-sq-ai-commerce-tools-061520606.html',
            'date':     '2026-04-30',
            'severity': '중상',
        },
        {
            'headline': '주요 IB 일제히 매수 상향 — Truist·HSBC·Morgan Stanley',
            'body':     '2026년 들어 주요 IB의 등급 상향이 잇따랐다. 2월 27일 Morgan Stanley가 Equal-Weight → Overweight로 상향, '
                        '3월 18일 Truist Securities·HSBC가 매수로 상향. 현재 40명 애널리스트 중 36명이 매수, 1명만 매도. 평균 목표가 $86.78 — '
                        '현재가 $70.83 대비 +21.4% 상승여력. 2025년 -26% 부진 후 본격 회복 국면.',
            'source':   'TipRanks · MarketBeat · Benzinga Korea',
            'url':      'https://www.tipranks.com/stocks/xyz/earnings',
            'date':     '2026-03-18',
            'severity': '중간',
        },
    ],
    'web_issues_research_date': '2026-05-07',
}
