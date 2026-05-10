---
name: finance-report
description: "투자 분석 보고서 자동 생성 스킬. 주식/크립토/한국기업 종목 분석 보고서(차트 + PDF + 마크다운)를 생성할 때 사용. Actions: 투자분석, 종목분석, 보고서 생성, finance report, investment report, 투자 리포트, 재무분석. Use when: 사용자가 특정 종목의 투자 분석 보고서를 만들고 싶을 때, config.py / generate_pdf.py / investment_report.md 파일 생성을 요청할 때."
argument-hint: "종목명 또는 '삼성전자 분석 보고서 만들어줘'"
license: MIT
metadata:
  author: traderparamita
  version: "4.1.0"
---

# 투자 분석 보고서 생성 스킬

## When to Use

다음 상황에서 이 스킬을 활성화한다:

- "~~ 분석 보고서 만들어줘"
- "~~ 투자 리포트 생성해줘"
- "새 종목 추가해줘"
- "finance-report", "investment report", "/finance-report"

---

## 지원 종목 유형

| 유형 | 예시 | 특이사항 |
|------|------|----------|
| 국내주식 | 삼성전자, NAVER, 카카오 | 금액 단위: 억원, 한글 폰트 필수 |
| 해외주식 | Apple, NVIDIA, Tesla | 금액 단위: 십억달러($B) |
| 크립토 | Bitcoin, Ethereum | 할빙 사이클, ETF 유입, DCA 시뮬레이션 차트 포함 |

---

## Phase 0: 섹터 감지 (인터뷰 전 자동 수행)

종목명·티커가 확보되면 **먼저 섹터를 분류**한다. 이후 Phase 1~2 전체가 섹터 분류에 따라 달라진다.

| 섹터 | 판별 기준 | 핵심 추가 지표 |
|------|----------|--------------|
| **테크 / SaaS** | 소프트웨어·플랫폼·반도체 | ARR, NRR, MAU, 클라우드 매출 비중 |
| **게임** | 게임 개발·퍼블리싱 | MAU/DAU, ARPU, IP 수, 플랫폼 비중 |
| **금융 / 보험** | 은행·증권·보험 | RBC비율(보험), NIM(은행), 손해율, 자기자본비율 |
| **소비재 / 유통** | 브랜드·리테일·식품 | 동일점포매출성장률(SSS), 브랜드 수, 재구매율 |
| **바이오 / 헬스케어** | 제약·의료기기 | 파이프라인 단계, FDA 허가 수, R&D 비율 |
| **에너지 / 산업재** | 정유·화학·건설 | EBITDA 마진, CAPEX 사이클, 수주잔고 |
| **모빌리티 / 플랫폼** | 차량호출·배달 | Gross Bookings, Take Rate, MAU |
| **기타 일반** | 위에 해당 없음 | 표준 12개 지표 |

섹터를 판별한 뒤, 해당 섹터의 "핵심 추가 지표"를 `generate_pdf.py` 산업 & 경쟁 분석 섹션과 밸류에이션 섹션에 반드시 포함한다.

---

## Phase 1: 종목 정보 수집

### 🚫 절대 금지 사항

다음 행위는 **어떤 상황에서도 금지**한다:

- 모델 학습 데이터·기억에서 주가, 시가총액, 재무수치를 꺼내 사용하는 것
- "약 ~", "추정", "대략", "~로 알려진" 등 불확실한 수치를 config.py에 기입하는 것
- 사용자가 직접 수치를 알려줬더라도 재무제표(손익·현금흐름)는 반드시 API로 조회하는 것

위반 시 목표주가·PER·상승여력 등 보고서의 모든 결론이 잘못된 수치 위에 세워진다.

### ✅ 강제 실행 순서

티커를 확보하는 즉시, **파일을 단 한 줄도 작성하기 전에** 아래 Bash를 실행한다. v4.0부터는 분기·Forward·뉴스까지 한 번에 가져오는 `fetch_full_enrichment()`를 사용한다.

