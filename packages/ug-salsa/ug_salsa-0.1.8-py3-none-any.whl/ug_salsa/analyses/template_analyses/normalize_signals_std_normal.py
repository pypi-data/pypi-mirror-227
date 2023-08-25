from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
from salsa.data.templatedata import TemplateData

class NormalizeSignalsStandardNormal(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData], target_num: int = None) -> None:
        super().__init__(templates)
        self.target_num = target_num
        self.template = list(templates.values())[0]
        
    def preprocess_data(self) -> None:        
        self.sigmat = self.template.sigmat
        
        self.total_beads = self.sigmat.shape[0]
        if self.target_num is not None:
            self.num_samples = int(self.target_num)
            if self.total_beads > self.num_samples:
                self.seed = int(''.join([char for char in self.runID if char.isnumeric()])) % (2**32 - 1)
                self.order = np.random.RandomState(seed = self.seed).permutation(self.total_beads)[:np.min([self.num_samples, self.total_beads])]
                self.sigmat = self.sigmat[self.order]
        self.normed_sigmat = np.zeros(self.sigmat.shape)
        return

    def analyze_data(self) -> None:
        for base_ind in range(4):
            sigmat_subset = self.sigmat[:,base_ind::4]
            scaling_subset = self.sigmat[:,base_ind:200:4]
            total_m = np.mean(np.median(scaling_subset, axis = 0))
            total_s = np.std(np.median(scaling_subset, axis = 0))
            m = np.mean(scaling_subset, axis = 1)
            s = np.std(scaling_subset, axis = 1)
            sigmat_subset = (sigmat_subset - np.tile(m, (sigmat_subset.shape[1],1)).transpose())/np.tile(s, (sigmat_subset.shape[1],1)).transpose()
            sigmat_subset = sigmat_subset*total_s + total_m
            self.normed_sigmat[:,base_ind::4] = sigmat_subset

    def report_data(self) -> np.ndarray:
        self.table = None
        return self.normed_sigmat
    
    def run_without_output(self):
        self.preprocess_data()
        self.analyze_data()

    def get_sigmat(self):
        return self.report_data()