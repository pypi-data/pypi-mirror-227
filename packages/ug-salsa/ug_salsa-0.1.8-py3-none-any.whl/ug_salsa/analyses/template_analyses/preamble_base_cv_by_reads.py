from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData


class PreambleBaseCVByReads(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        
    def preprocess_data(self) -> None:
        self.total_sigmat = np.vstack([self.templates[template_name].sigmat[:,:4] for template_name in self.templates.keys()])
        return
    
    def report_data(self) -> None:
        for flow in range(4):
            total_mean = np.nanmean(self.total_sigmat[:,flow])
            total_std = np.nanstd(self.total_sigmat[:,flow])
            self.metrics.add(f'tf_preamble_bead_cv_{self.params["flow_order"][flow]}', total_std/total_mean)
        return