> **Note**: 아래 명령어는 **현재 작업 디렉토리(cwd)가 finance-analysis 프로젝트 루트**라고 가정한다. Claude Code가 다른 디렉토리에서 실행 중이면 `cd $FINANCE_REPORTS_DIR` 또는 프로젝트 루트로 이동 후 실행한다.

```bash
# python3 명령이 가능하면 그대로, 가상환경이 있다면 .venv/bin/python 사용
python3 - <<'EOF'
import sys, os
# 프로젝트 루트(=run.py가 있는 디렉토리)를 sys.path에 추가
sys.path.insert(0, os.getcwd())
from shared.data_fetcher import fetch_full_enrichment
import json
data = fetch_full_enrichment('{{TICKER}}')
print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
EOF
```

반환된 JSON을 그대로 config.py의 해당 키에 채운다. v4.0 신규 키:
- `quarterly_labels`, `quarterly_revenue`, `quarterly_op_income`, `quarterly_net_income`, `quarterly_unit`
- `forward` (dict): `forward_pe`, `trailing_pe`, `target_mean/high/low/median`, `analyst_count`, `recommendation_mean`, `recommendation_key`, `recommendations` (buy/hold/sell 분포), `current_price`
- `news` (list): yfinance 뉴스 헤드라인 최근 10건

| fetch 결과 | 처리 방법 |
|-----------|----------|
| 데이터 정상 반환 | 반환값 그대로 사용, 사용자에게 "yfinance 기준 YYYY-MM-DD 시세" 명시 |
| 빈 dict `{}` 반환 | 파일 생성 중단, "티커를 찾을 수 없습니다. 정확한 티커를 알려주세요" 안내 |
| 예외 발생 | 에러 메시지를 사용자에게 그대로 보여주고 수동 입력 요청 |

**yfinance가 제공하지 않는 항목** (SWOT, 사업부문 비중, 경쟁사 수치, 섹터 특화 지표)은 모델의 최신 공개 지식을 활용하되, 반드시 출처 시점을 "공개 자료 기준" 으로 명시한다.

### 인터뷰 (사용자 질문)

API로 가져올 수 없는 항목만 질문한다. **한 번에 모두 질문**한다.

```
📊 투자 분석 보고서를 만들겠습니다!

아래 항목은 yfinance API로 자동 조회합니다:
  → 현재 주가, 시가총액, 연도별 매출/영업이익/순이익/ROE/ROA/현금흐름, 보고일

다음 정보만 입력해주세요 (모르는 항목은 "알아서" OK):

  1. 종목명 (한글/영문):
  2. 티커 (예: UBER, AAPL, 259960.KS, BTC-USD):
  3. 종목 유형: 국내주식 / 해외주식 / 크립토
  4. 투자의견 (매수 / 중립 / 매도):
  5. 목표주가 (없으면 "알아서" — 섹터별 배수로 자동 계산):
  6. 저장 폴더명 (예: samsung, apple, uber):
```

답변을 받으면 즉시 fetch → 섹터 감지 → Phase 1.5 → Phase 2 진입 순서로 처리한다.

---

## Phase 1.5: 데이터 깊이 확장 + 이슈 검색 (v4.0 신규)

`fetch_full_enrichment()`가 분기·Forward·뉴스를 자동으로 가져왔다면, 이제 **현재 가장 이슈가 되는 사안**을 외부 검색으로 보강한다. 이 단계가 보고서의 "지금 이 종목에 무슨 일이 벌어지고 있는가"를 결정한다.

### 1) WebSearch — 핵심 이슈 + 창업자 발굴

다음 5개 쿼리를 모두 실행한다 (영문 종목은 영문 쿼리도 병행):

```
1. "{종목명} {티커} latest earnings 2026"           # 최근 실적/가이던스
2. "{종목명} {티커} news lawsuit regulation"         # 소송·규제 이슈
3. "{종목명} {티커} M&A acquisition partnership"    # 사업 변화
4. "{종목명} 주가 전망 분석"  (한국어 — 국내 시각도 확인)
5. "{종목명} 창업자 {founder_name} 인터뷰 자서전 창업 스토리" (★ v4.1) — 창업 배경/철학
```

