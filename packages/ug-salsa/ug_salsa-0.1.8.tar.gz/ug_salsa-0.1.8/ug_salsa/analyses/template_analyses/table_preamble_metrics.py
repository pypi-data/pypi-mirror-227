from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import salsa.plots.new_plots as new_plt
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData


class MakePreambleMetrics(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)   
        
    def preprocess_data(self) -> None:
        self.metric_names = [['Mean Signal', 'Bead CV', 'Tile CV']]
        self.vals = [[self.metrics.get(f'tf_preamble_{base}'),
                 "%.3f" % self.metrics.get(f'tf_preamble_bead_cv_{base}'),
                 "%.3f" % self.metrics.get(f'tf_preamble_tile_cv_{base}')] for base in ['T','G','C','A']]
        self.metric_names.extend(self.vals)
        
        self.table = pd.DataFrame(data=np.vstack(self.metric_names).T,
                             columns=['Metric', 'T', 'G', 'C', 'A'])
        return

    def report_data(self) -> None:
        self.report_title = f'Template Preamble Metrics - {self.runID}'
        return