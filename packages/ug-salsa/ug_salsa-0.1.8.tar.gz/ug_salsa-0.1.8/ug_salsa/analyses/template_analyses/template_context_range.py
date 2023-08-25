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
from salsa.analyses.template_analyses.normalize_signals_std_normal import NormalizeSignalsStandardNormal
class TemplateContextRange(TemplateAnalysis):

    def __init__(self, templates: Dict[str,TemplateData], norm_func = None) -> None:
        super().__init__(templates)
        self.norm_func = norm_func
        self.template = list(templates.values())[0]
        
    def preprocess_data(self) -> None:
        # CALC PER BASE AS WELL
        # Set default norm func
        if self.norm_func is None:
            self.norm_func = NormalizeSignalsStandardNormal
        
        self.template.sigmat = self.norm_func({self.template.name: self.template})
        median_signal = np.median(self.template.sigmat, axis = 0)
        keys = self.template.template_tk.flatten()
        
        incorp_inds = np.where(keys > 0)[0]
        normalized_medians = median_signal[incorp_inds]/keys[incorp_inds]
        self.context_range = (np.max(normalized_medians) - np.min(normalized_medians))/np.mean(normalized_medians)
        return

    def report_data(self) -> None:
        self.metrics.add(f"{self.template.name}_context_range", self.context_range)
        
        self.table = pd.DataFrame(data=np.vstack([['Context Range'],['%.3f' % self.context_range]]).T,
                            columns=['Metric', 'Value'])
        self.report_title = f'{self.template.name} Context Range - {self.runID}'
        return