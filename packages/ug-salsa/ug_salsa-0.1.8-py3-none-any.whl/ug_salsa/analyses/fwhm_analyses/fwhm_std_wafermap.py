from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
import pandas as pd
import salsa.plots.new_plots as new_plt

class FWHMSTDWaferMap(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)


    def plot_data(self) -> None:
        data = np.vstack([self.data.tiles,
                          self.data.radii,
                          self.data.theta*180/np.pi,
                          np.nanstd(self.data.fwhmMap, axis = (0,2))]).transpose()
        df = pd.DataFrame(data, columns = ["tileID",'radius','theta','FWHM StDev (um)'])
        df['radius'] = df['radius'].astype(self.data.radii.dtype)
        df['theta'] = df['theta'].astype(self.data.theta.dtype)
        df['tileID'] = df['tileID'].astype(self.data.tiles.dtype)

        fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="FWHM StDev (um)",
                hover_name = np.array([f'Tile {tile}' for tile in df['tileID'].to_numpy()]),
                )
        fig.set_name(f"FWHM Full Run StDev - {self.runID}")
        fig.update_layout(title_text=fig.name)
        self.fig = fig