5번 쿼리는 창업자 이름을 모르는 경우 "{종목명} founder history origin story"로 영문 검색하여 창업자 이름부터 확보한 뒤 후속 검색을 진행한다.

각 검색 결과 상위 3~5개 중 **임팩트가 큰 3~5건**을 선별한다. 선별 기준:
- 보고일 기준 30~90일 이내 발생
- 실적·가이던스 발표, 주요 임원 변경, 대형 M&A, 소송·규제, 신제품 출시
- 단순 가격 변동 코멘트는 제외

### 2) WebFetch — 본문 인용 (이슈 + 창업자)

선별된 핵심 이슈 3~5건과 **창업자 인터뷰·자서전 1~2건** 각각에 대해 WebFetch로 원문을 가져와 **핵심 문장 1~2개를 직접 인용**한다. 인용 시 출처(언론사명·서적명)와 보도 날짜를 반드시 함께 기록한다.

```
WebFetch 프롬프트 예시:
"이 기사에서 {종목명}의 실적/가이던스/규제/M&A 관련 핵심 정보를 2~3문장으로 추출하고,
인용할 만한 직접 인용문 1~2개를 따옴표 포함하여 그대로 가져와라."
```

### 3) 이슈 카드 데이터 구조

각 이슈는 `generate_pdf.py`에서 `issue_card()` 헬퍼에 다음 형태로 전달한다:

```python
issue_card(
    headline='Block, Q1 2026 어닝 비트, Cash App MAU 5,800만 돌파',
    body='Block은 2026년 1분기 EPS $0.72(컨센서스 $0.65 비트)와 매출 $6.5B를 발표했다. ...',
    source='Bloomberg',
    url='https://www.bloomberg.com/news/...',
    date='2026-04-30',
    severity='상',  # 상 / 중상 / 중간 / 낮음
    styles=STY,
)
```

심각도(severity)는 투자 결정에 미치는 영향 기준:
- **상**: 가이던스 변경, 대형 M&A, 핵심 임원 사임, 중대 소송 패소
- **중상**: 실적 비트/미스, 규제 변화, 신제품 출시 지연
- **중간**: 일반적 실적 코멘트, 애널리스트 등급 변화
- **낮음**: 시장 분위기 코멘트

### 4) 뉴스 카드 (yfinance)

`cfg['news']` 리스트의 상위 6~8건을 PDF에 `news_card()`로 자동 삽입한다. WebSearch로 발굴한 이슈와 중복되더라도 yfinance 헤드라인은 별도 섹션으로 배치 (timestamp 보강 효과).

---

## Phase 2: 파일 생성

### ★ 공통 엔진 구조 (v2.0)

```
finance_analysis/
├── shared/
│   ├── chart_engine.py   ← 차트 12개 공통 로직 (수정 금지)
│   └── pdf_utils.py      ← PDF 스타일/빌드 유틸 (수정 금지)
│
├── stocks/{폴더명}/
│   ├── config.py             ← ★ 재무 데이터 + 색상 + 메타데이터
│   ├── generate_charts.py    ← 고정 래퍼
│   ├── generate_pdf.py       ← 회사 고유 서술
│   └── investment_report.md
│
└── run.py
```

---

## config.py 작성 규칙

