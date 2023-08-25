from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
from salsa.analyses.refbead_analyses import PlotRefFirsT
class PlotAnomsPerFlow(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData, ref_first_T: PlotRefFirsT) -> None:
        super().__init__(data)
        self.ref_first_T = ref_first_T
        return
    
    def analyze_data(self) -> None:
        self.ref_tileID = [int(tileID-1) for tileID in self.data.XYT[:,2]] # shift idx of tileID 1 -> 0 for pythonic indexing
        self.active_tiles, self.nbeads_perTile = np.unique(self.ref_tileID, return_counts = True) # active tiles are tiles on which refbeads were found
        self.tile_anomalies = np.zeros((self.data.sigmat.shape[1]-1, self.data.ntiles)) # shape: (flow, all tiles)
        self.mean_perTile = self.ref_first_T.mean_perTile
        self.sig_var = (np.diff(self.mean_perTile[:,self.active_tiles], axis = 0)/self.mean_perTile[1:,self.active_tiles]) # fraction of difference in average signal per tile / per flow

        self.tile_anomalies[:,self.active_tiles] = (np.abs(self.sig_var)>3*np.nanstd(self.sig_var, axis = 0)) # consider using std?
        self.ntile_anomalies = np.sum(self.tile_anomalies, axis = 1) # Add line plot of # tiles with flow-to-flow %change >X% to the CV per flow plot
        self.anomalies_perflow:np.ndarray = np.sum(self.tile_anomalies,1)
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self) -> None:
        
        df = pd.DataFrame({'x': np.arange(self.anomalies_perflow.shape[0]) + 1,
                            'y': self.anomalies_perflow})
        
        fig = new_plt.LinePlot(df, x='x', y='y')
        fig.set_name(f"Number of Unstable Tiles per Flow - {self.runID}")
        fig.update_layout(title_text=fig.name, hovermode='x unified')
        fig.update_xaxes(title_text='Flow #')
        fig.update_yaxes(title_text='# Tiles')
        self.fig = fig
        return

