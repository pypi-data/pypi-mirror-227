from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
from salsa.analyses.refbead_analyses.plot_anoms_perflow import PlotAnomsPerFlow

class PlotUnstableTiles(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData, anoms_per_flow: PlotAnomsPerFlow) -> None:
        super().__init__(data)
        self.anoms_per_flow = anoms_per_flow
        return
    def preprocess_data(self) -> None:
        self.unstable_tiles = np.any(self.anoms_per_flow.tile_anomalies, axis = 0)*1 # binary output (stable/unstable)
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self):                       
        data = np.vstack([self.data.tiles,
                            self.data.radii,
                            self.data.theta*180/np.pi,
                            np.array(['Unstable' if i else 'Stable' for i in self.unstable_tiles])]).transpose()
        df = pd.DataFrame(data, columns = ["tileID",'radius','theta','Unstable Tiles'])
        df['radius'] = df['radius'].astype(self.data.radii.dtype)
        df['theta'] = df['theta'].astype(self.data.theta.dtype)
        df['tileID'] = df['tileID'].astype(self.data.tiles.dtype)

        fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="Unstable Tiles",
                hover_name = np.array([f'Tile {tile}' for tile in df['tileID'].to_numpy()]),
                hover_data = {"Unstable Tiles": True},
                color_discrete_map = {'Stable': '#7095d7', 'Unstable': '#d7b270'},
                )
        fig.set_name(f"Unstable Tiles - {self.runID}")
        fig.update_layout(title_text=fig.name,
                coloraxis_colorbar=dict(title="Instability > 3&#963;"))
        self.fig = fig