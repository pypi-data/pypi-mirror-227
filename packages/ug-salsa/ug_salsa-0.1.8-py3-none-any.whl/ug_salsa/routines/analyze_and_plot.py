from salsa.routines.init__ import Runnable
from salsa.analyses.analysis import Analysis

class AnalyzeAndPlot(Runnable):
    
    def __init__(self, analysis: Analysis):
        self.analysis = analysis
        return

    def run(self):
        self.analysis.run()
        self.analysis.add_plot_to_html()
        return
    
# Check functionality of report_data() method. Only adds metrics or metrics + tables?