from .features import volatility_metrics

VOL_SPIKE = 0.35  # 35% annualized realized vol
BOLL_TOUCH = 0.0  # price within band edge (pct from current)


def make_signals(df):
    v = volatility_metrics(df)
    signals = []

    if v["realized_vol_20d"] >= VOL_SPIKE:
        signals.append({
            'type': 'volatility_alert',
            'message': f"Realized 20d vol is elevated at {v['realized_vol_20d']:.2f}",
            'severity': 'warning'
        })

    # Bollinger squeeze/expansion heuristics
    width = abs(v['bb_upper']) + abs(v['bb_lower'])
    if width < 0.04:
        signals.append({
            'type': 'trend_setup',
            'message': 'Bollinger squeeze detected: potential breakout setup',
            'severity': 'info'
        })
    elif width > 0.12:
        signals.append({
            'type': 'high_volatility_zone',
            'message': 'Wide Bollinger bands: high-volatility regime',
            'severity': 'info'
        })

    return signals, v
