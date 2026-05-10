"""
shared/data_fetcher.py
yfinance를 사용해 오늘 기준 실시간 재무 데이터를 가져온다.

사용법:
    from shared.data_fetcher import (
        fetch_stock_data,             # 연간 재무 (4~5년)
        fetch_quarterly_data,         # 분기 재무 (최근 8분기)
        fetch_forward_estimates,      # Forward PER + 애널리스트 컨센서스
        fetch_recent_news,            # yfinance 뉴스 헤드라인 (최근 10건)
        fetch_full_enrichment,        # 위 4가지 한 번에 호출
    )
    data = fetch_stock_data('192820.KS')
"""
from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

import yfinance as yf

KST = ZoneInfo("Asia/Seoul")


def fetch_stock_data(ticker: str, years: int = 5) -> dict:
    """
    yfinance로 주식 데이터를 가져와 config.py가 기대하는 형태로 반환.

    Parameters
    ----------
    ticker : str  예) '192820.KS', '259960.KS', 'AAPL'
    years  : int  가져올 연도 수 (기본 5년)

    Returns
    -------
    dict  CONFIG 딕셔너리에 merge할 재무 데이터
    """
    print(f"  📡 {ticker} 데이터 조회 중...")
    tk = yf.Ticker(ticker)

    # ── 기본 정보 ────────────────────────────────────
    info = tk.info or {}
    current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
    mkt_cap_raw   = info.get('marketCap', 0)
    currency      = info.get('currency', 'KRW')

    if currency == 'KRW':
        price_str  = f"{current_price:,.0f}원"
        # 억원 단위
        mkt_cap_str = f"{mkt_cap_raw / 1e8:,.0f}억원"
        divisor     = 1e8  # 억원
        unit        = '억원'
    else:
        price_str   = f"${current_price:,.2f}"
        mkt_cap_str = f"${mkt_cap_raw / 1e9:,.1f}B"
        divisor     = 1e9
        unit        = '십억달러'

    report_date = datetime.now(KST).strftime('%Y년 %m월 %d일')

    # ── 재무제표 ─────────────────────────────────────
    financials  = tk.financials          # 연간 손익계산서 (최신→과거)
    balance     = tk.balance_sheet       # 연간 대차대조표
    cashflow    = tk.cashflow            # 연간 현금흐름표

    def _series(df, *keys):
        """여러 후보 키 중 첫 번째로 존재하는 행을 연도순(오래된→최신)으로 반환."""
        if df is None or df.empty:
            return []
        for key in keys:
            if key in df.index:
                row = df.loc[key].dropna()
                row = row.sort_index()  # 날짜 오름차순
                return list(row.values[-years:])
        return []

    def _year_labels(df):
        if df is None or df.empty:
            return []
        cols = sorted(df.columns)[-years:]
        return [str(c.year) for c in cols]

    year_labels = _year_labels(financials)

    # 손익계산서
    revenue    = [v / divisor for v in _series(financials, 'Total Revenue')]
    op_income  = [v / divisor for v in _series(financials, 'Operating Income', 'EBIT')]
    net_income = [v / divisor for v in _series(financials, 'Net Income')]

    # 수익성 지표 (%)
    def _pct(num_list, den_list):
        result = []
        for n, d in zip(num_list, den_list):
            try:
                result.append(round(n / d * 100, 2) if d else 0.0)
            except Exception:
                result.append(0.0)
        return result

    op_margin  = _pct(op_income, revenue)
    net_margin = _pct(net_income, revenue)

    # ROE / ROA
    total_equity  = [v / divisor for v in _series(balance, 'Stockholders Equity', 'Common Stock Equity')]
    total_assets  = [v / divisor for v in _series(balance, 'Total Assets')]
    roe = _pct(net_income, total_equity)
    roa = _pct(net_income, total_assets)

    # 부채비율
    total_liab   = [v / divisor for v in _series(balance, 'Total Liabilities Net Minority Interest', 'Total Liabilities')]
    debt_ratio   = _pct(total_liab, total_equity)

    # 유동비율
    current_assets = [v / divisor for v in _series(balance, 'Current Assets')]
    current_liab   = [v / divisor for v in _series(balance, 'Current Liabilities')]
    current_ratio  = [round(a / l * 100, 1) if l else 0.0
                      for a, l in zip(current_assets, current_liab)]

    # 성장률 YoY
    def _growth(lst):
        result = [0.0]
        for i in range(1, len(lst)):
            try:
                result.append(round((lst[i] - lst[i-1]) / abs(lst[i-1]) * 100, 1) if lst[i-1] else 0.0)
            except Exception:
                result.append(0.0)
        return result

    rev_growth = _growth(revenue)
    op_growth  = _growth(op_income)
    ni_growth  = _growth(net_income)

    # 현금흐름
    ocf   = [v / divisor for v in _series(cashflow, 'Operating Cash Flow')]
    icf   = [v / divisor for v in _series(cashflow, 'Investing Cash Flow')]
    fin_cf = [v / divisor for v in _series(cashflow, 'Financing Cash Flow')]
    capex = [abs(v) / divisor for v in _series(cashflow, 'Capital Expenditure')]
    fcf   = [o - c for o, c in zip(ocf, capex)]

    # 유효 연도 (가장 짧은 시리즈 기준)
    valid_len = min(
        len(year_labels), len(revenue), len(op_income), len(net_income)
    )
    if valid_len == 0:
        print(f"  ⚠ {ticker}: 재무 데이터 없음. 수동 입력 필요.")
        return {}

    def _trim(lst):
        return lst[-valid_len:] if len(lst) >= valid_len else lst + [0.0] * (valid_len - len(lst))

    print(f"  ✅ {ticker} 데이터 조회 완료 ({year_labels[-valid_len] if year_labels else '?'} ~ {year_labels[-1] if year_labels else '?'})")

    return {
        'price':       price_str,
        'mkt_cap':     mkt_cap_str,
        'report_date': report_date,
        'unit':        unit,
        'years':       year_labels[-valid_len:],
        'revenue':     [round(v, 1) for v in _trim(revenue)],
        'op_income':   [round(v, 1) for v in _trim(op_income)],
        'net_income':  [round(v, 1) for v in _trim(net_income)],
        'op_margin':   [round(v, 2) for v in _trim(op_margin)],
        'net_margin':  [round(v, 2) for v in _trim(net_margin)],
        'roe':         [round(v, 2) for v in _trim(roe)],
        'roa':         [round(v, 2) for v in _trim(roa)],
        'debt_ratio':  [round(v, 2) for v in _trim(debt_ratio)],
        'current_ratio': [round(v, 1) for v in _trim(current_ratio)],
        'rev_growth':  [round(v, 1) for v in _trim(rev_growth)],
        'op_growth':   [round(v, 1) for v in _trim(op_growth)],
        'ni_growth':   [round(v, 1) for v in _trim(ni_growth)],
        'ocf':         [round(v, 1) for v in _trim(ocf)],
        'icf':         [round(v, 1) for v in _trim(icf)],
        'fin_cf':      [round(v, 1) for v in _trim(fin_cf)],
        'capex':       [round(v, 1) for v in _trim(capex)],
        'fcf':         [round(v, 1) for v in _trim(fcf)],
    }


