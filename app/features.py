import pandas as pd
import pandas_ta as ta

SIDEWAYS_BAND = 0.004  # ~0.4% per day threshold for direction labeling

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rsi14"] = ta.rsi(df["close"], length=14)
    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    df = pd.concat([df, macd], axis=1)
    df["sma20"] = ta.sma(df["close"], length=20)
    df["sma50"] = ta.sma(df["close"], length=50)
    bb = ta.bbands(df["close"], length=20, std=2)
    df = pd.concat([df, bb], axis=1)
    df["atr14"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    df["ret1"] = df["close"].pct_change()
    df["vol20"] = df["ret1"].rolling(20).std() * (252 ** 0.5)
    return df.dropna()

def label_direction(df: pd.DataFrame, horizon_days: int = 3) -> pd.Series:
    fwd = df["close"].shift(-horizon_days)
    ret = (fwd - df["close"]) / df["close"]
    direction = ret.copy()
    direction[:] = "sideways"
    direction[ret > SIDEWAYS_BAND * horizon_days] = "up"
    direction[ret < -SIDEWAYS_BAND * horizon_days] = "down"
    return direction

def volatility_metrics(df: pd.DataFrame):
    bb = ta.bbands(df["close"], length=20, std=2).dropna()
    atr = ta.atr(df["high"], df["low"], df["close"], length=14).iloc[-1]
    vol20 = df["close"].pct_change().rolling(20).std().iloc[-1] * (252 ** 0.5)
    last_close = df["close"].iloc[-1]
    return {
        "realized_vol_20d": float(vol20),
        "bb_upper": float(bb["BBU_20_2.0"].iloc[-1]) / last_close - 1.0,
        "bb_lower": float(bb["BBL_20_2.0"].iloc[-1]) / last_close - 1.0,
        "atr": float(atr)
    }
