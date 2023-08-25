#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
from salsa.helper_functions import log
# from tool_noise import tool_noise
# import new_plots as new_plt
from salsa.analyses import Analysis
from salsa.data.ttecdata import TTECData

class TTECAnalysis(Analysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__()
        self.data: TTECData = data
        self.runID = self.data.runID
        self.plotly_color = {
        "T": "red",
        "G": "black",
        "C": "blue",
        "A": "lime",
        "t": "red",
        "g": "black",
        "c": "blue",
        "a": "lime",
        0: "red",
        1: "black",
        2: "blue",
        3: "lime",
        }

    def meets_conditions_for_analysis(self, bead_count: int = None) -> bool:
        if bead_count is None:
            bead_count = 10_000
        if self.data.sigmat.shape[0] < bead_count:
            log(
                "info",
                f"Not enough TTEC samples ({self.data.sigmat.shape[0]} beads found, requires 10k). Skipping all analyses.",
            )
            return False
        return True