```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # ── 기본 정보 (yfinance 반환값으로 채움) ──
    'name':        '종목명',
    'ticker':      '티커코드',
    'exchange':    'NASDAQ',
    'price':       '$00.00',          # fetch 반환값
    'mkt_cap':     '$000B',           # fetch 반환값
    'opinion':     '매수 (Buy)',
    'target':      '목표주가',        # 아래 밸류에이션 기준으로 계산
    'report_date': 'YYYY년 MM월 DD일', # fetch 반환값
    'header_text': '종목명 (티커) 투자 분석 보고서',
    'pdf_filename': '종목명_investment_report.pdf',
    'base_dir':    BASE_DIR,
    'unit':        '십억달러',        # fetch 반환값 기준
    'revenue_label': '매출액',

    'colors': {
        'primary': '#색상코드',
        'accent':  '#색상코드',
        'green':   '#2ECC71',
        'red':     '#E74C3C',
        'purple':  '#8E44AD',
        'gray':    '#95A5A6',
    },

    # ── 이하 모두 fetch 반환값 그대로 ──
    'years':        [...],   # fetch['years']
    'revenue':      [...],   # fetch['revenue']
    'op_income':    [...],   # fetch['op_income']
    'net_income':   [...],   # fetch['net_income']
    'op_margin':    [...],   # fetch['op_margin']
    'net_margin':   [...],   # fetch['net_margin']
    'roe':          [...],   # fetch['roe']
    'roa':          [...],   # fetch['roa']
    'debt_ratio':   [...],   # fetch['debt_ratio']
    'current_ratio':[...],   # fetch['current_ratio']
    'debt_label':   '부채비율 (%)',
    'stability_secondary_label': '유동비율 (%)',
    'rev_growth':   [...],   # fetch['rev_growth']
    'op_growth':    [...],   # fetch['op_growth']
    'ni_growth':    [...],   # fetch['ni_growth']
    'ocf':          [...],   # fetch['ocf']
    'icf':          [...],   # fetch['icf']
    'fin_cf':       [...],   # fetch['fin_cf']
    'capex':        [...],   # fetch['capex']
    'fcf':          [...],   # fetch['fcf']

    # ── 사업부문 (공개 자료 기준, 비중 직접 작성) ──
    'seg_labels': ['부문명 (비중%)', ...],
    'seg_sizes':  [숫자, ...],
    'sub_labels': [...],   # 선택: 지역별 비중
    'sub_sizes':  [...],
    'sub_title':  '지역별 매출 비중',

    # ── SWOT (공개 자료·섹터 분석 기반으로 작성) ──
    'swot': {
        '강점': ['• 항목1', ...],
        '약점': ['• 항목1', ...],
        '기회': ['• 항목1', ...],
        '위협': ['• 항목1', ...],
    },

    # ── 투자매력도 레이더 ──
    'radar_categories': ['수익성', '성장성', '안정성', '밸류에이션', '섹터지표1', '섹터지표2'],
    'radar_scores':     [숫자, ...],  # 10점 만점

    # ── ★ v4.1 신규 — 창업자 & 창업 스토리 (선택, 없으면 섹션 자동 스킵) ──
    'founder': {
        'name':       '잭 도시 (Jack Dorsey)',
        'role':       'CEO / Block Head / 공동창업자',
        'born':       '1976년 11월, 미국 미주리 세인트루이스',
        'background': '뉴욕대 중퇴, 2006년 Twitter 공동창업, 2009년 Square(현 Block) 창업',
        'philosophy': '"Economic Empowerment" — 기술로 경제 시스템 접근권 확장',
        'timeline': [
            {'year': '2006', 'event': 'Twitter 공동창업', 'note': 'CEO 역임 후 2008년 해임'},
            {'year': '2009', 'event': 'Square 창업', 'note': '소상공인 카드결제 단말 출시'},
            {'year': '2013', 'event': 'Cash App 출시', 'note': 'P2P 송금으로 소비자 시장 진입'},
            {'year': '2021', 'event': '사명 Block으로 변경', 'note': '비트코인·블록체인 비전 강조'},
            {'year': '2025', 'event': '티커 SQ → XYZ 변경', 'note': '핀테크 슈퍼앱 정체성 재정의'},
        ],
        'quotes': [
            {'text': 'AI should replace the middle manager.', 'source': 'CoinDesk 인터뷰', 'date': '2026-04-01'},
            {'text': '...', 'source': 'WSJ', 'date': '2026-02-26'},
        ],
    },
}
```

---

## generate_charts.py 고정 템플릿

