---
name: finance-brief
description: "투자 브리프 1~2페이지 압축 보고서 생성 스킬. 회사 개요·Valuation·Forward 관점 3개 섹션만 담는다. Actions: 1페이지 보고서, 한장 브리프, brief, summary, 압축 보고서, finance-brief. Use when: 사용자가 \"~~ 1페이지로\", \"한 장으로\", \"브리프\", \"간단 분석\"을 요청할 때."
argument-hint: "종목명 또는 '삼성전자 1페이지 브리프'"
license: MIT
metadata:
  author: traderparamita
  version: "1.2.0"
---

# 투자 브리프 생성 스킬 (finance-brief)

## When to Use

다음 상황에서 활성화:
- "~~ 한 장으로 정리해줘"
- "~~ 1페이지 보고서"
- "~~ 브리프 만들어줘"
- "/finance-brief", "finance brief", "투자 브리프"
- 시간 압박 상황에서 의사결정용 압축 자료가 필요할 때

`finance-report`(전체 16~17페이지)와 차이:
- finance-report = 풀 스펙 분석 (재무/현금흐름/SWOT/창업자/이슈 등 14~15섹션)
- **finance-brief = 압축 2페이지** (회사 개요 + Valuation + Forward 관점만)

## 결과물

**Page 1**
- 헤더 박스: 종목명·티커·거래소·현재가·시가총액·투자의견·목표가
- **★ v1.2 신규 — 스냅샷 패널** (3행: 주가 포지션 / 최근 분기 / 다음 이벤트)
- 1. 회사 개요 (3~4문장)
- 2. Valuation 표 (PER, EV/EBITDA, FCF Yield, 컨센 목표가, 본 보고서 목표가 등)
- 차트 1 — 분기 모멘텀 (chart13) 또는 폴백으로 연간 매출/영업이익 (chart1)

**Page 2**
- **★ v1.2 신규 — 컨빅션 + 체크리스트 + 피어 비교 패널** (한 행 컴팩트 배지)
- 3. Forward 관점 (향후 12~24개월)
  - 핵심 촉매 (Catalysts) 3~4개
  - 핵심 리스크 (Risks) 3~4개
  - **★ v1.2 신규 — 의사결정 트리거 (Kill Switch)** 3~4개 (비중 축소 조건)
  - 시나리오 (Bull / Base / Bear) — 목표가·확률·전제 표
- 차트 2 — 애널리스트 컨센서스 (chart14) 또는 폴백으로 레이더 (chart12)
- 한 줄 결론
- 면책 (3줄)

**v1.2 의사결정 가치 향상 — 4개 키 추가**
1. `price_position` (자동, yfinance) — 52주 레인지·분위·20일 이평
2. `forward_thesis.next_catalyst` (수동) — 다음 실적 발표일·컨센·체크포인트
3. `forward_thesis.last_quarter` (자동 폴백) — 한 줄 재무 요약
4. `forward_thesis.conviction` + `checklist` + `kill_switch` + `peer_comparison` — 의사결정 강도

---

## Phase 0: 종목 확인 + 분기 처리

종목 폴더(`$HOME/finance-reports/stocks/{폴더명}/config.py`) 존재 여부로 분기:

| 경우 | 처리 |
|------|------|
| ✅ **폴더 있음** | Phase 1로 직진 — 기존 config 활용, forward_thesis만 갱신해 brief 생성 |
| ⚠️ **폴더 없음** | **Phase 0.5 Quick Setup 자가 워크플로우 진입** (★ v1.1) — 인터뷰 → fetch → 최소 config 자동 생성 → 차트 → brief PDF |

폴더 존재 확인:
```bash
test -f $HOME/finance-reports/stocks/{폴더명}/config.py && echo "EXISTS" || echo "NEW"
```

---

## Phase 0.5: Quick Setup — 자가 워크플로우 (★ v1.1, 종목 폴더 없을 때)

`finance-report` 호출 없이 brief 단독으로 새 종목을 30~60초 안에 처리한다. 풀 보고서 대비 분석 깊이는 얕지만 의사결정용 1~2페이지 자료로 충분.

### 1) 인터뷰 (한 번에)

```
📊 1페이지 브리프를 빠르게 만들겠습니다!

다음 정보만 입력해주세요:
  1. 종목명 (한글/영문):
  2. 티커 (예: UBER, AAPL, 259960.KS):
  3. 투자의견 (매수/중립/매도, 모르면 "알아서"):
  4. 목표주가 (모르면 "알아서" — 컨센·섹터 배수 자동 계산):
  5. 저장 폴더명 (영문 권장, 예: block, samsung):
```

