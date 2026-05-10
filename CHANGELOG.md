# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), SemVer.

## [Unreleased]

### Planned
- 포터블화 — 폰트 fallback (Linux/Windows), 경로 환경변수 (`$FINANCE_STOCKS_DIR`)
- DCF 모델 + 민감도 분석 (Tier A 1)
- 시나리오 분석 (Bull/Base/Bear) — 풀 보고서에 추가
- 세그먼트별 영업이익률 분리

---

## [1.0.0] - 2026-05-10

### Added
- **finance-report 스킬** — 풀 16~17 페이지 투자 분석 보고서
  - 17개 표준 섹션 (표지·목차·창업자 카드·재무·SWOT·이슈·밸류에이션 등)
  - 15개 표준 차트 (chart1~12 + chart13/14/15 옵션)
  - 8개 섹터 분류 + 섹터별 핵심 지표 자동 매핑
  - WebSearch 5개 쿼리 + WebFetch 본문 인용 (이슈 카드)
  - yfinance 자동 fetch (분기·Forward·뉴스 통합)
  - v4.1 창업자 카드 + 타임라인 + 직접 인용

- **finance-brief 스킬** — 1~2 페이지 압축 브리프
  - v1.2 스냅샷 패널 (52주 위치 / 최근 분기 / 다음 이벤트)
  - v1.2 컨빅션 점수 + 체크리스트 + 피어 비교 패널
  - v1.2 의사결정 트리거 (Kill Switch)
  - 시나리오 표 (Bull/Base/Bear) + 확률 가중
  - Quick Setup — finance-report 호출 없이 새 종목 30~60초 처리

- **shared 공통 엔진**
  - `data_fetcher.py` — `fetch_full_enrichment()` 단일 호출로 연간·분기·Forward·뉴스·가격포지션 통합
  - `chart_engine.py` — 12개 표준 차트 + chart13/14/15 옵션
  - `pdf_utils.py` — 표·카드·이슈·창업자·컨센서스 헬퍼
  - `brief_builder.py` — 2페이지 압축 빌더
  - 표 셀 자동 줄바꿈 (Paragraph wrap)

- **샘플 종목** (포함되지 않음 — 사용자 로컬에서 생성)
  - `stocks/`는 `.gitignore`로 분리 — 플러그인 업데이트가 사용자 분석 데이터에 영향 없음

### Notes
- macOS 전용 폰트 경로 (`/System/Library/Fonts/Supplemental/AppleGothic.ttf`)
- Linux/Windows fallback은 v1.1.0에서 제공 예정
- `$HOME/finance-reports`로 작업 디렉토리 가정 — 환경변수화는 v1.1.0 예정