```python
#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.chart_engine import generate_all_charts
from stocks.{폴더명}.config import CONFIG

if __name__ == '__main__':
    generate_all_charts(CONFIG)
```

---

## generate_pdf.py 작성 규칙

### 공통 보일러플레이트

```python
#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.platypus import PageBreak
from shared.pdf_utils import (
    build_pdf, make_table, tip_box, chart_image, hr_line, sp, make_styles,
    news_card, issue_card, quarterly_momentum_table, forward_consensus_table,
    founder_card, founder_quote_card, founder_timeline_table,  # ★ v4.1
)
from stocks.{폴더명}.config import CONFIG

CFG = CONFIG
BASE = CFG['base_dir']
STY = make_styles(CFG['colors']['primary'], CFG['colors']['accent'])
PRIMARY_HEX = CFG['colors']['primary']

from reportlab.platypus import Paragraph
def P(text, key='body'): return Paragraph(text, STY[key])
def img(name, width_cm=16):
    from reportlab.lib.units import cm
    return chart_image(BASE, name, width=width_cm * cm, styles=STY)
def tip(text): return tip_box(text, STY)
def hr():  return hr_line(CFG['colors']['accent'])
def tbl(headers, rows, widths=None):
    return make_table(headers, rows, col_widths=widths, primary_hex=PRIMARY_HEX)
```

### PDF 섹션 순서 (v4.1 — 반드시 준수)

1. 표지
2. 목차
3. 기업 개요
4. **창업자 & 창업 스토리 (founder_card + founder_timeline_table + founder_quote_card) ★ v4.1 신규**
5. 비전 & 전략
6. 사업 모델 분석
7. 재무 분석 (chart1, chart7)
8. 수익성 분석 (chart2, chart3)
9. 성장성 분석 (chart5)
10. 재무 안정성 (chart4)
11. 현금흐름 분석 (chart9, chart10, chart11)
12. 산업 & 경쟁 분석 (chart6)
13. SWOT & 리스크 분석 (chart8)
14. 분기 모멘텀 & 애널리스트 컨센서스 (chart13, chart14, chart15) ★ v4.0
15. 최신 이슈 & 뉴스 브리핑 (WebSearch + WebFetch + yfinance news) ★ v4.0
16. 밸류에이션 & 결론 (chart12)
17. 면책 고지

### 섹션별 서술 기준 (품질 체크리스트)

각 섹션을 작성할 때 아래 기준을 모두 충족해야 한다.

#### 3. 기업 개요 (3~5문장)
- [ ] 설립 연도·배경·창업자 또는 전환점
- [ ] 핵심 사업 한 줄 요약 (무엇을 누구에게 팔거나 연결하는가)
- [ ] 현재 시장 내 포지션 (1위/2위/niche 등)
- [ ] 최근 1~2년 중 가장 중요한 전략 변화 한 가지
- [ ] `tip()`: 비즈니스 모델을 초보자도 이해할 수 있는 1~2문장 비유

#### 4. 창업자 & 창업 스토리 (★ v4.1 신규)
- [ ] `founder_card(CFG['founder'], STY)` 호출 — 이름·역할·출생·약력·핵심 철학
- [ ] `founder_timeline_table(CFG['founder']['timeline'])` 호출 — 창업~성장 변곡점 3~5개 (연도/사건/맥락)
- [ ] `founder_quote_card()` 1~2개 호출 — 인터뷰·자서전 직접 인용
- [ ] WebSearch + WebFetch로 인용문 1차 출처를 확인 (전문 인용 시 출처·날짜 필수)
- [ ] 창업자 정보가 부족한 경우 founder dict 비워두면 섹션 자동 스킵 (backward-compat)
- [ ] `tip()`: "왜 창업자 이해가 투자에 중요한가" 한 줄 (예: 의사결정 스타일·리스크 성향·장기 전략 일관성)

