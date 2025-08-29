import pandas as pd
import yfinance as yf
from datetime import datetime
from .core import get_settings

_settings = get_settings()

_cache = {}

def get_ohlc(symbol: str) -> pd.DataFrame:
    key = (symbol, _settings.YF_PERIOD, _settings.YF_INTERVAL)
    if key in _cache:
        return _cache[key].copy()
    df = yf.download(symbol, period=_settings.YF_PERIOD, interval=_settings.YF_INTERVAL, auto_adjust=True, progress=False)
    df = df.rename(columns=str.lower)
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    _cache[key] = df
    return df.copy()

def recent_news(symbol: str):
    # yfinance has a .news attribute (no API key). Fallback-friendly.
    try:
        tk = yf.Ticker(symbol)
        return tk.news or []
    except Exception:
        return []