# ══════════════════════════════════════════════════════════
# 분기 재무 (최근 8분기)
# ══════════════════════════════════════════════════════════
def fetch_quarterly_data(ticker: str, n_quarters: int = 8) -> dict:
    """
    최근 N분기 매출·영업이익·순이익을 가져온다.

    Returns
    -------
    dict
        'quarterly_labels': ['24Q1', '24Q2', ...]
        'quarterly_revenue':   [...]
        'quarterly_op_income': [...]
        'quarterly_net_income':[...]
        'quarterly_unit':      '십억달러' 또는 '억원'
        빈 딕셔너리 — yfinance가 데이터를 안 주는 경우
    """
    print(f"  📡 {ticker} 분기 데이터 조회 중...")
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}
        currency = info.get('currency', 'KRW')
        divisor = 1e8 if currency == 'KRW' else 1e9
        unit = '억원' if currency == 'KRW' else '십억달러'

        qf = tk.quarterly_financials  # 분기 손익계산서 (열=분기, 행=항목)
        if qf is None or qf.empty:
            print(f"  ⚠ {ticker} 분기 데이터 없음")
            return {}

        cols = sorted(qf.columns)[-n_quarters:]
        labels = [f"{str(c.year)[-2:]}Q{((c.month - 1) // 3) + 1}" for c in cols]

        def _q_series(*keys):
            for k in keys:
                if k in qf.index:
                    s = qf.loc[k]
                    return [round((s.get(c, 0) or 0) / divisor, 2) for c in cols]
            return [0.0] * len(cols)

        revenue   = _q_series('Total Revenue')
        op_income = _q_series('Operating Income', 'EBIT')
        net_income = _q_series('Net Income')

        print(f"  ✅ {ticker} 분기 데이터 {len(labels)}개 ({labels[0]} ~ {labels[-1]})")
        return {
            'quarterly_labels':     labels,
            'quarterly_revenue':    revenue,
            'quarterly_op_income':  op_income,
            'quarterly_net_income': net_income,
            'quarterly_unit':       unit,
        }
    except Exception as e:
        print(f"  ⚠ {ticker} 분기 fetch 실패: {e}")
        return {}


