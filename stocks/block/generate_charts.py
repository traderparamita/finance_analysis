#!/usr/bin/env python3
"""Block, Inc. (XYZ) 차트 생성 — shared/chart_engine.py 호출 래퍼"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.chart_engine import generate_all_charts
from stocks.block.config import CONFIG

if __name__ == '__main__':
    generate_all_charts(CONFIG)
