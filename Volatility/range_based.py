import numpy as np
import math
import pandas as pd


class Parkinson:
    def __init__(self, window: int, annualize: bool = True, periods_per_year: int = 252):
        self.window = window
        self.annualize = annualize
        self.periods_per_year = periods_per_year

    def compute(self, high: np.ndarray, low: np.ndarray) -> np.ndarray:
        log_hl = np.log(high / low)

        daily_var = (1 / (4 * np.log(2))) * (log_hl ** 2)

        rolling_var = pd.Series(daily_var).rolling(self.window).mean()

        vol = np.sqrt(rolling_var)

        if self.annualize:
            vol *= np.sqrt(self.periods_per_year)

        return vol.values

class GarmanKlass:
    def __init__(self, window: int, annualize: bool = True, periods_per_year: int = 252):
        self.window = window
        self.annualize = annualize
        self.periods_per_year = periods_per_year

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
            vol *= np.sqrt(self.periods_per_year)
 
        return vol.values