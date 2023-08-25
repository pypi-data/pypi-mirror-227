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

class PreambleBaseMean(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)  

    def report_data(self) -> None:
        for flow in range(4):
            preamble_mean = 0
            count = 0
            for template_name in self.templates.keys():
                preamble_mean += np.nanmean(self.templates[template_name].sigmat[:,flow])
                count += 1
            self.metrics.add(f"tf_preamble_{self.params['flow_order'][flow]}", int(preamble_mean/count))
        return