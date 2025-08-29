from fastapi import FastAPI
from .schemas import PredictionRequest, PredictionResponse, VolatilityResponse, SentimentItem, SignalsResponse
from .data import get_ohlc
from .models import get_or_train
from .features import volatility_metrics
from .sentiment import news_sentiment
from .signals import make_signals

app = FastAPI(title="StockSense API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/symbols")
def symbols():
    return {"symbols": ["AAPL","MSFT","GOOGL","AMZN","TSLA","^NSEI","RELIANCE.NS"]}

@app.post("/predict", response_model=PredictionResponse)
async def predict(req: PredictionRequest):
    df = get_ohlc(req.symbol)
    m = get_or_train(req.symbol, req.horizon_days)
    direction, proba, exp = m.predict(df)
    return PredictionResponse(
        symbol=req.symbol,
        horizon_days=req.horizon_days,
        direction=direction,
        prob_up=float(proba[2]),
        prob_down=float(proba[0]),
        prob_sideways=float(proba[1]),
        expected_return_pct=float(exp)
    )

@app.get("/volatility/{symbol}", response_model=VolatilityResponse)
async def vol(symbol: str):
    df = get_ohlc(symbol)
    v = volatility_metrics(df)
    return VolatilityResponse(symbol=symbol, **v)

@app.get("/sentiment/{symbol}", response_model=list[SentimentItem])
async def sentiment(symbol: str):
    items = news_sentiment(symbol)
    return items

@app.get("/signals/{symbol}", response_model=SignalsResponse)
async def signals(symbol: str):
    df = get_ohlc(symbol)
    sigs, _ = make_signals(df)
    return SignalsResponse(symbol=symbol, signals=sigs)
