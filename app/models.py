import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import TimeSeriesSplit
from .features import make_features, label_direction
from .data import get_ohlc

_model_cache = {}

FEATURE_COLS = [
    "rsi14","MACD_12_26_9","MACDh_12_26_9","MACDs_12_26_9","sma20","sma50",
    "BBL_20_2.0","BBM_20_2.0","BBU_20_2.0","atr14","ret1","vol20"
]

LABELS = {"down":0,"sideways":1,"up":2}
INV_LABELS = {v:k for k,v in LABELS.items()}

class DirectionModel:
    def __init__(self, horizon_days: int = 3):
        self.h = horizon_days
        self.clf = RandomForestClassifier(n_estimators=400, max_depth=8, random_state=42, n_jobs=-1)
        self.fitted = False

    def fit(self, df: pd.DataFrame):
        feats = make_features(df)
        y = label_direction(feats, self.h).iloc[:-self.h]
        X = feats.iloc[:-self.h][FEATURE_COLS]
        tscv = TimeSeriesSplit(n_splits=5)
        # (Optional) Could evaluate here; keep fast for MVP
        self.clf.fit(X, y.map(LABELS))
        self.fitted = True
        return self

    def predict(self, df: pd.DataFrame):
        if not self.fitted:
            self.fit(df)
        feats = make_features(df)
        x = feats.iloc[[-1]][FEATURE_COLS]
        proba = self.clf.predict_proba(x)[0]
        idx = int(np.argmax(proba))
        direction = INV_LABELS[idx]
        exp_ret = (
            0.01 * (proba[2] - proba[0]) * self.h  # rough heuristic for MVP
        )
        return direction, proba, exp_ret


def get_or_train(symbol: str, horizon_days: int = 3):
    key = (symbol, horizon_days)
    if key in _model_cache:
        return _model_cache[key]
    df = get_ohlc(symbol)
    m = DirectionModel(horizon_days)
    m.fit(df)
    _model_cache[key] = m
    return m
