from pydantic import BaseModel
from typing import List, Optional

class OHLC(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class PredictionRequest(BaseModel):
    symbol: str
    horizon_days: int = 3

class PredictionResponse(BaseModel):
    symbol: str
    horizon_days: int
    direction: str  # 'up'|'down'|'sideways'
    prob_up: float
    prob_down: float
    prob_sideways: float
    expected_return_pct: float

class VolatilityResponse(BaseModel):
    symbol: str
    realized_vol_20d: float
    bb_upper: float
    bb_lower: float
    atr: float

class SentimentItem(BaseModel):
    title: str
    publisher: str
    link: str
    published: str
    sentiment: str
    score: float

class Signal(BaseModel):
    type: str  # 'volatility_alert'|'trend_reversal'
    message: str
    severity: str  # 'info'|'warning'|'critical'

class SignalsResponse(BaseModel):
    symbol: str
    signals: List[Signal]
