from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

from salsa.helper_functions import log
import numpy as np
import pandas as pd
import salsa.plots.new_plots as new_plt
import shutil

class LoadingDensityMetrics(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        self.outputs = {} # type hint later
        return
    def preprocess_data(self) -> None:
        self.refbeads_pertile = np.zeros_like(self.data.radii)
        ref_tileID = [int(tileID-1) for tileID in self.data.XYT[:,2]] # shift idx of tileID 1 -> 0 for pythonic indexing
        active_tiles, _ = np.unique(ref_tileID, return_counts = True) # active tiles are tiles on which refbeads were found
        _, _, counts = np.unique(self.XYT[:,2], return_counts = True, return_inverse = True)
        self.refbeads_pertile[active_tiles] = counts

    def analyze_data(self) -> None:
        # metrics table
        self.metrics_dict = {
                'Num Beads Loaded (M)':np.round(self.data.nbeads/(1e6),1),
                'Average Loading Density (kbeads/mm<sup>2</sup>)':np.round(np.mean(self.data.FullBeadsPerTile/self.data.tile_size)/1000,3), # units is (kbeads/mm2)
                'Loading Nonuniformity': np.nan, #CV of beads/mm2          FOR TESTING
                '''Num Low Loading Tiles (&lt;100 kbeads/mm<sup>2</sup>)''':np.sum((self.data.FullBeadsPerTile/self.data.tile_size)<self.params['min_bead_density']),      
                'Num Refbeads Loaded (M)': np.round(self.data.total_found/1e6,3),
                'Loading Nonuniformity': np.round(self.calculate_loading_nonuniformity(),3),
        }
        return

    def calculate_loading_nonuniformity(self):
        loading_density = self.data.FullBeadsPerTile/self.data.tile_size
        if np.isnan(loading_density).all():
                return np.nan
        
        cv = np.nanstd(loading_density)/np.nanmean(loading_density)
        return cv

    def report_data(self) -> None:
        metrics = [key for key in self.metrics_dict]
        values = [self.metrics_dict[key] for key in metrics]
        
        self.table = pd.DataFrame(data=np.vstack([metrics,values]).T, columns = ['Metric', 'Value'])

        self.metrics.add('loading_nonuniformity', self.metrics_dict['Loading Nonuniformity'])
        self.metrics.add('rb_num_beads_mil', self.data.total_found/1e6)
        return
    
    def add_report_to_html(self):
        new_plt.PlotHandler.add_table_to_report(self.table, f'Bead Loading Metrics - {self.runID}', escape = False)