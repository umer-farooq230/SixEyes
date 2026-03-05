import numpy as np
import math
import pandas as pd


class Parkinson:
    def __init__(self, window: int, annualize: bool = True, days_per_annum: int = 252):
        self.window = window
        self.annualize = annualize
        self.days_per_annum = days_per_annum

    def compute(self, high: np.ndarray, low: np.ndarray) -> np.ndarray:
        log_hl = np.log(high / low)

        daily_var = (1 / (4 * np.log(2))) * (log_hl ** 2)

        rolling_var = pd.Series(daily_var).rolling(self.window).mean()

        vol = np.sqrt(rolling_var)

        if self.annualize:
            vol *= np.sqrt(self.days_per_annum)

        return vol.values

    def predict(self, horizon: int = 1, **kwargs):
        vol = self.compute(**kwargs)
    
        forecast = np.full_like(vol, np.nan, dtype=float)
        forecast[horizon:] = vol[:-horizon]
    
        return forecast    

class GarmanKlass:
    def __init__(self, window: int, annualize: bool = True, days_per_annum: int = 252):
        self.window = window
        self.annualize = annualize
        self.days_per_annum = days_per_annum

    def compute(self, open_: np.ndarray,
                      high: np.ndarray,
                      low: np.ndarray,
                      close: np.ndarray) -> np.ndarray:

        log_hl = np.log(high / low)
        log_co = np.log(close / open_)

        daily_var = (
            0.5 * (log_hl ** 2)
            - (2 * np.log(2) - 1) * (log_co ** 2)
        )

        rolling_var = pd.Series(daily_var).rolling(self.window).mean()

        vol = np.sqrt(rolling_var)

        if self.annualize:
            vol *= np.sqrt(self.days_per_annum)
 
        return vol.values
    
    def predict(self, horizon: int = 1, **kwargs):
        vol = self.compute(**kwargs)
    
        forecast = np.full_like(vol, np.nan, dtype=float)
        forecast[horizon:] = vol[:-horizon]
    
        return forecast    