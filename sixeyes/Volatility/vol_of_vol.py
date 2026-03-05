import numpy as np

class VolOfVol:
    def __init__(self, window: int, annualize: bool = False, days_per_annum: int = 252):
        self.window = window
        self.annualize = annualize
        self.days_per_annum = days_per_annum

    def compute(self, vol_series: np.ndarray) -> np.ndarray:
        vov = np.full_like(vol_series, np.nan, dtype=float)

        for i in range(self.window - 1, len(vol_series)):
            window_slice = vol_series[i - self.window + 1 : i + 1]
            vov[i] = np.std(window_slice, ddof=1)

        if self.annualize:
            vov *= np.sqrt(self.days_per_annum)

        return vov

    def predict(self, horizon: int = 1, **kwargs):
        vol = self.compute(**kwargs)
    
        forecast = np.full_like(vol, np.nan, dtype=float)
        forecast[horizon:] = vol[:-horizon]
    
        return forecast    