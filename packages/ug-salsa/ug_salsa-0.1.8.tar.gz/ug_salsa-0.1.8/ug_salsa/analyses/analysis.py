from abc import ABC, abstractmethod
from typing import List, Tuple
from salsa.run_metrics import RunMetrics
from salsa.parameters import Parameters
from salsa.data.data_container import DataContainer
from salsa.routines.runnable import Runnable
from salsa.routines.output_handler import OutputHandler
import salsa.plots.new_plots as new_plt
from salsa.plots.figure import Figure
import pandas as pd

class Analysis(Runnable):

    def __init__(self, data: DataContainer = None) -> None: #, routine: OutputHandler
        self.params: Parameters = Parameters()
        self.metrics: RunMetrics = RunMetrics()
        self.data = data
        self.runID: str = ''
        if data:
            self.runID = data.runID
        self.fig: Figure = None
        self.table: pd.DataFrame = None
        self.report_title: str = ""
        self.parent_routine: OutputHandler = None
        self.subanalysis_figs: List[Figure] = []
        self.subanalysis_tables: List[Tuple(pd.DataFrame, str)] = []
        return
    
    def __str__(self) -> str:
        result = "\t" + "="*10 + "\n"
        result += "\t" + "Analysis __str__():\n"
        result += "\tThis analysis' runID:    " + str(self.runID) + "\n"
        result += "\t" + "="*10 + "\n\n"
        return result


    def run_without_output(self) -> None:
        self.preprocess_data()
        self.analyze_data()
        self.report_data()
        self.plot_data()

    def run(self):
        if(self.meets_conditions_for_analysis()):
            self.run_without_output()
            self.add_report_to_html()
            self.add_plot_to_html()

    @abstractmethod
    def meets_conditions_for_analysis(self, bead_count: int = None) -> bool:
        pass

    def preprocess_data(self) -> None:
        return

    def analyze_data(self) -> None:
        return

    @abstractmethod
    def report_data(self) -> None:
        pass

    def plot_data(self) -> None:
        return
    
    def add_report_to_html(self):
        if self.table is not None and self.report_title:
            self.parent_routine.add_table(self.table, self.report_title) 
        
        for report_title, table in self.subanalysis_tables:
            self.parent_routine.add_table(table, report_title) 
        return
    
    def add_plot_to_html(self):
        #self.fig.send_json(self.runID)
        if self.fig:
            self.parent_routine.add_interactive_plot(self.fig)

        for fig in self.subanalysis_figs:
                self.parent_routine.add_interactive_plot(fig)


    def add_table(self):
        print("Analysis does not create tables, refer to Routine instead")
        return
    
    def add_interactive_plot(self):
        print("Analysis does not create interactive plots, refer to Routine instead")
        return

    def add_noninteractive_plot(self):
        print("Analysis does not create noninteractive plots, refer to Routine instead")
        return


# import numpy as np
# from scipy.io import loadmat, savemat
# data = loadmat("metadata_test_data.mat")
# data.pop('__header__')
# data.pop('__version__')
# data.pop('__globals__')
# data.pop('fwhmMap')
# data['total_found'] = 0
# data['tilesDescription'] = data['tilesDescription'][::80]
# savemat('metadata_test_data.mat', data)

# import numpy as np
# from scipy.io import loadmat, savemat
# data = loadmat("fwhm_test_data.mat")
# # data.pop('__header__')
# # data.pop('__version__')
# # data.pop('__globals__')
# # data['fwhmMap'] = data['fwhmMap'][:10,::800,:]
# data['total_found'] = 0
# # data['tilesDescription'] = data['tilesDescription'][::800]
# savemat('fwhm_test_data.mat', data)

# import numpy as np
# from scipy.io import loadmat, savemat
# data = loadmat("RunID026484_1_reference_beads.mat")
# data.pop('__header__')
# data.pop('__version__')
# data.pop('__globals__')
# n_beads = data['ref_SigMat'].shape[0]-1
# random_sig_beads = np.random.choice(n_beads, size=40, replace=False)
# n_beads = data['ref_lost_SigMat'].shape[0]
# random_lost_beads = np.random.choice(n_beads, size=10, replace=False)
# data['ref_SigMat'] = data['ref_SigMat'][random_sig_beads,:10]
# data['ref_XYT'] = data['ref_XYT'][random_sig_beads]
# data['ref_lost_SigMat'] = data['ref_lost_SigMat'][random_lost_beads,:10]
# data['ref_lost_XYT'] = data['ref_lost_XYT'][random_lost_beads]
# data['tilesDescription'] = data['tilesDescription'][::80]
# savemat('refbead_test_data.mat', data)

# import numpy as np
# from scipy.io import loadmat, savemat
# data = loadmat("RunID026484_1_template_TFSA1.mat")
# data.pop('__header__')
# data.pop('__version__')
# data.pop('__globals__')
# n_beads = data['SigMat'].shape[0]-1
# random_beads = np.random.choice(n_beads, size=50, replace=False)
# data['SigMat'] = data['SigMat'][random_beads,:10]
# data['XYT'] = data['XYT'][random_beads]
# data['tilesDescription'] = data['tilesDescription'][::80]
# data['template_tk'] = data['template_tk'][:,:10]
# savemat('template_TFSA1_test_data.mat', data)

# import numpy as np
# from scipy.io import loadmat, savemat
# data = loadmat("RunID026484_1_template_TFSA2.mat")
# data.pop('__header__')
# data.pop('__version__')
# data.pop('__globals__')
# n_beads = data['SigMat'].shape[0]-1
# random_beads = np.random.choice(n_beads, size=50, replace=False)
# data['SigMat'] = data['SigMat'][random_beads,:10]
# data['XYT'] = data['XYT'][random_beads]
# data['tilesDescription'] = data['tilesDescription'][::80]
# data['template_tk'] = data['template_tk'][:,:10]
# savemat('template_TFSA2_test_data.mat', data)

# import pandas as pd
# import numpy as np
# data = pd.read_parquet('RunID026484_1_TTEC_SigMat.parquet.gzip')
# n_beads = data.shape[0]-1
# random_beads = np.random.choice(n_beads, size=50, replace=False)
# data = data.iloc[random_beads,:10]
# data.to_parquet('TTEC_sigmat_test_data.parquet.gzip', compression='gzip')
# data = pd.read_parquet('RunID026484_1_TTEC_truekey.parquet.gzip')
# data = data.iloc[random_beads,:10]
# data.to_parquet('TTEC_truekey_test_data.parquet.gzip', compression='gzip')

