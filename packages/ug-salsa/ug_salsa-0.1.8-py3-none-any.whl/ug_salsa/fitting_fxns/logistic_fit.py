from scipy.optimize import curve_fit
from salsa.fitting_fxns import Fit
import numpy as np

class LogisticFit(Fit):

    def __init__(self) -> None:
        return
    
    def fitting_fxn (self, x, L, r, x0):
        return L / (1 + np.exp(-r * (x - x0)))



    def fit(self, x, y):    
        results = dict()
        results['x'] = x
        results['y'] = y

        L_0 = np.max(y)
        r_0 = 1.0
        x0_0 = np.mean(x)

        popt, _ = curve_fit(
            self.fitting_fxn,
            x,
            y,
            p0=(L_0, r_0, x0_0),
            bounds=([0, 0, np.min(x)], [np.inf, np.inf, np.max(x)]),
            maxfev=10000,
        )
        fit_params = dict()
        fit_params['L'] = popt[0]
        fit_params['r'] = popt[1]
        fit_params['x0'] = popt[2]
        results["fit_params"] = fit_params
        results['predicted'] = self.fitting_fxn(x,
                                        fit_params['L'],
                                        fit_params['r'],
                                        fit_params['x0'])


        results['residuals'] = y - results['predicted']
        return results