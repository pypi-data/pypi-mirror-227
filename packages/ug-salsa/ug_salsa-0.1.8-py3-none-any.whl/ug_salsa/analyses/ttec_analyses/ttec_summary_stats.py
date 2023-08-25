from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
from salsa.data import TTECData

class TTECSummaryStats(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)

    def report_data(self) -> None:
        self.metrics.add("ec_num_beads_mil", self.data.total_found / 10**6)

        self.table = pd.DataFrame(
            data=np.vstack(
                [
                    ["Num EC Beads Found (M)"],
                    ["%.3f" % (self.data.total_found / 10**6)],
                ]
            ).T,
            columns=["Metric", "Value"],
        )
        self.report_title = f"TTEC Bead Loading - {self.runID}"
        pass