from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData
from salsa.analyses.template_analyses.normalize_signals_std_normal import NormalizeSignalsStandardNormal
from salsa.helper_functions import log

class TemplateSTS(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData], norm_func = None) -> None:
        super().__init__(templates)
        self.norm_func = norm_func
        self.template: TemplateData = list(templates.values())[0]
        
    def preprocess_data(self) -> None:        
        # Set default norm func
        if self.norm_func is None:
            self.norm_func = NormalizeSignalsStandardNormal
        
        self.norm_func({self.template.name: self.template}, 50000).run_without_output()
        self.SigMat = self.norm_func.get_sigmat()
        self.num_beads, self.num_flows = self.SigMat.shape
        self.cutoffs = np.append(np.arange(200, self.num_flows, 100), self.num_flows)[::-1]

        self.tk = self.template.template_tk.flatten()
        self.nbase = 4
        
        self.flow_order = self.template.flow_order
        
        self.train_vec = np.zeros( self.num_beads )
        self.n0 = self.num_beads//2
        self.train_vec[np.random.permutation(self.num_beads)[:self.n0]] = 1
        self.train_vec[:] = 1
        self.test_vec = self.train_vec
        self.base_vec = -1 * np.ones(self.tk.shape)
        self.base_ind_dict = {self.params["flow_order"][ind]: ind for ind in range(len(self.params["flow_order"]))}        
        return

    def analyze_data(self) -> None:
        self.data_dict = {}
        for i, target_flow in enumerate(self.cutoffs):
            log('info', f'        Working on STS for {self.template.name} w/ max flow {target_flow}')        
            self.flowsQ = [0, self.target_flow]
            
            for ind in range(np.min([len(self.base_vec), self.flowsQ[1] + 1])):
                self.base_vec[ind] = self.base_ind_dict.get(self.flow_order[ind], np.nan)
            
            pred_mat = np.zeros(self.SigMat.shape)
            for base_ind in range(self.nbase):
                self.ukey = np.unique( self.tk[self.base_vec == base_ind] )
        
                for lower_ind in range(len(self.ukey)-1):
                    upper_ind = lower_ind + 1
                    self.flows1 = np.where( (self.tk<=self.ukey[lower_ind]) & (self.base_vec == base_ind) )[0]
                    self.signal_vec1 = self.SigMat[self.train_vec==1,:][:,self.flows1].flatten()
        
                    self.flows2 = np.where( (self.tk>=self.ukey[upper_ind]) & (self.base_vec == base_ind) )[0]
                    self.signal_vec2 = self.SigMat[self.train_vec==1,:][:,self.flows2].flatten()
        
                    # set threshold on train, apply to test, and predict
                    if (len(self.signal_vec1) + len(self.signal_vec2)) > 100:
                        threshold = self.best_threshold( self.signal_vec1, self.signal_vec2 ) #need to write
                        flows_all = np.where( (self.base_vec == base_ind) )[0]
                        # assign TK
                        for k in range(len(flows_all)):
                            locs2 = np.where( (self.test_vec == 1) & (self.SigMat[:,flows_all[k]] > threshold) )[0]
                            pred_mat[locs2,flows_all[k]] = self.ukey[upper_ind]
            
            self.tk_mat = np.repeat(self.tk[None,:target_flow], pred_mat.shape[0], 0)
            self.err_tot = np.sum(np.abs( pred_mat[:,:target_flow].flatten() - self.tk_mat.flatten() )) / np.sum( self.tk_mat.flatten() )
            self.sts = -10*np.log10(self.err_tot)
            
            if i == 0:
                target_flow = 'max'
            
            self.metrics.add(f"{self.template.name}_STS_{target_flow}", self.sts)
            self.data_dict[target_flow] = '%.3f' % self.sts
        return

    def report_data(self) -> None:
        keys = list(self.data_dict.keys())[::-1]
        values = [self.data_dict[k] for k in keys]
        
        self.table = pd.DataFrame(data=np.vstack([keys, values]).T,
                            columns=['Calculated at Flow', 'STS'])
        self.report_title = f'{self.template.name} STS - {self.runID}'
        return