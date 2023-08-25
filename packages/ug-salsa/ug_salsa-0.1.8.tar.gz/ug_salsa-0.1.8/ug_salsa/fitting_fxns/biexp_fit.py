from salsa.fitting_fxns import Fit
import numpy as np
from scipy.optimize import curve_fit

class BiexpFit(Fit):

    def __init__(self) -> None:
        return
        
    def fitting_fxn(self, x, a1, b1, a2, b2):
      return (a1 * np.exp(b1*x)) + (a2 * np.exp(b2*x))

    def fit( x, y, self):    
        results = dict()
        results['x'] = x
        results['y'] = y    

        # filter out negative values
        positive_inds = np.where(y > 0)[0]
        y = y[positive_inds]
        x = x[positive_inds]

        # Bi-exponential fit
        halfway = len(x) // 2
        log_bc1, log_a1 = np.polyfit(x[:halfway], np.log(y[:halfway]), 1)
        log_bc2, log_a2 = np.polyfit(x[halfway:], np.log(y[halfway:]), 1)

        popt, _ = curve_fit(self.biexp, x, y,
                            p0=(np.exp(log_a1), log_bc1,
                            np.exp(log_a2), log_bc2),
                            bounds = [[0, -np.inf, 0, -np.inf], [np.inf, 0, np.inf, 0]],                           
                        maxfev = 10_000)
        fit_params = dict()
        fit_params['a1'] = popt[0]
        fit_params['b1'] = popt[1]
        fit_params['a2'] = popt[2]
        fit_params['b2'] = popt[3]
        results["fit_params"] = fit_params

        results['predicted'] = self.fitting_fxn(x,
                                    fit_params['a1'],
                                    fit_params['b1'],
                                    fit_params['a2'],
                                    fit_params['b2'])

        results['residuals'] = y - results['predicted']
        return results