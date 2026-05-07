#!/usr/bin/env python3
"""
run.py — 투자 분석 보고서 실행 진입점

사용법:
  python run.py 미래에셋생명          # 차트 + PDF 모두 생성
  python run.py 크래프톤 --charts     # 차트만
  python run.py 크래프톤 --pdf        # PDF만
  python run.py --all                  # 등록된 모든 종목 생성
"""

import argparse
import importlib
import sys
import os

# ── 등록된 종목 목록 ───────────────────────────────────
# 새 종목 추가 시 여기에만 추가하면 된다
COMPANIES = {
    '미래에셋생명': 'stocks.미래에셋생명',
    '크래프톤':     'stocks.크래프톤',
    '코스맥스':     'stocks.코스맥스',
    '우버':         'stocks.uber',
    '한국콜마':     'stocks.한국콜마',
    '블록':         'stocks.block',
}


def run_company(name, charts=True, pdf=True):
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


def main():
    parser = argparse.ArgumentParser(description='투자 분석 보고서 생성기')
    parser.add_argument('company', nargs='?', help='종목 폴더명 (예: 미래에셋생명, 크래프톤)')
    parser.add_argument('--charts', action='store_true', help='차트만 생성')
    parser.add_argument('--pdf',    action='store_true', help='PDF만 생성')
    parser.add_argument('--all',    action='store_true', help='모든 종목 생성')
    args = parser.parse_args()

    # --charts / --pdf 미지정 시 둘 다 실행
    do_charts = args.charts or (not args.charts and not args.pdf)
    do_pdf    = args.pdf    or (not args.charts and not args.pdf)

    # 경로 설정
    root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, root)

    if args.all:
        for name in COMPANIES:
            run_company(name, charts=do_charts, pdf=do_pdf)
    elif args.company:
        if args.company not in COMPANIES:
            print(f'❌ 등록된 종목이 아닙니다: {args.company}')
            print(f'   등록된 종목: {", ".join(COMPANIES.keys())}')
            sys.exit(1)
        run_company(args.company, charts=do_charts, pdf=do_pdf)  # noqa: E501
    else:
        parser.print_help()
        print(f'\n등록된 종목: {", ".join(COMPANIES.keys())}')


if __name__ == '__main__':
    main()
