from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from salsa.data import TemplateData
from salsa.analyses.template_analyses.base_1mer_fit_signal import Base1MerSignalFit


class Base1MerSignalFitAggregated(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        
    def preprocess_data(self) -> None:
        self.intercepts = {ind:0 for ind in range(4)}
        self.early_intercepts = {ind:0 for ind in range(4)}
        self.count = {ind:0 for ind in range(4)}
        return

    def analyze_data(self) -> None:
        for template in self.templates.keys():
            b1merfit = Base1MerSignalFit({template.name : template})
            b1merfit.run_without_output()
            early_fit, _, temp_fit, _ = b1merfit.get_fit_data()
            self.subanalysis_figs.append(b1merfit.fig) 
            for base_num, fit in enumerate(temp_fit):
                self.intercepts[base_num] += fit*(~np.isnan(fit))
                self.early_intercepts[base_num] += early_fit[base_num]*(~np.isnan(early_fit[base_num]))
                self.count[base_num] += 1*(~np.isnan(fit))
        return

    def report_data(self) -> None:
        self.fit_data = []
        self.early_fit_data = []
        for base_num in range(4):
            if np.isnan(self.intercepts[base_num]) or np.isnan(self.early_intercepts[base_num]) or self.count[base_num] == 0:
                self.fit_data.append(np.nan)
                self.early_fit_data.append(np.nan)
                self.metrics.add(f"tf_1mer_fit_1{self.params['flow_order'][base_num]}", np.nan)
                self.metrics.add(f"tf_1mer_fit_1{self.params['flow_order'][base_num]}_200", np.nan)
            else:
                self.fit_data.append(int(self.intercepts[base_num]/self.count[base_num]))
                self.early_fit_data.append(int(self.early_intercepts[base_num]/self.count[base_num]))
                self.metrics.add(f"tf_1mer_fit_1{self.params['flow_order'][base_num]}", int(self.intercepts[base_num]/self.count[base_num]))
                self.metrics.add(f"tf_1mer_fit_1{self.params['flow_order'][base_num]}_200",
                                int(self.early_intercepts[base_num]/self.count[base_num]))
        self.table = pd.DataFrame(data=np.vstack([['T','G','C','A'],self.fit_data, self.early_fit_data]).T,
                             columns=['Base', '1mer Fit Intecept', '1mer Early Fit Intercept'])
        self.report_title = f"Template 1mer Fit Metrics - {self.runID}"
        return