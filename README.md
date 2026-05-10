# finance-analysis

Claude Code 플러그인 — 투자 분석 보고서 자동 생성기.

**스킬 2개 제공**:
- `/finance-report` — 풀 16~17 페이지 투자 분석 보고서 (DCF·시나리오 제외 IB 정규 리포트 수준)
- `/finance-brief` — 1~2 페이지 압축 브리프 (의사결정 가속용)

> ⚠️ 본 도구가 생성하는 보고서는 **공개 재무 데이터 기반 참고 자료**이며, 투자 권유·조언이 아닙니다. 투자 판단의 최종 책임은 투자자 본인에게 있습니다.

---

## 설치

### 사전 요건
- macOS (현재 v1.0) — Linux/Windows 폰트 fallback은 v1.1+ 예정
- Python 3.10+
- Claude Code CLI 또는 IDE 확장

### 1) 플러그인 설치
```bash
# Claude Code 안에서
/plugin marketplace add lifesailor/finance-analysis
/plugin install finance-analysis@lifesailor
```

### 2) Python 의존성 설치
```bash
git clone https://github.com/lifesailor/finance-analysis.git $HOME/finance-reports
cd $HOME/finance-reports
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3) 스킬 활성화 확인
```bash
# Claude Code 안에서
/finance-report 펨트론     # 풀 보고서
/finance-brief 펨트론       # 압축 브리프
```

---

## 사용법

### 풀 보고서 생성
```
/finance-report 펨트론
```
대화형으로 종목명·티커·투자의견·목표가를 묻고, yfinance에서 재무 데이터를 자동 fetch한 뒤 다음 산출물을 생성:

- `stocks/pemtron/config.py` — 모든 데이터·메타정보
- `stocks/pemtron/generate_charts.py` — 차트 래퍼
- `stocks/pemtron/generate_pdf.py` — PDF 빌더
- `stocks/pemtron/investment_report.md` — 마크다운 요약
- `stocks/pemtron/펨트론_investment_report.pdf` — **최종 16~17 페이지 PDF**
- `stocks/pemtron/chart1~15_*.png` — 15개 차트

### 압축 브리프 생성
```
/finance-brief 펨트론
```
풀 보고서가 이미 있으면 `forward_thesis`만 갱신해 2페이지 PDF 생성. 없으면 Quick Setup으로 30~60초 안에 새 종목 처리.

### 직접 실행 (개발용)
```bash
cd $HOME/finance-reports
.venv/bin/python run.py 펨트론              # 차트 + 풀 PDF
.venv/bin/python run.py 펨트론 --pdf        # PDF만
.venv/bin/python run.py 펨트론 --brief      # 브리프만
.venv/bin/python run.py --all               # 등록된 모든 종목
```

---

## 구조

```
finance-analysis/
├── .claude-plugin/
│   └── plugin.json               # 플러그인 메타데이터
├── skills/
│   ├── finance-report/SKILL.md   # 풀 보고서 스킬
│   └── finance-brief/SKILL.md    # 브리프 스킬
├── shared/                        # 공통 엔진 (수정 금지)
│   ├── data_fetcher.py           # yfinance 통합 fetch
│   ├── chart_engine.py           # 15개 표준 차트
│   ├── pdf_utils.py              # PDF 빌드 유틸
│   └── brief_builder.py          # 브리프 빌더
├── run.py                         # 진입점
├── requirements.txt
├── CHANGELOG.md
└── README.md (이 파일)

# 사용자 로컬 (.gitignore — 플러그인 repo에 포함되지 않음)
stocks/                            # 종목별 분석 데이터
├── 펨트론/
├── 펩트론/
└── ...
```

---

## 핵심 기능

### finance-report (풀 보고서)
- **자동 데이터 수집** — yfinance API (연간·분기·Forward·뉴스·가격 포지션)
- **8개 섹터 자동 분류** — 테크/게임/금융/소비재/바이오/에너지/모빌리티/일반
- **15개 표준 차트** — 매출/마진/ROE/현금흐름/SWOT/레이더/분기 모멘텀/컨센서스
- **WebSearch + WebFetch** — 30~90일 이내 핵심 이슈 5건 본문 인용
- **창업자 카드 (v4.1)** — 약력·철학·타임라인·직접 인용
- **섹터별 밸류에이션** — PER·EV/EBITDA·EV/Sales 자동 적용
- **초보자 가이드 박스** — 모든 섹션에 💡 설명

### finance-brief (브리프, v1.2)
- **2페이지 고정** — 의사결정 30초용
- **스냅샷 패널** — 52주 위치 + 최근 분기 + 다음 이벤트
- **컨빅션 점수** — 1~10 + 5개 항목 체크리스트 (색상 배지)
- **시나리오 표** — Bull/Base/Bear 목표가·확률·전제
- **Kill Switch** — 비중 축소 트리거 (객관적 임계값)
- **피어 비교** — 한 줄 동종업계 multiple 비교

---

## 업데이트

```bash
# Claude Code 안에서
/plugin update finance-analysis
```

자세한 변경 이력은 [CHANGELOG.md](CHANGELOG.md) 참조.

### 버전 관리 약속 (SemVer)
- **PATCH** (1.0.0 → 1.0.1): 버그 수정, 동작 동일
- **MINOR** (1.0.x → 1.1.0): 새 기능, 하위 호환 유지
- **MAJOR** (1.x → 2.0.0): 호환 불가 변경 (CHANGELOG 마이그레이션 가이드 명시)

기존 종목 폴더의 `config.py`는 **선택형 키 폴백**으로 보호되어, MINOR 업데이트 시 데이터를 다시 작성할 필요 없이 새 기능 자동 활성화.

---

## 한계 (v1.0)

- **macOS 폰트만 지원** — `AppleGothic.ttf` 경로 하드코딩 (v1.1에서 fallback 제공)
- **DCF 모델 부재** — 밸류에이션은 PER × EPS 단일 배수 (v1.1에서 추가 예정)
- **시나리오 분석은 브리프에만** — 풀 보고서엔 미포함 (v1.1 예정)
- **수급 분석 없음** — 외국인·기관 매매 동향 미포함
- **ESG·지배구조 없음** — 향후 Tier B 항목

자세한 갭 분석은 SKILL.md 참조.

---

## 라이선스

MIT — 자유롭게 사용·수정·배포 가능. 단, **투자 손실에 대한 책임은 사용자 본인**.

---

## 기여

Pull Request 환영. 새 섹터 추가, 차트 개선, 폴백 로직 강화 등.

이슈 리포트는 GitHub Issues로.
