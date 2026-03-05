import numpy as np

def future_realized_vol(returns: np.ndarray, horizon: int = 1) -> np.ndarray:
    realized = np.full_like(returns, np.nan, dtype=float)
    n=len(realized)
    for i in range(n - horizon):
        window = returns[i+1 : i+1 + horizon]
        realized[i] = np.sqrt(np.mean(window **2))
        
    return realized


def rmse(predicted: np.ndarray, realized: np.ndarray) -> float:
    mask = ~np.isnan(predicted) & ~np.isnan(realized)
    return np.sqrt(np.mean((predicted[mask] - realized[mask])**2))


def evaluate(model, returns: np.ndarray, 
             compute_kwargs: dict,
             horizon: int = 1) -> float:
    
    forecast = model.predict(horizon=horizon, **compute_kwargs)
    realized = future_realized_vol(returns, horizon=horizon)

    return rmse(forecast, realized)