### 2) fetch_full_enrichment 실행

```bash
python3 - <<'EOF'
import sys, os; sys.path.insert(0, os.getcwd())
from shared.data_fetcher import fetch_full_enrichment
import json
data = fetch_full_enrichment('{{TICKER}}')
print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
EOF
```

빈 dict 반환 시 "티커를 찾을 수 없습니다" 안내 후 중단.

### 3) WebSearch 압축 (2개)

풀 보고서의 5개 쿼리 대신 **brief 핵심 2개**:
```
1. "{종목명} {티커} latest earnings 2026 guidance"   # 실적·가이던스
2. "{종목명} 주가 전망 2026"                          # 국내 컨센
```

각 결과 상위 1~2건을 `forward_thesis.catalysts/risks` 작성에 활용. WebFetch 본문 인용은 brief에서는 생략(사용자 요청 시만).

### 4) 최소 config.py 자동 생성

`stocks/{폴더명}/__init__.py` (빈 파일) + `config.py` 생성. **brief 빌드에 꼭 필요한 키만** (SWOT·세그먼트·창업자 등 풀 보고서 전용 키는 빈 값으로 둠 — backward-compat):

```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # ── 기본 정보 (fetch 그대로 + 인터뷰 답변) ──
    'name':        '{종목명}',
    'ticker':      '{티커}',
    'exchange':    '{거래소}',
    'price':       '{fetch.price}',
    'mkt_cap':     '{fetch.mkt_cap}',
    'opinion':     '{투자의견}',
    'target':      '{목표가} (현재 {price} 대비 {±%})',
    'report_date': '{fetch.report_date}',
    'header_text': '{종목명} ({티커}) 1페이지 브리프',
    'pdf_filename':  '{폴더명}_investment_report.pdf',  # 호환용
    'brief_filename':'{폴더명}_brief.pdf',
    'base_dir':    BASE_DIR,
    'unit':        '{fetch.unit}',
    'revenue_label': '매출액',

    'colors': {
        'primary': '#1B4F72',  # 디폴트 (요청 시 종목 컬러로 변경)
        'accent':  '#E67E22',
        'green':   '#27AE60',
        'red':     '#C0392B',
        'gray':    '#7F8C8D',
        'teal':    '#2E86AB',
    },

    # ── 연간 재무 (fetch 그대로) ──
    'years': [...], 'revenue': [...], 'op_income': [...], 'net_income': [...],
    'op_margin': [...], 'net_margin': [...], 'roe': [...], 'roa': [...],
    'debt_ratio': [...], 'current_ratio': [...],
    'debt_label': '부채비율 (%)', 'stability_secondary_label': '유동비율 (%)',
    'rev_growth': [...], 'op_growth': [...], 'ni_growth': [...],
    'ocf': [...], 'icf': [...], 'fin_cf': [...], 'capex': [...], 'fcf': [...],

    # ── chart6/8/12 호환용 디폴트 (brief에는 안 쓰이지만 generate_all_charts 안전) ──
    'seg_labels': ['핵심 사업 (100%)'], 'seg_sizes': [100],
    'swot': {'강점': [], '약점': [], '기회': [], '위협': []},
    'radar_categories': ['수익성', '성장성', '안정성', '밸류에이션', '시장지위', '미래모멘텀'],
    'radar_scores':     [5, 5, 5, 5, 5, 5],

    # ── 분기·Forward·뉴스 (fetch 그대로) ──
    'quarterly_labels': [...], 'quarterly_revenue': [...],
    'quarterly_op_income': [...], 'quarterly_net_income': [...],
    'quarterly_unit': '{fetch.quarterly_unit}',
    'forward': {...},   # fetch['forward']
    'news':    [...],   # fetch['news'] 상위 5건

    # ── ★ brief 핵심: forward_thesis (Claude가 fetch + WebSearch 기반으로 작성) ──
    'forward_thesis': {
        'overview':  '3~4문장 회사 개요',
        'catalysts': ['•...', '•...', '•...'],
        'risks':     ['•...', '•...', '•...'],
        'scenarios': [
            {'case': 'Bull', 'price': '...', 'prob': 25, 'thesis': '...'},
            {'case': 'Base', 'price': '...', 'prob': 50, 'thesis': '...'},
            {'case': 'Bear', 'price': '...', 'prob': 25, 'thesis': '...'},
        ],
        'one_line':  '한 줄 결론',
    },
}
```

### 5) 차트 + brief 빌드 (한 번에)

