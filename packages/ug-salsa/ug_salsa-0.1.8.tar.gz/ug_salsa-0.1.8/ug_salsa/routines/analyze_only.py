from salsa.routines.init__ import Runnable
from salsa.analyses import Analysis

class AnalyzeOnly(Runnable):
    
    def __init__(self, analysis: Analysis):
        self.analysis = analysis
        return
    
    def run(self):
        self.analysis.run()
        return