#### 5. 비전 & 전략 (표 + 서술)
- [ ] 회사의 공식 미션/비전 문구
- [ ] 전략 방향 3~5개를 표로 정리 (전략명 / 구체적 내용)
- [ ] 현재 추진 중인 M&A·파트너십·신사업 중 핵심 1~2개 심층 서술
- [ ] 해당 전략이 3~5년 뒤 재무에 미치는 기대 효과 언급

#### 6. 사업 모델 분석 (chart6 + 표)
- [ ] 수익 구조 한 줄 설명 (어떻게 돈을 버는가)
- [ ] 사업부문별 매출 비중 표 (chart6와 일치)
- [ ] 섹터 특화 지표 포함 (아래 "섹터별 핵심 지표" 참고)
- [ ] 지역별/채널별 비중이 있으면 sub_labels로 추가

#### 7. 재무 분석 (표 + chart1, chart7)
- [ ] 5개년(또는 yfinance 제공 연도) 손익 테이블
- [ ] 전년 대비 가장 큰 변화 1~2개를 굵은 글씨로 강조
- [ ] 일회성 항목이 있으면 반드시 주석 처리 (예: "세금 환입 일회성 포함")
- [ ] `tip()`: 매출/영업이익/순이익 3가지의 차이를 초보자용으로 설명

#### 8. 수익성 분석 (chart2, chart3)
- [ ] ROE·ROA·영업이익률 테이블
- [ ] 동종 업계 평균 또는 경쟁사와 비교 한 문장
- [ ] 수익성 개선/악화의 구체적 원인 서술 (비용 구조, Mix shift 등)

#### 9. 성장성 분석 (chart5)
- [ ] YoY 성장률 테이블
- [ ] 성장 동력이 된 이벤트를 연도별로 1줄씩 서술 (예: "2024년 +41.8% — 인도 수익화 가속")
- [ ] 향후 성장 촉매 2~3개 전망

#### 10. 재무 안정성 (chart4)
- [ ] 부채비율·유동비율 테이블
- [ ] "이 수치가 왜 안전/위험한가"를 업종 기준으로 설명
- [ ] 최대 위험 시나리오 한 줄 언급

#### 11. 현금흐름 분석 (chart9, chart10, chart11)
- [ ] OCF/ICF/FCF 테이블
- [ ] "이익과 현금흐름의 차이"를 구체적 수치로 설명
- [ ] CAPEX 성격 판단: 유지보수 vs 성장투자
- [ ] `tip()`: FCF가 왜 중요한지 초보자용 설명

#### 12. 산업 & 경쟁 분석 (chart6)
- [ ] 경쟁사 3~4개를 표로 비교 (매출, 영업이익률, PER, 특징)
- [ ] 섹터 특화 지표로 비교 (아래 "섹터별 핵심 지표" 참고)
- [ ] 이 회사의 차별화 포인트 3가지 명시

#### 13. SWOT & 리스크 (chart8)
- [ ] 강점·약점·기회·위협 각 4~5개 (chart8과 일치)
- [ ] 리스크 테이블: 리스크명 / 심각도(상/중상/중/낮음) / 내용 / 모니터링 포인트
- [ ] 심각도 "상" 이상의 리스크는 반드시 하나 이상 포함

#### 14. 분기 모멘텀 & 애널리스트 컨센서스 (★ v4.0)
- [ ] `quarterly_momentum_table(CFG)` 호출 — 최근 8분기 매출/영업이익/순이익 테이블
- [ ] `chart13_quarterly_momentum.png` 삽입
- [ ] 분기별 변곡점 1~2개를 굵은 글씨로 강조 (예: "24Q3 마진 점프 — Afterpay 흑자 전환")
- [ ] `forward_consensus_table(CFG)` 호출 — Forward PER + 목표가 분포 + 추천 등급
- [ ] `chart14_analyst_consensus.png`, `chart15_recommendation_pie.png` 삽입
- [ ] 애널리스트 평균 목표가와 본 보고서 목표가의 차이를 1~2문장으로 비교
- [ ] `tip()`: "왜 분기 데이터가 연간 데이터보다 빠른 신호인가" 초보자 설명

