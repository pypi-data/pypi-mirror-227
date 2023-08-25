from salsa.fitting_fxns import Fit
import numpy as np
from salsa.helper_functions import log, MAPE

class RefBeadFit(Fit):

      def __init__(self, sigmat: np.ndarray):
            last_cycle = sigmat.shape[0] // 4
            self.num_flows = 4 * last_cycle
            self.y = sigmat[:self.num_flows]
            self.x = np.array(range(1, self.num_flows + 1), dtype= np.float32)
            self.fit_success = False
            
            self.T = dict()
            self.G = dict()
            self.C = dict()
            self.A = dict()
            self.r2 = np.ndarray(0,)
            self.attr_order = [self.T, self.G, self.C, self.A]
            self.order = ['T', 'G', 'C', 'A']
            self.color = ['r', 'k', 'b', 'g']          
            return
    
      def residual_metric(self, base_dict):
            y = base_dict['y']
            pred = base_dict['predicted']
            return MAPE(y, pred)
      
      def get_attr_order(self):
            return self.attr_order
      
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
                  
      def get_ref_stability(self):
        return {"overall": self.r2,
                              "T": self.T['residual_metric'] if ~np.isnan(self.T['residual_metric']) else None,
                              "G": self.G['residual_metric'] if ~np.isnan(self.G['residual_metric']) else None,
                              "C": self.C['residual_metric'] if ~np.isnan(self.C['residual_metric']) else None,
                              "A": self.A['residual_metric'] if ~np.isnan(self.A['residual_metric']) else None,
                              "% decay (predicted)": self.get_decay_percent_predicted(),
                              "% decay (raw signal)": self.get_decay_percent_raw_signal()}
      
      def get_intercepts(self):
            return {
                              'rb_fit_int_T': int(self.T['predicted'][0]) if self.T['predicted'] is not None else np.nan,
                              'rb_fit_int_G': int(self.G['predicted'][0]) if self.G['predicted'] is not None else np.nan,
                              'rb_fit_int_C': int(self.C['predicted'][0]) if self.C['predicted'] is not None else np.nan,
                              'rb_fit_int_A': int(self.A['predicted'][0]) if self.A['predicted'] is not None else np.nan,
            }
      
      