# ══════════════════════════════════════════════════════════
# Forward 컨센서스 (애널리스트 목표가·추천 분포)
# ══════════════════════════════════════════════════════════
def fetch_forward_estimates(ticker: str) -> dict:
    """
    yfinance info에서 Forward PER, 목표가 분포, 추천 등급을 가져온다.

    Returns
    -------
    dict — 가져올 수 있는 항목만 담겨 있음. 빈 dict 가능.
        'forward_pe':           18.5
        'trailing_pe':          22.1
        'target_mean':          85.0
        'target_high':          110.0
        'target_low':           60.0
        'target_median':        88.0
        'analyst_count':        35
        'recommendation_mean':  2.1   (1=Strong Buy, 5=Strong Sell)
        'recommendation_key':   'buy'
        'recommendations':  {'strongBuy': 8, 'buy': 18, 'hold': 7, 'sell': 1, 'strongSell': 1}
    """
    print(f"  📡 {ticker} Forward 컨센서스 조회 중...")
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}

        result = {}
        for src, dst in [
            ('forwardPE',           'forward_pe'),
            ('trailingPE',          'trailing_pe'),
            ('targetMeanPrice',     'target_mean'),
            ('targetHighPrice',     'target_high'),
            ('targetLowPrice',      'target_low'),
            ('targetMedianPrice',   'target_median'),
            ('numberOfAnalystOpinions', 'analyst_count'),
            ('recommendationMean',  'recommendation_mean'),
            ('recommendationKey',   'recommendation_key'),
            ('currentPrice',        'current_price'),
        ]:
            v = info.get(src)
            if v is not None:
                result[dst] = v

        # 추천 등급 분포 (DataFrame): yfinance는 최근 4개월 분포를 줌
        try:
            recs = tk.recommendations
            if recs is not None and not recs.empty:
                latest = recs.iloc[0]  # 가장 최신 row
                buckets = {}
                for k in ['strongBuy', 'buy', 'hold', 'sell', 'strongSell']:
                    if k in latest.index:
                        buckets[k] = int(latest[k]) if latest[k] is not None else 0
                if buckets and sum(buckets.values()) > 0:
                    result['recommendations'] = buckets
        except Exception:
            pass

        if result:
            print(f"  ✅ {ticker} Forward 컨센서스: 항목 {len(result)}개")
        else:
            print(f"  ⚠ {ticker} Forward 컨센서스 데이터 없음")
        return result
    except Exception as e:
        print(f"  ⚠ {ticker} Forward fetch 실패: {e}")
        return {}


