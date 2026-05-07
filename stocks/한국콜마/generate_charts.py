#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.chart_engine import generate_all_charts
from stocks.한국콜마.config import CONFIG

if __name__ == '__main__':
    generate_all_charts(CONFIG)
