# SixEyes

A Python library for volatility estimation, regime analysis, and hidden state modeling in financial time series.

**SixEyes** is designed for quantitative teams and research groups that require transparent, modular, and production-aligned volatility forecasting infrastructure.

---

## Modules

| Module | Status | Description |
|---|---|---|
| `Volatility` | Available | Rolling, EWMA, range-based, asymmetric, and vol-of-vol estimators |
| `RegimeModel` | In development | Regime-switching models for structural break detection |

---

## Installation
```bash
pip install sixeyes
```

---

## Setup & Testing 

All examples below use S&P 500 daily OHLC data pulled from Yahoo Finance.
```python
import yfinance as yf
import numpy as np

df = yf.download("^GSPC", start="2020-01-01", end="2024-12-31")
returns = np.log(df["Close"] / df["Close"].shift(1)).dropna()
```

---

## Volatility

### Rolling Standard Deviation

Close-to-close log return vol over a fixed 21-day window.
```python
from Volatility.realized import RollingSTD

model = RollingSTD(window_size=21, days_per_annum=252, annualize=True)
vol = model.compute(returns)
```

---

### EWMA

Same as rolling std but decays older observations — a spike in March weights less by April. RiskMetrics standard is `alpha=0.94` for daily data.
```python
from Volatility.realized import EWMA

model = EWMA(alpha=0.94, span=20, days_per_annum=252, annualize=True)
vol = model.compute(returns.values)
```

---

### Parkinson

Replaces close-to-close returns with the daily high-low range — more efficient for FX or futures where overnight gaps are small.
```python
from Volatility.range_based import Parkinson

model = Parkinson(window=21, annualize=True)
vol = model.compute(df["High"].values, df["Low"].values)
```

---

### Garman-Klass

Uses all four OHLC prices — the most efficient classical daily estimator for equities where the open-close drift matters.
```python
from Volatility.range_based import GarmanKlass

model = GarmanKlass(window=21, annualize=True)
vol = model.compute(
    open_=df["Open"].values,
    high=df["High"].values,
    low=df["Low"].values,
    close=df["Close"].values,
)
```

---

### Downside Volatility

Computes vol using only negative return days — separates loss dispersion from gain dispersion, which rolling std conflates.
```python
from Volatility.assymetric import DownSideVolatility

model = DownSideVolatility(window=21, annualize=True)
downside_vol = model.compute(returns.values)

# Sortino ratio
ann_return = returns.mean() * 252
sortino = (ann_return - 0.05) / downside_vol[-1]
```

---

### Vol of Vol

Rolling standard deviation of a vol series — measures how much volatility is itself moving day to day.
```python
from Volatility.vol_of_vol import VolOfVol
from Volatility.realized import EWMA

ewma_vol = EWMA(alpha=0.94, span=20, days_per_annum=252).compute(returns.values)

model = VolOfVol(window=21)
vov = model.compute(ewma_vol)
```

---

## Forecasting and Evaluation

Each estimator's `predict(horizon)` shifts the vol series forward to produce a persistence forecast. `evaluate()` scores it against future realized vol using RMSE — useful for choosing the right estimator per instrument.
```python
from Volatility.range_based import Parkinson, GarmanKlass
from Volatility.realized import EWMA
from Volatility.evaluation import evaluate

high, low = df["High"].values, df["Low"].values
r = returns.values

results = {
    "Parkinson":   evaluate(Parkinson(21, annualize=False), r, {"high": high, "low": low}, horizon=5),
    "GarmanKlass": evaluate(GarmanKlass(21, annualize=False), r, {"open_": df["Open"].values, "high": high, "low": low, "close": df["Close"].values}, horizon=5),
    "EWMA":        evaluate(EWMA(0.94, 252, 20, annualize=False), r, {"returns": r}, horizon=5),
}

for name, rmse in results.items():
    print(f"{name:12s}  RMSE: {rmse:.6f}")
```

---

## Putting It Together
```python
import pandas as pd
import numpy as np
import yfinance as yf
from Volatility.realized    import RollingSTD, EWMA
from Volatility.range_based import GarmanKlass
from Volatility.assymetric  import DownSideVolatility
from Volatility.vol_of_vol  import VolOfVol

df      = yf.download("^GSPC", start="2020-01-01", end="2024-12-31")
returns = np.log(df["Close"] / df["Close"].shift(1)).dropna()
r       = returns.values
ev      = EWMA(alpha=0.94, span=20, days_per_annum=252).compute(r)

summary = pd.DataFrame({
    "rolling":    RollingSTD(21, 252).compute(returns),
    "ewma":       ev,
    "gk":         GarmanKlass(21).compute(df.Open.values, df.High.values, df.Low.values, df.Close.values),
    "downside":   DownSideVolatility(21, annualize=True).compute(r),
    "vol_of_vol": VolOfVol(21).compute(ev),
}, index=returns.index)

print(summary.tail(3))
```

---

## RegimeModel *(coming soon)*

The `RegimeModel` module will provide regime-switching models for identifying structural breaks and latent market states. Planned:

- Hidden Markov Model state estimation
- Regime-conditional vol and return statistics
- Transition probability matrices
- State sequence visualization

---


## License

MIT License © Umer Farooq
