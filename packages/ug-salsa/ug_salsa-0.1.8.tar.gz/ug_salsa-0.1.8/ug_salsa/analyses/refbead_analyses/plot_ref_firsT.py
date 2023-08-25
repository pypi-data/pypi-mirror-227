from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
import plotly.graph_objects as go

class PlotRefFirsT(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    def preprocess_data(self) -> None:
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
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self):                       
            data = np.vstack([self.data.tiles,
                              self.data.radii,
                              self.data.theta*180/np.pi,
                              self.mean_perTile[0,:]]).transpose()
            df = pd.DataFrame(data, columns = ["tileID",'radius','theta','Signal'])
            df = df.dropna()
            df['Signal'] = df['Signal'].astype(np.int64)

            fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="Signal",
                  hover_name = np.array([f'Tile {int(tile)}' for tile in df['tileID'].to_numpy()]),
                  hover_data = {"Signal": True},
                  # color_continuous_scale='jet',
                  range_color=[int(df['Signal'].quantile(0.01)), int(df['Signal'].quantile(0.99))],
                  opacity=0.5)
            fig.set_name(f"RefBead Flow 1 Signal - {self.runID}")
            fig.update_layout(title_text=fig.name,
                  coloraxis_colorbar=dict(title="Mean Signal per Tile"))
            self.fig = fig