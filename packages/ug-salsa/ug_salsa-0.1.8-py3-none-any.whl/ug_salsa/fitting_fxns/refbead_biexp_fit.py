from salsa.fitting_fxns.biexp_fit import BiexpFit
from salsa.fitting_fxns.refbead_fit import RefBeadFit
import numpy as np
from salsa.helper_functions import log, MAPE

class RefBeadBiexpFit(BiexpFit, RefBeadFit):

      def __init__(self, sigmat: np.ndarray):
            super().__init__(sigmat)
            return
      
      def fit(self):
            try:
                  for i in range(4):
                        indices = range(0+i, self.num_flows, 4)
                        base_dict = self.attr_order[i]
                        x = self.x[indices]
                        y = self.y[indices]
                        base_dict['x'] = x
                        base_dict['y'] = y
                        
                        try:
                              #fit = biexp_fit(x, y)
                              fit = super().fit(x, y)
                              base_dict['predicted'] = fit['predicted']
                              base_dict['residuals'] = fit['residuals']
                              base_dict['fit_params'] = fit['fit_params']
                              base_dict['residual_metric'] = self.residual_metric(base_dict)

                        except Exception as e:
                              log('warning', f"Issue fitting refbead base {i}: {e}")
                              fit = None
                              base_dict['predicted'] = None
                              base_dict['residuals'] = None
                              base_dict['fit_params'] = None
                              base_dict['residual_metric'] = np.nan
                  
                  self.fit_success = True
                  
                  try:
                        rm_list = [base['residual_metric'] for base in self.attr_order]
                        self.r2 = np.nansum(rm_list)/np.sum(~np.isnan(rm_list))
                              
                  except:
                        self.r2 = np.nan
            except Exception as e:
                  log("info", f"Encountered Exception in fitting: {e}")
                  self.fit_success = False
            return

      def residual_metric(self, base_dict):
            y = base_dict['y']
            pred = base_dict['predicted']
            return MAPE(y, pred)
      
      def aggregate(self, field):
            result = np.zeros(self.y.shape, dtype = float)
            result[0::4] = self.T[field]
            result[1::4] = self.G[field]
            result[2::4] = self.C[field]
            result[3::4] = self.A[field]
            return result
      
      def get_rfit(self):
            return self.aggregate('predicted')
      
      def get_rb_resid(self):
            return self.aggregate('residuals')
      
      def get_rb_resid_sigma(self):
            return 100*np.std(self.aggregate('predicted'))
      
      def get_bleach_rate(self):
            return np.nan      
      
      def get_decay_percent_raw_signal(self):
            if self.num_flows < 200:
                  return np.nan
            return (self.y[0] - self.y[199])/self.y[0]
      
      def get_decay_percent_predicted(self):
            if self.num_flows < 200:
                  return np.nan
            try:
                  decays = [(b["predicted"][0] - b["predicted"][49])/(b["predicted"][0]) for b in self.attr_order]                  
                  return np.mean(decays)
            except Exception as e:
                  log('exception', e)
                  return np.nan
