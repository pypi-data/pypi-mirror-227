from salsa.analyses.template_analyses import TemplateAnalysis
import numpy as np
import pandas as pd
from typing import Dict
import salsa.plots.new_plots as new_plt
import os
import numpy as np
import pandas as pd
import os
import pickle
from salsa.data import TemplateData


class DetectOil(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)

    def analyze_data(self) -> None:
        if self.metrics.get("TFSA1_num_beads",0) == 0:
            self.is_oily = np.nan
            self.table = pd.DataFrame(data=np.vstack([['Run is Oily'],
                                                 ["Unknown"]]).T,   
                                 columns=['Metric', 'Value'])
        else:
            deserts = {
                "TFSA1_T": 0 + 4*(np.arange(7, 12) - 1),
                "TFSA1_G": 1 + 4*(np.arange(11, 18) - 1),
                "TFSA1_C": 2 + 4*(np.arange(17, 22) - 1),
                "TFSA1_A": 3 + 4*(np.arange(2, 7) - 1),
            }
            sigmat = self.templates['TFSA1'].sigmat
            run_data = np.zeros((1,4))
            for ind, base in enumerate(["T","G","C","A"]):
                flows = deserts[f"TFSA1_{base}"]
                y = np.median(sigmat, axis = 0)[flows][1:-1]
                A = np.vstack([flows[1:-1], np.ones(len(flows[1:-1]))]).T
                m, _ = np.linalg.lstsq(A, y, rcond=None)[0]
                run_data[0,ind] = m
                self.metrics.add(f"tf_desert_ramp_{base}", m)
            
            model_backup_path = os.path.join(os.path.dirname(__file__),
                                            'supplemental_data/oil_model.pkl')
            with open(model_backup_path, 'rb') as file:
                clf = pickle.load(file)
            self.is_oily = int(clf.predict(run_data)[0])            
            self.table = pd.DataFrame(data=np.vstack([['Run is Oily'],
                                    [str(self.is_oily)]]).T,
                                columns=['Metric', 'Value'])
        return

    def report_data(self) -> None:
        self.metrics.add('oily_run', self.is_oily)
        self.report_title = f'Oily Status - {self.runID}'
        return