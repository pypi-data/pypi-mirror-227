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
from salsa.analyses.template_analyses.base_1mer_fit_signal import Base1MerSignalFit
from salsa.analyses.template_analyses.floor_sig_per_base import FloorSignalPerBase

class MisincorpRate(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates) 
        
    def preprocess_data(self) -> None:
        self.sigmat_med = np.median(self.templates["TFSA2"].sigmat, axis = 0)
        self.misincorp_flows = {"T": 12,
                           "G": 85,
                           "C": 98,
                           "A": 131}
        fsperbase = FloorSignalPerBase({"TFSA2": self.templates["TFSA2"]}, save=False)
        fsperbase.run_without_output()
        floor_signals = {base: floor for base, floor in zip(['T','G','C','A'], fsperbase.get_floors())}
        tfsa2_fit = Base1MerSignalFit({"TFSA2": self.templates["TFSA2"]}, make_plot=False)
        tfsa2_fit.run_without_output()
        A, b, _, _ = tfsa2_fit.get_fit_data()
        base_1mer_signal = {base: (A[ind]*np.exp(b[ind] * np.arange(1,201))) for base, ind in zip(['T','G','C','A'],range(4))}
        
        self.misincorp_rate_list = []
        self.misincorp_signal_list = []
        for base in ['T','G','C','A']:
            self.misincorp_flow = self.misincorp_flows[base]
            self.misincorporation_rate = ((self.sigmat_med[self.misincorp_flow] - floor_signals[base]) 
                                     / (base_1mer_signal[base][self.misincorp_flow] - floor_signals[base]))
            self.metrics.add(f"TFSA2_misincorp_rate_{base}", self.misincorporation_rate)
            self.metrics.add(f"TFSA2_misincorp_signal_{base}", int(self.sigmat_med[self.misincorp_flow]))
            self.misincorp_rate_list.append('%.3f' % self.misincorporation_rate)
            self.misincorp_signal_list.append(int(self.sigmat_med[self.misincorp_flow]))
        return
    
    def report_data(self) -> None:
        self.table = pd.DataFrame(data=np.vstack([['T','G','C','A'],
                                 self.misincorp_rate_list,
                                 self.misincorp_signal_list]).T,
                            columns=['Base', 'Misincorp Rate', "Misincorp Signal"])
        self.report_title = f"Misincorporation Metrics - {self.runID}"
        return