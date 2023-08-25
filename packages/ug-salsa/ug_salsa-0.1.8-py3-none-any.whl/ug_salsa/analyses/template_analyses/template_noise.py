from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData
import salsa.plots.new_plots as new_plt
import types

class TemplateNoise(TemplateAnalysis):


    def __init__(self, templates: Dict[str, TemplateData], norm_func: types.FunctionType = None) -> None:
        super().__init__(templates)
        self.template: TemplateData = list(templates.values())[0]
        self.norm_func = norm_func    
        
    def preprocess_data(self) -> None:
        # set default norm func
        if self.norm_func is None:
            self.norm_func = self.signals_standard_normal
        
        sigmat = self.norm_func(self.template)
        
        # average normalized signal over beads per flow
        self.median_signal = np.nanmedian(sigmat, axis = 0)
        self.std_signal = np.nanstd(sigmat, axis = 0)
        self.keys = self.template.template_tk.flatten()
        
        # below incorp_ variables are all 1 x num_flows arrays
        incorp_inds = np.where(self.keys > 0)[0]
        incorp_signal = self.median_signal[incorp_inds]
        incorp_number = self.keys[incorp_inds]
        
        # below incorp_ variables are single numbers (averaged over flows)
        incorp_mean = np.mean(incorp_signal/incorp_number)
        incorp_std = np.sqrt(np.sum((self.std_signal[incorp_inds]/incorp_number)**2)/np.sum(incorp_number))
        self.incorp_noise = incorp_std/incorp_mean
        self.metrics.add(f"{self.template}_noise", self.incorp_noise)
        return

    def analyze_data(self) -> None:
        return

    def report_data(self) -> None:
        noise_list = ['%.3f' % self.incorp_noise]
        for base_num in range(4):
            base_keys = self.keys[base_num::4]
            base_incorp_inds = np.where(base_keys > 0)[0]
            base_median = self.median_signal[base_num::4][base_incorp_inds]
            base_incorp_number = base_keys[base_incorp_inds]
            
            base_incorp_mean = np.mean(base_median/base_incorp_number)
            base_incorp_std = np.sqrt(np.sum((self.std_signal[base_num::4][base_incorp_inds]/base_incorp_number)**2)/np.sum(base_incorp_number))
            base_incorp_noise = base_incorp_std/base_incorp_mean
            self.metrics.add(f"{self.template.name}_noise_{self.params['flow_order'][base_num]}", base_incorp_noise)
            noise_list.append('%.3f' % base_incorp_noise)
        
        self.table = pd.DataFrame(data=np.vstack([['Overall','T','G','C','A'],noise_list]).T,
                             columns=['Base', 'Noise'])
        self.report_title = f'{self.template.name} Noise - {self.runID}'
        return
    