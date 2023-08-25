from salsa.analyses import Analysis
from typing import Dict
from salsa.data import TemplateData
from salsa.plots.new_plots import PlotHandler
from salsa.helper_functions import log
import traceback
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

class HighHmerCorrelation(Analysis):
    
    def __init__(self, templates: Dict[str, TemplateData]):
        super().__init__(templates)
        self.templates = templates
        self.runID = self.templates['TFSA1'].runID
        
    def preprocess_data(self) -> None:
        thresh = 1000
        supported_templates = ['TFHP20T', 'TFHP20A', 'TFHP30T', 'TFHP30A']
        
        # for template in supported_templates:
        #     try:
        #         self.load_template(f"{self.params['base_out']}RunID{self.runID}_template_{template}.mat")
        #         log("info",f"High hmer template analysis: template {template} loaded")
        #     except FileNotFoundError:
        #         log("warning",f"High hmer template analysis: template {template} not found")
        #     except Exception:
        #         log("exception", traceback.format_exc())
        
        valid_templates = [template for template in self.templates if (template.name in supported_templates and template.sigmat.shape[0] > thresh)]
        if not valid_templates:
            log("info", "No high hmer templates found, skipping correlation")
            return
        
        valid_templates_names = [template.name for template in valid_templates]
        self.valid_templates = valid_templates
        log("info",f"Valid high hmer templates: {valid_templates_names}")
        
        return
    
    def analyze_data(self) -> None:
        df = pd.DataFrame(index = [template.name for template in self.valid_templates], columns=['Before','After'])
        
        for template in self.valid_templates:
            sigmat = template.sigmat
            sigmat_medians = np.nanmedian(sigmat, axis = 0)
            keys = template.template_tk
    
            high_hmer_flow = np.where(keys > 19)[0]
            if high_hmer_flow.shape[0] == 0:
                continue
            high_hmer_flow = high_hmer_flow[0]
            
            before_flows = [high_hmer_flow - 24, high_hmer_flow - 4]
            after_flows = [high_hmer_flow + 5, high_hmer_flow + 25]
            
            keys_before_high_hmer = keys[before_flows[0]:before_flows[1]]
            keys_after_high_hmer = keys[after_flows[0]:after_flows[1]]
            sigmat_median_before_high_hmer = sigmat_medians[before_flows[0]:before_flows[1]]
            sigmat_median_after_high_hmer = sigmat_medians[after_flows[0]:after_flows[1]]
            
            corrs_before = []
            corrs_after = []
            
            for i in range(4):
                k_b = keys_before_high_hmer[i::4]
                k_a = keys_after_high_hmer[i::4]
                s_b = sigmat_median_before_high_hmer[i::4]
                s_a = sigmat_median_after_high_hmer[i::4]
                
                corr_before, _ = pearsonr(s_b, k_b)
                corr_after, _ = pearsonr(s_a, k_a)
                corrs_before.append(corr_before)
                corrs_after.append(corr_after)
                
            aggregated_correlation_before = np.nanmean(corrs_before)
            aggregated_correlation_after = np.nanmean(corrs_after)
            self.metrics.add(f"tf_{template}_correlation_before", aggregated_correlation_before)
            self.metrics.add(f"tf_{template}_correlation_after", aggregated_correlation_after)
            df.loc[(template,"Before")] = aggregated_correlation_before
            df.loc[(template,"After")] = aggregated_correlation_after
        df.insert(0, "Template", df.index)
        self.high_hmer_df = df
        return 
    
    def report_data(self) -> None:
        PlotHandler.add_table_to_report(self.high_hmer_df, f"High Hmer Correlation - {self.runID}")
        return
    
    def plot_data(self) -> None:
        return