```bash
python3 - <<'EOF'
import sys, os; sys.path.insert(0, os.getcwd())
from shared.chart_engine import generate_all_charts
from shared.brief_builder import build_brief
from stocks.{폴더명}.config import CONFIG
generate_all_charts(CONFIG)
build_brief(CONFIG)
EOF
```

`generate_all_charts`가 12개 표준 + chart13/14/15(옵션)을 생성하지만, brief PDF에는 **chart13/14만 실제 삽입**(`brief_builder._pick_chart` 폴백). 나머지 차트 PNG는 디스크에 남아 향후 풀 보고서 만들 때 재활용 가능.

### 6) run.py 등록 (선택, 다음 실행 편의)

`run.py`의 `COMPANIES` dict에 `'{종목명}': 'stocks.{폴더명}'` 한 줄 추가하면 다음부터:
```bash
python run.py {종목명} --brief    # brief 갱신
python run.py {종목명}            # 풀 보고서로 승격
```

---

## Phase 1: 데이터 보강 (기존 종목, 선택)

`config.py`가 이미 있고 `quarterly_*`, `forward`, `news` 등이 채워져 있다면 추가 fetch 불필요.
오래된 config라면 `fetch_full_enrichment()`로 재조회 권장.

```bash
python3 - <<'EOF'
import sys, os; sys.path.insert(0, os.getcwd())
from shared.data_fetcher import fetch_full_enrichment
import json
data = fetch_full_enrichment('{{TICKER}}')
print(json.dumps({k: data.get(k) for k in ['price', 'mkt_cap', 'forward']}, indent=2, ensure_ascii=False, default=str))
EOF
```

---

## Phase 2: forward_thesis 작성 (브리프 핵심)

`config.py`에 `forward_thesis` dict를 추가한다. **없으면 SWOT/web_issues에서 자동 폴백**되지만, 품질 좋은 브리프를 위해 직접 작성 권장.

```python
'forward_thesis': {
    'overview': '3~4문장 회사 개요 (핵심 비즈니스 + 최근 변화 + 시장 위치)',

    'catalysts': [
        '• 향후 12~24M 핵심 촉매 1 (구체 수치 포함)',
        '• 촉매 2',
        '• 촉매 3',
        '• 촉매 4 (선택)',
    ],

    'risks': [
        '• 단기·중기 리스크 1 (모니터링 포인트 포함)',
        '• 리스크 2',
        '• 리스크 3',
    ],

    'scenarios': [
        {'case': 'Bull', 'price': '$110', 'prob': 25,
         'thesis': '낙관 시나리오 핵심 전제 (1~2 키워드)'},
        {'case': 'Base', 'price': '$85',  'prob': 50,
         'thesis': '베이스 시나리오 핵심 전제'},
        {'case': 'Bear', 'price': '$55',  'prob': 25,
         'thesis': '비관 시나리오 핵심 전제'},
    ],

    'one_line': '투자 의견 + 핵심 베팅 포인트 한 줄 (예: "단기 과열에도 중장기 흑자 가속 베팅 — BUY 유지")',

    # ══════════════════════════════════════════════════════
    # ★ v1.2 신규 — 의사결정 가치 향상 키 (모두 선택)
    # ══════════════════════════════════════════════════════

    # — Tier 1.1: 다음 이벤트 (수동 입력) —
    'next_catalyst': {
        'date':       '2026-08-13 예정',         # 발표 예정일
        'event':      '26Q2 실적 발표',          # 이벤트 명
        'consensus':  '매출 320억 / OP +60억',   # 컨센서스 추정치
        'checkpoint': 'HBM 매출 비중 50% 돌파', # 무엇을 봐야 하는지
    },

    # — Tier 1.2: 한 줄 재무 요약 (생략 시 자동 생성) —
    # 생략하면 brief_builder가 quarterly_* + ocf + debt_ratio에서 자동 작성:
    #   '25Q4: 매출 241.9억 (YoY +70%) / OP +48.7억 / OCF -57.2억 / 부채비율 317%'
    # 'last_quarter': '...직접 작성하면 자동 생성 대신 사용...',

    # — Tier 2.1: 컨빅션 점수 (1~10, 생략 시 radar_scores 평균) —
    'conviction': 6.5,

    # — Tier 2.2: 체크리스트 (생략 시 radar_categories+scores에서 자동) —
    # score 7+ = 초록(양호), 5~6 = 주황(보통), 5 미만 = 빨강(취약)
    'checklist': [
        {'label': '수익성',     'score': 4},
        {'label': '성장성',     'score': 9},
        {'label': '안정성',     'score': 3},
        {'label': '밸류에이션', 'score': 7},
        {'label': '모멘텀',     'score': 9},
    ],

    # — Tier 2.3: Kill Switch — 비중 축소 트리거 —
    'kill_switch': [
        '• 26Q1 영업이익 < +20억 — 모멘텀 둔화 신호',
        '• 부채비율 > 350% — 재무 안정성 추가 악화',
        '• HBM4 양산 일정 4Q26 이후로 후퇴',
    ],

    # — Tier 2.4: 피어 비교 (한 줄) —
    'peer_comparison':
        '펨트론 PER 18x vs 고영 24x — 국내 검사장비 평균 대비 -25% 디스카운트',
},
```

