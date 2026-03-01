import numpy as np 
import math
import pandas as pd

class RollingSTD():
    def __init__(self, window_size, days_per_annum, annualize:bool=True):
        self.window_size = window_size
        self.days_per_annum = days_per_annum
        self.annualize = annualize
    
    def compute(self, returns:np.ndarray) -> np.ndarray:
        vol = returns.rolling(self.window_size).std()

        if self.annualize:
            vol = vol * np.sqrt(self.days_per_annum)

        return vol.values

    def predict(self, **kwargs):
        vol = self.compute(**kwargs)
        return np.roll(vol, 1)

class EWMA():
    def __init__(self, alpha:float, days_per_annum, span, annualize:bool=True):
        self.alpha = 2 / (span + 1)
        self.days_per_annum = days_per_annum
        self.annualize = annualize
    
        if not 0 < alpha < 1:
            raise ValueError("Alpha must be between 0 and 1")

    def compute(self, returns:np.ndarray):
        r2 = returns**2
        var = np.zeros_like(r2) 

        var[0] = r2[0]
        for i in range(1, len(r2)):
            var[i] = self.alpha * r2[i-1] + (1-self.alpha) * var[i-1]

        vol = np.sqrt(var)
        if self.annualize:
            vol = vol * np.sqrt(self.days_per_annum)
        
        return vol
    
    def predict(self, **kwargs):
        vol = self.compute(**kwargs)
        return np.roll(vol, 1)    