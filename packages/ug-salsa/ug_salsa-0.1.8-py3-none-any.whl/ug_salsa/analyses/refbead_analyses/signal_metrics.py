from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
from salsa.analyses.refbead_analyses import PlotRefFirsT, PlotRefCVPerFlow
class SignalMetrics(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData, ref_first_T: PlotRefFirsT, ref_cv: PlotRefCVPerFlow) -> None:
        super().__init__(data)
        self.ref_first_T = ref_first_T
        self.ref_cv = ref_cv
        return
    
    def analyze_data(self) -> None:
        self.full_run_avg = np.zeros( self.data.ntiles ) # avg sig/tile over all flows
        self.full_run_avg[self.ref_first_T.active_tiles] = np.nanmean(self.ref_first_T.mean_perTile[:,self.ref_first_T.active_tiles], axis = 0) 
            
        self.rb_signal_nonuniformity = np.nanstd(self.full_run_avg)/np.nanmean(self.full_run_avg)
    
        self.tile_anomalies = np.zeros((self.data.sigmat.shape[1]-1, self.data.ntiles)) # shape: (flow, all tiles)
        self.unstable_tiles = np.any(self.tile_anomalies, axis = 0)*1 # binary output (stable/unstable)
        self.ntiles_unstable = np.sum(self.unstable_tiles)
        self.firsT_signal = np.nanmean(self.data.sigmat[:,0])
        return
    
    def report_data(self) -> None:
        metrics_dict = {
                  'Flow 1 Signal Mean':int(self.firsT_signal),        
                  'Flow 1 Tile CV':np.round(self.ref_cv.CV_per_flow[0],3),
                  'Signal NonUniformity':np.round(self.rb_signal_nonuniformity,3),
                  '# unstable tiles':self.ntiles_unstable,
                  'Total # of tiles': self.data.ntiles,
            }
        
        self.metrics.add('rb_firstT_signal_mean', float(np.nanmean(self.firsT_signal)))
        self.metrics.add('rb_signal_nonuniformity', self.rb_signal_nonuniformity)
        self.metrics.add('rb_num_tiles_high_variance', int(self.ntiles_unstable))

        metrics = [key for key in metrics_dict]
        values = [metrics_dict[key] for key in metrics]
        
        self.table = pd.DataFrame(data=np.vstack([metrics,values]).T, columns = ['Metric', 'Value'])
        self.report_title = f"Signal Metrics - {self.runID}"