# ══════════════════════════════════════════════════════════
# 최근 뉴스 헤드라인 (yfinance)
# ══════════════════════════════════════════════════════════
def fetch_recent_news(ticker: str, limit: int = 10) -> list[dict]:
    """
    yfinance 뉴스 헤드라인 (최신순). 각 항목:
      {'title', 'publisher', 'link', 'published' (YYYY-MM-DD), 'summary'}

    Returns
    -------
    list — 빈 리스트 가능
    """
    print(f"  📡 {ticker} 최근 뉴스 조회 중...")
    try:
        tk = yf.Ticker(ticker)
        news = tk.news or []
        items = []
        for n in news[:limit]:
            # yfinance 신/구 응답 포맷 모두 대응
            content = n.get('content', n)
            title = content.get('title') or n.get('title', '')
            publisher = (
                content.get('provider', {}).get('displayName')
                if isinstance(content.get('provider'), dict)
                else n.get('publisher', '')
            )
            link = (
                content.get('canonicalUrl', {}).get('url')
                if isinstance(content.get('canonicalUrl'), dict)
                else n.get('link', '')
            )
            published_raw = content.get('pubDate') or n.get('providerPublishTime')
            if isinstance(published_raw, (int, float)):
                published = datetime.fromtimestamp(published_raw, tz=KST).strftime('%Y-%m-%d')
            elif isinstance(published_raw, str):
                published = published_raw[:10]
            else:
                published = ''
            summary = content.get('summary', '') or n.get('summary', '')
            if title:
                items.append({
                    'title':     title,
                    'publisher': publisher or 'Unknown',
                    'link':      link,
                    'published': published,
                    'summary':   summary,
                })
        print(f"  ✅ {ticker} 뉴스 {len(items)}건")
        return items
    except Exception as e:
        print(f"  ⚠ {ticker} 뉴스 fetch 실패: {e}")
        return []


# ══════════════════════════════════════════════════════════
# 가격 포지션 (52주 레인지 · 분위 · 20일 이평)
# ══════════════════════════════════════════════════════════
def fetch_price_position(ticker: str) -> dict:
    """52주 고가/저가, 현재 주가의 분위, 20일 이평선 대비 위치를 반환.

    finance-brief의 '52주 위치' 스냅샷 섹션에서 사용된다.
    데이터가 부분적으로 빠져 있어도 가능한 만큼 채워서 반환.
    """
    print(f"  📡 {ticker} 가격 포지션 조회 중...")
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}

        cur    = info.get('currentPrice') or info.get('regularMarketPrice')
        high52 = info.get('fiftyTwoWeekHigh')
        low52  = info.get('fiftyTwoWeekLow')

        # 20일 이동평균 (close)
        ma20 = None
        try:
            hist = tk.history(period='2mo')
            if not hist.empty and 'Close' in hist.columns:
                closes = hist['Close'].dropna()
                if len(closes) >= 5:
                    ma20 = float(closes.tail(20).mean())
        except Exception:
            pass

        currency = info.get('currency', 'KRW')
        if currency == 'KRW':
            fmt = lambda v: f"{v:,.0f}원" if v else 'N/A'
        else:
            fmt = lambda v: f"${v:,.2f}" if v else 'N/A'

        percentile = None
        if cur and high52 and low52 and high52 != low52:
            percentile = (cur - low52) / (high52 - low52) * 100

        ma20_diff = None
        if cur and ma20:
            ma20_diff = (cur / ma20 - 1) * 100

        result = {
            'current':       cur,
            'current_str':   fmt(cur),
            'high_52w':      high52,
            'low_52w':       low52,
            'high_52w_str':  fmt(high52),
            'low_52w_str':   fmt(low52),
            'percentile':    percentile,
            'ma20':          ma20,
            'ma20_str':      fmt(ma20),
            'ma20_diff':     ma20_diff,
        }
        if percentile is not None:
            print(f"  ✅ 52주 분위 {percentile:.0f}%, 20일 이평 대비 {ma20_diff:+.1f}%" if ma20_diff is not None else f"  ✅ 52주 분위 {percentile:.0f}%")
        return result
    except Exception as e:
        print(f"  ⚠️  가격 포지션 조회 실패: {e}")
        return {}


# ══════════════════════════════════════════════════════════
# 통합 enrichment (한 번에 호출)
# ══════════════════════════════════════════════════════════
def fetch_full_enrichment(ticker: str) -> dict:
    """
    fetch_stock_data + 분기 + Forward + 뉴스 + 가격 포지션을 한 번에 호출하여 병합한 dict 반환.

    config.py에 그대로 spread해서 사용하면 된다.
    """
    base = fetch_stock_data(ticker) or {}
    if not base:
        return {}
    quarterly = fetch_quarterly_data(ticker)
    forward   = fetch_forward_estimates(ticker)
    news      = fetch_recent_news(ticker)
    position  = fetch_price_position(ticker)
    return {
        **base,
        **quarterly,
        'forward':         forward,
        'news':            news,
        'price_position':  position,
    }
