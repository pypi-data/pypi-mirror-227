from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

from salsa.fitting_fxns import RefBeadFit
from salsa.helper_functions import log
import numpy as np
import traceback

class NSB(RefBeadAnalysis):
        
    def __init__(self, data: RefBeadData, fit: RefBeadFit) -> None:
        super().__init__(data)
        self.outputs: dict[str, np.ndarray] = {}
        self.fit = fit
        return
    
    def analyze_data(self) -> None:
        min_per_cycle = self.get_min_per_cycle()
        
        for b, x in zip(['T','G','C','A'], self.fit.get_attr_order()):
            try:
                if x['predicted'] is not None:
                    self.outputs[b] = np.mean(x['predicted'] - min_per_cycle)
                else:
                    self.outputs[b] = np.nan
            except:
                self.outputs[b] = np.nan
                log('exception', f'Failed to generate NSB metrcis for base {b}: {traceback.format_exc()}')
            self.metrics.add(f"rb_sig_offset_{b}", self.outputs[b])
        return

    def report_data(self) -> None:
        pass
    
    def get_min_per_cycle(self)-> np.ndarray:
        total_predicted = np.vstack([x['predicted'] for x in self.fit.get_attr_order() if x['predicted'] is not None])
        min_per_cycle = np.min(total_predicted, axis = 0)
        return min_per_cycle
    
    def get_output(self):
        return self.outputs