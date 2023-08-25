from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd

import salsa.plots.new_plots as new_plt
from salsa.data.templatedata import TemplateData
from salsa.helper_functions import log
class SummaryStatsSupp(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData], barcode) -> None:
        super().__init__(templates)
        self.barcode = barcode
        
    def preprocess_data(self) -> None:
        log('info', "    Recording summary statistics for " + self.barcode)
        bc_temps = [temp for temp in self.templates.values() if 'BC' + self.barcode in temp.name]
        template_counts = []
        template_firstTs =[]
        template_names = []
        flow = 0
        for template in bc_temps:        
            self.metrics.add(f"{template}_num_beads_found", template.total_found)
            self.metrics.add(f"{template}_preamble_{self.params['flow_order'][flow]}", np.nanmean(template.sigmat[:,flow]))
            template_counts.append(template.total_found)
            template_firstTs.append(int(np.round(np.nanmean(template.sigmat[:,flow]))))
            template_names.append(template.name)

        template_names, template_counts, template_firstTs = zip(*sorted(zip(template_names, template_counts, template_firstTs)))

        self.data = np.vstack([
            template_names,
            template_counts,
            template_firstTs]
        ).T
        return

    def report_data(self) -> None:
        self.table = pd.DataFrame(data=self.data,
                            columns=['Template','Beads Found', 'First T Signal'])
        self.report_title = f'Template Bead Count - {self.runID}'
        return


   