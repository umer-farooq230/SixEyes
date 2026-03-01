# Downside volatility Upside volatility Semi-variance

import numpy as np

class DownSideVolatility:
    def __init__(self, window: int, annualize: bool = False, days_per_annum: int = 252):
        self.window = window
        self.annualize = annualize
        self.days_per_annum = days_per_annum

    def compute(self, returns:np.ndarray) -> np.ndarray:
        vol = np.full_like(returns, np.nan, dtype = float)

        for i in range(self.window - 1, len(returns)):
            window_slice = returns[i - self.window+1 : i+1]
            negative_returns = window_slice[window_slice < 0]

            if len(negative_returns) > 0:
                vol[i] = np.sqrt(np.mean(negative_returns**2) ) 

        if self.annualize:
            vol = vol * np.sqrt(self.days_per_annum)

        return vol           

    def predict(self, **kwargs):
        vol = self.compute(**kwargs)
        return np.roll(vol, 1)
