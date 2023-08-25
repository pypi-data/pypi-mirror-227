from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
import pandas as pd
import salsa.plots.new_plots as new_plt

class FWHMFlow1WaferMap(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)


    def plot_data(self) -> None:
        data = np.vstack([self.data.tiles,
                          self.data.radii,
                          self.data.theta*180/np.pi,
                          np.nanmean(self.data.fwhmMap[0,:,:], axis = 1)]).transpose()
        df = pd.DataFrame(data, columns = ["tileID",'radius','theta','FWHM Mean (um)'])
        df['radius'] = df['radius'].astype(self.data.radii.dtype)
        df['theta'] = df['theta'].astype(self.data.theta.dtype)
        df['tileID'] = df['tileID'].astype(self.data.tiles.dtype)

        fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="FWHM Mean (um)",
                hover_name = np.array([f'Tile {tile}' for tile in df['tileID'].to_numpy()]),
                )
        fig.set_name(f"Flow 1 FWHM - {self.runID}")
        fig.update_layout(title_text=fig.name)
        self.fig = fig