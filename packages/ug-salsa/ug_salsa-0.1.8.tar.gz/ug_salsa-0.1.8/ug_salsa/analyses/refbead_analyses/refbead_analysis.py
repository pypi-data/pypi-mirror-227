from salsa.analyses.analysis import Analysis
from salsa.data.refbeaddata import RefBeadData
from salsa.fitting_fxns.refbead_biexp_fit import RefBeadBiexpFit

class RefBeadAnalysis(Analysis):

    def __init__(self, data: RefBeadData, fit: RefBeadBiexpFit = None) -> None:
        self.data: RefBeadData = data
        self.fit = fit
    
    def meets_conditions_for_analysis(self, bead_count: int = None) -> bool:
        if bead_count is None:
            bead_count = 1000
        if self.data.sigmat.shape[0] < bead_count:
            print(f"Too few refbeads detected. Found {self.data.sigmat.shape[0]}, require >1000.")
            return False
        return True