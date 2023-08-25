from salsa.data import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
import numpy as np
# from salsa.data import *

class TTECPreambleBaseMean(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        self.num_beads = self.data.sigmat.shape[0]

    def report_data(self) -> None:
        for flow, base in enumerate(self.params['flow_order']):
            preamble_mean = np.nansum(self.data.sigmat[:, flow] / self.num_beads)
            self.metrics.add(
                f"ec_preamble_{base}", int(preamble_mean)
            )
