#!/usr/bin/env python3
"""
run.py — 투자 분석 보고서 실행 진입점

사용법:
  python run.py 미래에셋생명          # 차트 + PDF 모두 생성
  python run.py 크래프톤 --charts     # 차트만
  python run.py 크래프톤 --pdf        # PDF만
  python run.py --all                  # 등록된 모든 종목 생성

환경변수 (선택):
  FINANCE_STOCKS_DIR   — stocks/ 디렉토리 위치 오버라이드
                          (기본: run.py가 있는 디렉토리/stocks)
  FINANCE_KOREAN_FONT  — 한글 폰트 경로 오버라이드 (Linux/Windows에서 유용)
"""

import argparse
import importlib
import sys
import os

# ── 경로 자동 감지 (포터블) ─────────────────────────────────
# run.py 위치 기준으로 프로젝트 루트와 stocks/ 디렉토리를 결정.
# 환경변수 FINANCE_STOCKS_DIR로 stocks/ 위치를 오버라이드 가능.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STOCKS_DIR = os.environ.get(
    'FINANCE_STOCKS_DIR',
    os.path.join(PROJECT_ROOT, 'stocks'),
)

# Python import 경로에 PROJECT_ROOT 추가 (shared.* 임포트 가능하게)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# stocks/ 가 PROJECT_ROOT 외부에 있으면 그 부모 디렉토리도 sys.path에 추가
# (stocks.{종목} 임포트 가능하게 하려면 stocks/ 부모가 sys.path에 있어야 함)
_stocks_parent = os.path.dirname(STOCKS_DIR)
if _stocks_parent and _stocks_parent != PROJECT_ROOT and _stocks_parent not in sys.path:
    sys.path.insert(0, _stocks_parent)


# ── 등록된 종목 목록 ───────────────────────────────────
# 새 종목 추가 시 여기에만 추가하면 된다
COMPANIES = {
    '미래에셋생명': 'stocks.미래에셋생명',
    '크래프톤':     'stocks.크래프톤',
    '코스맥스':     'stocks.코스맥스',
    '우버':         'stocks.uber',
    '한국콜마':     'stocks.한국콜마',
    '블록':         'stocks.block',
    '삼화콘덴서':   'stocks.samwha',
    '한미글로벌':   'stocks.hanmiglobal',
    '대한항공':     'stocks.koreanair',
    '펨트론':       'stocks.pemtron',
    '일본전산':     'stocks.nidec',
    '인터플렉스':   'stocks.인터플렉스',
    '스노우플레이크': 'stocks.snowflake',
    'snowflake':    'stocks.snowflake',
}


def run_company(name, charts=True, pdf=True, brief=False):
    folder_name = COMPANIES[name]
    print(f'\n{"="*50}')
    print(f'  {name} 보고서 생성')
    print(f'{"="*50}')

    if charts:
        cfg_mod = importlib.import_module(f'{folder_name}.config')
        from shared.chart_engine import generate_all_charts
        generate_all_charts(cfg_mod.CONFIG)

    if pdf:
        mod = importlib.import_module(f'{folder_name}.generate_pdf')
        mod.build()

    if brief:
        cfg_mod = importlib.import_module(f'{folder_name}.config')
        from shared.brief_builder import build_brief
        build_brief(cfg_mod.CONFIG)


def main():
    parser = argparse.ArgumentParser(description='투자 분석 보고서 생성기')
    parser.add_argument('company', nargs='?', help='종목 폴더명 (예: 미래에셋생명, 크래프톤)')
    parser.add_argument('--charts', action='store_true', help='차트만 생성')
    parser.add_argument('--pdf',    action='store_true', help='PDF만 생성')
    parser.add_argument('--brief',  action='store_true', help='1~2페이지 브리프 생성 (finance-brief)')
    parser.add_argument('--all',    action='store_true', help='모든 종목 생성')
    args = parser.parse_args()

    # --brief 단독 시 차트·풀PDF 안 만들고 브리프만
    if args.brief:
        do_charts = False
        do_pdf    = False
    else:
        # --charts / --pdf 미지정 시 둘 다 실행
        do_charts = args.charts or (not args.charts and not args.pdf)
        do_pdf    = args.pdf    or (not args.charts and not args.pdf)

    # 경로 설정은 모듈 로드 시 이미 완료 (PROJECT_ROOT, STOCKS_DIR 참고)

    if args.all:
        for name in COMPANIES:
            run_company(name, charts=do_charts, pdf=do_pdf, brief=args.brief)
    elif args.company:
        if args.company not in COMPANIES:
            print(f'❌ 등록된 종목이 아닙니다: {args.company}')
            print(f'   등록된 종목: {", ".join(COMPANIES.keys())}')
            sys.exit(1)
        run_company(args.company, charts=do_charts, pdf=do_pdf, brief=args.brief)  # noqa: E501
    else:
        parser.print_help()
        print(f'\n등록된 종목: {", ".join(COMPANIES.keys())}')


if __name__ == '__main__':
    main()
