from salsa.routines.init__ import Runnable
from salsa.analyses import Analysis

class AnalyzeAndReport(Runnable):
    
    def __init__(self, analysis: Analysis):
        self.analysis = analysis
        return
    
    def run(self):
        self.analysis.run()
        self.analysis.add_report_to_html()
        return