from salsa.fitting_fxns import Fit
import numpy as np
from scipy.optimize import curve_fit

class SingleExpFit(Fit):

    def __init__(self) -> None:
        return
    
    def fitting_fxn(self, x, L, r, k):
        return L*np.exp(r*x) + k


    def fit(self, x, y):    
        results = dict()
        results['x'] = x
        results['y'] = y

        L_0 = np.max(y)
        r_0 = -1.0
        k_0 = np.min(y)

        popt, _ = curve_fit(
            self.fitting_fxn,
            x,
            y,
            p0=(L_0, r_0, k_0),
            bounds=[[0, -np.inf, -1000], [np.inf, 0, np.inf]],
            maxfev=10000,
        )
        fit_params = dict()
        fit_params['L'] = popt[0]
        fit_params['r'] = popt[1]
        fit_params['k'] = popt[2]
        results["fit_params"] = fit_params
        results['predicted'] = self.fitting_fxn(x,
                                        fit_params['L'],
                                        fit_params['r'],
                                        fit_params['k'])


        results['residuals'] = y - results['predicted']
        return results