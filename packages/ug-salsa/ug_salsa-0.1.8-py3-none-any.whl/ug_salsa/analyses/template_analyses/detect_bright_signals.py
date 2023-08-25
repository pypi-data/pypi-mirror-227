from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd

import salsa.plots.new_plots as new_plt
from salsa.data.templatedata import TemplateData
import os 

class DetectBrightSignals(TemplateAnalysis):
    
    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)

    def preprocess_data(self) -> None:
        self.tfsa1_cutoffs = np.load(os.path.join(os.path.dirname(__file__),'supplemental_data/TFSA1_bright_cutoff.npy'))
        self.tfsa2_cutoffs = np.load(os.path.join(os.path.dirname(__file__),'supplemental_data/TFSA2_bright_cutoff.npy'))
        self.num_flows = np.min([self.tfsa1_cutoffs.shape[0], self.tfsa2_cutoffs.shape[0]])
        return

    def analyze_data(self) -> None:
        self.profiles = {}
        for template in self.templates:
            medians = np.median( self.templates[template].sigmat[:,:self.num_flows], axis = 0)
            keys =  self.templates[template].template_tk[:self.num_flows]
            profile = np.zeros(medians.shape)
            
            for ind, _ in enumerate(["T","G","C","A"]):
                base_medians = medians[ind::4]
                base_keys = keys[ind::4]
                
                incorp_inds = np.where(base_keys > 0)[0]
                base_normalization_factor = np.median(base_medians[incorp_inds]/base_keys[incorp_inds])
                
                adjusted_base_keys = base_keys.copy()
                adjusted_base_keys[np.where(base_keys == 0)[0]] = 1
                
                profile[ind::4] = (base_medians/adjusted_base_keys)/base_normalization_factor
            self.profiles[template] = profile
            self.bright = int((self.profiles['TFSA1'] > self.tfsa1_cutoffs).any()*(self.profiles['TFSA2'] > self.tfsa2_cutoffs).any())
        return

    def report_data(self) -> None:
        self.metrics.add('tf_initial_bright_flow', self.bright)