또한 `config.py` 최상위에 (forward_thesis 밖) 가격 포지션 키:
```python
# ★ v1.2 신규 — 가격 포지션 (yfinance 자동 채움 권장)
'price_position': {
    'current':       24150.0,
    'current_str':   '24,150원',
    'high_52w':      34700.0,
    'low_52w':       8310.0,
    'high_52w_str':  '34,700원',
    'low_52w_str':   '8,310원',
    'percentile':    60.0,        # 0~100, 현재가의 52주 분위
    'ma20':          23707.5,
    'ma20_str':      '23,708원',
    'ma20_diff':     1.87,        # 현재가 / MA20 - 1, %
},
```

`shared.data_fetcher.fetch_price_position(ticker)` 또는 `fetch_full_enrichment(ticker)['price_position']`로 자동 조회 가능 (v1.2부터 포함).

### 시나리오 작성 가이드
- **Bull**: 컨센서스 최고 목표가 또는 그 이상 — 모든 촉매가 실현
- **Base**: 컨센서스 평균 목표가 또는 본 보고서 목표가 — 가장 가능성 높은 경로
- **Bear**: 핵심 리스크 1~2개 동시 발생 — 컨센 최저 또는 그 이하
- 확률 합계 = 100%

### Kill Switch 작성 가이드 (★ v1.2)
"투자 논리가 깨지는 조건"을 객관적이고 측정 가능한 임계값으로 명시한다.
- 좋은 예: `26Q1 영업이익 < +20억`, `부채비율 > 350%`, `HBM4 양산 일정 4Q26 이후 후퇴`
- 나쁜 예: `실적 부진`, `시장 악화` (측정 불가능, 주관적)
- 3~4개 권장. 발생 시 자동 매도가 아니라 **재평가 트리거**.

### 폴백 동작
`forward_thesis`가 없으면:
- catalysts ← `swot['기회'][:4]`
- risks ← `swot['위협'][:4]`
- scenarios ← 빈 리스트 (시나리오 표 생략)
- one_line ← `투자 의견: {opinion} / 목표가: {target}`

v1.2 키 폴백:
- `last_quarter` ← `quarterly_revenue`+`quarterly_op_income`+`ocf`+`debt_ratio` 에서 자동 작성
- `conviction` ← `radar_scores` 평균
- `checklist` ← `radar_categories` + `radar_scores`에서 자동 매핑
- `kill_switch`, `peer_comparison`, `next_catalyst` ← 누락 시 해당 패널 자체가 생략 (backward-compat)

---

## Phase 3: 실행

```bash
python3 run.py {종목명} --brief
```

또는 직접:
```bash
python3 - <<'EOF'
import sys, os; sys.path.insert(0, os.getcwd())
from shared.brief_builder import build_brief
from stocks.{폴더명}.config import CONFIG
build_brief(CONFIG)
EOF
```

생성 파일: `stocks/{폴더명}/{종목명}_brief.pdf` (`brief_filename` 키로 변경 가능)

---

## 완료 후 안내

```
✅ {종목명} 투자 브리프 생성 완료!

📄 stocks/{폴더명}/{종목명}_brief.pdf  (2페이지 압축)

🎯 투자의견: {의견} / 목표가: {목표가} ({상승여력}%)
💡 핵심 한 줄: {one_line}

▶️ 풀 보고서: python run.py {종목명}
   브리프 재생성: python run.py {종목명} --brief
```

---

## 주의사항

- 브리프는 **2페이지 고정** — 더 자세한 내용은 finance-report 사용
- v1.1부터 **finance-report 호출 없이도 새 종목 처리 가능** (Phase 0.5 Quick Setup)
- Quick Setup으로 만든 config.py는 SWOT·세그먼트·창업자가 비어 있음 — 향후 풀 보고서로 승격 시 finance-report로 보강 권장
- `forward_thesis`가 비어 있고 SWOT도 비어 있으면 Forward 섹션이 거의 비어 보일 수 있음
- 출력 PDF 파일명: `{폴더명}_brief.pdf` (config.py의 `brief_filename` 키로 오버라이드 가능)
