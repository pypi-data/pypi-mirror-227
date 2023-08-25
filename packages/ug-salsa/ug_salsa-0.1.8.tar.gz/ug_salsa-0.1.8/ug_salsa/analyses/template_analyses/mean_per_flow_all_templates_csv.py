from salsa.analyses.template_analyses import TemplateAnalysis
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data import TemplateData
from typing import Dict, Any

class MeanPerFlowAllTemplatesCSV(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData], output_name: str = None) -> None:
        super().__init__(templates)
        self.output_name = output_name
        
    def preprocess_data(self) -> None:
        self.template_names = list(self.templates.keys())
        self.nflows = self.templates[self.templates.keys()[0]].sigmat.shape[1]
        self.flow_nums = [f'flow{"%03d" % flow}' for flow in range(1, self.nflows + 1)]
        self.signal_mean_per_flow_df = pd.DataFrame(index=self.template_names, columns=self.flow_nums)
        for template in self.template.keys():
            self.signal_mean_per_flow_df.loc[template] = np.nanmean(self.templates[template].sigmat, axis = 0)
        return
    def report_data(self) -> None:
        if self.output_name is not None:
            self.signal_mean_per_flow_df.to_csv(f"{self.params['save_loc']}{self.output_name}.csv")
            with open(f"{self.params['save_loc']}RunID{self.params['runid']}_uploads_list.txt", 'a+') as file:
                file.write(f"{self.output_name}.csv\n") 