#### 15. 최신 이슈 & 뉴스 브리핑 (★ v4.0)
- [ ] WebSearch로 발굴 + WebFetch로 본문 인용한 핵심 이슈 3~5건을 `issue_card()`로 렌더링
- [ ] 각 이슈마다: 헤드라인, 2~3문장 본문, 직접 인용문, 출처(언론사·날짜·URL), 심각도
- [ ] 심각도 "상" 또는 "중상" 이슈가 최소 1건 포함 (없으면 추가 검색)
- [ ] yfinance 뉴스 헤드라인 6~8건을 별도 서브섹션 "데이터 소스: yfinance 헤드라인"으로 `news_card()` 렌더링
- [ ] 섹션 마지막에 한 줄 종합 코멘트: "최근 30~90일 핵심 변화 한 줄 요약"
- [ ] WebSearch/WebFetch 조사 시점을 보고서에 명시 (예: "2026-05-07 조사 기준")

#### 16. 밸류에이션 & 결론
- [ ] 아래 "섹터별 밸류에이션 방법론"에 따라 목표주가 계산
- [ ] 밸류에이션 테이블 (지표명 / 현재값 / 해석)
- [ ] radar chart (chart12)
- [ ] 핵심 투자 포인트 ①~⑥ 불릿 형식
- [ ] 투자의견 + 목표주가 + 단기 리스크 한 줄

---

## 섹터별 핵심 지표 (산업 분석 + 밸류에이션 섹션에 반드시 포함)

### 테크 / SaaS
- **핵심 지표**: ARR(연간반복수익), NRR(순수익유지율), 클라우드 매출 비중, R&D 비율
- **경쟁사 비교 추가 컬럼**: ARR 성장률, Gross Margin, Rule of 40
- **밸류에이션**: PER(Forward) 25~40x, EV/Sales 5~10x (성장률 따라 조정)

### 게임
- **핵심 지표**: MAU/DAU, ARPU, 플랫폼별 매출 비중, 신작 파이프라인 수
- **경쟁사 비교 추가 컬럼**: MAU, ARPU, IP 수
- **밸류에이션**: PER 15~25x, EV/EBITDA 10~18x

### 모빌리티 / 플랫폼
- **핵심 지표**: Gross Bookings, Take Rate, MAU, 광고 매출 비중
- **경쟁사 비교 추가 컬럼**: Gross Bookings, Take Rate, 영업이익률
- **밸류에이션**: EV/EBITDA 20~30x, FCF Yield 3~6%

### 금융 / 보험
- **핵심 지표**: NIM(순이자마진, 은행), RBC비율(보험), 손해율, 자기자본비율
- **경쟁사 비교 추가 컬럼**: NIM 또는 합산비율, ROE, 배당수익률
- **밸류에이션**: PBR 0.8~1.5x, PER 8~15x

### 소비재 / 유통
- **핵심 지표**: 동일점포매출성장률(SSS), 브랜드/SKU 수, 재구매율, 마케팅비 비율
- **경쟁사 비교 추가 컬럼**: SSS, 영업이익률, 브랜드 수
- **밸류에이션**: EV/EBITDA 12~18x, PER 18~25x

### 바이오 / 헬스케어
- **핵심 지표**: 파이프라인 단계(Phase 1/2/3), FDA 허가 수, R&D 비율, 특허 만료 일정
- **경쟁사 비교 추가 컬럼**: 파이프라인 수, R&D/매출, 최근 허가 수
- **밸류에이션**: EV/Sales 3~8x (흑자 전 기업은 파이프라인 가치 별도 산정)

### 에너지 / 산업재
- **핵심 지표**: EBITDA 마진, CAPEX 사이클, 수주잔고(Backlog), 가동률
- **경쟁사 비교 추가 컬럼**: EBITDA 마진, 수주잔고, 배당수익률
- **밸류에이션**: EV/EBITDA 6~12x, PBR 1~2x

