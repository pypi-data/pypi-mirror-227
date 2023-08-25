#%% Load imports
import numpy as np
import pandas as pd
from collections import UserDict
from itertools import combinations

from salsa.parameters import Parameters
from salsa.helper_functions import log
class Nexus:
    pass
# try:
#     from salsa.nexus import Nexus
# except ImportError:
#     pass

#%% metrics class
class RunMetrics(UserDict):
    
    _metrics = {}
    
    def __init__(self, runID: str = ''):
        self.params = Parameters()
        if runID:
            self.runID = runID
        else:
            self.runID = self.params['runid']
        self.data = self._metrics
        return
    
    def add(self, key, value):
        self._metrics[key] = value
        # try:
        #     Nexus.update_metrics(self.runID, {key: value}, purpose='rundmc')
        # except Exception as e:
        #     log('warning',f"Failed to update Nexus metrics with {dict({key: value})}. Error: {e}")
        return
        
    def update_report(self, key, value):
        return Nexus.update_report(key, value)
    
    def to_csv(self, filename = None, *args, **kwargs):
        if filename is None:
            filename = f"{self.params['save_loc']}/RunID{self.runID}_denominator_metrics.csv"    
        with open(f"{self.params['save_loc']}RunID{self.params['runid']}_uploads_list.txt", 'a+') as file:
            file.write(f"RunID{self.runID}_denominator_metrics.csv\n")
        
        keys = self._metrics.keys()
        out_df = pd.DataFrame(index=keys, columns=["value"])
        for k in keys:
            out_df.loc[(k,"value")] = self._metrics[k]
        out_df.to_csv(filename, *args, **kwargs)
        return
    
    # def take_ratio(self, numerator_name, denominator_name, output_name):
    #     numerator_val = self._metrics.get(numerator_name, None)
    #     denominator_val = self._metrics.get(denominator_name, None)
    #     if numerator_val is None or denominator_val is None:
    #         out = np.nan
    #     else:
    #         out = numerator_val/denominator_val
    #     self._metrics[output_name] = out
    #     return
    
    # def compute_ratios(self):
        
    #     for base in ['T','G','C','A']:
    #         self.take_ratio(f'ec_1mer_1{base}', f'tf_1mer_fit_1{base}',
    #                         f'ec_to_tf_1mer_ratio_{base}')
            
    #         self.take_ratio(f'ec_preamble_{base}', f'ec_1mer_1{base}',
    #                         f'ec_preamble_to_1mer_fit_ratio_{base}')
            
    #         self.take_ratio(f'tf_preamble_{base}', f'tf_1mer_fit_1{base}',
    #                         f'tf_preamble_raw_to_fit_ratio_{base}')
            
    #         self.take_ratio(f'tf_1mer_fit_1{base}', f'rb_fit_1{base}',
    #                         f'tf_to_rb_1mer_ratio_{base}')
            
    #         self.take_ratio(f'ec_1mer_1{base}', f'rb_fit_1{base}',
    #                         f'ec_to_rb_1mer_ratio_{base}')
        
    #     base_combinations = combinations('TGCA', 2)
    #     for b1, b2 in base_combinations:
    #         self.take_ratio(f'ec_droop_{b1}', f'ec_droop_{b2}',
    #                         f'ec_droop_ratio_{b1}_to_{b2}')

    #     return