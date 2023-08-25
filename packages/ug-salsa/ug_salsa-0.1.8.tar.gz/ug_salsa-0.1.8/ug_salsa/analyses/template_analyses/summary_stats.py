from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd

import salsa.plots.new_plots as new_plt
from salsa.data.templatedata import TemplateData

class SummaryStats(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        
    def preprocess_data(self) -> None:
        for template_name in self.templates.keys():        
            self.metrics.add(f"{template_name}_num_beads", self.templates[template_name].total_found)
        #self.count_sequencing_refbeads()
        
        self.data = np.vstack([
            ['TFSA1','TFSA2','Sequencing RefBeads'],
            [self.metrics.get('TFSA1_num_beads'),
             self.metrics.get('TFSA2_num_beads'),
             'Coming soon']]
        ).T
        return

    def report_data(self) -> None:
        self.table = pd.DataFrame(data=self.data,
                            columns=['Template','Beads Found'])
        self.report_title = f'Template Bead Count - {self.runID}'
        return