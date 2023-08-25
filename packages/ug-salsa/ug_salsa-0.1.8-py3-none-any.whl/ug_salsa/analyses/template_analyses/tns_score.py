from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
from salsa.analyses.template_analyses.tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data import TemplateData
import salsa.plots.new_plots as new_plt

class TNSScore(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)    
        
    def preprocess_data(self) -> None:
        self.TNS_data = tool_noise([self.sample_beads(temp, 50000) for temp in self.templates.values()], self.params)
        self.TNS_metrics = {f"tf_TNS_{base}": self.NS_data[f"TNS_{base}"] for base in ['T','G','C','A']}
        self.TNS_metrics['tf_TNS'] = np.nanmean(list(self.TNS_metrics.values()))          
        return

    def analyze_data(self) -> None:
        return

    def report_data(self) -> None:
        for metric_name, metric_value in self.TNS_metrics.items():
            self.metrics.add(metric_name, metric_value)
        #TNS_score = np.mean([TNS_data[f"TNS_{base}"] for base in ['T','G','C','A']])
        #self.metrics.add("tf_TNS", TNS_score)
        
        self.table = pd.DataFrame(data=np.vstack([['T','G','C','A','Overall'],
                                 ['%.3f' % self.TNS_metrics["tf_TNS_T"],
                                  '%.3f' % self.TNS_metrics["tf_TNS_G"],
                                  '%.3f' % self.TNS_metrics["tf_TNS_C"],
                                  '%.3f' % self.TNS_metrics["tf_TNS_A"],
                                  '%.3f' % self.TNS_metrics["tf_TNS"]]]).T,
                            columns=['Base', 'TNS Score'])
        self.report_title = f'Tool Noise Score - {self.runID}'
        return