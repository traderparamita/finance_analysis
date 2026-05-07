# Finance Analysis - 투자 보고서 생성기

## 프로젝트 개요

자동화된 투자 분석 보고서 생성 시스템. 주식, 한국 기업, 암호화폐에 대한 차트 및 PDF 형식의 전문 투자 보고서를 생성합니다.

## 프로젝트 구조

```
finance_analysis/
├── shared/                   # ★ 공통 엔진 (핵심)
│   ├── chart_engine.py       # 차트 12개 생성 함수 (모든 종목 공통)
│   └── pdf_utils.py          # PDF 스타일/빌드 유틸리티 (모든 종목 공통)
│
├── 미래에셋생명/
│   ├── config.py             # ★ 재무 데이터 + 색상 + 메타데이터 (이것만 수정)
│   ├── generate_charts.py    # 얇은 래퍼 — shared/chart_engine 호출
│   ├── generate_pdf.py       # 회사 고유 서술 + shared/pdf_utils 호출
│   └── investment_report.md  # 마크다운 보고서
│
├── 크래프톤/                  # 동일한 구조
│   ├── config.py
│   ├── generate_charts.py
│   ├── generate_pdf.py
│   └── investment_report.md
│
├── stocks/                   # 기존 레거시 종목 (google, 샘표 등)
│   └── {종목명}/generate_charts.py, generate_pdf.py
│
├── cryptocurrency/           # 비트코인 분석 (크립토 전용 차트)
│
└── run.py                    # ★ 실행 진입점
```

## 핵심 설계 원칙

**공통 엔진 + 회사별 config 분리**

- 차트 로직, PDF 스타일은 `shared/` 한 곳에만 존재
- 각 회사 폴더는 **`config.py` 하나만** 수정하면 차트·PDF 모두 자동 반영
- 버그 수정이나 차트 개선 시 `shared/`만 수정하면 모든 종목에 적용됨

## 실행 방법

```bash
# 단일 종목 (차트 + PDF 동시)
python run.py 미래에셋생명
python run.py 크래프톤

# 차트만
python run.py 미래에셋생명 --charts

# PDF만
python run.py 미래에셋생명 --pdf

# 모든 종목 한 번에
python run.py --all
```

또는 개별 실행:
```bash
cd 미래에셋생명
python generate_charts.py   # 차트 12개 생성
python generate_pdf.py      # PDF 생성
```

## 새 종목 추가 방법

1. 기존 회사 폴더를 복사 → 새 폴더명으로 변경
2. **`config.py`만 수정** (재무 데이터, 색상, 메타데이터)
3. `generate_pdf.py`의 서술 내용(섹션별 텍스트) 업데이트
4. `investment_report.md` 내용 업데이트
5. `run.py`의 `COMPANIES` 딕셔너리에 등록
6. `python run.py {종목명}` 실행

`generate_charts.py`는 수정 불필요 — config.py 데이터를 공통 엔진이 자동 처리

## config.py 주요 키

| 키 | 설명 | 예시 |
|----|------|------|
| `name` | 종목명 | `'미래에셋생명'` |
| `colors.primary` | 주 브랜드 컬러 | `'#1A3A6B'` |
| `colors.accent` | 포인트 컬러 | `'#FF6B00'` |
| `revenue` | 매출액 5년 배열 | `[25200, 28100, ...]` |
| `op_income` | 영업이익 5년 배열 | `[820, 1150, ...]` |
| `swot` | SWOT 딕셔너리 | `{'강점': [...], '약점': [...], ...}` |
| `radar_categories` | 레이더 축 이름 | `['수익성', '성장성', ...]` |
| `seg_labels/sizes` | 사업부문 파이 | `['변액보험', ...]` / `[35, 30, ...]` |
| `sub_labels/sizes` | 보조 막대 (선택) | 지역별 비중 등 |

## 기술 스택

- **Python 3** — 핵심 언어
- **Matplotlib + NumPy** — 차트/시각화 생성
- **ReportLab** — PDF 문서 생성
- **한국어 폰트**: AppleGothic (`/System/Library/Fonts/Supplemental/AppleGothic.ttf`)

## 차트 유형 (12개, shared/chart_engine.py)

| 번호 | 파일명 | 내용 |
|------|--------|------|
| 1 | chart1_revenue_profit.png | 매출 & 영업이익 묶음 막대 |
| 2 | chart2_margins.png | 영업이익률 + 순이익률 꺾은선 |
| 3 | chart3_roe_roa.png | ROE + ROA 면적+꺾은선 |
| 4 | chart4_financial_stability.png | 부채비율 + 보조지표 혼합 |
| 5 | chart5_growth_rates.png | 성장률 막대 |
| 6 | chart6_segments.png | 사업부문 파이 (+ 선택적 보조 막대) |
| 7 | chart7_net_income.png | 순이익 막대 + 순이익률 꺾은선 |
| 8 | chart8_swot.png | SWOT 4분면 |
| 9 | chart9_cashflow.png | 영업/투자/재무 CF 묶음 막대 |
| 10 | chart10_capex_fcf.png | CAPEX + FCF 혼합 |
| 11 | chart11_earnings_quality.png | 영업이익 vs 영업CF |
| 12 | chart12_radar.png | 투자매력도 레이더 |

## PDF 보고서 구성 (shared/pdf_utils.py)

1. 표지 (종목명, 티커, 주가, 투자의견, 목표주가)
2. 목차
3. 기업 개요
4. 비전 & 전략
5. 사업 모델 분석
6. 재무 분석 (5개년 테이블 + chart1, chart7)
7. 수익성 분석 (chart2, chart3)
8. 성장성 분석 (chart5)
9. 재무 안정성 (chart4)
10. 현금흐름 분석 (chart9, chart10, chart11)
11. 산업 & 경쟁 분석 (chart6)
12. SWOT & 리스크 분석 (chart8)
13. 밸류에이션 & 결론 (chart12)
14. 면책 고지

## 주요 규칙

- 재무 데이터는 `config.py` 배열에 하드코딩 — 외부 API 호출 없음
- 차트 저장 경로는 항상 `os.path.join(BASE, ...)` 사용 — 절대경로 금지
- `plt.close()`를 각 차트 저장 후 반드시 호출 (메모리 누수 방지)
- 암호화폐 분석은 `cryptocurrency/` 폴더에서 별도 관리 (레거시 구조 유지)
- 모든 금액 단위: 미국 주식은 10억 달러(USD), 한국 주식은 억원(KRW)
- PDF 보고서 전반에 초보자 팁 박스 포함 (💡 초보자 가이드)

## 차트 사양

- 크기: 10" x 5.5" @ 150 DPI (1500 x 825 px)
- 형식: PNG
- 폰트: AppleGothic (한국어), 기본 폴백 (영어)

## 플랫폼 참고사항

- macOS에서 개발 — 폰트 경로는 `/System/Library/Fonts/` 사용
- Windows/Linux에서는 `shared/chart_engine.py` 및 `shared/pdf_utils.py`의 폰트 경로 수정 필요
