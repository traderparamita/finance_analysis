#!/usr/bin/env python3
"""코스맥스 차트 생성 — 공통 엔진 호출"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.chart_engine import generate_all_charts
from stocks.코스맥스.config import CONFIG

if __name__ == '__main__':
    generate_all_charts(CONFIG)
