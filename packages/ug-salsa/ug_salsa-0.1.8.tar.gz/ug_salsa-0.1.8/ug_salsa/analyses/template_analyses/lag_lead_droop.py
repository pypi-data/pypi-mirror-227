from salsa.analyses.template_analyses import TemplateAnalysis
import numpy as np
import pandas as pd
from typing import Dict
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
from salsa.helper_functions import log
# from tool_noise import tool_noise
import salsa.plots.new_plots as new_plt
import numpy as np
import pandas as pd
import os
from scipy.optimize import minimize
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData
from salsa.analyses.template_analyses.floor_sig_per_base import FloorSignalPerBase
from salsa.analyses.template_analyses.base_1mer_fit_signal import Base1MerSignalFit

class LagLeadDroop(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        self.template: TemplateData = templates.values()[0]

        
    def preprocess_data(self) -> None:
        total_flows = self.template.sigmat.shape[1]
        self.cutoffs = np.append(np.arange(200, total_flows, 100), total_flows)[::-1]
        
        self.conversion_dict = {base: ind for ind, base in enumerate(self.params["flow_order"])}
        temp_medians: np.ndarray = np.median(self.template.sigmat, axis = 0)
        fsperbase = FloorSignalPerBase({self.template.name: self.template}, save = False)
        fsperbase.run_without_output()
        floor_vec = np.tile(fsperbase.get_floors(), (temp_medians.shape[0]//4) + 1)[:temp_medians.shape[0]]
        b1mersigfit = Base1MerSignalFit({self.template.name: self.template}, make_plot=False)
        b1mersigfit.run_without_output()
        base_1mer_vec = np.tile(b1mersigfit.get_fit_data()[0], (temp_medians.shape[0]//4) + 1)[:temp_medians.shape[0]]
        self.Sig_concat =  ((temp_medians - floor_vec)/(base_1mer_vec))
        return

    def analyze_data(self) -> None:
        
        self.data_dict = {}
        for i, cutoff in enumerate(self.cutoffs):
            log('info', f'        Working on L/L/D for {self.template.name} w/ max flow {cutoff}')
            flows = np.array([self.conversion_dict.get(letter, np.nan) for letter in self.template.flow_order[:cutoff]], dtype = int)
            sequence = np.array([self.conversion_dict.get(letter, np.nan) for letter in self.template.template_sq[:cutoff]], dtype = int)
            
    
            sig_concat = self.Sig_concat[:cutoff]
            
            ph0 = np.array([0.005, 0.005, 0.001]) #initialize lag, lead, droop
            
            #rss_i = templErr(ph0, flows, sequence, sig_concat)  # initial error
            ph = minimize(self.templErr, ph0, args = (flows, sequence, sig_concat), bounds=[(0,1),(0,1),(None,1)]).x
            #rss_f = templErr(ph, flows, sequence, sig_concat)  # final error
            
            simtrace, ph_eff = self.phase_keys(ph,flows,sequence)
            
            # explained variance
            sigvec = np.reshape(sig_concat, (1,np.size(sig_concat)))
            tot_var = np.sum( (sigvec - np.mean(sigvec) )**2)
            ve = 1 - np.sum( (sigvec - simtrace)**2)/tot_var
            
            # save outputs
            if i == 0:
                cutoff = 'max'
            
            self.metrics.add(f"{self.template.name}_lag_eff_pct_{cutoff}", ph_eff[0])
            self.metrics.add(f"{self.template.name}_lead_eff_pct_{cutoff}", ph_eff[1])
            self.metrics.add(f"{self.template.name}_droop_pct_{cutoff}", ph[2]*100)
            self.metrics.add(f"{self.template.name}_expl_var_pct_{cutoff}", ve*100)
            self.data_dict[cutoff] = ['%.5f' % (ph_eff[0]), '%.5f' % (ph_eff[1]),
                                 '%.5f' % (ph[2]*100), '%.1f' % (ve*100)]
        return

    def report_data(self) -> None:
        max_flows = list(self.data_dict.keys())[::-1]
        column_names = ['Calculated at Flow','Effective Lag (%)','Effective Lead (%)',
                        'Droop (%)','Variance Explained (%)']
        
        self.table = pd.DataFrame(data=np.vstack([max_flows,
                                 [self.data_dict[mf][0] for mf in max_flows],
                                 [self.data_dict[mf][1] for mf in max_flows],
                                 [self.data_dict[mf][2] for mf in max_flows],
                                 [self.data_dict[mf][3] for mf in max_flows],
                                 ]).T,
                            columns=column_names)
        self.report_title = f"{self.template.name} Phasing Metrics - {self.runID}"
        return
    