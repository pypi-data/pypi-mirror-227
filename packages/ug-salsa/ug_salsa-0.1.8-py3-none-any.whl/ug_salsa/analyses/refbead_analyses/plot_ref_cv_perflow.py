from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd

class PlotRefCVPerFlow(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    
    def analyze_data(self) -> None:
        self.ref_tileID = [int(tileID-1) for tileID in self.data.XYT[:,2]] # shift idx of tileID 1 -> 0 for pythonic indexing
        self.active_tiles, self.nbeads_perTile = np.unique(self.ref_tileID, return_counts = True) # active tiles are tiles on which refbeads were found
        self.sig_perTile = np.nan*np.zeros((self.data.sigmat.shape[1],
                                    self.data.ntiles)) # shape: (flow, tiles)
            
        self.rb_perTile = np.zeros(self.ntiles).astype(int)
            
        sig_offset, self.rb_perTile[self.active_tiles] = (np.cumsum(self.nbeads_perTile) - self.nbeads_perTile, 
                                      np.unique(self.data.XYT[:,2], return_counts=True)[1])
            
        sigmat_sorted = self.data.sigmat[np.argsort(self.ref_tileID),:] # sort signals by tile ID for avg/tile calc 
            
        #filter out bottom 5% of rb_perTile
        
        for x,y in zip(*np.where(sigmat_sorted == 0)):
                sigmat_sorted[x,y] = np.nan
        
        for i,tile in enumerate(self.active_tiles):
                self.sig_perTile[:,tile] = np.nansum(sigmat_sorted[sig_offset[i]:sig_offset[i]+self.rb_perTile[tile],:], axis = 0)

        self.mean_perTile = self.sig_perTile/self.rb_perTile
        self.CV_per_flow = np.nanstd(self.mean_perTile, axis = 1)/np.nanmean(self.mean_perTile, axis = 1)
        return
    
    def report_data(self) -> None:
        self.metrics.add('rb_firstT_tile_cv', self.CV_per_flow)
        return
    
    def plot_data(self) -> None:        
        df = pd.DataFrame({'Flow': np.arange(self.CV_per_flow.shape[0] - 1) + 1,
                            'CV per Flow':  self.CV_per_flow[:-1]})
        
        fig = new_plt.LinePlot(df, x='Flow', y='CV per Flow')
        fig.set_name(f"Refbead CV over tiles, per flow - {self.runID}")
        fig.update_layout(title = fig.name, hovermode='x unified')
        fig.update_xaxes(title_text="Flow #")
        fig.update_yaxes(title_text="CV")
        fig.send_json(self.runID)
        return

