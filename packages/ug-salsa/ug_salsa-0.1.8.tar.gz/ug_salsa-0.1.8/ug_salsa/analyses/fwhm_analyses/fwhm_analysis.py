from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData

class FWHMAnalysis(Analysis):
    def __init__(self, data: FWHMData) -> None:
        self.data: FWHMData = data


    def meets_conditions_for_analysis(self, bead_count: int = None) -> bool:
        if bead_count is None:
            bead_count = 1000
        if self.data.total_found < bead_count:
            print(f"Too few refbeads detected. Found {self.data.total_found}, require >1000.")
            return False
        return True