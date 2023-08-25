from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import numpy as np
from salsa.data import TemplateData

class FloorSignalPerBase(TemplateAnalysis):
    def __init__(self, templates: Dict[str, TemplateData], save: bool = True, inds = None) -> None:
        super().__init__(templates)    
        self.save = save
        self.inds = inds
        self.template: TemplateData = list(templates.values())[0]

        
    def preprocess_data(self) -> None:
        # Note: will be calculated over 200 flows when full data loading is implemented
        if self.inds is not None:
            self.signal = self.template.sigmat[self.inds,:]
        else:
            self.signal = self.template.sigmat
        self.avg_signal = np.nanmedian(self.signal, axis = 0)
        self.floors = []
       
        return

    def report_data(self) -> None:
        for base_ind in range(4):
            floor_val = np.nanmin(self.avg_signal[base_ind::4])
            self.floors.append(floor_val)
            if self.save:
                self.metrics.add(f"tf_min_floor_{self.params['flow_order'][base_ind]}", int(floor_val))
        return

    def get_floors(self):
        return self.floors