### 기타 일반
- 표준 지표(PER, PBR, EV/EBITDA, FCF Yield)로 밸류에이션
- **밸류에이션**: PER 산업 평균 기준 ±20% 범위

---

## 섹터별 목표주가 계산 방법론

"알아서" 또는 목표주가 미제공 시 아래 공식으로 계산한다. **반드시 계산 근거를 generate_pdf.py 밸류에이션 섹션에 명시**한다.

```
목표주가 계산 흐름:
1. 섹터 감지 → 해당 섹터의 대표 밸류에이션 배수 선택
2. 최신 연도 또는 Forward(+1년) 지표 추정값 사용
3. 기업가치(EV) = 지표 × 배수
4. 주당가치 = (EV - 순부채) / 발행주식수
5. 목표주가 = 주당가치 (소수 첫째 자리 반올림)
6. 상승여력 = (목표주가 / 현재주가 - 1) × 100%
```

계산 예시 (EV/EBITDA 기준):
```
EBITDA(최신) = 영업이익 + 감가상각 ≈ op_income × 1.15 (보수적 추정)
EV = EBITDA × 섹터 배수
순부채 = 총부채 - 현금 (yfinance balance sheet에서 추출 or 0 근사)
주당가치 = (EV - 순부채) / shares_outstanding
```

목표주가 계산 결과와 함께 "어떤 배수를 왜 적용했는지" 1~2문장으로 반드시 서술한다.

---

## investment_report.md 작성 규칙

```markdown
# {종목명} 투자 분석 보고서

> **투자의견: {의견}** | **목표주가: {가격}** | **현재주가: {가격}** | **상승여력: {%}**
> 작성일: {날짜} | 데이터 출처: yfinance API 실시간 조회

## 핵심 투자 포인트
| 구분 | 내용 |
|------|------|
| ① | ... |
...

## 1. 기업 개요
## 2. 비전 & 전략
## 3. 사업 모델 분석
## 4. 재무 분석 (표 + 차트)
## 5. 수익성 분석
## 6. 성장성 분석
## 7. 재무 안정성
## 8. 현금흐름 분석
## 9. 산업 & 경쟁 분석
## 10. SWOT 분석
## 11. 밸류에이션 & 결론
## 면책 고지
```

---

## run.py 등록

```python
COMPANIES = {
    '기존종목': 'stocks.기존종목',
    '{새종목}': 'stocks.{폴더명}',  # 추가
}
```

---

## Phase 3: 실행 및 완료 안내

파일 생성 후 즉시 실행하여 오류 없이 완료되는지 확인한다. 현재 작업 디렉토리는 프로젝트 루트(`run.py` 있는 곳)여야 한다.

```bash
python3 run.py {종목명}
```

완료 후 사용자에게 안내:

```
✅ {종목명} 투자 분석 보고서 생성 완료!

📊 yfinance 조회: {티커} / {조회일} 기준
📁 생성 파일: stocks/{폴더명}/
   ├── config.py
   ├── generate_charts.py
   ├── generate_pdf.py
   ├── investment_report.md
   └── {종목명}_investment_report.pdf  ← 최종 보고서

🎯 섹터: {감지된 섹터}
💰 목표주가: {가격} (현재 {현재가} 대비 {상승여력}%)
   근거: {배수} × {지표명} {값} 적용

▶️ 재실행:
   python run.py {종목명}          # 차트 + PDF
   python run.py {종목명} --pdf    # PDF만
```

---

## 주의사항

- 폰트 경로 `/System/Library/Fonts/Supplemental/AppleGothic.ttf`는 macOS 전용
- 금액 단위: 국내 억원, 해외 십억달러($B), 크립토 USD — fetch 반환 `unit` 키 따름
- 차트 저장 경로는 config.py의 `base_dir` 기준 — 절대경로 직접 사용 금지
- `generate_charts.py`는 항상 고정 래퍼 형식 — 차트 로직 직접 작성 금지
- 암호화폐(`cryptocurrency/`)는 레거시 구조 유지 (공통 엔진 미적용)
